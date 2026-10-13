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

## Before the first test

- **Find the real test command.** Read the repo (`package.json`,
  `pyproject.toml`, `Makefile`, CI config) — never assume `npm test` or
  `pytest`. Run it once so you know what green looks like.
- **Test at the agreed seam.** The spec's Testing Seams section (or the
  plan step) names where tests attach. Pick the highest seam that observes
  the behaviour; don't invent new seams per test.

## The cycle

1. **Red** — write **one** test that encodes the requirement (a plan
   step's verification, or a bug's reproduction). Run it. It must fail, and fail
   for the reason you expect — not from a typo or missing import.
2. **Green** — write the minimum code to pass. Not the most elegant code,
   not the version that also handles three hypothetical future cases — the
   minimum that makes this specific test pass.
3. **Refactor** — clean up with the safety net of a passing test. Naming,
   duplication, structure. Re-run the test after every change.

Then the next test. One test at a time, vertically: writing every test up
front (horizontal slicing) locks in a design before the first one has
taught you anything.

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
- An expected value written down, not recomputed. `expect(add(a, b))
  .toBe(a + b)` re-derives the answer the way the code does and passes
  whatever the code does — a tautological test. Write `toBe(5)`.
- Never weaken an assertion to make a red test go green. If the assertion
  was right and the code is wrong, fix the code.
- Tests may repeat themselves. Each test should read on its own (DAMP);
  the DRY rule in `engineering-standards` exempts test bodies.

## Test doubles

Mock only at **system boundaries** — external APIs, the clock, randomness,
the network. Never mock the unit under test, and never mock your own
modules to make a test easier to write. When a double is needed, prefer
the most real one that works:

**Real > Fake** (working in-memory version) **> Stub** (canned answers)
**> Mock** (asserts on calls).

Prefer SDK-style interfaces (`payments.charge(order)`) over generic ones
(`http.post(url, body)`) at the boundary — they're easier to fake.

## Verification

Before handing back to the calling skill:

- [ ] The test was seen failing, for the expected reason (paste the failure line)
- [ ] It now passes, and the full file it lives in passes
- [ ] No test was skipped, deleted, or loosened to get there
- [ ] Coverage of the touched code didn't drop, where the project measures it

## Common rationalizations

| Rationalization | Reality |
|---|---|
| "I already know what it should do, I'll write the code first" | The test is the check that you actually know. Code first → delete it, start over |
| "It passed first time, great" | It never failed for the right reason, so it may not exercise the new behaviour. Make it fail first |
| "I tested it manually" | Manual checks don't survive the next refactor. Only a test in the suite counts |
| "I'll compute the expected value the same way, it's cleaner" | That's a tautological test — it passes whatever the code does |
| "Mocking this internal module makes the test simpler" | It makes the test agree with the mock. Mock only at system boundaries |
| "It works, refactor can wait" | Working and clean are different bars; refactor while the test still protects you |
| "This assertion is too strict, I'll loosen it" | If the assertion was right, the code is wrong. Fix the code |

## Red flags

- A green test you never saw red
- A new `skip`, `xfail`, `.only`, or commented-out assertion in the diff
- Expected values built with the same expressions as the code under test
- A mock of a module the project owns
- Several new failing tests at once

## Next

Feeds `implement` (per plan step) and `debug-systematically` (per bug fix).
