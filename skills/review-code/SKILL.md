---
name: review-code
description: Use when about to commit, push, or open a PR for any non-trivial change — the last gate that checks the change against its spec and the engineering standards before it ships.
---

# review-code
Status: stable

## Overview

Two-axis review. **Axis 1 (primary): spec compliance** — does the diff
satisfy the spec's Success Criteria & Evals? **Axis 2 (secondary): standards
compliance** — does it hold up against `engineering-standards` and
`codebase-architecture`? The diff tells you what changed; this skill checks
whether the change is *correct in full context*, which the diff alone can't
show.

## When to use

- Before every commit inside `implement` (per-step, not just at the end)
- Before `git push` or opening a PR
- Any time you're about to claim a change is "done"

## No-spec fallback

If no spec is linked, do not skip Axis 1 silently. Report it explicitly:
**"spec axis skipped — no spec found."** Then run Axis 2 (standards) in
full — standards compliance never depends on a spec existing.

## Process

### Step 1 — Establish scope

List every changed file and the total additions/deletions. State in one
sentence what the change is trying to do.

### Step 2 — Axis 1: spec compliance

Read the spec's Success Criteria & Evals (if one exists). For each
criterion: does the diff satisfy it? Concretely — run the check the
criterion describes, don't eyeball it. Report each criterion as met, not
met, or not applicable, with why.

### Step 3 — Read the full diff, then the full changed files

Read the diff completely first. Then, for **every** file that appears in
it, read the entire file — not just the changed lines. Diff context is
misleading; bugs hide in the surrounding code that wasn't touched. Pay
attention to: callers of the changed code, error/exception handling above
and below the change, module-level state the change touches, imports
added or removed.

### Step 4 — Caller and cross-file impact

For every public function, endpoint, or exported symbol that changed:

1. Grep for all usages across the codebase.
2. If a public interface (API, endpoint, exported function signature)
   changed: does every caller still send/receive what it now expects? Does
   it handle new response codes or error states?
3. Do existing tests cover the new behavior, or are they still asserting
   the old contract?
4. Do scripts, CLIs, or other tools call the changed function?

### Step 5 — Resource and failure-path audit

For every resource allocated in the changed code (connections, file
handles, locks, background tasks, external clients): trace every early
return (validation failure, auth failure, capacity check, dependency
absent). Was the resource allocated before that return? If yes, is it
released on that path? Check `try/finally`, context managers, and
equivalent cleanup constructs are actually reached on all paths, not just
the happy one.

For every external dependency touched (network call, database, queue, LLM
API): what happens if it's absent/unconfigured, times out, returns
unexpected data, or raises mid-operation? A conditional check like
`if dependency is not None:` needs its `else` branch audited too — nothing
security- or correctness-critical should be silently skipped there.

### Step 6 — Axis 2: standards and architecture

Run the change against `engineering-standards` (naming, SRP, error
handling, security, DRY, necessity/simplicity, backward compatibility) and
`codebase-architecture` (module depth, interface width, and layer-boundary
direction). A change can be fully spec-compliant and pass every other
standards check and still be over-engineered — check necessity
explicitly, don't assume it falls out of the other checks.

### Step 7 — Structured report

```markdown
### Scope
Files changed, additions/deletions, one-paragraph summary of intent.

### Spec compliance (Axis 1)
Per criterion: met / not met / not applicable — with why.
(No spec at all: "spec axis skipped — no spec found.")

### Confirmed issues
File, line, what's wrong, failure scenario, concrete fix.

### Plausible issues
Lower-confidence concerns needing verification, or genuine edge cases.

### Standards & architecture (Axis 2)
Findings against engineering-standards / codebase-architecture.

### Clean
What's done well and correct — don't skip this, it's signal too.

### Verdict
READY — no confirmed issues; spec criteria met or not applicable, or the spec axis was explicitly skipped (no spec).
NEEDS FIXES — N confirmed issues listed above.
```

Do not report READY until every confirmed issue is resolved.

## Common mistakes

| Mistake | Fix |
|---|---|
| Reviewing only the diff lines | Read the complete changed files — bugs hide in unchanged surrounding code |
| Treating a missing spec as an automatic pass | Report "spec axis skipped," never silently treat it as satisfied |
| Checking Axis 2 but skipping caller/cross-file grep | A correct-looking diff can still break every caller of a changed signature |
| Eyeballing whether a criterion is met | Actually run the check the criterion describes |
| Skipping the resource/failure-path audit on "small" changes | Small diffs leak resources just as easily as big ones — audit every early return regardless of diff size |

## Next

READY hands off to `finish-branch`. NEEDS FIXES goes back to `implement`.
