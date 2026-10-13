---
name: plan-from-spec
description: Use when a spec or set of requirements exists and needs to become an ordered, executable implementation plan before any code is written — turns a spec's goals and success criteria into sequenced steps with named files and per-step verification.
---

# plan-from-spec
Status: stable

## Overview

Turns a spec (from `spec-from-idea`, or any written requirements) into an
ordered implementation plan: steps with explicit dependencies, the critical
files each step touches, and a verification action carried forward from the
spec's Success Criteria & Evals. A plan step with no traceable eval is
incomplete — it means either the spec is missing a criterion or the step
doesn't actually deliver something checkable.

## When to use

- A spec exists (or short bounded design was confirmed) and it's time to
  sequence the actual implementation work
- A large task needs to be broken into steps small enough to implement and
  verify independently
- Before `implement` — implementing without a plan means no dependency
  ordering and no per-step verification, just improvisation

## Process

The plan is read by people as well as by `implement`. Call the Skill tool
with `plain-technical-writing` before writing it: step names say what
changes in plain words, and every command, path, and `SC-n` stays exact.

1. **Read the spec fully.** Extract every Goal and every numbered Success
   Criterion (`SC-1`, `SC-2`, ...). If there's no spec, say so explicitly
   and ask whether to fall back to a short in-chat plan for a small,
   well-understood change, or to call the Skill tool with `spec-from-idea`
   first.
2. **Never overwrite a plan that's partly done.** If
   `docs/plans/` already has a plan for this topic with steps marked done,
   stop and ask: extend it, re-cut the remaining steps, or start a new
   file. Silent overwrites lose the record of what already shipped.
3. **Call the Skill tool with `codebase-architecture`, then identify the
   critical files** the
   work touches — it settles whether a step's natural boundary is a new
   module or an extension of an existing one before the file list gets
   locked in. Name files, don't enumerate every line; for a pattern
   repeated across many files, describe the pattern once and list a few
   representative paths.
4. **Prefactor first.** If the change is awkward in the code as it stands,
   the first step reshapes the code so the change becomes easy — behaviour
   unchanged, existing tests green — and the next steps make the easy
   change.
5. **Sequence into steps.** Each step is a tracer bullet through the
   system, independently implementable and verifiable — not a
   layer-by-layer build-out that can't be checked until everything is
   done. Order by dependency first; among steps that are ready, put the
   **riskiest first**, so a wrong assumption fails on step 1, not step 7.
   For a wide mechanical change that breaks many call sites at once, no
   vertical slice lands green — use **expand / migrate / contract**: add
   the new form beside the old, migrate callers in batches sized by blast
   radius, then delete the old form in its own step.
6. **Size every step** so one fresh context window can implement it:

   | Size | Shape |
   |---|---|
   | XS | One function or config value |
   | S | One file plus its tests, ~100 changed lines |
   | M | A few files in one module, ~300 changed lines |
   | L | Crosses a module boundary — split if you can |
   | XL | Always split |

   Also split a step that has more than 3 verification bullets, an "and"
   in its name, or touches two subsystems. Keep refactor steps separate
   from feature steps. Don't split below what one commit naturally holds:
   a small change is one or two steps, not six XS ones.
7. **Attach verification to every step**, citing the spec criterion it
   satisfies (`Satisfies: SC-2`) and the command that checks it. A step
   that maps to no criterion is **dropped by default**. Adding a criterion
   to keep it needs the user's explicit yes, and the new criterion goes
   into the spec first. Never invent a check to justify a step.
8. **Deletion test every step.** Ask: "if this step were dropped, which
   criterion would fail?" If none would, drop it. This catches steps that
   cite a criterion but don't move it, such as a config layer or an
   abstraction "for later".
9. **Mark checkpoints** every 2-3 steps: a point where the full suite runs
   and a human can look before more is built on top. A plan of 3 steps or
   fewer needs only the final full-suite run.
10. **Call out reuse.** Reference existing functions, modules, or patterns
   found during spec-writing or exploration that steps should reuse instead
   of reimplementing.

## Plan shape

```markdown
# Plan: <topic>

## Source spec
<path to spec, or "none — short bounded change confirmed in chat on <date>">

## Critical files
- <path> — <what changes and why>

## Order
<4+ steps: a Mermaid flowchart of step dependencies, e.g.
`1 --> 2`, `1 --> 3`, `2 & 3 --> 4`. Fewer steps: omit this section.>

## Steps
### 1. <step name>
- Status: todo                 ← todo / done <commit sha> / blocked <reason>
- Depends on: none
- Touches: <files>
- Size: S
- Satisfies: SC-1
- Verification: `<exact command>` → <expected result>

### 2. <step name>
- Status: todo
- Depends on: step 1
- Touches: <files>
- Size: M
- Satisfies: SC-2, SC-3
- Verification: `<exact command>` → <expected result>

**Checkpoint:** full suite green; human look before step 3.
```

`implement` updates each step's `Status` as it commits, so the plan file
is also the record of progress — a fresh session resumes from it.

Write the plan to `docs/plans/YYYY-MM-DD-<topic>.md`, mirroring the spec's
location, so `implement`, `finish-branch`, and `handoff` can link to it by
path. A small, well-understood change may keep the plan in chat instead —
but anything handed to `implement` as "the plan" gets the file.

## Common mistakes

| Mistake | Fix |
|---|---|
| Steps that can't be verified until the whole plan is done | Break further — every step should produce something checkable on its own |
| A step with no linked Success Criterion | Drop it. Keep it only if the user agrees to add a criterion to the spec first |
| Adding a criterion so a step has something to cite | That's scope growth through the back door. The spec changes only with the user's yes |
| A step for flexibility nothing asks for (config option, plugin point, generic base class) | Deletion test: if no criterion fails without it, it isn't in the plan |
| Enumerating every file/line for a repeated pattern | Describe the pattern once, list a few representative paths |
| Ignoring existing code that already does this | Reuse first — check what spec-from-idea's exploration already surfaced |
| Building the riskiest step last | Order risk-first among ready steps — a bad assumption should fail early, before other steps depend on it |
| One giant step "migrate all callers" | Expand / migrate in batches / contract, each batch its own step |
| Rewriting a plan file that already has done steps | Stop and ask; extend or re-cut, never silently overwrite |
| Step names in abstract jargon ("Implement resilience layer") | Name what changes: "Retry failed chunk uploads, up to 3 times" |
| Planning without reading the full spec | Half-read specs produce plans that miss non-goals and re-litigate settled questions |

## Next

Call the Skill tool with `implement`, step by step.
