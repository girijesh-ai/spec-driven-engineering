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
scope turns out bigger once you're in it, say so and reclassify up. A
heavier classification means more checking, never more features: the
design is still sized to the Goals.

## Process (bounded and architectural)

Everything written here is read by a person: the hypothesis, each
question, the restate, the design, the spec file. Before the first
question, call the Skill tool with `plain-technical-writing` and follow it
throughout. Simpler words, never less precision.

1. **Check existing context first** — files, docs, prior specs, the
   project's `GLOSSARY.md` and ADRs if present — before asking anything.
   Facts are your job: look them up (or dispatch a subagent) instead of
   asking. Decisions are the user's. If a requirement's terms are vague,
   overloaded, or used inconsistently, call the Skill tool with
   `domain-modeling` before continuing — an ambiguous term now becomes an
   ambiguous Success Criterion later.
2. **Open with your hypothesis.** One line each:
   `HYPOTHESIS: <what you think they want>` and
   `CONFIDENCE: ~N% — missing: <what would raise it>`.
3. **Ask clarifying questions one at a time**, each carrying your guess:
   `Q: <question>` / `GUESS: <your recommended answer and why>`. Word the
   question so "yes" accepts the guess: "Keep exports under 10k rows?",
   not "How big can exports get?". One
   question is one decision — never a bundle of sub-questions under one
   `Q:`. Cover purpose, constraints, who's affected, what "done" looks
   like, across successive questions. When an
   answer is a buzzword, probe it: "If you didn't have to justify this to
   anyone, what would you actually want?"

   The interview needs a live user. In an unattended run (CI, a loop, a
   scheduled job), don't answer your own questions: list them as blockers
   and stop.
4. **Stop asking when you can predict the answers to your next three
   questions.** If several rounds pass and you still can't, stop and say
   so: something foundational is missing, so ask whether to step back and
   reframe. Once you can predict them, restate in six lines and get a
   real yes:
   Outcome / User / Why now / Success / Constraint / Out of scope.
   "Sounds good", "sure", "whatever you think" are not a yes — ask the
   one question that would change the design.
5. **Right-size.** State the expected scale (users, requests, data
   volume) and lifetime (spike, prototype, or long-lived), as facts you
   found or as assumptions the user confirms. The design is sized to
   these numbers, not to growth nobody has asked for. Growth gets its own
   spec when it arrives.
6. **Propose approaches with trade-offs, one of them minimal.** The
   minimal approach is the smallest thing that meets the Goals. Climb
   `engineering-standards`' ladder for it: no new code, then a platform
   feature or an installed dependency, then the smallest change.
   Recommend it unless a named Goal or constraint rules it out, and name
   that Goal. Bounded: the recommendation next to the minimal option is
   enough (they may be the same). Architectural: 2-3 approaches. Cut
   speculative features from every approach — YAGNI applies at design
   time, not only at implementation time.
7. **Present the design in sections**, confirming each one lands before
   moving to the next.
8. **Architectural only:** write the spec to
   `docs/specs/YYYY-MM-DD-<topic>.md` using the template below, then stop.
   Planning happens in a later turn, after the user has read the file.

## Required spec sections (architectural)

```markdown
# <Topic>

## Context
Why this is being built. What prompted it, what problem it addresses.

## Goals
What this must achieve. Specific, not aspirational.

## Non-Goals
What's explicitly out of scope, one line each with its reason:
`<thing> — <why not now>`. List the tempting cuts too: anything a reader
might expect to see (a cache, an admin screen, a config option) that the
stated scale doesn't need. This is what stops scope creep later.

## Assumptions
ASSUMPTIONS I'M MAKING: one per line. The user corrects these now, or
they stand. The first line is always scale and lifetime, e.g. "Scale: ~5
internal users, reports under 2k rows. Lifetime: long-lived."

## Boundaries
- Always: <what every change under this spec must do>
- Ask first: <what needs a human yes before doing>
- Never: <what is off-limits>

## Approach
The chosen approach and why, briefly noting alternatives considered.
Name behaviour and interfaces, not file paths or code — those go stale;
the plan names files. Exception: a snippet that *is* the decision (a
signature, a schema). A flow of 3+ steps or 2+ interacting components
gets a Mermaid diagram.

## Testing Seams
Where tests attach: the highest seam that observes the behaviour, and as
few seams as possible. One line per seam on what it catches and what it
misses. Confirmed with the user.

## Success Criteria & Evals
Numbered, measurable, pass/fail — never "test manually" or "works
correctly." Each one names the exact command that checks it.

- **SC-1:** <condition>. Check: `<exact command, with flags>` → <expected result>
- **SC-2:** ...

`review-code` checks the implementation against exactly this list, and
plan steps cite these numbers.

## Open Questions
Anything still unresolved, and who needs to resolve it.
```

A spec without a completed **Success Criteria & Evals** section is not
done — do not hand it to `plan-from-spec` in that state.

**The spec is living.** When requirements change mid-build, change the
spec first, then the plan, then the code — never the code alone.

## Common rationalizations

| Rationalization | Reality |
|---|---|
| "The criterion is obvious, 'works correctly' is enough" | Downstream skills can only check what's written. Name the input, the command, the expected output |
| "I'll just ask, it's faster than reading the code" | Facts the repo already holds are yours to find. Asking costs the user time and signals you didn't look |
| "There's only one sensible approach" | Show it next to the minimal option and say why the minimal one falls short. If nothing does, the minimal one is the design |
| "It should be fast, so let's cache it" | Performance work needs a measured problem: a number from a profile, a log, or a load test. No number, no cache |
| "We'll need this at scale eventually" | Size to the stated scale. Growth that arrives gets its own spec, with real numbers |
| "Adding it now is cheaper than adding it later" | Only with a named Goal behind it. Unused flexibility is code someone has to read, test, and keep working |
| "They said 'sounds good', that's approval" | That's politeness. Approval names the design it's approving |
| "It's bounded, so I can skip confirmation" | Bounded skips the file, never the explicit yes before `plan-from-spec` |
| "It turned out bigger, but redoing the classification wastes work" | Hidden complexity upgrades the classification; it never downgrades one in progress |

## Red flags

- A question asked without a `GUESS:` attached
- A question the user has to read twice to understand
- A Success Criterion with no command next to it
- A Goal or criterion no one asked for and no stated constraint requires
- A queue, cache, background job, new service, or plugin point in a design with no scale number behind it
- An "Assumptions" section that is empty on an architectural spec
- Starting `plan-from-spec` in the same turn the spec file was written
- Code changed to match a new requirement while the spec still says the old one

## Verification

Before calling the spec done, confirm with evidence, not memory:

- [ ] No "TBD", placeholder, or vague requirement remains
- [ ] No two sections contradict each other
- [ ] One coherent spec — not two independent pieces that should be split
- [ ] Every Success Criterion has a number, one reading, and a command
- [ ] Every Goal traces to something the user said or a stated constraint
- [ ] Scale and lifetime are stated, and the minimal approach was shown
- [ ] Reading the recommendation, a staff engineer wouldn't ask "why didn't you just…?"
- [ ] Every Non-Goal has a reason, and the tempting cuts are listed
- [ ] The spec passes `plain-technical-writing`'s Verification list
- [ ] The user gave an explicit yes on the six-line restate and on the approach

## Next

Once the user has approved the written spec, call the Skill tool with
`plan-from-spec`.
