# Proposal: plan → tickets (units) → parallel, model-tiered implementation

Date: 2026-10-12. Status: **idea under assessment — nothing decided or implemented.**

Related: [upstream findings](2026-10-12-upstream-findings.md) (themes 4 and 15: mattpocock's
`to-tickets` / `implement-spec`, agent-skills' `/build auto`).

## The idea (as raised)

When we create the spec and plan, and grill them, the final input to `implement` should be
**tickets** (Matt's term) or smaller implementable units. Then we can spin up parallel and
sequential agents to code them, and pick a **haiku / sonnet / opus** model per ticket depending on
its complexity.

## Verdict

Worth doing. It fits our spine better than either upstream's, because our plan steps are already
80% of a ticket. Build it as an extension of `plan-from-spec` and `implement`, not as new spine
links. The three risks to design around: ticket quality, integration drift, and model
misclassification.

## Why it fits

Each `plan-from-spec` step already has most of what a ticket needs:

| Ticket needs (Matt / Addy) | Our plan step today |
|---|---|
| Blocking edges | `Depends on` ✅ |
| Acceptance criteria | `Verification`, traced to spec Success Criteria ✅ (stricter than either upstream) |
| Vertical slice | "tracer bullet" rule ✅ |
| Fits one fresh context window | ❌ missing |
| Self-contained for a cold agent | ❌ missing — a step assumes the session that wrote the plan |
| Complexity rating | ❌ missing |
| Parallel-safety | ❌ `Touches` is predicted but not used for conflict detection |

So this is: tighten plan steps into cold-startable **units**, then give `implement` an orchestrator
mode. Matt dropped the plan and kept only tickets; we shouldn't — the plan-step → eval trace is our
edge.

## Proposed flow

```
spec-from-idea ─► grill-me ─► plan-from-spec (emits units + blocking edges + complexity)
                                    │
                         grill the breakdown (granularity, edges, tiers) ← one human approval
                                    │
                    implement (orchestrator) reads the units as a task graph
                    ├─ sequential: dependent chain, or a small plan
                    └─ parallel: the ready frontier, each unit →
                       ├─ implementer subagent, own worktree, model chosen by tier
                       ├─ TDD → its verification command → review-code (reviewer subagent)
                       └─ merge into integration branch → full suite + spec evals there
                                    │
                    review-code on the integration branch (whole spec) ─► finish-branch
```

Matt's context rule applies: keep spec, grill, and ticket-writing in **one unbroken context**; each
implementer then starts fresh from its unit file. That is what makes units self-contained.

## Unit shape (sketch)

```markdown
## U03: Expire stale sessions on login
- Blocked by: U01
- Touches (predicted): auth/session.py, tests/test_session.py
- Satisfies: SC-2, SC-4            ← needs numbered criteria in the spec
- Verify: `pytest tests/test_session.py -k expiry`
- Complexity: M → sonnet   (ambiguity low · 2 modules · existing pattern in auth/token.py · no data risk)
- Context: spec §Approach; follow the pattern in auth/token.py
```

Small knock-on change: `spec-from-idea` numbers its criteria (`SC-1…`) so units can cite them.

## Model routing by complexity

Score each unit on five things the planner can judge: **ambiguity, blast radius, novelty (is
there an existing pattern to copy?), risk (security / data / irreversible), test difficulty.**

| Tier | Typical unit | Model |
|---|---|---|
| S | Mechanical: an expand–contract migration batch, add a field following an existing pattern, wiring, docs | haiku |
| M | Normal feature slice with a pattern to follow (**default**) | sonnet |
| L | Ambiguous, cross-module, concurrency, security, new interface design | opus |

Three rules make this safe:

- **Escalate on failure.** A unit that fails its verification twice is re-dispatched one tier up,
  with the failure notes — not retried on the same model. This absorbs misclassification and is
  what makes cheap tiers worth using.
- **Never downgrade the orchestrator or the reviewer.** Review is the gate, and it has the least
  context pressure (reads a diff), so a strong model there is cheap insurance.
- **Tier aliases, not model IDs.** Claude Code's Agent tool takes `haiku` / `sonnet` / `opus`;
  hardcoded IDs go stale. OpenCode configures subagents and models differently, so the skill
  degrades to sequential, single-model mode there and says so (same pattern as "no spec found —
  proceeding ad-hoc").

## Risks

1. **Garbage units parallelize into garbage faster.** Parallelism multiplies unit quality, so the
   grill on the breakdown is load-bearing, not optional.
2. **Integration drift.** Each unit is green in its worktree, the merge is red. After every merge,
   run the full suite and the spec evals on the integration branch. Units with no edge but
   overlapping `Touches` run one after another — or accept conflicts and use
   `resolve-merge-conflicts` (one more reason to keep it).
3. **Cost.** Parallel agents multiply tokens; retries can eat haiku savings. Probably pays off at
   **≥4 independent units**. Below that, today's sequential in-session `implement` is cheaper and
   better, and should stay the default.
4. **Discipline at depth.** Implementers don't spawn agents (both upstreams cap depth at 1).
   Per-commit review becomes per-unit review plus one final integration-branch review.
5. **Autonomy bounds** (from Addy's `/build auto`): one unambiguous approval of the breakdown,
   clean baseline, stage only that unit's files, stop on anything not undoable with `git revert`.
6. **Practical overhead.** Worktree setup may need a dependency install per worktree — slow for
   some stacks.

## Shape options

- **Recommended — extend what exists.** `plan-from-spec` emits units; `implement` gets an
  orchestrator mode, with the parallel mechanics in `implement/references/parallel.md` (it will
  pass 100 lines). Model tiers live in a reference table. The spine stays five links, per CLAUDE.md.
- **Alternative — new supporting skill** like Matt's `implement-spec`. Cleaner separation, but a
  second way to implement that people have to choose between.
- **Not recommended — replace the plan with tickets**, Matt-style. Loses the per-step eval trace.

## Validation before it's stable

Dry run on `examples/spine-walkthrough/` or a real feature with 5–8 units. Measure wall time,
tokens, rework, and merge conflicts against a sequential baseline. Starts as `**Status:** draft`
per CLAUDE.md.

## Open decisions

1. **Where units live:** local files (`docs/plans/<topic>/units/NN-slug.md`, works everywhere),
   GitHub issues, or both with files as the default?
2. **Landing:** one integration branch and one `finish-branch` at the end (Matt), or a PR per unit?
3. **Default tier and escalation:** sonnet default with automatic escalation, or ask before
   escalating to opus?
4. **OpenCode parity:** must it run parallel too, or is sequential fallback acceptable?

## Next step

Agree the direction, then run these decisions through `grill-me` before writing the spec for
the change itself.
