# Developer persona: `debug-systematically`, `resolve-merge-conflicts`

Real bugfix work against [`huggingface/smolagents`](https://github.com/huggingface/smolagents),
using the skills a Developer reaches for day-to-day.

## 1. `debug-systematically` — real upstream bug #2703

**Issue:** [#2703](https://github.com/huggingface/smolagents/issues/2703) —
"`_run_stream` yields inside `finally`, so closing the stream raises
'generator ignored GeneratorExit'." Currently open on the real repo.

### Reproduce

The full framework needs a live LLM API to run an agent end-to-end, so
the minimal mechanism was reproduced directly first — the exact
`try/except/finally: yield` shape from the real code at
`agents.py:594-603`:

```python
def gen():
    try:
        for i in range(5):
            yield i
    except ValueError:
        pass
    finally:
        print("finalizing")
        yield "final_step_marker"

g = gen()
next(g)     # step into the generator, suspend inside the try
g.close()   # what happens when a caller breaks a `for` loop early
```

```
0
finalizing
Traceback (most recent call last):
  ...
RuntimeError: generator ignored GeneratorExit
```

Reproduced exactly — not a plausible guess, an observed match to the
reported symptom.

### Confirm against the real `Agent` class, not just the isolated repro

```python
from smolagents import CodeAgent
from smolagents.models import ChatMessage, MessageRole, Model

class FakeCodeModel(Model):
    def generate(self, messages, stop_sequences=None):
        return ChatMessage(role=MessageRole.ASSISTANT,
            content="Thought: work\n<code>\nresult = 1 + 1\n</code>\n")

agent = CodeAgent(tools=[], model=FakeCodeModel())
gen = agent.run("test task", stream=True)
next(gen)     # take one step, suspend mid-step
gen.close()   # simulate a caller breaking a `for` loop early
```

With the original code: `RuntimeError: generator ignored GeneratorExit`
— the real bug, reproduced on the real class, not just the toy pattern.

### Root cause, not symptom

Grepped every caller of `_run_stream` before touching anything (2 total):
one fully drains the generator via `list(...)` (never closes early —
safe); the other hands the raw generator to `run(..., stream=True)`
callers, who can legitimately close it mid-step. The fix has to live in
`_run_stream` itself — a caller-side workaround would leave every future
caller exposed to the same bug.

### The fix

```diff
             finally:
+                # No yield in finally: closing this generator mid-step sends GeneratorExit here,
+                # and yielding while handling GeneratorExit raises "generator ignored GeneratorExit".
                 self._finalize_step(action_step)
                 self.memory.steps.append(action_step)
-                yield action_step
                 self.step_number += 1
+            yield action_step
```

Move the yield out of `finally` — cleanup (non-yielding) stays there,
safe during `GeneratorExit`; the yield happens as a normal statement
right after, only reached on the non-close paths.

### Verification

```python
gen = agent.run("test task", stream=True)
next(gen)
gen.close()
# -> "CLOSED CLEANLY - no RuntimeError"
```

Confirmed against the real class both ways: reproduced broken with the
original code, confirmed clean after the fix. A permanent regression
test was added to the real suite
(`test_run_stream_closes_cleanly_when_stopped_mid_step`); full
`test_agents.py` — **96 passed, 2 skipped, 0 failed** — no regression.

## 2. `resolve-merge-conflicts` — a real git conflict, resolved by intent

Two branches, each independently fixing the same typo in `tools.py`'s
`Tool` docstring ("It has one `type`key and a `description`key." — no
spaces before "key"):

- **branch-a:** spacing fix only — `It has one `type` key and a
  `description` key.`
- **branch-b:** a fuller rewrite that also happens to fix the same
  spacing defect — `It has two required keys, `type` and `description`.`

Merging produced a real conflict:

```
<<<<<<< HEAD
      It has one `type` key and a `description` key.
=======
      It has two required keys, `type` and `description`.
>>>>>>> branch-b
```

**Resolved by intent, not mechanically:** branch-a's fix is narrower and
already covered by branch-b's rewrite — keeping both would mean
concatenating two versions of the same sentence, keeping "theirs" would
be right here, but *for the reason that it supersedes*, not because
"theirs" is a default. Re-ran `test_tools.py` (72 passed, 3 skipped)
before completing the merge, per the skill's own rule — a clean-looking
resolution can still be behaviorally wrong in ways a read-through misses.

## What this demonstrates

Both skills produced work indistinguishable from what a careful human
engineer would do — grep callers before fixing, verify against the real
class not just a toy repro, resolve conflicts by understanding intent
instead of picking a side. Nothing here required inventing a scenario;
the material was either a real filed issue or a realistic conflict
pattern (two people fixing the same defect differently), and the git/test
mechanics involved were 100% real either way.
