---
name: plain-technical-writing
description: Use when writing anything a person on the team will read — a spec, plan, interview question, handoff, PR description, ADR, glossary entry, or project doc — so it reads as simple, plain language while keeping its full technical precision.
---

# plain-technical-writing
Status: stable

## Overview

One standard for everything a person reads: **simple words, the same
technical rigour.** Simple means easy to read, not less exact. Every number,
command, file path, `SC-n` ID, and technical term stays. What goes is the
padding around them: inflated words, long sentences, and points buried in
clauses.

The bar: a new engineer on the team understands it in one read, and a
senior engineer finds nothing vague.

Not this skill: instructions an agent reads (SKILL.md, CLAUDE.md) follow
`writing-for-agents`. Rewriting an existing dense document as a companion
explainer for non-engineers is `simple`.

## Keep vs cut

| Keep (precision) | Cut (padding) |
|---|---|
| Numbers, limits, units, timeouts | Openers: "It's worth noting", "Importantly", "Let's dive in" |
| Exact commands, paths, `SC-n` IDs, SHAs | Inflated words: leverage, robust, seamless, ensure (full list in `references/patterns.md`) |
| Technical terms, glossed on first use | Hedge stacks: "may potentially", "could possibly" |
| Edge cases and constraints | Restating the question; "In summary" closers |
| The reason behind each decision | Flourishes: "not just X, but Y", three-adjective lists |

## Rules

1. **Lead with the point.** The first sentence says what it is or what to
   do. Background comes after.
2. **One idea per sentence.** Aim for under 20 words. A sentence with two
   "and"s or a dash-wrapped aside is two sentences.
3. **Active voice, real subject.** "The worker retries 3 times", not
   "Retries are performed".
4. **Plain word first.** "use", not "leverage"; "check", not "ensure";
   "help", not "facilitate".
5. **Keep the term, explain it once.** The first time a term appears that
   a new engineer may not know, add a plain gloss: "idempotent (safe to run
   twice; the second run changes nothing)". Never swap the term for a vague
   phrase.
6. **Concrete beats abstract.** "A 2 GB export times out after 30 s", not
   "large exports may have performance issues".
7. **State the consequence, not the adjective.** Not "critical", but "if
   this fails, the order is charged twice".
8. **Format serves reading.** Bullets for parallel items, tables for
   comparisons, prose for reasoning. Bold only what the reader must not
   miss, not a label on every bullet.

## Draw it when words get tangled

Add a diagram when the text describes:

- a flow of 3+ steps, or a decision with branches → flowchart
- 2+ parts exchanging messages over time → sequence diagram
- something that moves between states (order: new → paid → shipped) →
  state diagram
- a before/after change in structure → two small side-by-side sketches

Pick the format by where it will be read:

- **Markdown files** (specs, plans, docs, ADRs, PR descriptions) → Mermaid.
- **Chat, terminal, code comments** → ASCII. Mermaid shows up there as raw
  text.

Keep diagrams to about 10 boxes, with plain labels. The diagram shows the
shape; the text still carries every precise detail (commands, numbers,
criteria). Templates and examples are in `references/patterns.md`.

## Applied to each artifact

| Artifact | What it looks like |
|---|---|
| Spec (`spec-from-idea`) | Context in 2-4 plain sentences. Approach gets a diagram when it has a flow or 2+ components. Success Criteria stay exact: condition, command, expected result |
| Plan (`plan-from-spec`) | Step names say what changes, in plain words: "Add retry to the upload worker", not "Implement resilience layer". A plan with 4+ steps gets a dependency diagram |
| Interview question (`spec-from-idea`, `grill-me`) | `Q:` is one plain sentence the user can answer without decoding it. `GUESS:` is the answer plus "because", in one or two sentences. Use the user's own words for things; gloss any term they didn't use |
| Handoff, PR description, ADR, glossary entry | Lead with the outcome. One diagram if there is a flow. Every claim still points at a command, path, or SHA |

## Common mistakes

| Mistake | Fix |
|---|---|
| Simplifying by dropping detail ("handles errors") | Keep the detail, simplify the sentence: "on a 5xx it retries 3 times, then fails the job" |
| Replacing a term with a vague phrase ("the thing that stores sessions") | Keep "Redis session store" and gloss it once |
| A diagram that repeats the paragraph next to it | Let the diagram show the shape; cut the paragraph down to what the diagram can't show |
| Mermaid in a chat reply | ASCII in chat, Mermaid in files |
| A diagram for a two-step flow | Two steps fit in one sentence; draw from three up |

## Verification

Before calling the text done:

- [ ] Read only the first sentence of each section: together they tell the story
- [ ] No word from the swap list in `references/patterns.md` is left
- [ ] Every term a new engineer may not know is glossed once
- [ ] Nothing precise was lost: every number, command, path, and ID from the draft is still there
- [ ] A flow of 3+ steps or 2+ interacting parts that would take a paragraph to follow has a diagram: Mermaid in files, ASCII in chat
