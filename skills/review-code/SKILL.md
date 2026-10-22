---
name: review-code
description: Use when about to commit, push, or open a PR for any non-trivial change, or when asked to review a change or diff — including a diff pasted inline rather than on a branch — the last gate that checks it against its spec and the engineering standards before it ships.
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

## Finding the spec

Look in this order and stop at the first hit: a spec path passed to you →
the plan's `Source spec` line → issue or spec references in the branch's
commit messages → a `docs/specs/` file whose topic matches the branch or
feature name → ask.

## No-spec fallback

If no spec is found, do not skip Axis 1 silently. Report it explicitly:
**"spec axis skipped — no spec found."** Then run Axis 2 (standards) in
full — standards compliance never depends on a spec existing.

## Process

### Step 1 — Pin the fixed point, establish scope

Record exactly what is under review: `git rev-parse HEAD` and the base
(merge-base with the target branch). Before a commit (the per-step review
inside `implement`) the work isn't in HEAD yet: review `git diff <base>`,
which runs to the working tree, plus untracked files from `git status
--porcelain`. `<base>...HEAD` would miss all of it. Confirm the diff is
non-empty — reviewing an empty or wrong range reports READY on nothing.
List every changed file and the total additions/deletions. State in one
sentence what the change is trying to do.

Size check: ~100 changed lines reviews well, ~300 is acceptable, ~1000
should have been split — say so. Whole-file deletions and codemod output
don't count toward the size: check their intent, not every line. A
refactor mixed into a feature diff is
a finding: they belong in separate commits.

### Step 2 — Axis 1: spec compliance

Read the spec's Success Criteria & Evals (if one exists). For each
criterion: does the diff satisfy it? Concretely — run the check the
criterion describes, don't eyeball it. Report each criterion as met, not
met, or not applicable, with why.

**Mutation spot-check.** For at least one criterion the diff claims to
satisfy, copy the file, then break the code it depends on — invert one
condition, return early. Confirm the mutation landed (diff against the
copy), run that criterion's check, then restore the file from the copy.
If the check stays green, it doesn't guard the criterion: that's a
confirmed finding against the test, not the code. Name the test case
that's missing.

**Scope creep.** Also report behaviour in the diff that no criterion or
goal asked for. Unrequested behaviour has nothing to be checked against.

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

### Step 6 — Floor guard

Run this skill's `scripts/floor_guard.py` from the repo under review:
`python3 <this skill's dir>/scripts/floor_guard.py --base <target branch>`.
It flags new suppressions, skipped or focused tests, stubs (including an
empty `catch` and a `TODO` comment), deleted test files, net-removed assertions,
lowered coverage thresholds, relaxed lint/type config, and in
`CONSTRAINTS.md`: rules removed or with their numbers changed, new rows
in an Exceptions table, or the file itself deleted. Exit 0 = clean,
1 = findings, **2 = it didn't run** — report a 2 as "floor guard did not
run", never as clean. Each finding is a confirmed issue unless the spec
or plan explicitly calls for that change.
If the project has a `CONSTRAINTS.md`, check its enforced rules too.

### Step 7 — Axis 2: standards and architecture

Call the Skill tool with `engineering-standards`, then again with
`codebase-architecture`. Run the change against the first (naming, SRP,
error handling, security, DRY, necessity/simplicity, backward
compatibility) and the second (module depth, interface width, and
layer-boundary direction). A change can be fully spec-compliant and pass every other
standards check and still be over-engineered — check necessity
explicitly, don't assume it falls out of the other checks.

Skip anything the project's tooling already enforces (formatter, linter,
typechecker, CI checks): report only what would get past those tools.

Also check:
- **Smells** — the baseline in `engineering-standards`'
  `references/smells.md`, in code the diff added or changed only. Name the
  smell and quote the hunk. Always judgement calls; a documented repo
  standard overrides them.
- **Refactors** — does it reduce complexity or just move it? Count the
  concepts a reader needs before and after.
- **Performance** — queries or calls inside loops, unbounded reads or
  result sets, work repeated on a hot path.
- **Dead code and dependencies** — list code the change made unreachable
  and ask before deleting it. For each new dependency, ask: does the
  standard library or an existing dependency already do this? Is it
  maintained, of a reasonable size, with a compatible license and no known
  vulnerabilities? A "no" is a finding. Read the lockfile diff for what
  came along with it. An upgrade is one dependency per change, with its
  changelog read.

For the final whole-branch review (before `finish-branch`), you may run
Axis 1 and Axis 2 in separate subagents so neither colours the other.
Report each axis's findings as they came; never re-rank across axes.

### Step 8 — Structured report

```markdown
### Scope
Files changed, additions/deletions, one-paragraph summary of intent.

### Spec compliance (Axis 1)
Per criterion: met / not met / not applicable — with why.
(No spec at all: "spec axis skipped — no spec found.")

### Scope creep
Behaviour in the diff no criterion or goal asked for (or "none").

### Floor guard
Exit code and findings, or "did not run — <reason>".

### Confirmed issues
Severity, file, line, what's wrong, failure scenario, concrete fix.

### Plausible issues
Lower-confidence concerns needing verification, or genuine edge cases.

### Standards & architecture (Axis 2)
Findings against engineering-standards / codebase-architecture.

### Clean
What's done well and correct — don't skip this, it's signal too.

### Verdict
READY — no confirmed Critical or Required issues; spec criteria met or not applicable, or the spec axis was explicitly skipped (no spec).
NEEDS FIXES — N confirmed Critical/Required issues listed above.
```

**Severity** is a second label on every finding, separate from
confirmed/plausible (which is confidence):

| Severity | Meaning | Blocks READY? |
|---|---|---|
| Critical | Wrong behaviour, data loss, security hole, unmet criterion | Yes |
| Required | Breaks a standard the project holds, or a caller | Yes |
| Optional | Worth doing; the author decides | No |
| Nit | Style or taste | No |
| FYI | Context, no action | No |

Do not report READY while any confirmed Critical or Required issue is
open.

## Common rationalizations

| Rationalization | Reality |
|---|---|
| "The diff looks fine, no need to open the files" | Bugs hide in the unchanged code around the diff. Read the complete files |
| "There's no spec, so Axis 1 passes" | Report "spec axis skipped — no spec found". A missing spec is never a pass |
| "The signature change is small, callers will be fine" | Grep every caller. A correct-looking diff can break all of them |
| "The test for that criterion exists, so it's met" | Run it — then break the code once and run it again. A check that can't fail guards nothing |
| "It's a small change, skip the failure-path audit" | Small diffs leak resources as easily as big ones |
| "The floor guard errored, I'll treat it as clean" | Exit 2 means nothing was checked. Say so |
| "It's not perfect, but it's better than before" | Severity decides what blocks, not overall impression. Confirmed Critical/Required still block |

## Red flags

- A READY verdict with no command output behind any criterion
- No `git rev-parse` value recorded for what was reviewed
- Floor guard missing from the report
- Behaviour in the diff that no criterion mentions, unreported
- Every finding marked Nit

## Verification

Before issuing the verdict:

- [ ] HEAD and base SHAs are recorded, uncommitted work is in the range, and the diff is non-empty
- [ ] Each criterion's check ran in this session (or the axis is explicitly skipped)
- [ ] At least one mutation spot-check ran and went red
- [ ] Floor guard exit code is in the report
- [ ] Every changed file was read in full and every changed public symbol grepped

## Next

Inside `implement` (one step): READY returns to `implement` to commit;
NEEDS FIXES returns to it to fix. On the whole branch: READY means call
the Skill tool with `finish-branch`.
