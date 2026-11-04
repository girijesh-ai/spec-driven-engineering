#!/usr/bin/env bash
# The code-auto repo, plus unit 1's file as code-journey wrote it before the engineer said go.
set -euo pipefail
mkdir -p tests docs/specs docs/plans
cat > utils.py <<'PY'
def truncate(text, limit):
    """Cut text to at most `limit` characters, adding an ellipsis if cut."""
    if len(text) <= limit:
        return text
    return text[: limit - 1] + "…"
PY
: > tests/__init__.py
cat > tests/test_utils.py <<'PY'
import unittest

from utils import truncate


class TruncateTest(unittest.TestCase):
    def test_long_text_cut_with_ellipsis(self):
        self.assertEqual(truncate("abcdef", 4), "abc…")


if __name__ == "__main__":
    unittest.main()
PY
cat > docs/specs/2026-01-05-text-utils.md <<'MD'
# Text utils

## Goals
Add slugify and a safe filename helper to utils.py.

## Success Criteria & Evals
- **SC-1:** `slugify("Hello, World!")` returns `"hello-world"`. Check: `python3 -m unittest tests.test_utils -k slugify` → OK
- **SC-2:** `safe_filename("../etc/passwd")` returns `"etc-passwd"`: no path separators or `..` survive. Check: `python3 -m unittest tests.test_utils -k safe_filename` → OK
MD
cat > docs/plans/2026-01-05-text-utils.md <<'MD'
# Plan: text utils

## Source spec
`docs/specs/2026-01-05-text-utils.md`

## Steps
### 1. Add slugify
- Status: todo
- Depends on: none
- Touches: `utils.py`, `tests/test_utils.py`
- Size: XS
- Model: sonnet (one function, routine)
- Satisfies: SC-1
- Verification: `python3 -m unittest tests.test_utils -k slugify` → OK

### 2. Add safe_filename on top of slugify
- Status: todo
- Depends on: step 1
- Touches: `utils.py`, `tests/test_utils.py`
- Size: S
- Model: opus (path handling; a miss lets a caller write outside its folder)
- Satisfies: SC-2
- Verification: `python3 -m unittest tests.test_utils -k safe_filename` → OK
MD
mkdir -p docs/plans/2026-01-05-text-utils/units
cat > docs/plans/2026-01-05-text-utils/units/01-slugify.md <<'MD'
# Unit 01: add slugify

## The picture
Titles like "Hello, World!" need to become web-safe names like
"hello-world". This step adds one small function that does that.

## What changes
A new `slugify(title)` in `utils.py`: lowercase, spaces to hyphens,
punctuation removed.

## Why
Step 2's `safe_filename` builds on it (SC-1).

## Files
`utils.py`, `tests/test_utils.py`

## How we'll know
`python3 -m unittest tests.test_utils -k slugify` → OK
MD
printf 'Run tests with: python3 -m unittest discover -s tests -t .\n' > README.md
git init -q && git add -A && git -c user.name=eval -c user.email=eval@example.com commit -q -m init
