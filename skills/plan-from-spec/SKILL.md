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

1. **Read the spec fully.** Extract every Goal and every Success Criterion.
   If there's no spec, say so explicitly and ask whether to fall back to a
   short in-chat plan for a small, well-understood change, or to go back to
   `spec-from-idea` first.
2. **Check `codebase-architecture`, then identify the critical files** the
   work touches — it settles whether a step's natural boundary is a new
   module or an extension of an existing one before the file list gets
   locked in. Name files, don't enumerate every line; for a pattern
   repeated across many files, describe the pattern once and list a few
   representative paths.
3. **Sequence into steps.** Each step should be independently implementable
   and independently verifiable — a tracer bullet through the system, not a
   layer-by-layer build-out that can't be checked until everything is done.
   Order by dependency: a step never assumes something a later step
   produces.
4. **Attach verification to every step**, sourced from the spec's Success
   Criteria & Evals. If a step doesn't map to any criterion, either the
   step is unnecessary or the spec is missing one — resolve which before
   moving on, don't silently invent a check.
5. **Call out reuse.** Reference existing functions, modules, or patterns
   found during spec-writing or exploration that steps should reuse instead
   of reimplementing.

## Plan shape

```markdown
# Plan: <topic>

## Source spec
<path to spec, or "none — short bounded change confirmed in chat on <date>">

## Critical files
- <path> — <what changes and why>

## Steps
### 1. <step name>
- Depends on: none
- Touches: <files>
- Verification: <the spec criterion this satisfies, stated as a concrete check>

### 2. <step name>
- Depends on: step 1
- Touches: <files>
- Verification: <criterion>
```

## Common mistakes

| Mistake | Fix |
|---|---|
| Steps that can't be verified until the whole plan is done | Break further — every step should produce something checkable on its own |
| A step with no linked Success Criterion | Stop and resolve: either drop the step or fix the spec, don't invent an ad-hoc check silently |
| Enumerating every file/line for a repeated pattern | Describe the pattern once, list a few representative paths |
| Ignoring existing code that already does this | Reuse first — check what spec-from-idea's exploration already surfaced |
| Planning without reading the full spec | Half-read specs produce plans that miss non-goals and re-litigate settled questions |

## Next

Hand off to `implement`, step by step.
