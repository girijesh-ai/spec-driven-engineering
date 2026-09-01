# resolve-merge-conflicts

**Status:** stable

## What it does

Resolves git conflicts hunk by hunk by tracing what each side's change was
actually trying to do, instead of mechanically picking one side or
concatenating both.

## When to reach for it

- Any merge or rebase that stops with conflict markers.

## Common questions

**Why not just "accept theirs" for a whole file?**
Because it silently discards every real change the other side made across
that file, not just the ones that actually conflict with something.

**What if I genuinely can't tell what one side intended?**
Check the commit history or PR discussion for that hunk, or ask — don't
guess and move on.

## It's working if

- Resolved code passes tests, not just compiles.
- No hunk gets resolved by concatenating both sides without checking
  whether one actually supersedes the other.
