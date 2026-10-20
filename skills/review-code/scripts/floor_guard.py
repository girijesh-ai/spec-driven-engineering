#!/usr/bin/env python3
"""Floor guard: flag changes that lower the project's quality bar.

Scans the diff from the merge-base with a base branch to the working tree
(staged, unstaged and untracked files) and reports anything that makes a
check easier to pass without making the code better: new suppressions,
skipped or focused tests, stubs, deleted test files, net-removed assertions,
lowered thresholds, relaxed lint/type config.

Tightening the bar is silent; loosening it is loud.

Usage:  python3 floor_guard.py [--base REF] [--repo PATH]

Exit codes:
  0  clean
  1  findings (each printed as RULE  path:line  (marker))
  2  could not run (not a git repo, no base found, git failed)
A 2 must never be read as a 0: the guard did not check anything.

Findings name the rule and location only, never the line's content, so a
secret on a flagged line is not echoed into logs.

Stdlib only; Python 3.8+.
"""

from __future__ import annotations

import argparse
import fnmatch
import re
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, NamedTuple, Optional, Tuple

DEFAULT_BASES = ("origin/HEAD", "main", "master")

SUPPRESSION = re.compile(
    r"#\s*noqa\b|#\s*type:\s*ignore|pyright:\s*ignore|pylint:\s*disable"
    r"|eslint-disable|@ts-ignore|@ts-expect-error|@ts-nocheck"
    r"|istanbul\s+ignore|c8\s+ignore|nosemgrep|#\s*nosec\b|NOSONAR"
    r"|pragma:\s*no\s*cover|//\s*nolint|#\[allow\(|@SuppressWarnings"
    r"|rubocop:disable|phpcs:ignore"
)
SKIPPED_TEST = re.compile(
    r"@pytest\.mark\.(skip|skipif|xfail)\b|\bpytest\.skip\(|@unittest\.skip"
    r"|@unittest\.expectedFailure|\b(it|test|describe|context)\.(skip|todo|only)\("
    r"|(?<![\w.])x(it|describe|test)\(|(?<![\w.])f(it|describe)\(|@Disabled\b|@Ignore\b"
    r"|\bt\.Skip(Now|f)?\(|#\[ignore\]"
)
STUB = re.compile(
    r"\braise\s+NotImplementedError\b|throw\s+new\s+Error\(\s*['\"]not\s+implemented"
    r"|\btodo!\(|\bunimplemented!\(|panic\(\s*\"not\s+implemented",
    re.I,
)
ASSERTION = re.compile(
    r"\bassert\w*\b|\bexpect\(|\.should\b|\bt\.(Error|Errorf|Fatal|Fatalf)\(|\brequire\.\w+\("
)
THRESHOLD = re.compile(
    r"(fail[_-]under|cov-fail-under|min(imum)?[_-]coverage|coverage[_-]?threshold"
    r"|\b(branches|functions|lines|statements)\b)[\"']?\s*[:=]\s*[\"']?(\d+(\.\d+)?)",
    re.I,
)
RELAXED_CONFIG = re.compile(
    r"\bstrict\w*[\"']?\s*[:=]\s*[\"']?false\b|\b(extend-)?ignore\s*[:=]"
    r"|per-file-ignores|\bdisable\s*[:=]|[\"']off[\"']|\bwarn_unused_ignores\s*=\s*false",
    re.I,
)
TEST_PATH_GLOBS = (
    "test_*.py", "*_test.py", "*_test.go", "*.test.*", "*.spec.*",
    "*Test.java", "*Tests.java", "*Test.kt", "*_spec.rb",
)
TEST_DIR_NAMES = {"test", "tests", "__tests__", "spec", "specs"}
CONFIG_GLOBS = (
    ".eslintrc*", "eslint.config.*", "ruff.toml", ".ruff.toml", ".flake8",
    "setup.cfg", "tox.ini", "pyproject.toml", "mypy.ini", ".pylintrc",
    "tsconfig*.json", ".golangci.*", ".rubocop.yml", "biome.json",
    "jest.config.*", "vitest.config.*", ".coveragerc", "package.json",
)
# Prose that *mentions* a suppression or a skip isn't one.
PROSE_GLOBS = ("*.md", "*.rst", "*.txt", "*.adoc")
# Thresholds also live in CI and build files; code files are excluded so a
# local variable named `lines` can't read as a coverage threshold.
THRESHOLD_GLOBS = CONFIG_GLOBS + (
    "*.yml", "*.yaml", "*.toml", "*.ini", "*.cfg", "*.json", "Makefile",
)


class Finding(NamedTuple):
    rule: str
    path: str
    line: int
    marker: str


class FileDiff(NamedTuple):
    path: str
    added: List[Tuple[int, str]]
    removed: List[Tuple[int, str]]


class GuardError(Exception):
    pass


def git(repo: Path, *args: str) -> str:
    try:
        result = subprocess.run(
            # quotepath=off: non-ASCII paths come out as-is, not "\303\251"-quoted
            ["git", "-C", str(repo), "-c", "core.quotepath=off", *args],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
            errors="replace",
        )
    except OSError as exc:
        raise GuardError(f"could not run git: {exc}") from exc
    if result.returncode != 0:
        raise GuardError(f"git {' '.join(args)} failed: {result.stderr.strip()}")
    return result.stdout


def resolve_merge_base(repo: Path, base: Optional[str]) -> Tuple[str, str]:
    candidates = (base,) if base else DEFAULT_BASES
    for ref in candidates:
        try:
            merge_base = git(repo, "merge-base", "HEAD", ref).strip()
        except GuardError:
            continue
        if merge_base:
            return merge_base, ref
    raise GuardError(
        f"no merge-base with {', '.join(candidates)} — pass --base <ref>"
    )


def parse_unified_diff(text: str) -> List[FileDiff]:
    files: List[FileDiff] = []
    current: Optional[FileDiff] = None
    in_header = False  # between "diff --git" and the first "@@"
    old_line = new_line = 0
    hunk = re.compile(r"^@@ -(\d+)(?:,\d+)? \+(\d+)(?:,\d+)? @@")
    for raw in text.splitlines():
        if raw.startswith("diff --git "):
            current, in_header = None, True
        elif in_header and raw.startswith("+++ "):
            path = raw[4:].rstrip("\t")  # git appends a tab to paths with spaces
            if path == "/dev/null":
                current = None
                continue
            current = FileDiff(path[2:] if path.startswith("b/") else path, [], [])
            files.append(current)
        elif in_header and raw.startswith("--- "):
            continue
        elif current is None or (in_header and not raw.startswith("@@")):
            continue
        elif raw.startswith("@@"):
            in_header = False
            match = hunk.match(raw)
            if match:
                old_line, new_line = int(match.group(1)), int(match.group(2))
        elif raw.startswith("+"):
            current.added.append((new_line, raw[1:]))
            new_line += 1
        elif raw.startswith("-"):
            current.removed.append((old_line, raw[1:]))
            old_line += 1
        elif raw.startswith(" "):
            old_line += 1
            new_line += 1
    return files


def matches_any(path: str, globs: Tuple[str, ...]) -> bool:
    name = Path(path).name
    return any(fnmatch.fnmatch(name, glob) for glob in globs)


def is_test_path(path: str) -> bool:
    return matches_any(path, TEST_PATH_GLOBS) or any(
        part in TEST_DIR_NAMES for part in Path(path).parts[:-1]
    )


def first_match(pattern: "re.Pattern[str]", line: str) -> Optional[str]:
    match = pattern.search(line)
    return match.group(0).strip() if match else None


def thresholds(lines: List[Tuple[int, str]]) -> Dict[str, Tuple[int, float]]:
    found: Dict[str, Tuple[int, float]] = {}
    for number, text in lines:
        match = THRESHOLD.search(text)
        if match:
            found[match.group(1).lower()] = (number, float(match.group(4)))
    return found


def scan_file(diff: FileDiff) -> List[Finding]:
    findings: List[Finding] = []
    if matches_any(diff.path, PROSE_GLOBS):
        return findings
    for number, text in diff.added:
        for rule, pattern in (("SUPPRESSION", SUPPRESSION), ("STUB", STUB)):
            marker = first_match(pattern, text)
            if marker:
                findings.append(Finding(rule, diff.path, number, marker))
        if is_test_path(diff.path):
            marker = first_match(SKIPPED_TEST, text)
            if marker:
                findings.append(Finding("SKIPPED_TEST", diff.path, number, marker))
        if matches_any(diff.path, CONFIG_GLOBS):
            marker = first_match(RELAXED_CONFIG, text)
            if marker:
                findings.append(Finding("RELAXED_CONFIG", diff.path, number, marker))

    if is_test_path(diff.path):
        removed = [(n, t) for n, t in diff.removed if ASSERTION.search(t)]
        added = [(n, t) for n, t in diff.added if ASSERTION.search(t)]
        if len(removed) > len(added):
            net = len(removed) - len(added)
            findings.append(
                Finding("REMOVED_ASSERTION", diff.path, removed[0][0], f"net -{net}")
            )

    if not matches_any(diff.path, THRESHOLD_GLOBS):
        return findings
    before, after = thresholds(diff.removed), thresholds(diff.added)
    for key, (number, new_value) in after.items():
        if key in before and new_value < before[key][1]:
            findings.append(
                Finding(
                    "LOOSENED_THRESHOLD",
                    diff.path,
                    number,
                    f"{key} {before[key][1]:g} -> {new_value:g}",
                )
            )
    return findings


def untracked_as_diffs(repo: Path) -> List[FileDiff]:
    diffs: List[FileDiff] = []
    for path in git(repo, "ls-files", "--others", "--exclude-standard").splitlines():
        try:
            text = (repo / path).read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue  # binary or unreadable — nothing line-based to check
        lines = [(i, line) for i, line in enumerate(text.splitlines(), start=1)]
        diffs.append(FileDiff(path, lines, []))
    return diffs


def run(repo: Path, base: Optional[str]) -> Tuple[List[Finding], str, str, int]:
    git(repo, "rev-parse", "--is-inside-work-tree")
    merge_base, ref = resolve_merge_base(repo, base)
    diff_text = git(
        repo, "diff", "--no-color", "--no-ext-diff", "--unified=0", "-M", merge_base
    )
    diffs = parse_unified_diff(diff_text) + untracked_as_diffs(repo)

    findings: List[Finding] = []
    for diff in diffs:
        findings.extend(scan_file(diff))

    status = git(repo, "diff", "--name-status", "-M", merge_base)
    for row in status.splitlines():
        fields = row.split("\t")
        if len(fields) == 2 and fields[0] == "D" and is_test_path(fields[1]):
            findings.append(Finding("DELETED_TEST_FILE", fields[1], 0, "deleted"))

    return findings, merge_base, ref, len(diffs)


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--base", help="branch or ref to diff against (default: origin/HEAD, main, master)")
    parser.add_argument("--repo", default=".", help="repository path (default: .)")
    args = parser.parse_args(argv)

    try:
        findings, merge_base, ref, file_count = run(Path(args.repo), args.base)
    except GuardError as exc:
        print(f"floor-guard: ERROR — {exc}. Nothing was checked.", file=sys.stderr)
        return 2

    where = f"merge-base {merge_base[:7]} ({ref}), {file_count} changed file(s)"
    if not findings:
        print(f"floor-guard: clean against {where}")
        return 0
    print(f"floor-guard: {len(findings)} finding(s) against {where}")
    for finding in sorted(findings, key=lambda f: (f.path, f.line, f.rule)):
        location = f"{finding.path}:{finding.line}" if finding.line else finding.path
        print(f"  {finding.rule:<18} {location}  ({finding.marker})")
    return 1


if __name__ == "__main__":
    sys.exit(main())
