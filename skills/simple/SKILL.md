---
name: simple
description: Use when asked to simplify, explain, or make a plain-language / visual version of a dense document (spec, design doc, RFC, ADR, technical proposal) for PMs, leadership, or new engineers — also triggers on "explain this doc", "make it understandable", "KISS version", "TL;DR with diagrams", "add pictures" — producing a companion plain-language explainer.
---

# simple
Status: stable

## Overview

Turns a dense technical document into a **companion plain-language explainer** that a PM, a leader,
or a brand-new engineer can understand in one read — heavy on pictures (Mermaid diagrams, ASCII
mockups, tables), light on prose. Technical vocabulary is **kept** (readers will meet it on the
team) but every term is explained in plain words the first time it appears.

This is a **transformation**, not a rewrite: the explainer says the same things the source says,
more simply. It never invents facts, decisions, or numbers the source doesn't contain.

## When to use

- "Simplify / explain this doc", "make a KISS version", "make this understandable for leadership",
  "add pictures", "TL;DR with diagrams", "onboarding version of this spec."
- Any dense artifact: spec, design doc, RFC, ADR, architecture proposal, long README.

Skip for: something already short and simple, or a doc with no stable source to point back to
(the explainer must link to a source of truth).

## The one hard rule

**Simplify, never fabricate.** Every claim, number, scope boundary, and decision in the explainer
must trace to the source document. If the source doesn't say it, the explainer doesn't either.
When the source is genuinely unclear on a point, say so plainly ("the spec doesn't specify X yet")
rather than inventing an answer. A confident wrong simplification is worse than no explainer.

## Process

1. **Read the whole source document first.** Identify: the core idea, the problem it solves, the
   key decision(s), the moving parts, what's in/out of scope, how success is measured, and who the
   readers are. If the argument (a doc path) is missing, ask which document to simplify.
2. **Find the single sentence.** What is this doc about, in one sentence a non-expert gets? This
   becomes §1. If you can't write it, re-read — you don't understand the doc yet.
3. **Name the audiences.** Usually PM/leadership (want the *why* and the differentiator) and new
   engineers (want the *shape* and where to start). Tailor the closing takeaways to each.
4. **Draft the explainer** using the section template below. Reach for a picture before a
   paragraph. Every major concept gets a diagram, a table, or a worked example — not three
   paragraphs of prose.
5. **Glossary-on-first-use.** The first time a technical term appears, explain it in plain words
   (inline or in a small "what it means simply" table). Keep the term — don't dumb the vocab down.
6. **Write one worked example** that walks a concrete input through the whole thing end-to-end.
   Concrete beats abstract every time (use real example values from the source).
7. **Write the output** to the **same folder** as the source, named `<source-stem>-explained.md`.
   Open with a callout block: who it's for, what it explains, and a link back to the source doc.
8. **Self-check** (below) before calling it done.

## Section template (adapt to the source; drop what doesn't apply)

```markdown
# <Title> — the plain-language version

> **Who this is for:** <audiences>.
> **What it explains:** the why and what of <link to source doc> — in pictures.
> Technical terms are kept but explained on first use.

## 1. The one-sentence version         → a single blockquote
## 2. The problem, in one picture       → Mermaid + a good/bad table + the guiding principle
## 3. Where this fits                    → Mermaid pipeline/architecture, our part highlighted
## 4. The core idea                      → the central decision as a flowchart (the "aha" diagram)
## 5. Key mechanism(s)                   → diagram + plain-English glossary table
## 6. A worked example, end to end       → sequence diagram or step-through with real values
## 7. How we'll know it works            → the metrics/success table, each as "the question it answers"
## 8. In scope vs out of scope           → two-column Mermaid (green = in, red = out)
## 9. The takeaway for each reader        → one short paragraph per audience, linking into the source
```

Not every doc needs all nine — a bounded doc might be 4–5 sections. Keep sections short.

## Visual toolkit (use liberally)

- **Mermaid `flowchart`** for pipelines, decisions (`{diamond}` for choices), architecture.
- **Mermaid `sequenceDiagram`** for a request/interaction walked over time.
- **ASCII box mockups** for anything the user would see on screen (a question, a UI, a message).
- **Tables** for "term → what it means simply" and "metric → the question it answers."
- **Good/bad or before/after** framing to make a decision's motivation obvious.
- **Tasteful emoji** as visual anchors (✅ ❓ 🚦 👤 🔎 ⛔ 💡) — a few per diagram, not confetti.
- **Color classes** in Mermaid (`classDef`) to make "our part" / "in scope" / "danger" pop.

## Self-review before done

- Could a smart person outside the team read this once and explain the idea back? If not, simplify.
- Is every claim traceable to the source? Remove anything you can't point to.
- More pictures than prose blocks? If it's a wall of text, you've under-diagrammed.
- Is each technical term explained on first use, with the term itself kept?
- Does it link back to the source of truth so readers can go deeper?
- Does the closing tailor a takeaway to each named audience?
- Does every first-class element in the source (each routed outcome, branch, exit, scope item)
  appear in the pictures with equal weight? **Count them** — if the source has N, the diagram has N.
  Simplifying *density* is the job; dropping or demoting *structure* is a bug.

## Common mistakes

| Mistake | Fix |
|---|---|
| Inventing detail to fill a section | Cut the section, or say "the source doesn't cover this yet" |
| Dumbing down the vocabulary | Keep the term, add a plain-English gloss on first use |
| Walls of prose with one diagram at the top | Lead with the picture; prose only supports it |
| Abstract examples ("some query") | Use the source's real example values in a concrete walk-through |
| One-size-fits-all summary | Tailor the closing takeaway per audience (PM vs engineer) |
| Writing it as a replacement | It's a companion — always link back to the authoritative source |
| Demoting or burying a first-class element (a routed outcome, branch, or scope entry) as a footnote or aside | Give peer elements **equal visual weight**. If the source treats N outcomes as siblings, the diagram shows N siblings — a buried element reads as a missing one and misleads reviewers. |
