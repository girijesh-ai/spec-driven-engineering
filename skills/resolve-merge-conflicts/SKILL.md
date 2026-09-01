---
name: resolve-merge-conflicts
description: Use when a git merge or rebase produces conflicts — resolves each hunk by tracing what each side actually intended, not by mechanically picking one side or pasting both.
---

# resolve-merge-conflicts
Status: stable

## Overview

A conflict marker shows two changes that touched the same lines — it
doesn't show why either one was made. Resolving by pattern-matching the
diff (pick ours, pick theirs, concatenate both) produces code that compiles
but silently drops one side's actual intent.

## When to use

- Any `git merge`/`git rebase` that stops with conflict markers

## Process

1. **Read both commit messages/PR context for the conflicting change**,
   not just the diff. What was each side trying to accomplish?
2. **For each conflicting hunk**, determine: are these two changes to the
   same concern (one supersedes the other), or two unrelated changes that
   happen to touch adjacent lines (both need to be kept, merged)?
3. **Resolve by intent.** If one side's change is now redundant because
   the other side already covers it differently, say so and drop the
   redundant one — don't keep both out of caution. If both are needed,
   merge them properly, don't just concatenate the two hunks and hope they
   compose.
4. **After resolving, re-run the relevant tests** — a conflict resolution
   that compiles can still be behaviorally wrong in a way tests catch and
   a read-through doesn't.
5. **If genuinely unsure what one side intended**, don't guess — ask, or
   look at the commit history/PR discussion for that line before
   resolving.

## Common mistakes

| Mistake | Fix |
|---|---|
| "Accept theirs"/"accept ours" across a whole file without reading each hunk | Resolve hunk by hunk — a whole-file accept silently discards real changes |
| Concatenating both sides when they conflict on the same logic | Determine if one supersedes the other first — concatenation often produces dead or duplicated logic |
| Skipping tests after a clean-looking resolution | Re-run tests — a resolution can compile and still be behaviorally wrong |
| Guessing at unclear intent rather than checking history | Check the commit/PR context, or ask, before resolving a hunk you don't understand |

## Next

Once resolved and tests pass, this feeds back into whatever finished the
merge/rebase — `finish-branch` if it was blocking an integration.
