# Engineer persona: `domain-modeling`, `triage-issues`, `handoff`

Real planning/coordination work against
[`huggingface/smolagents`](https://github.com/huggingface/smolagents),
using the skills an Engineer reaches for when owning work end-to-end.

## 1. `domain-modeling` — "step" means three different things

Checked existing context first (per the skill's own process): the
codebase has a `MemoryStep` base class with five subclasses — `TaskStep`,
`SystemPromptStep`, `PlanningStep`, `ActionStep`, `FinalAnswerStep` — but
`step_number`/`max_steps` only track `ActionStep`s. The codebase's own
authors already flag this is easy to get wrong — a defensive comment at
`agents.py:557` reads: *"Don't use the attribute step_number here,
because there can be steps from previous runs."*

### The near-miss question that surfaces it

*"Does `max_steps=20` bound how many entries land in `agent.memory.steps`?"*

Not asserted from reading — checked empirically, on a real agent run:

```python
agent = CodeAgent(tools=[], model=FakeCodeModel(), planning_interval=1)
agent.run("test")
print([type(s).__name__ for s in agent.memory.steps])
print(len(agent.memory.steps), agent.step_number)
```

```
['TaskStep', 'PlanningStep', 'ActionStep']
3 2
```

**Confirmed:** `len(memory.steps) == 3` while `step_number == 2` on the
*same run*. The answer to the near-miss question is no, and it's not a
technicality — it's a real gap between what a new contributor would
reasonably assume and what the code actually does.

### Where this bites in practice

Anyone building a pagination scheme, a transcript truncation policy, or
a token-budget estimate on top of this library and reasoning
"`max_steps=20` means at most 20 transcript entries" has made a wrong
assumption that will surface as an off-by-a-variable-amount bug,
depending on `planning_interval`.

### Resolved terminology

- **"action step"** — the `ActionStep`-loop-iteration sense; what
  `step_number`/`max_steps` actually track.
- **"memory step" / "transcript entry"** — the broader `memory.steps`
  sense.
- Never use bare "step" in new docs/comments without saying which.

## 2. `triage-issues` — real backlog, real judgment calls

Pulled 8 real open issues, triaged each with a stated reason (per the
skill's rule: write the reason once, don't re-litigate it next pass).

| # | Title | State | Why |
|---|---|---|---|
| [2699](https://github.com/huggingface/smolagents/issues/2699) | "[Agent Test] Issue management tool test" | **rejected** | Body states outright it's a test artifact, not a real report |
| [2701](https://github.com/huggingface/smolagents/issues/2701) | "DOC: PZERO OpenAIModel api_base example" | **needs-info** | Filed by an automated bot, promoting one named paid provider — genuine gap or promotional content? |
| [2712](https://github.com/huggingface/smolagents/issues/2712) | "Step-Level WAL Durability Callback (LetItLoop)" | **needs-info** | Real underlying need (crash-resilience), but names a specific vendor product — generic hook or vendor pitch? |
| [2722](https://github.com/huggingface/smolagents/issues/2722) | "Make code executors pluggable via entry points" | **ready** (already) | Maintainers already labeled `status:accepted`, `priority:p1` — not re-litigated |
| [2720](https://github.com/huggingface/smolagents/issues/2720) | "BUG: repr leaks into plan text" | **ready** | Specific, well-described, implementable directly |
| 2703 | The bug fixed in [developer.md](developer.md) | **in-progress** | A verified local fix exists, not yet upstream |
| [2700](https://github.com/huggingface/smolagents/issues/2700) | "Add missing return type annotations" | **ready** | Well-scoped, low-risk, already labeled |
| [2690](https://github.com/huggingface/smolagents/issues/2690) | "Regression coverage for no-tool CodeAgent" | **ready** | Test-only, well-scoped |

Two of eight items resolved to **needs-info**, not a rubber-stamp
**ready** — the skill's process caught genuine ambiguity (a bot-filed doc
request, a vendor-named feature pitch) that a fast pass would have waved
through.

## 3. `handoff` — proven usable, not just written

Wrote a handoff doc mid-exercise capturing exactly what was done, what
was next, and — the skill's own claim — "the single most useful line":
where the work sits, so the next session knows which skill to invoke.
Then tested that claim for real: resumed using *only* the doc's "what's
next" line (`writing-for-agents` against the real `AGENTS.md`), routing
through `dev-workflow` first to confirm the handoff was specific enough
that the generic router wasn't even needed — the handoff had already
named the exact next skill.

## What this demonstrates

An Engineer persona isn't just "write the code" — it's catching ambiguity
before it becomes a bug (domain-modeling), making backlog decisions that
don't need re-arguing (triage-issues), and leaving work in a state
someone else can actually pick up (handoff), verified by actually picking
it up.
