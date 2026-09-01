# spec-driven-engineering

By [girijesh-ai](https://github.com/girijesh-ai)

**Give your coding agent a spec to build against, not just a prompt to
guess from.**

An agent without a spec ships fast and drifts fast — every session
re-guesses what "done" means, and nothing downstream can check its work
against anything but vibes. `spec-driven-engineering` is a Claude Code
plugin that makes the spec the thing everything else is checked against:
one spine (idea → spec → plan → code → review → ship) carrying measurable
Success Criteria & Evals all the way through, plus the standards,
architecture, and debugging disciplines that spine leans on. 16 skills,
free, installs in two commands.

Not sure where to start? Invoke **[dev-workflow](docs/engineering/dev-workflow.md)**
— it's a routing table from "where the work actually is" to the right
skill, and it works regardless of which of the roles below you are.

## Pick your persona

### 🔧 Developer — writing code today

You're here if you've got a plan (or a small, well-understood fix) and
you're about to actually write code.

**Start with [`implement`](docs/engineering/implement.md).** It drives
test-first at every seam and runs a review before each commit, so you're
never shipping code that hasn't been checked against something.

Your everyday skills: [`implement`](docs/engineering/implement.md),
[`test-driven-development`](docs/engineering/test-driven-development.md),
[`review-code`](docs/engineering/review-code.md),
[`debug-systematically`](docs/engineering/debug-systematically.md),
[`resolve-merge-conflicts`](docs/engineering/resolve-merge-conflicts.md),
[`engineering-standards`](docs/engineering/engineering-standards.md) (what
your code gets checked against).

### 🧭 Engineer — owns a feature end-to-end

You're here if you own a task from "someone described an idea" to "it
shipped" — not just the coding part, the whole thing.

**Start with [`spec-from-idea`](docs/engineering/spec-from-idea.md).** It
turns a conversation into a spec with measurable Success Criteria, which
is the thing every other skill in this repo checks its work against.

Your everyday skills: [`spec-from-idea`](docs/engineering/spec-from-idea.md),
[`plan-from-spec`](docs/engineering/plan-from-spec.md),
[`domain-modeling`](docs/engineering/domain-modeling.md),
[`grill-me`](docs/productivity/grill-me.md) (pressure-test the plan before
committing to it),
[`triage-issues`](docs/engineering/triage-issues.md),
[`finish-branch`](docs/engineering/finish-branch.md),
[`handoff`](docs/productivity/handoff.md) (when the session ends before the
task does).

### 🏛️ Architect — owns the shape other people build inside of

You're here if your job is less "ship this feature" and more "make sure
the next fifty features don't turn this codebase into a mess" — module
boundaries, standards, what a spec is even allowed to assume.

**Start with [`codebase-architecture`](docs/engineering/codebase-architecture.md).**
It's the module-depth/interface-width/layer-boundary lens that
`plan-from-spec` and `review-code` both defer to before code exists and
after it does.

Your everyday skills: [`codebase-architecture`](docs/engineering/codebase-architecture.md),
[`engineering-standards`](docs/engineering/engineering-standards.md),
[`domain-modeling`](docs/engineering/domain-modeling.md) (the vocabulary
specs get written in),
[`review-code`](docs/engineering/review-code.md)'s standards axis,
[`writing-for-agents`](docs/productivity/writing-for-agents.md) (how your
team's own skills and CLAUDE.md should be written).

A skill isn't fenced off to one persona — `review-code` and
`domain-modeling` show up twice above on purpose. Pick the entry point
that matches what you're doing right now.

**Want to see it working on a real codebase before installing?** See
[`examples/smolagents/`](examples/smolagents/) — all three personas run
against a real, popular open-source Python AI framework, including a
genuine upstream bug found and fixed. Nothing staged, nothing pushed
upstream.

## Quick install

```
claude plugin marketplace add girijesh-ai/spec-driven-engineering
claude plugin install spec-driven-engineering@spec-driven-engineering-dev
```

See `## Install` further down for how this exact command was verified.

---

This is not a flat catalog of independent tools. It's one spine, and a set
of supporting skills that plug into it — the technical detail below is for
when you want the full picture.

## The spine

```
spec-from-idea -> plan-from-spec -> implement -> review-code -> finish-branch
```

1. **[spec-from-idea](docs/engineering/spec-from-idea.md)** — idea →
   clarifying questions → 2-3 approaches → written spec with measurable
   Success Criteria & Evals.
2. **[plan-from-spec](docs/engineering/plan-from-spec.md)** — spec →
   ordered implementation plan, each step carrying a verification traced
   back to the spec's evals.
3. **[implement](docs/engineering/implement.md)** — writes the code, one
   plan step at a time, test-first, reviewed before each commit.
4. **[review-code](docs/engineering/review-code.md)** — two-axis review:
   does it satisfy the spec (primary), does it hold up against standards
   and architecture (secondary).
5. **[finish-branch](docs/engineering/finish-branch.md)** — confirms
   review is current and every Success Criterion is resolved, then decides
   how the work lands.

`implement` and `review-code` work without an upstream spec/plan, but say
so explicitly ("no spec/plan found — proceeding ad-hoc" /
"spec axis: skipped — no spec found") rather than silently treating a
missing spec as satisfied. See this repo's [CLAUDE.md](CLAUDE.md) for the
full governance rule.

If it's unclear where to start, use
**[dev-workflow](docs/engineering/dev-workflow.md)** — it's a routing table
to the rest of this catalog, nothing more.

## Supporting skills

These plug into the spine; none of them are peers of it.

| Skill | Bucket | Consumed by |
|---|---|---|
| [engineering-standards](docs/engineering/engineering-standards.md) | engineering | `implement`, `review-code` |
| [test-driven-development](docs/engineering/test-driven-development.md) | engineering | `implement`, `debug-systematically` |
| [domain-modeling](docs/engineering/domain-modeling.md) | engineering | `spec-from-idea` |
| [codebase-architecture](docs/engineering/codebase-architecture.md) | engineering | `plan-from-spec`, `review-code` |
| [debug-systematically](docs/engineering/debug-systematically.md) | engineering | standalone → feeds `implement` |
| [resolve-merge-conflicts](docs/engineering/resolve-merge-conflicts.md) | engineering | standalone → feeds `finish-branch` |
| [triage-issues](docs/engineering/triage-issues.md) | engineering | standalone → feeds `spec-from-idea` |
| [grill-me](docs/productivity/grill-me.md) | productivity | mid-`spec-from-idea` or standalone |
| [handoff](docs/productivity/handoff.md) | productivity | standalone → feeds `dev-workflow` (next session) |
| [writing-for-agents](docs/productivity/writing-for-agents.md) | productivity | governs how every skill here is written |

## Dependency graph

```
spec-from-idea ──┬─> domain-modeling
                  └─> grill-me (optional)
       │
       v
plan-from-spec ──> codebase-architecture
       │
       v
implement ──┬─> test-driven-development
            └─> review-code ──┬─> engineering-standards
                               └─> codebase-architecture
       │
       v
finish-branch

debug-systematically ──> test-driven-development
resolve-merge-conflicts (standalone)
triage-issues ──> spec-from-idea (for non-trivial items)
handoff ──> dev-workflow (routes the next session back in)
writing-for-agents (governs authoring, not invoked mid-task)
```

## Layout

```
spec-driven-engineering/
  .claude-plugin/
    plugin.json
    marketplace.json
  skills/
    <skill-name>/SKILL.md      # flat namespace — required for plugin discovery
  docs/
    engineering/<skill-name>.md   # bucket + promotion status tracked here, not in skills/
    productivity/<skill-name>.md
  CLAUDE.md
```

`skills/` is deliberately flat: Claude Code's plugin loader scans
`skills/*/` one level deep, so bucket membership lives in `docs/` and this
README instead of in nested directories.

## Install

```
claude plugin marketplace add girijesh-ai/spec-driven-engineering
claude plugin install spec-driven-engineering@spec-driven-engineering-dev
```

Verified end-to-end from the real repo: `claude plugin validate`, a clean
`claude plugin marketplace add` clone from GitHub (not a local path), and
`claude plugin install` from that marketplace showing all 16 skills
discovered (`claude plugin details spec-driven-engineering`). Working
from a local clone instead works the same way — pass the local path to
`marketplace add` in place of `girijesh-ai/spec-driven-engineering`.

Repo: [github.com/girijesh-ai/spec-driven-engineering](https://github.com/girijesh-ai/spec-driven-engineering)

## Status

v1. Every skill dispatches correctly through the actual `Skill` tool once
installed, and all 16 are `stable` — dry-run against a real task, per
`CLAUDE.md`'s promotion rule. The last 6 were promoted after a real-repo
persona test against `huggingface/smolagents`: a genuine root-caused bug
fix (`debug-systematically`), a manufactured-but-real git conflict
resolved by intent (`resolve-merge-conflicts`), an empirically-confirmed
terminology ambiguity (`domain-modeling`), real backlog triage
(`triage-issues`), a handoff doc proven usable by actually resuming from
it (`handoff`), and a critique of the target repo's own `AGENTS.md`
against this skill's rules (`writing-for-agents`) — all local-only,
nothing pushed upstream. Formal subagent pressure-testing is a known
follow-up, not a v1 requirement.

| Skill | Status |
|---|---|
| `dev-workflow` | stable |
| `spec-from-idea` | stable |
| `plan-from-spec` | stable |
| `implement` | stable |
| `review-code` | stable |
| `finish-branch` | stable |
| `engineering-standards` | stable |
| `test-driven-development` | stable |
| `codebase-architecture` | stable |
| `grill-me` | stable |
| `domain-modeling` | stable |
| `debug-systematically` | stable |
| `resolve-merge-conflicts` | stable |
| `triage-issues` | stable |
| `handoff` | stable |
| `writing-for-agents` | stable |

## Credits & prior art

Built by [girijesh-ai](https://github.com/girijesh-ai). Two of this
repo's skills are direct generalizations of his own pre-existing work, not
just inspiration:

- **[`engineering-standards`](docs/engineering/engineering-standards.md)**
  is his personal global `CLAUDE.md` coding-standards file, restructured
  section by section and made language-agnostic.
- **[`review-code`](docs/engineering/review-code.md)** carries most of its
  actual review process (full-file reads, caller/cross-file tracing,
  resource-leak and failure-path audit, structured report shape) directly
  from his pre-existing personal `pre-push-review` skill, generalized
  beyond the one project it was written for.

Also structured after [mattpocock/skills](https://github.com/mattpocock/skills)
(bucket + promotion-rule layout) and presented the way
[aihero.dev](https://www.aihero.dev/) frames its own skill catalog
(mission-first, persona-facing). Packaged the way
[DietrichGebert/ponytail](https://github.com/DietrichGebert/ponytail) and
Anthropic's own `superpowers` plugin ship
(`.claude-plugin/plugin.json` + `marketplace.json`).

`engineering-standards` carries its own lightweight necessity/YAGNI
check (no unrequested abstractions, stdlib/native-feature-first, simplest
correct solution), applied at write-time by `implement` and as a backstop
by `review-code`'s Axis 2 — not left as review-only. What isn't
reimplemented here is `ponytail`'s deeper, dedicated audit
(`ponytail-review`/`ponytail-audit` scan a whole diff or repo
specifically for over-engineering); pairs well with that for anyone who
wants it.
