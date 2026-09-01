---
name: debug-systematically
description: Use when encountering any bug, test failure, or unexpected behavior, before proposing a fix — a disciplined reproduce, minimize, hypothesize, instrument, root-cause loop instead of guessing at symptoms.
---

# debug-systematically
Status: draft

## Overview

A report names a symptom, not a cause. This skill's job is to find the
cause before touching code — guessing at a fix from the symptom alone
produces patches that fix one path and leave every sibling path broken.

## When to use

- Any bug report, failing test, or unexpected behavior
- Before proposing any fix — including a fix that feels obvious

## The loop

1. **Reproduce.** Get a reliable repro first. A bug you can't reproduce
   on demand is a bug you can't confirm you fixed.
2. **Minimize.** Strip the repro down to the smallest input/state that
   still triggers it. Every extra variable in the repro is a hypothesis
   you haven't ruled out.
3. **Hypothesize.** State a specific, falsifiable hypothesis for the
   cause — not "something's wrong with X," but "X returns null when Y is
   empty, and the caller doesn't check."
4. **Instrument.** Add the smallest check that would prove or disprove the
   hypothesis — a log line, an assertion, a debugger breakpoint. Don't
   change behavior yet, only observe it.
5. **Confirm the root cause**, not just a plausible one. If the
   instrumentation doesn't confirm the hypothesis, form a new one — don't
   patch around the disproven guess anyway.
6. **Fix at the root, not the symptom.** Before editing, grep every caller
   of the function about to change. A guard added in the one shared
   function all callers route through is usually a smaller diff than a
   guard added in the caller the report happened to name, and it's the
   only version that fixes every sibling caller too.
7. **Write the failing-test-first regression check** (via
   `test-driven-development`) using the minimized repro, then fix.

## Common mistakes

| Mistake | Fix |
|---|---|
| Patching the code path the report happened to name | Grep all callers of the function first — fix where they all route through |
| Proposing a fix before reproducing | No repro, no confirmed fix — get the repro first, even if it takes longer |
| Treating a plausible hypothesis as confirmed | Instrument and observe before believing it — plausible isn't the same as confirmed |
| Fixing without a regression test | The minimized repro is exactly the input a test needs — write it before or as part of the fix |
| Debugging with print statements left in the final diff | Remove instrumentation once the root cause is confirmed, unless it belongs as permanent logging |

## Next

Fix goes through `implement`'s normal test-first, review-before-commit
flow — this skill only covers finding the cause, not landing the change.
