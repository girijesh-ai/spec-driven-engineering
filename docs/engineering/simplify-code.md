# simplify-code

**Status:** stable

## What it does

Makes working code simpler while its behaviour stays exactly the same.
It records a test baseline first and adds characterization tests (tests
that pin what the code does today) where coverage is thin. It finds out
why odd-looking code exists before removing it. Then it makes one
simplification per test run and per commit, and leaves existing tests
unchanged.

## When to reach for it

- A review flagged code as over-complex, dead, or a pass-through.
- A `plan-from-spec` prefactor step: the next change is hard to make
  because of the code around it.
- Explicit cleanup work.
- Not for anything that changes behaviour, even slightly. That's
  `spec-from-idea` or `debug-systematically`.

## Common questions

**What if the code has no tests?**
Write characterization tests first. Without them, "behaviour unchanged"
can't be checked. Each new test should fail when the code it pins is
broken; check that once by breaking it.

**What if a simplification needs a test changed?**
Stop. Either the behaviour moved, or the test was testing internals.
Decide which before going on.

**How do I know it got simpler?**
Count the concepts a reader needs before and after. If the count didn't
drop, the complexity moved instead of going away. Revert it.

**How was it proven?**
On this repo's `floor_guard.py` and `validate.py` (commits `8432295`
to `768074a`). Three characterization tests landed first. Then came three
simplifications, one per commit, with no existing test changed. The old
and new `is_test_path` gave the same result on 101 paths. Breaking each
changed piece turned a test red.

## It's working if

- Every commit holds one simplification, and the tests pass at each one.
- `git diff` on the existing tests shows only added lines.
- Each removed piece of odd-looking code has a stated reason it was safe
  to remove.
