# Proposal: plan → units → sequential, model-tiered implementation

Date: 2026-10-12 (revised same day: sequential dispatch is now the default; parallel deferred).
Status: **idea under assessment — nothing decided or implemented.**

Related: [upstream findings](2026-10-12-upstream-findings.md) — themes 4 and 15 (mattpocock's
`to-tickets` / `implement-spec`, agent-skills' `/build auto`), plus 6, 10, 14 and 16 for the
robustness rules below. Credits use the findings doc's tags: **A** = addyosmani/agent-skills
0.6.12, **M** = mattpocock/skills v1.3.1.

## The idea (as raised)

When we create the spec and plan, and grill them, the final input to `implement` should be
**tickets** (Matt's term) or smaller implementable units. Then we can spin up agents to code them,
and pick a **haiku / sonnet / opus** model per unit depending on its complexity.

## Verdict

Worth doing, **sequentially**. Tighten plan steps into units a fresh agent can start cold, and give
`implement` a dispatch mode that runs them one at a time, each in a fresh subagent on a model
chosen by tier. Parallel worktrees are deferred: they add only wall-clock speed, and most of the
risks come with them.

This is A's `/build auto` shape (one step at a time, one approval, strict stop rules) plus fresh
context and model tiers per unit. M's `implement-spec` is the parallel variant we are not
starting with.

## What parallelism actually buys

| Part of the idea | Gain | Needs parallel? |
|---|---|---|
| Self-contained units | Better plans; fresh context per unit, so long `implement` sessions don't degrade | No |
| Model tier per unit | Cost down; the strongest model goes where it's needed | No |
| Parallel worktrees | Wall-clock time | Yes |

Wall-clock time is rarely the bottleneck: approving the breakdown and reviewing the result are,
and parallelism doesn't shorten them.

## Why it fits

Each `plan-from-spec` step already has most of what a unit needs:

| Unit needs | Our plan step today |
|---|---|
| Blocking edges | `Depends on` ✅ |
| Acceptance criteria | `Verification`, traced to spec Success Criteria ✅ (stricter than either upstream) |
| Vertical slice | "tracer bullet" rule ✅ |
| Fits one fresh context window (M) | ❌ missing |
| Self-contained for a cold agent | ❌ missing — a step assumes the session that wrote the plan |
| Size and complexity rating | ❌ missing |
| Durable status, for resume | ❌ missing |

Matt dropped the plan and kept only tickets; we shouldn't — the plan-step → eval trace is our edge.

## Proposed flow

```
spec-from-idea ─► grill-me ─► plan-from-spec (emits units: edges, size, tier, risk)
                                    │
                    grill the breakdown → one unambiguous approval
                                    │
                    implement (dispatch mode): clean baseline, then the per-unit loop
                                    │
                    review-code on the whole branch (whole spec) ─► finish-branch
```

M's context rule applies: keep spec, grill and unit-writing in **one unbroken context**; each
implementer then starts fresh from its unit file. That is what makes units self-contained.

## Per-unit loop

```
clean baseline + approved breakdown
for each ready unit (dependency order, riskiest first):
  implementer subagent (model by tier) → test-first → verify
  orchestrator: re-run verify · floor guard · stage only the unit's files
  reviewer (strong model; sees unit + diff + criteria, not the implementer's reasoning) → ≤3 rounds
  commit · mark the unit done + SHA · collect NOTICED items
  2 failures → escalate a tier · stop condition hit → stop and ask
  every 2–3 units → checkpoint
```

Where each rule comes from:

| Stage | Rule | Source |
|---|---|---|
| Start | Tests green before unit 1, so a failure can be blamed on the unit | A `/build auto` |
| Start | One unambiguous approval of the breakdown — "looks reasonable" doesn't count | A `/build auto` |
| Order | Riskiest ready unit first, so a bad breakdown fails on unit 1–2, not unit 7 | A `planning-and-task-breakdown` |
| Implement | Test-first; stop if >100 lines are written without running tests | ours (`test-driven-development`); tripwire from A `incremental-implementation` |
| Implement | Report out-of-scope finds as `NOTICED BUT NOT TOUCHING`, don't fix them | A `incremental-implementation` |
| Verify | The orchestrator re-runs the unit's verify command itself; an implementer's "tests pass" is data, not evidence | A `using-agent-skills` (verify, don't assume; trust levels) |
| Verify | Floor guard on the unit's diff: flags skipped tests, removed assertions, new suppressions, loosened thresholds | A `constraint-driven-development` |
| Review | Reviewer gets the unit file, the diff and the success criteria only — no implementer reasoning — and is told to look for problems, not confirm | A `doubt-driven-development` |
| Review | At most 3 rounds; two rounds with nothing actionable means stop | A `doubt-driven-development` |
| Commit | Stage only that unit's files; no delete-and-replace in one commit; code compiles at every commit | A `/build auto`, `incremental-implementation` |
| Record | Unit file gets `Status: done` + commit SHA; resume is just re-invoking | A `/build auto`; approvals live in the artifact, not the conversation (A `context-engineering`) |
| Stop | Unfixable failure (after escalation), spec ambiguity, or anything `git revert` can't undo → stop and ask | A `/build auto` |
| Checkpoint | Human glance every 2–3 units | A `planning-and-task-breakdown` |
| Depth | Implementers and reviewers never spawn agents (max depth 1) | A personas rule; M `implement-spec` |

## Unit shape (sketch)

```markdown
## U03: Expire stale sessions on login
- Status: todo                      ← todo / in-progress / done <sha> / blocked <reason>
- Blocked by: U01
- Touches (predicted): auth/session.py, tests/test_session.py
- Satisfies: SC-2, SC-4             ← needs numbered criteria in the spec
- Verify: `pytest tests/test_session.py -k expiry`
- Size: S                           ← XS–L; XL must be split
- Tier: M → sonnet   (ambiguity low · 2 modules · existing pattern in auth/token.py · no data risk)
- Risk: low
- Parallel: safe                    ← recorded, not acted on (see Deferred: parallel)
- Context: spec §Approach; follow the pattern in auth/token.py
```

Split rules, mechanical so the breakdown grill can check them (A `planning-and-task-breakdown`):
split a unit with more than 3 acceptance bullets, "and" in its title, or two subsystems touched.
Size is how much work; Tier is how hard. They're scored separately.

Small knock-on change: `spec-from-idea` numbers its criteria (`SC-1…`) so units can cite them.

## Model routing by tier

Score each unit on five things the planner can judge: **ambiguity, blast radius, novelty (is
there an existing pattern to copy?), risk (security / data / irreversible), test difficulty.**

| Tier | Typical unit | Model |
|---|---|---|
| S | Mechanical: an expand–contract migration batch, add a field following an existing pattern, wiring, docs | haiku |
| M | Normal feature slice with a pattern to follow (**default**) | sonnet |
| L | Ambiguous, cross-module, concurrency, security, new interface design | opus |

Rules:

- **Escalate on failure.** A unit that fails its verification twice is re-dispatched one tier up,
  with the failure notes — not retried on the same model. This absorbs misclassification.
- **The floor guard is what makes cheap tiers safe.** The easiest way for a weak model to turn a
  verification green is to weaken the test; the guard makes that a mechanical failure.
- **Never downgrade the orchestrator or the reviewer.** Review is the gate and reads only a diff,
  so a strong model there is cheap insurance.
- **Optional for L units: a separate test writer.** A subagent writes the failing test without
  knowledge of the implementation (A `test-driven-development`), so the implementer can't write a
  tautological one. Costs one more agent; only worth it where the tier says the unit is hard.
- **Tier aliases, not model IDs.** Claude Code's Agent tool takes `haiku` / `sonnet` / `opus`;
  hardcoded IDs go stale. OpenCode runs the same loop single-model and says so (same pattern as
  "no spec found — proceeding ad-hoc").

## Risks

| Risk | Under sequential dispatch | If parallel is added later |
|---|---|---|
| 1. Bad units | **Remains — the plan still decides the outcome.** Smaller blast radius: risk-first order surfaces a bad breakdown after unit 1–2, and the plan is re-cut instead of overwritten (A: never overwrite an incomplete plan; stop and ask). Split rules make the grill checkable | Same, but every bad unit is built at once before anything fails |
| 2. Integration drift | **Gone.** Each unit starts from the previous unit's commit; no merges | Parallel only when no edge **and** disjoint `Touches`; full suite + spec evals after every merge; `resolve-merge-conflicts` for the rest |
| 3. Cost | **Mostly gone.** One fresh-context start per unit; tiering saves instead of offsetting parallel spend | Gate on ≥4 independent units |
| 4. Discipline at depth | Max depth 1; per-unit review plus one whole-branch review | Same |
| 5. Autonomy | One approval, stop conditions, checkpoints every 2–3 units, durable status | Same, plus a merger role |
| 6. Worktree overhead | **Gone.** One checkout, one dependency install | Per-worktree install; skip parallel on slow stacks |
| 7. Model misclassification | Escalate after 2 failures; floor guard catches weakened tests | Same |
| 8. Unit scope creep | `NOTICED BUT NOT TOUCHING` → new units or follow-ups; stage only the unit's files | Same |
| 9. Reviewer rubber-stamps | Reviewer sees no implementer reasoning; ≤3 rounds | Same |

## Prerequisites

**All three landed in 2.0.0** (floor guard `0a65296`, NOTICED BUT NOT TOUCHING `295a79d`,
numbered criteria `e08fad2`). They were blockers for this mode:

- **Floor guard** (finding 10) — without it, model tiers are unsafe.
- **`NOTICED BUT NOT TOUCHING`** in `implement` (finding 6) — without it, units bleed into each
  other.

Numbered success criteria in `spec-from-idea` (above) are the third.

## Shape options

- **Recommended — extend what exists.** `plan-from-spec` emits units; `implement` gets a dispatch
  mode, with its mechanics in `implement/references/dispatch.md` (it will pass 100 lines). Tier
  table in the same reference. The spine stays five links, per CLAUDE.md.
- **Alternative — new supporting skill** like M's `implement-spec`. Cleaner separation, but a
  second way to implement that people have to choose between.
- **Not recommended — replace the plan with tickets**, M-style. Loses the per-step eval trace.

Not taken from A: 200–400-line skills (CLAUDE.md wants a scannable `SKILL.md`; detail goes in
`references/`), "manual check" as verification (we keep "never test manually"), and rationalization
tables in place of positive rules (M's point: naming the forbidden behaviour primes it).

## Deferred: parallel

Not in v1. Add it only if the dry run shows wall time is a real cost. When it comes, it gates on
≥4 units with no edges between them **and** disjoint `Touches`, is opt-in, and reuses the per-unit
`Parallel:` notes (A `planning-and-task-breakdown`: safe / sequential / needs coordination). The
mechanics would follow M's `implement-spec`: own worktree per implementer, a merger, one
integration branch.

## Validation before it's stable

Dry run on `examples/spine-walkthrough/` or a real feature with 5–8 units, two arms: today's
single-session `implement` vs sequential dispatch. Run both through `claude -p` on a fixture repo
with the model and Claude Code version pinned (A found skill firing varies run to run), and have a
second `claude -p` grade each trace against written expectations (A's behavioural eval tier).
Measure tokens, wall time, rework, escalations and floor-guard hits. Starts as
`**Status:** draft` per CLAUDE.md.

## Open decisions

1. **Where units live:** local files (`docs/plans/<topic>/units/NN-slug.md`, works everywhere),
   GitHub issues, or both with files as the default?
2. **Landing:** one branch and one `finish-branch` at the end, or a PR per unit?
3. **Escalation:** automatic up to opus, or ask before escalating to opus?
4. **Checkpoint cadence:** every 2–3 units always, or only at units marked high-risk?
5. **L-tier test writer:** always on for L units, opt-in, or left out of v1?

Resolved: **OpenCode parity** — sequential is the default, so OpenCode loses only model tiers.

## Next step

Agree the direction, then run the open decisions through `grill-me` before writing the spec for
the change itself.
