# Examples

Two kinds of example: a worked **spine walkthrough** that shows the core
spec → plan → implement → review → finish workflow and its Success Criteria
& Evals thread end to end, and **real, end-to-end runs** of the supporting
skills against external open-source repositories (every skill invocation a
genuine `Skill` dispatch; every bug, conflict, and finding real; nothing
ever pushed upstream).

- **[spine-walkthrough/](spine-walkthrough/)** — one change carried through
  the entire spine (spec with Success Criteria & Evals → plan → implement →
  review → finish). An illustrative worked example showing the eval thread
  end to end; this is the plugin's core workflow, so start here.
- **[smolagents/](smolagents/)** — all three personas (Developer,
  Engineer, Architect) run against
  [`huggingface/smolagents`](https://github.com/huggingface/smolagents),
  a real, actively maintained Python agentic-AI framework. Includes a
  genuine upstream bug found and fixed, a real git conflict resolved by
  traced intent, and more.
