#!/usr/bin/env python3
"""Regression tests for skills/review-code/scripts/floor_guard.py — stdlib unittest.

Each test builds a throwaway git repo with a `main` commit, makes a change on
a branch, and checks what the guard reports.

Run from the repo root:  python3 scripts/test_floor_guard.py
"""
from __future__ import annotations

import io
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

GUARD_DIR = Path(__file__).resolve().parent.parent / "skills" / "review-code" / "scripts"
sys.path.insert(0, str(GUARD_DIR))
import floor_guard  # noqa: E402  (path is set on the line above)

TEST_FILE = "tests/test_math.py"
BASE_TEST = """def test_add():
    assert add(2, 3) == 5
    assert add(0, 0) == 0
"""


class FloorGuardRepo(unittest.TestCase):
    def setUp(self) -> None:
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.repo = Path(tmp.name)
        self._git("init", "-q", "-b", "main")
        self.write(TEST_FILE, BASE_TEST)
        self.write("pyproject.toml", "[tool.coverage.report]\nfail_under = 90\n")
        self.write("src/app.py", "def add(a, b):\n    return a + b\n")
        self.commit("base")
        self._git("checkout", "-q", "-b", "feature")

    def _git(self, *args: str) -> None:
        subprocess.run(
            ["git", "-c", "user.name=t", "-c", "user.email=t@t", *args],
            cwd=self.repo,
            check=True,
            stdout=subprocess.DEVNULL,
        )

    def write(self, path: str, text: str) -> None:
        target = self.repo / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text)

    def commit(self, message: str) -> None:
        self._git("add", "-A")
        self._git("commit", "-q", "-m", message)

    def guard(self, *extra: str) -> tuple[int, str]:
        out, err = io.StringIO(), io.StringIO()
        with redirect_stdout(out), redirect_stderr(err):
            code = floor_guard.main(["--repo", str(self.repo), *extra])
        return code, out.getvalue() + err.getvalue()

    def rules(self) -> list[str]:
        findings, _, _, _ = floor_guard.run(self.repo, None)
        return sorted(f.rule for f in findings)

    def test_clean_change_exits_zero(self) -> None:
        self.write("src/app.py", "def add(a, b):\n    return b + a\n")
        code, output = self.guard()
        self.assertEqual(code, 0, output)
        self.assertIn("clean", output)

    def test_tightening_is_silent(self) -> None:
        self.write(TEST_FILE, BASE_TEST + "    assert add(-1, 1) == 0\n")
        self.write("pyproject.toml", "[tool.coverage.report]\nfail_under = 95\n")
        self.assertEqual(self.rules(), [])

    def test_skipped_test_is_flagged(self) -> None:
        self.write(TEST_FILE, "import pytest\n\n@pytest.mark.skip\n" + BASE_TEST)
        self.assertEqual(self.rules(), ["SKIPPED_TEST"])

    def test_removed_assertion_is_flagged(self) -> None:
        self.write(TEST_FILE, "def test_add():\n    assert add(2, 3) == 5\n")
        self.assertEqual(self.rules(), ["REMOVED_ASSERTION"])

    def test_deleted_test_file_is_flagged_but_rename_is_not(self) -> None:
        (self.repo / TEST_FILE).unlink()
        self.assertEqual(self.rules(), ["DELETED_TEST_FILE"])
        self.write("tests/test_arith.py", BASE_TEST)
        self._git("add", "-A")
        self.assertEqual(self.rules(), [])

    def test_lowered_threshold_is_flagged(self) -> None:
        self.write("pyproject.toml", "[tool.coverage.report]\nfail_under = 70\n")
        self.assertEqual(self.rules(), ["LOOSENED_THRESHOLD"])

    def test_code_variable_named_lines_is_not_a_threshold(self) -> None:
        self.write("src/app.py", "lines = 10\n")
        self.commit("add lines")
        self.write("src/app.py", "lines = 5\n")
        self.assertEqual(self.rules(), [])

    def test_untracked_file_with_suppression_is_flagged(self) -> None:
        self.write("src/new.py", "import os  # noqa\n")
        self.assertEqual(self.rules(), ["SUPPRESSION"])

    def test_prose_mentioning_a_suppression_is_not_flagged(self) -> None:
        self.write("docs/guide.md", "Never add `# noqa` or `@pytest.mark.skip` to pass.\n")
        self.assertEqual(self.rules(), [])

    def test_ml_fit_call_is_not_a_focused_test(self) -> None:
        self.write(TEST_FILE, BASE_TEST + "\ndef test_fit():\n    model.fit(x)\n    assert model\n")
        self.assertEqual(self.rules(), [])

    def test_content_lines_that_look_like_headers_stay_in_their_file(self) -> None:
        # "++ m;" is diffed as "+++ m;" and "-- k;" as "--- k;" — content, not headers.
        self.write("src/count.c", "void f() {\n-- k;\n}\n")
        self.commit("c file")
        self.write("src/count.c", "void f() {\n++ m;\nint x = 1; // NOSONAR\n}\n")
        findings, _, _, _ = floor_guard.run(self.repo, None)
        self.assertEqual([(f.rule, f.path, f.line) for f in findings], [("SUPPRESSION", "src/count.c", 3)])

    def test_output_names_location_not_content(self) -> None:
        self.write("src/app.py", 'TOKEN = "sk-secret-value"  # noqa\n')
        code, output = self.guard()
        self.assertEqual(code, 1)
        self.assertIn("src/app.py:1", output)
        self.assertNotIn("sk-secret-value", output)

    def test_missing_base_exits_two(self) -> None:
        code, output = self.guard("--base", "no-such-branch")
        self.assertEqual(code, 2)
        self.assertIn("Nothing was checked", output)


if __name__ == "__main__":
    unittest.main()
