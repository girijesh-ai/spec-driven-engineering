---
name: domain-modeling
description: Use when a spec's requirements use terms that are vague, overloaded, or inconsistently used across the conversation — builds and stress-tests the project's domain vocabulary so the spec is written in precise, shared language.
---

# domain-modeling
Status: stable

## Overview

Feeds `spec-from-idea`. A spec written with fuzzy or inconsistently-used
terms produces a plan and implementation that quietly diverge from what was
actually meant. This skill forces the vocabulary to get precise before the
spec is finalized, not after the code reveals the ambiguity.

## When to use

- A requirement uses a term that could mean two different things
  ("active," "valid," "owner," "complete") and the spec would be ambiguous
  without pinning it down
- Multiple people/messages use the same word for what turn out to be
  different concepts, or different words for the same concept
- A spec's Non-Goals section is hard to write because the boundary of what
  the feature covers isn't clear yet

## Process

0. **Read the project's `GLOSSARY.md` and ADRs first**, if they exist.
   A term already defined there is settled — challenge the new usage
   against it instead of redefining it. Check any claim about how the
   system behaves against the code, not memory.
1. **List every domain term the requirement depends on.** Not every noun —
   the ones a wrong definition would actually break the spec's Success
   Criteria.
2. **For each term, ask: what makes something a member of this category,
   and what's a close case that's explicitly NOT a member?** The
   near-miss is usually where the real ambiguity lives.
3. **Check for silent synonyms and silent overloads.** Two terms for one
   concept: pick one, use it everywhere in the spec. One term for two
   concepts: split it into two named things.
4. **Stress-test with edge cases**, not the common case. "A user with no
   completed orders — are they 'active'?" surfaces more than "what does
   active mean" asked in the abstract.
5. **Write the resolved definitions into the spec** (either inline in
   Context, or as a short glossary if there are several) so `plan-from-spec`
   and `implement` inherit the precise meaning, not the fuzzy one.
6. **Promote lasting terms to the repo's `GLOSSARY.md`** so they outlive
   this spec. Create the file the first time a term needs it, at the repo
   root. One entry per term: the definition, a near-miss that is *not* a
   member, and synonyms to avoid. Domain meaning only — no class names,
   tables, or file paths; those change, the meaning shouldn't.
7. **Offer an ADR only when all three hold:** the decision is hard to
   reverse, it would surprise a reader who lacks today's context, and
   there was a real trade-off. Follow the repo's existing ADR convention
   if it has one; otherwise `docs/adr/NNNN-<title>.md` with **Status**,
   **Context**, **Decision**, **Alternatives considered**,
   **Consequences**. A changed decision gets a new ADR that marks the old
   one superseded — never edit or delete the old one.

Definitions, glossary entries, and ADRs are read by people joining later.
Write them per `plain-technical-writing` (call the Skill tool with it):
plain words, exact meaning, a concrete example of a member and a
near-miss.

## Common mistakes

| Mistake | Fix |
|---|---|
| Accepting a term's common-sense meaning without checking edge cases | Test it against a near-miss case before treating it as settled |
| Leaving the resolved definition only in chat, not in the spec | Write it into the spec — a definition that exists only in conversation history isn't available to `implement` later |
| Renaming a term mid-spec without updating every earlier use | Sweep the whole spec once a term changes, don't leave the old name in some sections |
| Redefining a term `GLOSSARY.md` already settles | Use the existing definition, or raise the conflict explicitly |
| Writing an ADR for every choice | Only hard-to-reverse, surprising, real-trade-off decisions get one |
| Over-modeling terms that don't affect any Success Criterion | Only chase precision on terms that could actually change what "done" means |

## Next

Resolved vocabulary feeds back into `spec-from-idea`'s Context/Goals
sections, and lasting terms into `GLOSSARY.md`.
