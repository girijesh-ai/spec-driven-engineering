---
name: triage-issues
description: Use when grooming a backlog of issues, bugs, or requests and deciding what's next — moves items through a tracker-agnostic state machine instead of an ad-hoc priority argument.
---

# triage-issues
Status: draft

## Overview

Tracker-agnostic: the states below apply whether the backlog lives in
GitHub Issues, Linear, Jira, or a markdown file. This skill is about the
decision at each transition, not about any specific tool's API.

## States

```
new -> triaged -> ready -> in-progress -> done
         |
         v
      rejected / duplicate / needs-info
```

- **new** — reported, not yet looked at.
- **triaged** — someone has read it and made a call: real issue, needs more
  info, duplicate, or rejected.
- **ready** — real, understood, and has enough detail that `spec-from-idea`
  (for anything non-trivial) or a direct fix could start without further
  clarification.
- **in-progress** — someone's actively working it.
- **done** — resolved and verified, not just "code merged."

## Process per item

1. **Is it understood?** If the report is too vague to reproduce or act on,
   it's `needs-info` — ask a specific question, don't triage further until
   answered.
2. **Is it real and not already covered?** Check for duplicates before
   anything else — grep the tracker, not just memory.
3. **Does it need a spec?** Anything beyond a trivial fix goes through
   `spec-from-idea` before being marked `ready` — "ready" means ready to
   implement, not ready to start figuring out what to build.
4. **Prioritize by impact and cost, stated explicitly** — not by recency or
   who's loudest. Write the one-line reason next to the priority, so the
   next triage pass doesn't re-litigate it from scratch.
5. **Re-triage stale items.** An item sitting in `ready` for a long time
   without being picked up is a signal to re-check it's still wanted, not
   just carry it forward indefinitely.

## Common mistakes

| Mistake | Fix |
|---|---|
| Marking something "ready" while it's still vague | Ready means implementable now — if it needs a spec first, it's not ready yet |
| Re-litigating priority from scratch every triage pass | Write the reason down next to the decision so it doesn't need re-deciding |
| Not checking for duplicates before triaging | Grep the tracker first — a duplicate triaged as new wastes the eventual dedup effort |
| Letting `needs-info` items sit silently | A specific, answerable question moves it, a vague "need more detail" doesn't |

## Next

`ready` items needing more than a trivial fix go to `spec-from-idea`.
