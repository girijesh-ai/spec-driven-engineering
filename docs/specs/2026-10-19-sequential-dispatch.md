# Sequential dispatch: plan → units → one fresh agent per unit

## Context

Today `implement` runs a whole plan in one session with one model. On a
long plan, the context grows with every step, so later steps work with a
crowded context, and easy steps run on the same model as hard ones.

This spec turns each plan step into a **unit**: a step written so that a
fresh agent, without the conversation that wrote the plan, can build it
from its own file. `implement` then runs the units one at a time, each in a
new subagent on a model picked by how hard the unit is.

The idea and its rules come from
[`research/2026-10-12-tickets-and-parallel-implement.md`](../../research/2026-10-12-tickets-and-parallel-implement.md).
Its five open decisions, and three new ones, were settled in a `grill-me`
session on 2026-10-19. All three prerequisites landed in 2.0.0:

- the floor guard (`d4aa33c`): a script that flags changes that weaken
  tests or checks;
- NOTICED BUT NOT TOUCHING (`42edd5c`): a list `implement` keeps of
  problems it saw but deliberately left alone;
- numbered success criteria, `SC-n` (`3793d64`).

## Goals

1. `plan-from-spec` writes a plan index plus one unit file per step,
   when the plan has 3 or more steps. Each field lives in one place only.
2. `implement` switches to dispatch mode automatically for a plan with 3
   or more units, and runs them one at a time, each in a fresh subagent.
3. On Claude Code, each unit runs on `sonnet` (tiers S and M) or `opus`
   (tier L). A tier is how hard the unit is, set in the plan. Reviewers
   always run on `opus`.
4. On OpenCode, the same loop runs with two implementer agent definitions,
   "standard" and "strong", whose models the user sets.
5. One real 5–8 unit plan is run in both modes, and the token, time, and
   rework numbers are recorded.

## Non-Goals

- Parallel worktrees — wall-clock speed is not the bottleneck; approvals
  and review are. Revisit only if the SC-9 numbers show time is a real cost.
- A separate test-writer agent for tier-L units — the floor guard, the
  mutation spot-check (the reviewer breaks the code and checks the test
  goes red), and the diff-only reviewer already catch a bent test. Add it
  if the dry run shows a bent test getting through on an L unit.
- `haiku` as a tier — the user chose `sonnet` and `opus` only.
- Units as GitHub issues — files work offline, in OpenCode, and need no
  permissions.
- A PR per unit — many criteria pass only once several units land, and
  `finish-branch` checks every criterion on the whole set.
- A new skill (like mattpocock's `implement-spec`) — the spine stays five
  links; this is a mode of `implement`.
- Tempting cuts, none needed at this scale: a unit database or JSON state
  file, a dashboard of unit progress, per-unit cost tracking inside the
  run, a config option for the 3-unit threshold.

## Assumptions

ASSUMPTIONS I'M MAKING:
- Scale: plans of 3–8 steps, one engineer running one plan at a time.
  Lifetime: long-lived.
- The plan's existing step fields (`Status`, `Depends on`, `Touches`,
  `Size`, `Satisfies`, `Verification`) and checkpoints stay as they are
  in `plan-from-spec` 2.0.1.
- Claude Code's Agent tool takes the aliases `sonnet` and `opus`, so no
  model IDs are hard-coded.
- OpenCode (1.18.10, from `opencode --version`) sets a subagent's model
  in its agent definition (`model: provider/model-id`), not per call: the
  Task tool takes no `model` parameter
  ([`tool/task.ts:44-58`](https://github.com/anomalyco/opencode/blob/v1.18.10/packages/opencode/src/tool/task.ts#L44-L58)). With no `model` set,
  the subagent runs on the caller's model
  ([`tool/task.ts:181`](https://github.com/anomalyco/opencode/blob/v1.18.10/packages/opencode/src/tool/task.ts#L181)). Project agent files go in
  `.opencode/agents/` (`.opencode/agent/` also loads,
  [`config/agent.ts:13`](https://github.com/anomalyco/opencode/blob/v1.18.10/packages/opencode/src/config/agent.ts#L13)).
- SC-4 and SC-5 run on a host where Bash works inside the eval sandbox
  (it did not on the RHEL 8 host in `evals/README.md`).

## Boundaries

- Always: the orchestrator (the agent running the loop) re-runs each
  unit's Verification itself; an implementer's "tests pass" is a claim,
  not evidence.
- Always: stage only the unit's files; one commit per unit; the code
  builds at every commit.
- Ask first: before starting the run (one explicit approval of the units),
  at every pause, and whenever a stop condition is hit.
- Never: an implementer edits a unit's test to make it pass by weakening
  it; implementers or reviewers start agents of their own (depth 1).

## Approach

**Artifacts (option C, chosen over a plan-only and a full-copy design).**
The plan file becomes an index; each unit file holds the detail. No field
appears in both, so they can't drift apart.

| Lives in the plan index | Lives in the unit file |
|---|---|
| Unit ID, `Status`, `Depends on`, `Satisfies`, `Tier`, `Risk` | Plain step name, `Touches` (predicted), `Size`, `Verification`, `Context` |

- Plan: `docs/plans/YYYY-MM-DD-<topic>.md`, with a `## Units` table.
- Units: `docs/plans/YYYY-MM-DD-<topic>/units/NN-<slug>.md`.
- `Size` (XS–L; XL must be split) is how much work. `Tier` (S/M/L) is how
  hard: scored on ambiguity, blast radius, novelty, risk, and test
  difficulty. They are scored separately.
- `Context` names the spec sections to read, the existing code pattern to
  copy, and gotchas found while planning.
- Plans with 1–2 steps keep today's format, with no units folder.

Alternatives: **A, plan only** (add Tier/Risk/Context to plan steps) was
smallest, but gives a cold agent the whole plan and little room for
per-unit context. **B, full copy in unit files** (the research
proposal's sketch) gives focus, but repeats Status and criteria in two
places.

**The loop**, in `implement`, with its mechanics in
`implement/references/dispatch.md`:

```mermaid
flowchart TD
  A{Plan has 3+ units?} -- no --> S[Today's single-session implement]
  A -- yes --> B[Clean baseline + one explicit approval]
  B --> C[Next ready unit: dependencies done, riskiest first]
  C --> D[Implementer subagent, model by Tier:<br/>reads its unit file + cited spec sections,<br/>test first, runs Verification]
  D --> E[Orchestrator: re-runs Verification,<br/>floor guard, stages the unit's files]
  E --> F[Reviewer subagent on opus:<br/>unit file + diff + criteria only, up to 3 rounds]
  F --> G[Commit; index Status: done sha;<br/>collect NOTICED BUT NOT TOUCHING]
  G --> H{3 units since last pause,<br/>or next unit high-risk?}
  H -- yes --> P[Pause for the user] --> C
  H -- no --> I{More ready units?}
  I -- yes --> C
  I -- no --> R[review-code on the whole branch, then finish-branch]
```

Rules on the loop:
- **Escalation:** two failed verifications on `sonnet` re-run the unit on
  `opus`, with the failure notes. Two failures on `opus` stop the run and
  ask the user.
- **Other stops:** the spec turns out to be ambiguous, or a change can't be
  undone with `git revert`.
- **Files outside `Touches`:** the implementer lists them. The
  orchestrator stages them only if the reviewer agrees the unit's criteria
  need them; otherwise they go under NOTICED BUT NOT TOUCHING.
- **Resume:** run `implement` again; it continues from the index's
  `Status` column.
- **Landing:** one branch, one PR, through `finish-branch`.
- **OpenCode:** the orchestrator calls `sde-implementer-standard` for S/M
  units and `sde-implementer-strong` for L units and reviews. With no
  model set on either, both inherit the main model and the run is
  single-model; `implement` says so at the start.

## Testing Seams

- **Plugin evals** (`claude plugin eval`), one case per behaviour: the
  highest seam that sees what a user sees (which skill fired, which
  subagents ran on which model, what was committed).
- **`scripts/validate.py`** and its tests for structure.
- **One real dry run** (SC-9) for the cost comparison, which no eval can
  give.

## Success Criteria & Evals

Eval runs use the harness default of 3 runs per case. Cases with a
scaffold need `--scaffold`.

- **SC-1:** Given a spec with 4 criteria, `plan-from-spec` writes the index
  table (Unit, Status, Depends on, Satisfies, Tier, Risk) and one unit file
  per unit, and no index field appears in a unit file. Check:
  `claude plugin eval . --no-publish --model sonnet --case plan-emits-units`
  → all graders pass in ≥2 of 3 runs.
- **SC-2:** Planning doesn't regress. Check:
  `claude plugin eval . --no-publish --model sonnet --case plan-traces-criteria`
  → passes in ≥2 of 3 runs.
- **SC-3:** A 2-step plan runs in a single session: no subagent starts and
  no units folder is written. Check:
  `claude plugin eval . --no-publish --model sonnet --case implement-small-plan --scaffold --allow-tools Write Edit Bash`
  → passes in 3 of 3 runs.
- **SC-4:** A 4-unit plan (tiers M, S, L, M; one high-risk unit) gets one
  implementer subagent per unit; S and M run on `sonnet`, the L unit and
  every reviewer on `opus`; each commit sets that unit's
  `Status: done <sha>`; the run pauses before the high-risk unit. Check:
  `claude plugin eval . --no-publish --model sonnet --case implement-dispatch --scaffold --allow-tools Write Edit Bash Agent`
  → passes in ≥2 of 3 runs.
- **SC-5:** A unit whose verification can't pass is re-run on `opus` after
  2 `sonnet` failures; after 2 `opus` failures the run stops and asks; no
  test is weakened. Check:
  `claude plugin eval . --no-publish --model sonnet --case dispatch-escalation --scaffold --allow-tools Write Edit Bash Agent`
  → passes in ≥2 of 3 runs.
- **SC-6:** The repo still validates. Check: `python3 scripts/validate.py`
  → `All checks passed.`; `python3 scripts/test_validate.py` and
  `python3 scripts/test_floor_guard.py` → `OK`.
- **SC-7:** `implement/SKILL.md` stays scannable. Check:
  `wc -l < skills/implement/SKILL.md` → 150 or less, and
  `test -f skills/implement/references/dispatch.md` → exit 0.
- **SC-8:** OpenCode ships `sde-implementer-standard` and
  `sde-implementer-strong` agent definitions with no model hard-coded, and
  `OPENCODE.md` says how to set them. Check: `rg -c '^model:'` on both
  files → no matches; `rg -n 'sde-implementer-strong' OPENCODE.md` → at
  least 1 match.
- **SC-9:** One real 5–8 unit plan runs in both modes, and
  `docs/in-progress.md` records tokens, wall time, rework, escalations, and
  floor-guard hits for each. Check:
  `rg -n 'sequential dispatch' docs/in-progress.md` → a row with all 5
  numbers for both modes.

## Open Questions

- Whether `claude plugin eval` accepts `Agent` in `--allow-tools`. Owner:
  resolved by a trial run at planning time; if not, SC-4 and SC-5 name the
  right flag.
