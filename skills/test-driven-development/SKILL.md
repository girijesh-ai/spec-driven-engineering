---
name: test-driven-development
description: Use when implement or debug-systematically reaches a code seam that needs a test written before the implementation — the test-first sub-routine those skills drive, not a standalone entry point.
---

# test-driven-development
Status: stable

## Overview

Red-green-refactor, applied per seam within a plan step (see `implement`)
or per bug (see `debug-systematically`). The test is written first because
it's the only way to know the requirement was understood correctly before
code exists to rationalize around.

## The cycle

1. **Red** — write a test that encodes the requirement (a plan step's
   verification, or a bug's reproduction). Run it. It must fail, and fail
   for the reason you expect — not from a typo or missing import.
2. **Green** — write the minimum code to pass. Not the most elegant code,
   not the version that also handles three hypothetical future cases — the
   minimum that makes this specific test pass.
3. **Refactor** — clean up with the safety net of a passing test. Naming,
   duplication, structure. Re-run the test after every change.

## What counts as "the test first"

- Code before test → delete the code, start over. Not "keep it as
  reference," not "adapt it while writing the test" — delete means delete.
- "I already tested it manually" is not the same as a test existing in the
  suite. Manual verification doesn't survive the next refactor.
- Tests written immediately after the code, based on what the code already
  does, prove the code does what it does — not that it does what it
  should. That's not the same exercise.

## What the test should assert

- Behavior, not implementation. A test that breaks when you refactor
  without changing behavior is testing the wrong thing.
- Never mock the unit under test — only its external dependencies.
- Never weaken an assertion to make a red test go green. If the assertion
  was right and the code is wrong, fix the code.

## Common mistakes

| Mistake | Fix |
|---|---|
| Writing implementation first "since I already know what it should do" | Write the test first anyway — it's the check that you actually know, not a formality |
| Test passes on the first run | It didn't fail for the right reason first — verify the test actually exercises the new behavior |
| Gold-plating the green step | Write the minimum to pass this test; the next test drives the next increment |
| Skipping refactor because "it works" | Working and clean aren't the same bar — refactor while the test still protects you |

## Next

Feeds `implement` (per plan step) and `debug-systematically` (per bug fix).
