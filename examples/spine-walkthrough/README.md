# Spine walkthrough: idea → spec → plan → implement → review → finish

An **illustrative worked example** of the plugin's core workflow — the spine —
on one small, concrete change: adding retry-with-backoff to a metadata-sync
HTTP client. It exists to show the one thing the [smolagents case
study](../smolagents/) doesn't: the **Success Criteria & Evals thread** running
unbroken from the first artifact to the landed commit.

Unlike `../smolagents/` (a real, executed run of the *supporting* skills
against a public repo), this is a worked example of the *spine's artifacts* —
the spec and plan are real files in the format the skills produce; the code and
test output are shown illustratively, not captured from a live run.

## The artifacts

| File | Stage | What to look at |
|---|---|---|
| [spec.md](spec.md) | `spec-from-idea` | the **Success Criteria & Evals** section — six runnable pass/fail checks |
| [plan.md](plan.md) | `plan-from-spec` | every step's **Verification** line, traced to a specific SC |
| [walkthrough.md](walkthrough.md) | `implement` → `review-code` → `finish-branch` | how those six checks become the acceptance bar, then the review's primary axis |

## Start here

Read [walkthrough.md](walkthrough.md) — it narrates the flow and quotes what
each stage produces. The spec and plan are linked from it.
