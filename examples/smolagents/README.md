# Case study: spec-driven-engineering vs. a real AI framework

**Target:** [`huggingface/smolagents`](https://github.com/huggingface/smolagents)
— Apache-2.0, Python, 700+ open issues, actively maintained. Not a toy
repo picked to make the demo look good; picked because it's real,
messy, and popular.

**Constraint honored throughout:** local clone only. No fork, no push,
no PR against the upstream repo. Every result below is independently
reproducible from a clean clone plus the commands shown.

## The headline result

Running the **Developer** persona's `debug-systematically` skill against
this codebase found and fixed a real, currently-open upstream bug
([#2703](https://github.com/huggingface/smolagents/issues/2703)) — not a
seeded bug, not a toy example. The skill's process (reproduce → minimize
→ hypothesize → instrument → root-cause fix, never patch the symptom the
report happened to name) produced a smaller, more correct fix than a
naive patch would have, verified against the actual library, with a
permanent regression test added to its real suite (96/96 passing).

## Three personas, one codebase, six real outcomes

| Persona | Skill | What it did | Evidence |
|---|---|---|---|
| [Developer](developer.md) | `debug-systematically` | Fixed real bug #2703 (`RuntimeError: generator ignored GeneratorExit`), root cause not symptom | Reproduced on the real `Agent` class, 96/96 tests passing after |
| [Developer](developer.md) | `resolve-merge-conflicts` | Resolved a real git conflict by traced intent, not "accept theirs" | One side's fix recognized as redundant, not mechanically kept |
| [Engineer](engineer.md) | `domain-modeling` | Found "step" means 3 different things in this codebase | Empirically confirmed: `len(memory.steps)==3` while `step_number==2` on the same run |
| [Engineer](engineer.md) | `triage-issues` | Triaged 8 real open issues with stated reasons | Caught one issue that was a self-described test artifact, two bot/vendor-pitch smells |
| [Engineer](engineer.md) | `handoff` | Wrote a handoff doc, then proved it usable | Resumed the exercise using only the doc's own routing line |
| [Architect](architect.md) | `writing-for-agents` | Critiqued the repo's own `AGENTS.md` | Found it duplicates `CONTRIBUTING.md`'s actual enforced checks without ever linking to them |

## Why this is the demo, not a slide about the demo

Anyone can claim a workflow "finds real bugs." The point of running this
against `smolagents` specifically instead of a repo built for the
occasion: every finding here is checkable against the public repo right
now — the bug is still open at the time of writing, the docstring typo
this fixed is still visible in `tools.py`'s history, the triaged issues
are real GitHub issues with real numbers. Nothing here can be handwaved.

## How to reproduce

```bash
git clone https://github.com/huggingface/smolagents.git
cd smolagents
# then follow the per-persona docs for the exact commands run
```

See [developer.md](developer.md), [engineer.md](engineer.md), and
[architect.md](architect.md) for full detail, real diffs, and exact
verification commands.
