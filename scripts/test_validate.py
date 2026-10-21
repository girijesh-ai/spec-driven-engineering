#!/usr/bin/env python3
"""Regression tests for scripts/validate.py — stdlib unittest, no external deps.

Run from the repo root:  python3 scripts/test_validate.py
"""
from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import validate  # noqa: E402  (path is set on the line above)


class CheckPromotedDocs(unittest.TestCase):
    def setUp(self) -> None:
        # check_promoted_docs reads the module-level REPO_ROOT; each test points
        # it at a throwaway tree. Capture the real one now and restore it at
        # teardown so the suite stays hermetic for any later test that needs it.
        original_root = validate.REPO_ROOT
        self.addCleanup(setattr, validate, "REPO_ROOT", original_root)

    def _errors_for(self, root: Path) -> list[str]:
        validate.REPO_ROOT = root  # point the checker at a throwaway tree
        errors: list[str] = []
        validate.check_promoted_docs(errors)
        return errors

    def test_non_bucket_doc_dirs_are_ignored(self) -> None:
        """docs/specs/ and docs/plans/ hold artifacts, not skill docs.

        spec-from-idea and plan-from-spec tell users to write
        docs/{specs,plans}/YYYY-MM-DD-<topic>.md. Those files must not make
        the validator demand a skill named after each dated artifact.
        """
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for bucket in ("specs", "plans"):
                bucket_dir = root / "docs" / bucket
                bucket_dir.mkdir(parents=True)
                (bucket_dir / "2026-09-02-example.md").write_text("# artifact\n")
            self.assertEqual(self._errors_for(root), [])

    def test_bucket_doc_without_skill_is_still_flagged(self) -> None:
        """The real check must keep firing: a promoted doc with no skill."""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            bucket_dir = root / "docs" / "engineering"
            bucket_dir.mkdir(parents=True)
            (bucket_dir / "ghost.md").write_text("# ghost\n")
            errors = self._errors_for(root)
            self.assertTrue(
                any("skills/ghost/SKILL.md does not" in e for e in errors),
                f"expected a missing-skill error, got: {errors}",
            )

    def test_unexpected_docs_subdir_is_flagged(self) -> None:
        """A docs/ subdir that is neither a known bucket nor a known artifact
        dir must error. Without this, restricting the scan to DOC_BUCKETS would
        let a future bucket go silently unvalidated instead of loudly flagged.
        """
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            surprise = root / "docs" / "security"
            surprise.mkdir(parents=True)
            (surprise / "some-doc.md").write_text("# doc\n")
            errors = self._errors_for(root)
            self.assertTrue(
                any("unexpected docs/ subdir" in e for e in errors),
                f"expected an unexpected-subdir error, got: {errors}",
            )


class CheckDisciplineSections(unittest.TestCase):
    def setUp(self) -> None:
        original_root = validate.REPO_ROOT
        self.addCleanup(setattr, validate, "REPO_ROOT", original_root)

    def _errors_for(self, root: Path) -> list[str]:
        validate.REPO_ROOT = root
        errors: list[str] = []
        validate.check_discipline_sections(errors)
        return errors

    def _write_skills(self, root: Path, body: str) -> None:
        for name in validate.DISCIPLINE_SKILLS:
            skill_dir = root / "skills" / name
            skill_dir.mkdir(parents=True)
            (skill_dir / "SKILL.md").write_text(body)

    def test_all_sections_present_is_clean(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self._write_skills(
                root, "## Common rationalizations\n## Red flags\n## Verification\n"
            )
            self.assertEqual(self._errors_for(root), [])

    def test_missing_section_is_flagged_per_skill(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self._write_skills(root, "## Common mistakes\n## Verification\n")
            errors = self._errors_for(root)
            self.assertEqual(len(errors), 2 * len(validate.DISCIPLINE_SKILLS), errors)
            self.assertTrue(any("'## Red flags'" in e for e in errors), errors)


class CheckPromotionState(unittest.TestCase):
    """A promotion edits SKILL.md, its doc, README.md and docs/in-progress.md.
    Each half-done state must fail, not just the doc's own structure.
    """

    def setUp(self) -> None:
        original_root = validate.REPO_ROOT
        self.addCleanup(setattr, validate, "REPO_ROOT", original_root)
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.root = Path(tmp.name)
        self.skill("done", "stable")
        self.doc("done", "stable")
        self.readme_rows = ["| `done` | stable |"]
        self.in_progress_rows: list[str] = []

    def skill(self, name: str, status: str) -> None:
        skill_dir = self.root / "skills" / name
        skill_dir.mkdir(parents=True)
        (skill_dir / "SKILL.md").write_text(f"# {name}\nStatus: {status}\n")

    def doc(self, name: str, status: str) -> None:
        bucket_dir = self.root / "docs" / "engineering"
        bucket_dir.mkdir(parents=True, exist_ok=True)
        (bucket_dir / f"{name}.md").write_text(f"# {name}\n\n**Status:** {status}\n")

    def errors(self) -> list[str]:
        (self.root / "README.md").write_text("\n".join(self.readme_rows) + "\n")
        (self.root / "docs" / "in-progress.md").write_text(
            "\n".join(self.in_progress_rows) + "\n"
        )
        validate.REPO_ROOT = self.root
        errors: list[str] = []
        validate.check_promotion_state(errors)
        return errors

    def test_fully_promoted_and_untouched_draft_are_clean(self) -> None:
        self.skill("wip", "draft")
        self.in_progress_rows.append("| `wip` | engineering |")
        self.assertEqual(self.errors(), [])

    def test_doc_status_differs_from_skill_status(self) -> None:
        self.skill("half", "draft")
        self.doc("half", "stable")
        self.assertTrue(any("half" in e and "Status" in e for e in self.errors()))

    def test_skill_with_doc_page_still_in_progress(self) -> None:
        self.in_progress_rows.append("| `done` | engineering |")
        self.assertTrue(any("in-progress.md" in e for e in self.errors()))

    def test_stable_skill_without_doc_page(self) -> None:
        self.skill("bare", "stable")
        self.readme_rows.append("| `bare` | stable |")
        self.assertTrue(any("bare" in e and "docs page" in e for e in self.errors()))

    def test_draft_skill_listed_in_readme(self) -> None:
        self.skill("early", "draft")
        self.readme_rows.append("| `early` | stable |")
        self.assertTrue(any("lists draft skill 'early'" in e for e in self.errors()))

    def test_stable_skill_missing_from_readme_status_table(self) -> None:
        self.readme_rows = []
        self.assertTrue(any("README.md" in e for e in self.errors()))


if __name__ == "__main__":
    unittest.main()
