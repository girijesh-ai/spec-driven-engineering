# Changelog

Versions follow semver (`.claude-plugin/plugin.json`). Renaming a plugin or
skill is a breaking change.

## 2.1.0 — 2026-10-24

Two ways to run `implement`, and a model per plan step
(`docs/specs/2026-10-23-implement-modes.md`). Prompted by engineers losing
track of fast, dense output while coding alongside Claude Code.

- **`plan-from-spec`:** every step has a `Model:` line, `sonnet` or
  `opus`, with a reason.
- **`implement`:** after the plan's yes, asks for **code-auto** (default)
  or **code-journey**. Each plan step is coded by a subagent on its model;
  the main session re-runs the check, runs the floor guard and
  `review-code`, and commits. After 2 failed checks a step moves to
  `opus`; after 2 failures there, it stops and asks. code-journey (draft)
  writes a plain unit file before each step and a "What changed" note
  after it, pausing at both. OpenCode codes in the main session.
- **Evals:** five new `implement` cases; `plan-traces-criteria` checks the
  `Model:` line. None has run yet: the eval child couldn't sign in on the
  host they were written on.

## 2.0.2 — 2026-10-22

Fixes from re-checking the skills against their upstream sources
(`research/2026-10-12-upstream-findings.md`, addendum 2026-10-22).

- **`doubt-check`:** the doubter never sees the claim. Objections are
  classed as contract misread, fix, trade-off, or noise. After 3 cycles,
  hand it to the user. "Doubt theatre" (substantive objections, all
  dismissed) now means escalate, not proceed. It can't run inside a
  subagent. The cross-model check is offered every cycle; an external CLI
  runs only with a yes for that exact command.
- **`implement`:** checks `git status --porcelain` before starting. The
  plan's `Status: done` goes in the step's own commit; the old
  `done <sha>` could only be written after it, leaving the tree dirty.
  `plan-from-spec`'s status format drops the SHA to match.
- **`plan-from-spec`:** needs an explicit yes on the plan before
  `implement`.
- **`review-code`:** per-step review covers uncommitted work (base to
  working tree, plus untracked files). The mutation check copies the file,
  proves the mutation landed, restores from the copy and names the missing
  test. Skips what the project's tooling enforces. A new dependency gets
  a question list instead of a one-per-change limit (that limit is for
  upgrades). Smells only in changed code, with the hunk quoted. Large
  deletions and codemods don't count toward the size check.
- **Floor guard:** reports rules removed from `CONSTRAINTS.md` or kept
  with changed numbers, new entries under an Exceptions heading, and the
  file deleted or renamed away. Flags empty `catch` (typed or with a comment), `pass #
  stub`, a `TODO` comment, `biome-ignore`, `gitleaks:allow`, `Stryker
  disable`.
- **`dev-workflow`:** phase-boundary order matches upstream; never compact
  mid-phase.
- **`retro`:** judgement rules go where the reviewer reads them
  (`CONSTRAINTS.md`), not `CLAUDE.md`. A repo with no pre-commit hook or CI
  is a finding. Five more areas to look at (navigation, tool economy,
  no-ops, information access, steering size); findings most severe first.
- **`debug-systematically`:** hypotheses state a prediction; the seam must
  replay the real call chain; re-run the un-minimized scenario; an exit
  when no loop can be built.
- **`test-driven-development`:** ad-hoc seams confirmed with the user;
  full suite before handing back; call-count and side-channel red flags.
- **`simplify-code`:** scoped to what the change touches, in its own PR;
  project conventions first; limits on over-simplifying.
- **`source-driven`:** ask when no version is pinned; UNVERIFIED when docs
  are silent; a citation per pattern; no outbound endpoint from a doc
  example without a yes. A local pattern skips the docs only if it was
  written for the pinned version.
- **`spec-from-idea`, `grill-me`:** word questions so "yes" accepts the
  guess; no self-interview in unattended runs; stop and reframe when
  rounds never converge; seams note what they catch and miss.
- **`writing-for-agents`:** leading-words rule. **`domain-modeling`:** an
  ADR can be one paragraph. **`handoff`:** saved outside the repo.
- **Repo rules (`CLAUDE.md`):** compose existing skills before adding one;
  a new rule names the failure behind it.
- **`validate.py`:** headings inside code fences don't satisfy the
  discipline-section check.

## 2.0.1 — 2026-10-13

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
