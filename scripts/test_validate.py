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


if __name__ == "__main__":
    unittest.main()
