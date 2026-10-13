#!/usr/bin/env bash
# Small Python repo with a utils module and a unittest suite, no spec or plan.
set -euo pipefail
mkdir -p tests
cat > utils.py <<'PY'
def truncate(text, limit):
    """Cut text to at most `limit` characters, adding an ellipsis if cut."""
    if len(text) <= limit:
        return text
    return text[: limit - 1] + "…"
PY
cat > tests/__init__.py <<'PY'
PY
cat > tests/test_utils.py <<'PY'
import unittest

from utils import truncate


class TruncateTest(unittest.TestCase):
    def test_short_text_unchanged(self):
        self.assertEqual(truncate("abc", 5), "abc")

    def test_long_text_cut_with_ellipsis(self):
        self.assertEqual(truncate("abcdef", 4), "abc…")


if __name__ == "__main__":
    unittest.main()
PY
printf 'Run tests with: python3 -m unittest discover -s tests -t .\n' > README.md
git init -q && git add -A && git -c user.name=eval -c user.email=eval@example.com commit -q -m init
