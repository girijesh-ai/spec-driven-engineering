---
name: spec-from-idea
description: Use when starting any non-trivial feature, subsystem, or design change before writing code, or when requirements exist only in conversation with nothing written down — turns an idea into a spec with measurable success criteria that downstream implementation and review can be checked against.
---

# spec-from-idea
Status: stable

## Overview

Turns an idea into a written spec: goals, non-goals, chosen approach, and
measurable success criteria. This is the entry point of this repo's spine
(`spec-from-idea -> plan-from-spec -> implement -> review-code ->
finish-branch`) — everything downstream traces back to what gets written
here.

## When to use

- Starting a new feature, subsystem, or any change that isn't a one-line fix
- Requirements exist only in conversation, nothing written down yet
- Before `plan-from-spec` — a plan without a spec has nothing to verify against

Skip for: typo fixes, one-line config changes, anything an existing spec
already covers.

## Classify first

State the classification out loud before asking anything else:

- **Spike** — a feasibility question ("can we...", "is this possible").
  Output is an answer, not a spec. State the question and probe plan in
  2-3 sentences, get a nod, investigate as cheaply as correctness allows,
  report a recommendation. Stop here — skip the rest of this skill.
- **Bounded** — a well-scoped change to something that already exists, small
  enough to hold in one head. A short design in chat (a few sentences to a
  few short paragraphs) is enough; skip the file unless Success Criteria
  genuinely need more than a couple of lines.
- **Architectural** — a new subsystem, new project, or a change to an
  interface other things depend on. Full process below, spec written to a
  file.

When in doubt, take the heavier path. Nothing downgrades mid-task — if
scope turns out bigger once you're in it, say so and reclassify up.

## Process (bounded and architectural)

1. Check existing context first — files, docs, prior specs — before asking
   anything. Don't make the user repeat what's already written down.
   If a requirement's terms are vague, overloaded, or used inconsistently
   across the conversation, invoke `domain-modeling` before continuing —
   an ambiguous term now becomes an ambiguous Success Criterion later.
2. Ask clarifying questions **one at a time**: purpose, constraints, who's
   affected, what "done" looks like. Prefer specific questions over
   open-ended ones.
3. Propose 2-3 approaches with trade-offs. Lead with the recommendation and
   why. Cut speculative features from every approach — YAGNI applies at
   design time, not only at implementation time.
4. Present the design in sections, confirming each one lands before moving
   to the next.
5. Architectural only: write the spec to `docs/specs/YYYY-MM-DD-<topic>.md`.

## Required spec sections (architectural)

```markdown
# <Topic>

## Context
Why this is being built. What prompted it, what problem it addresses.

## Goals
What this must achieve. Specific, not aspirational.

## Non-Goals
What's explicitly out of scope. This is what stops scope creep later.

## Approach
The chosen approach and why, briefly noting alternatives considered.

## Success Criteria & Evals
Measurable, pass/fail conditions — never "test manually" or "works
correctly." Each one must be checkable by running something specific or
reading a specific output. `review-code` checks the implementation against
exactly this list.

## Open Questions
Anything still unresolved, and who needs to resolve it.
```

A spec without a completed **Success Criteria & Evals** section is not
done — do not hand it to `plan-from-spec` in that state.

## Self-review before done

Re-read with fresh eyes before calling it finished:

- Any "TBD", placeholder, or vague requirement? Fix it now.
- Do any sections contradict each other?
- Is this one coherent spec, or does it actually cover two or more
  independent pieces that should be split and sequenced separately?
- Could any Success Criterion be read two different ways? Pick one meaning
  and make it explicit.

## Common mistakes

| Mistake | Fix |
|---|---|
| Success criteria that say "works correctly" | Replace with a concrete check: input X produces output Y, command Z exits 0, endpoint returns status N |
| Writing the spec before checking existing code/docs | Explore first — the thing may already exist, partially or fully |
| Jumping straight to one approach | Always present 2-3 with trade-offs, even when the answer feels obvious — the trade-offs are what get approved, not just the pick |
| Treating "bounded" as a way to skip approval | Bounded skips the file, never the confirmation — get an explicit yes before moving to `plan-from-spec` |
| Downgrading scope mid-task to avoid redoing work | Hidden complexity upgrades the classification; it never downgrades one already in progress |

## Next

Once approved, hand off to `plan-from-spec`.
