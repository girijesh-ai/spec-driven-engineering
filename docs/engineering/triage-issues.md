# triage-issues

**Status:** draft

## What it does

Moves backlog items through a tracker-agnostic state machine (new →
triaged → ready → in-progress → done, with needs-info/rejected/duplicate
side states) so prioritization decisions get made explicitly and once, not
re-argued every time someone looks at the backlog.

## When to reach for it

- Grooming a backlog of issues, bugs, or feature requests.
- Deciding what's next when there's more than one candidate and no
  existing explicit priority.

## Common questions

**What tracker does this assume?**
None — GitHub Issues, Linear, Jira, or a markdown list all work. The states
and the questions at each transition are the point, not any tool's API.

**When does something graduate to `spec-from-idea`?**
When it's non-trivial and being marked `ready` — "ready" means ready to
implement, which for anything beyond a trivial fix means a spec exists
first.

## It's working if

- Priority decisions have a written one-line reason attached, so the next
  triage pass builds on it instead of re-arguing it.
- Nothing sits in `ready` vague enough that whoever picks it up has to
  re-ask what it actually means.
