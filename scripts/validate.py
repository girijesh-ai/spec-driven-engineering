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
# Discipline skills hold a line under pressure; writing-for-agents requires
# each to close with these three sections.
DISCIPLINE_SKILLS = (
    "spec-from-idea",
    "implement",
    "review-code",
    "test-driven-development",
    "debug-systematically",
)
DISCIPLINE_SECTIONS = ("Common rationalizations", "Red flags", "Verification")
SKILL_STATUS = re.compile(r"^Status:\s*(draft|stable)\s*$", re.M)
DOC_STATUS = re.compile(r"^\*\*Status:\*\*\s*(draft|stable)\s*$", re.M)


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


def headings(text: str) -> set[str]:
    return set(re.findall(r"^## (.+?)\s*$", text, re.M))


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
        if not SKILL_STATUS.search(text):
            errors.append(f"{path}: missing 'Status: draft' or 'Status: stable' line")


def check_discipline_sections(errors: list[str]) -> None:
    for skill_name in DISCIPLINE_SKILLS:
        path = REPO_ROOT / "skills" / skill_name / "SKILL.md"
        if not path.exists():
            errors.append(f"discipline check: {path} does not exist")
            continue
        found = headings(path.read_text())
        for section in DISCIPLINE_SECTIONS:
            if section not in found:
                errors.append(f"{path}: discipline skill missing '## {section}'")


def check_promoted_docs(errors: list[str]) -> None:
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
        if not DOC_STATUS.search(text):
            errors.append(
                f"{doc_path}: missing '**Status:** draft' or '**Status:** stable' line"
            )
        found = headings(text)
        for section in REQUIRED_DOC_SECTIONS:
            if section not in found:
                errors.append(f"{doc_path}: missing required section '## {section}'")
        for heading in sorted(found - set(REQUIRED_DOC_SECTIONS)):
            errors.append(
                f"{doc_path}: unexpected section '## {heading}' — docs allow "
                "exactly the four required sections"
            )


def check_promotion_state(errors: list[str]) -> None:
    # Promotion edits SKILL.md, its doc, README.md and docs/in-progress.md
    # (CLAUDE.md); a half-done one passes every per-file check, so cross-check.
    readme = REPO_ROOT / "README.md"
    in_progress = REPO_ROOT / "docs" / "in-progress.md"
    readme_text = readme.read_text() if readme.exists() else ""
    in_progress_text = in_progress.read_text() if in_progress.exists() else ""
    docs = {
        p.stem: p for bucket in DOC_BUCKETS for p in (REPO_ROOT / "docs" / bucket).glob("*.md")
    }
    for path in sorted(REPO_ROOT.glob("skills/*/SKILL.md")):
        name = path.parent.name
        match = SKILL_STATUS.search(path.read_text())
        if not match:
            continue  # check_skill_frontmatter reports it
        status = match.group(1)
        row = rf"^\| `{re.escape(name)}` \|"
        doc = docs.get(name)
        if doc:
            doc_match = DOC_STATUS.search(doc.read_text())
            if doc_match and doc_match.group(1) != status:
                errors.append(
                    f"{doc}: Status {doc_match.group(1)} but {path} says {status}"
                )
            if re.search(row, in_progress_text, re.M):
                errors.append(f"{in_progress}: still lists '{name}', which has a docs page")
        listed = re.search(row, readme_text, re.M)
        if status == "draft" and listed:
            errors.append(f"{readme}: lists draft skill '{name}'")
        if status == "stable":
            if not doc:
                errors.append(f"{path}: stable but has no docs page")
            if not re.search(rf"{row} stable \|", readme_text, re.M):
                errors.append(f"{readme}: status table has no '| `{name}` | stable |' row")


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
        check_promotion_state(errors)
        check_dependency_claims(errors)
        check_discipline_sections(errors)
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
