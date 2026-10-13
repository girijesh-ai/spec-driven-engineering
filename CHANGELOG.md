# Changelog

Versions follow semver (`.claude-plugin/plugin.json`). Renaming a plugin or
skill is a breaking change.

## Unreleased

- **New draft skill `plain-technical-writing`:** one standard for anything
  a person reads. Plain words, short sentences, and terms glossed on first
  use, with no loss of precision: numbers, commands, paths, and `SC-n` IDs
  stay. Draw a diagram for any flow of 3+ steps: Mermaid in files, ASCII
  in chat. `spec-from-idea`, `plan-from-spec`, `grill-me`, `handoff`,
  `finish-branch`, and `domain-modeling` call it. Plans with 4+ steps gain
  an Order diagram. Prompted by user feedback that output read as too
  "Claude-like".
- **Right-sized specs and plans.** `spec-from-idea` states scale and
  lifetime first and always shows the minimal approach, recommending it
  unless a named Goal rules it out. `plan-from-spec` drops steps that map
  to no criterion (adding a criterion needs the user's yes) and runs a
  deletion test on every step. `codebase-architecture` runs design-it-twice
  only for interfaces that are hard to change later, without a fixed
  "most flexible" option. `grill-me` weighs an edge case before making it
  a requirement. `engineering-standards` extracts duplicates on the third
  copy, or the second when they must change together. New eval
  `spec-right-size`. From addyosmani/agent-skills (`idea-refine`,
  `incremental-implementation`, `performance-optimization`): Non-Goals
  carry a reason and list the tempting cuts; over-built vs simple
  examples and the "why didn't you just…?" check; no performance work
  without a measured problem. `plain-technical-writing` asks for a
  diagram only where a flow would take a paragraph to follow, not for
  every 3-step flow.

## 2.0.0 — 2026-10-12

**Breaking:** the plugin is renamed `spec-driven-engineering` → `sde`, and
the dev marketplace `spec-driven-engineering-dev` → `sde-dev`. Skills are
now `/sde:<skill>`; skill names are unchanged. Reinstall once — see
README, "Renamed to `sde` in 2.0.0".

Adopts the accepted items from
[`research/2026-10-12-upstream-findings.md`](research/2026-10-12-upstream-findings.md)
(mattpocock/skills v1.3.1, addyosmani/agent-skills 0.6.12):

- **spec-from-idea, grill-me** — hypothesis and confidence up front; every
  question carries a `GUESS:`; one question is one decision; facts are
  looked up, decisions asked; stop test; "not a yes" list. Spec template
  adds Assumptions, Boundaries, Testing Seams, and numbered `SC-n`
  criteria that each name their command; the spec is living.
- **plan-from-spec** — prefactor first, XS–XL sizing with split rules,
  riskiest ready step first, expand/migrate/contract, checkpoints, per-step
  `Status`, never overwrite a partly-done plan.
- **implement** — clean baseline, NOTICED BUT NOT TOUCHING, 100-line
  tripwire, stop the line into `debug-systematically`, revertable commits,
  plan status updates. Fires on small ad-hoc changes too.
- **test-driven-development** — find the real test command, agreed seams,
  tautological and horizontal-slicing anti-patterns, mock only at system
  boundaries, Real > Fake > Stub > Mock.
- **review-code** — spec discovery order, pinned fixed point, change
  sizing, scope creep, mutation spot-check, severity (only Critical and
  Required block READY), smells baseline, performance and dependency
  checks, and the new **floor guard** (`scripts/floor_guard.py`). Fires
  on inline diffs.
- **finish-branch** — PR template with Summary, Evidence, Merge danger,
  Not touched; rollback plan for one-way doors; a stakeholder summary via
  `simple`, sourced from the shipped code.
- **debug-systematically** — red-capable feedback loop before any
  hypothesis (`references/feedback-loops.md`), 3–5 ranked hypotheses,
  can't-reproduce table, tagged debug logs, untrusted error output,
  redaction.
- **handoff, dev-workflow** — working tree, verification, and approvals
  sections; phase-boundary order; shared operating rules and trust levels.
- **codebase-architecture, domain-modeling** — deletion test, adapter
  rule, dependency categories, design it twice, contracts; `GLOSSARY.md`
  and ADRs.
- **engineering-standards** — DAMP exemption for tests, untrusted text,
  redaction, `CONSTRAINTS.md` override, smells reference.
- **writing-for-agents** — positive prompts, completion criteria, leading
  words, progressive disclosure, explicit "Call the Skill tool with `x`"
  (applied across all skills), discipline-skill sections.
- **Discipline skills** (spec-from-idea, implement, review-code,
  test-driven-development, debug-systematically) close with Common
  rationalizations, Red flags, and Verification; `scripts/validate.py`
  enforces it.
- **New draft skills:** `doubt-check`, `retro`, `simplify-code`,
  `source-driven` — tracked in `docs/in-progress.md` until dry-run.
- **Plugin evals** in `evals/` for six skills (`claude plugin eval`).
- **Repo:** this changelog, a CI workflow, and `docs/out-of-scope.md`.

## 1.1.0 — 2026-09-23

- Added `simple` (plain-language explainer for dense docs).
- OpenCode support as a Claude-Code-independent skill catalog.

## 1.0.2 — 2026-09-04

- `grill-me` requires a live answer and never answers on the requester's
  behalf.

## 1.0.1 — 2026-09-03

- Casing, version, and walkthrough accuracy fixes from review.

## 1.0.0 — 2026-09-02

- Catalog hardened for team rollout; all skills promoted to stable after
  dry runs.

## 0.1.0 — 2026-09-01

- First release: 16-skill spec/design-driven workflow.
