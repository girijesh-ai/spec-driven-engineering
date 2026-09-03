#!/usr/bin/env python3
"""Structural checks for this repo's CLAUDE.md quality bar. Exit 0 = clean."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
REQUIRED_DOC_SECTIONS = (
    "What it does",
    "When to reach for it",
    "Common questions",
    "It's working if",
)
# Promoted skill docs live only in these buckets (CLAUDE.md); their files are
# validated as skill docs.
DOC_BUCKETS = ("engineering", "productivity")
# Artifact dirs hold the dated files spec-from-idea and plan-from-spec tell
# users to write (docs/specs/YYYY-MM-DD-<topic>.md, docs/plans/...) — not skill
# docs, so their files are skipped rather than scanned by filename.
DOC_ARTIFACT_DIRS = ("specs", "plans")


def check_json_manifests(errors: list[str]) -> None:
    for name in ("plugin.json", "marketplace.json"):
        path = REPO_ROOT / ".claude-plugin" / name
        try:
            json.loads(path.read_text())
        except (OSError, json.JSONDecodeError) as exc:
            errors.append(f"{path}: invalid JSON ({exc})")


def parse_frontmatter(text: str) -> dict[str, str] | None:
    match = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not match:
        return None
    fields: dict[str, str] = {}
    for key in ("name", "description"):
        field_match = re.search(rf"^{key}:\s*(.+)$", match.group(1), re.M)
        if field_match:
            fields[key] = field_match.group(1).strip()
    return fields


def check_skill_frontmatter(errors: list[str]) -> None:
    for path in sorted(REPO_ROOT.glob("skills/*/SKILL.md")):
        skill_name = path.parent.name
        text = path.read_text()
        fields = parse_frontmatter(text)
        if fields is None:
            errors.append(f"{path}: no YAML frontmatter block")
            continue
        if fields.get("name") != skill_name:
            errors.append(
                f"{path}: frontmatter name '{fields.get('name')}' != "
                f"directory '{skill_name}'"
            )
        description = fields.get("description", "")
        if not description.startswith("Use when"):
            errors.append(f"{path}: description must start with 'Use when'")
        if not re.search(r"^Status:\s*(draft|stable)\s*$", text, re.M):
            errors.append(f"{path}: missing 'Status: draft' or 'Status: stable' line")


def check_promoted_docs(errors: list[str]) -> None:
    status_re = re.compile(r"^\*\*Status:\*\*\s*(draft|stable)\s*$", re.M)
    # Every docs/ subdir must be a known bucket (validated below) or a known
    # artifact dir (skipped). Anything else is either a new bucket that would
    # otherwise go silently unvalidated or a stray dir — flag it, don't skip it.
    known_subdirs = set(DOC_BUCKETS) | set(DOC_ARTIFACT_DIRS)
    for sub in sorted(p for p in (REPO_ROOT / "docs").glob("*") if p.is_dir()):
        if sub.name not in known_subdirs:
            errors.append(
                f"{sub}: unexpected docs/ subdir — classify it in "
                "scripts/validate.py (add to DOC_BUCKETS to validate its docs, "
                "or DOC_ARTIFACT_DIRS to skip them)"
            )
    doc_paths = sorted(
        p for bucket in DOC_BUCKETS for p in (REPO_ROOT / "docs" / bucket).glob("*.md")
    )
    for doc_path in doc_paths:
        skill_name = doc_path.stem
        if not (REPO_ROOT / "skills" / skill_name / "SKILL.md").exists():
            errors.append(f"{doc_path}: doc exists but skills/{skill_name}/SKILL.md does not")
            continue
        text = doc_path.read_text()
        if not status_re.search(text):
            errors.append(
                f"{doc_path}: missing '**Status:** draft' or '**Status:** stable' line"
            )
        headings = set(re.findall(r"^## (.+?)\s*$", text, re.M))
        for section in REQUIRED_DOC_SECTIONS:
            if section not in headings:
                errors.append(f"{doc_path}: missing required section '## {section}'")
        for heading in sorted(headings - set(REQUIRED_DOC_SECTIONS)):
            errors.append(
                f"{doc_path}: unexpected section '## {heading}' — docs allow "
                "exactly the four required sections"
            )


def check_dependency_claims(errors: list[str]) -> None:
    # ponytail: hardcoded, duplicates README.md's dependency table. Upgrade
    # to parsing that table if the mapping grows past a handful of entries
    # or starts drifting; not worth a markdown-table parser at this size.
    consumed_by = {
        "engineering-standards": ["implement", "review-code"],
        "test-driven-development": ["implement", "debug-systematically"],
        "domain-modeling": ["spec-from-idea"],
        "codebase-architecture": ["plan-from-spec", "review-code"],
    }
    for dependency, consumers in consumed_by.items():
        for consumer in consumers:
            path = REPO_ROOT / "skills" / consumer / "SKILL.md"
            if not path.exists():
                errors.append(f"dependency check: {path} does not exist")
                continue
            if dependency not in path.read_text():
                errors.append(
                    f"{path}: claimed to consume '{dependency}' but does not mention it"
                )


def main() -> int:
    errors: list[str] = []
    try:
        check_json_manifests(errors)
        check_skill_frontmatter(errors)
        check_promoted_docs(errors)
        check_dependency_claims(errors)
    except (OSError, UnicodeDecodeError) as exc:
        print(f"Could not read repo files: {exc}")
        return 1

    if errors:
        print(f"{len(errors)} validation error(s):")
        for error in errors:
            print(f" - {error}")
        return 1

    print("All checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
