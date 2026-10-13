# In progress

Draft skills: their `SKILL.md` exists under `skills/` (so they load and can
be dry-run), but they aren't promoted — no `docs/<bucket>/` page, not in
`README.md`, not routed by `dev-workflow`. Each gets promoted once it has
been dry-run against a real task (see `CLAUDE.md`).

| Skill | Bucket (planned) | Plugs in | Source | Dry run needed |
|---|---|---|---|---|
| `doubt-check` | engineering | between `implement` and `review-code` | agent-skills `doubt-driven-development` | A real mid-work design decision challenged by a fresh subagent, with at least one objection accepted or refuted with evidence |
| `retro` | productivity | after `finish-branch` | mattpocock/skills `retro` | A real finished branch with rework, producing at least one mechanical guardrail that lands as a commit |
| `simplify-code` | engineering | supporting; fed by `review-code` findings and `plan-from-spec` prefactor steps | agent-skills `code-simplification` | A real simplification on an existing codebase, one change per commit, existing tests unmodified |
| `source-driven` | engineering | supports `implement` | agent-skills `source-driven-development` | A real dependency upgrade or new API use, with the version detected from a lockfile and docs cited |
| `plain-technical-writing` | productivity | called by `spec-from-idea`, `plan-from-spec`, `grill-me`, `handoff`, `finish-branch`, `domain-modeling` | user feedback: output read as too "Claude-like" | A real spec and a real `grill-me` session where a reader outside the work confirms they understood them in one read, with every number, command, and `SC-n` still present |

Also tracked, not yet a skill: the [tickets / sequential dispatch
proposal](../research/2026-10-12-tickets-and-parallel-implement.md).
