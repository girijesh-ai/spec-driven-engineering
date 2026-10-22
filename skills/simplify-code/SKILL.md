---
name: simplify-code
description: Use when existing code works but is harder to read or change than it needs to be — removing dead code, collapsing needless layers, untangling a function — and behaviour must stay exactly the same.
---

# simplify-code
Status: draft

## Overview

Simplifying is a change with one requirement: behaviour doesn't move.
This skill makes that requirement checkable. Adapted from
addyosmani/agent-skills' `code-simplification`. It complements
`engineering-standards`' necessity check, which prevents complexity
being added; this removes complexity that's already there. `review-code`
findings like Middle Man or Speculative Generality often land here.

## When to use

- A review flagged code as over-complex, dead, or a pass-through
- A change is hard to make because of the code around it (as a prefactor
  step from `plan-from-spec`)
- Explicit cleanup work

Not for: changing behaviour, even slightly. That's a feature or a fix and
goes through `spec-from-idea` or `debug-systematically`.

**Scope.** Simplify the code the current change touches, or what the user
named. Code outside that is a drive-by refactor: list it under
`implement`'s NOTICED BUT NOT TOUCHING instead. Simplifications land in
their own commits and PR, never mixed into a feature or fix.

## Process

1. **Read the conventions.** Read the project's `CLAUDE.md` and how the
   neighbouring code handles the same pattern (naming, error handling,
   imports, type annotations). Simpler means more like this codebase, not
   more like your own taste.
2. **Baseline.** Run the existing tests for the code you'll touch and
   record the result. If coverage of that code is thin, add
   characterization tests first (assert what it does today) — they're
   the only thing that makes "behaviour unchanged" checkable.
3. **Chesterton's Fence.** Before removing anything that looks pointless,
   find out why it's there: `git log -L` or `git blame` on the lines, the
   linked issue or PR. Remove it only once you know, and say what you
   found. If you can't find out, ask.
4. **One simplification at a time.** Make one change (inline one wrapper,
   delete one dead branch, extract one function), run the tests, commit.
   Then the next. A batch of simplifications that breaks something can't
   tell you which one did.
5. **Existing tests pass unmodified.** If a simplification needs a test
   changed, the behaviour moved, or the test was testing internals. Stop
   and decide which before going on.
6. **Check it got simpler.** Count the concepts a reader needs to follow
   the code before and after. If the count didn't drop, the complexity was
   moved, not removed — revert. Fewer lines is not the goal: inlining a
   helper that named a concept, or merging two simple functions into one
   complex one, makes the code harder to read. Error handling stays at
   least as strict as before.
7. **Over ~500 changed lines of the same mechanical edit, use a codemod**
   (an AST rewrite, `sed` with a review of every hunk, an IDE refactoring)
   rather than editing by hand — hand edits at that scale drift.
8. **Dead code:** list what you believe is unreachable, with how you know
   (no callers found by grep, no dynamic lookup by name), and ask before
   deleting public or exported symbols.

## Common mistakes

| Mistake | Fix |
|---|---|
| Removing a check whose purpose isn't obvious | Find out why it exists first (blame, history, issue); ask if you can't |
| Ten simplifications in one commit | One per test run, one per commit |
| Editing a test so a simplification passes | The behaviour moved or the test is wrong — stop and decide which |
| Removing error handling because it "makes the code cleaner" | Keep it; that's a behaviour change |
| Inlining a helper whose name explained the code | Keep the name; fewer lines isn't simpler |
| Simplifying code outside the current change | List it as NOTICED BUT NOT TOUCHING; simplify only what was asked |
| Extracting helpers until the code is "clean" | Count concepts; if it didn't drop, it wasn't simpler |
| Deleting an exported symbol because grep found no callers | Callers outside the repo, or by-name lookups, don't show in grep. Ask |

## Next

Call the Skill tool with `review-code` before each commit, as with any
change.
