# simple

**Status:** stable

## What it does

Turns a dense technical document (spec, design doc, RFC, ADR, long README)
into a **companion plain-language explainer** — a `<source-stem>-explained.md`
written next to the original, heavy on Mermaid diagrams, tables, and one
end-to-end worked example, that a PM, a leader, or a brand-new engineer can
understand in a single read. It keeps the technical vocabulary but explains
each term on first use, and it never invents anything the source doesn't say.

## When to reach for it

- Someone outside the authoring team needs to understand a dense doc:
  leadership deciding on it, a PM tracking it, a new engineer picking it up.
- You want a "TL;DR with pictures" that still links back to the authoritative
  source rather than replacing it.
- Not for docs already short and simple, or for anything with no stable
  source to point back to.

## Common questions

**Isn't this just summarizing?**
No — it's a faithful transformation, not a précis. Every claim, number, and
scope boundary must trace to the source; where the source is unclear it says
so ("the spec doesn't specify X yet") instead of guessing. A confident wrong
simplification is worse than none.

**Why keep the jargon instead of removing it?**
Readers will meet the terms on the team, so the explainer teaches them: the
term stays, with a plain-English gloss the first time it appears. Dumbing the
vocabulary down would leave the reader unable to follow the real doc.

**How is it different from `writing-for-agents`?**
`writing-for-agents` governs docs an agent reads to act; `simple` produces a
doc a *person* reads to understand. Different audience, different rules.

## It's working if

- A smart person outside the team can read the explainer once and explain the
  idea back correctly.
- Every first-class element in the source (each routed outcome, branch, exit,
  scope item) appears in the diagrams with equal weight — count them: N in the
  source means N in the picture.
- The explainer links back to the source, and nothing in it contradicts or
  outruns what the source actually says.
