# Out of scope

Ideas considered and not taken, so they aren't re-proposed without new
evidence. Each line says why. To reopen one, bring the evidence that
changed and move it to `research/` as a proposal.

Source of most entries: [upstream findings, 2026-10-12](../research/2026-10-12-upstream-findings.md)
(**M** = mattpocock/skills v1.3.1, **A** = addyosmani/agent-skills 0.6.12).

## Rejected

| Idea | From | Why not |
|---|---|---|
| Remove `resolve-merge-conflicts` ("the agent handles it without a skill") | M 1.3.0 | Dry-run proven on a real conflict; parallel implementation would lean on it more, not less |
| Move refactoring out of the TDD loop into review | M | Refactor-while-green is where the test protects the change; review is too late |
| Grill in numbered rounds over a frontier | M | One question at a time, each with a guess, gets real answers; rounds invite skimming |
| Allow "manual check" as a verification | A | Every Success Criterion must be runnable; manual checks don't survive the next change |
| Approve when overall code health improves, even with open issues | A | Kept the READY gate; severity now decides which findings block |
| Split skills into user-invoked vs model-invoked | M | The spine calls itself; a user-only skill breaks the chain |
| SessionStart hook injecting the router | A | Native skill routing already works; A leaves its own hook unwired; never run two routers |
| Ban em-dashes repo-wide | M | Style only; no effect on behaviour |
| Replace the plan with tickets | M | Loses the plan-step → Success Criterion trace that review and finish depend on |
| Skill named `simplify` | — | Clashes with Claude Code's built-in `simplify` and this repo's `simple`; shipped as `simplify-code` |

## Deferred

Accepted in principle, not done yet; each needs its own decision or work.

| Idea | From | Waiting on |
|---|---|---|
| Sequential dispatch of plan units with model tiers | M `implement-spec`, A `/build auto` | Its own spec — see the [tickets proposal](../research/2026-10-12-tickets-and-parallel-implement.md) |
| Parallel worktree implementation | M `implement-spec` | Dry-run evidence that sequential dispatch is too slow |
| Trigger/collision eval (TF-IDF) and an eval step in CI | A | Plugin evals first; then measure collisions (implement/TDD, review-code/engineering-standards, grill-me/domain-modeling/spec-from-idea) |
| Behavioural / pressure-test eval tier (`claude -p` + LLM grader) | A | The formal pressure-testing follow-up named in `CLAUDE.md` |
| Run review axes in parallel subagents on every commit | M | Allowed for the final branch review only; per-commit cost too high |

## Not adopted (no fit)

M: `prototype`, `research`, `wizard`, `to-questionnaire`, `teach`,
`wait-what` (overlaps `simple`), `wayfinder`,
`improve-codebase-architecture`, `setup-matt-pocock-skills` and issue-tracker
config, heavier triage (AGENT-BRIEF, OUT-OF-SCOPE labels).

A: `frontend-ui-engineering`, `browser-testing-with-devtools`,
`performance-optimization`, `observability`, `ci-cd`,
`shipping-and-launch` (deploy is beyond `finish-branch`), `idea-refine`,
personas as a separate layer, the WebFetch-cache and simplify-ignore hooks.
Security checklists were skimmed for `engineering-standards`; only
untrusted-text handling and redaction were taken.
