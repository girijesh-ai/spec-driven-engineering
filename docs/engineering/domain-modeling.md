# domain-modeling

**Status:** stable

## What it does

Forces vague or inconsistently-used terms in a requirement to become
precise, checked definitions before they land in a spec — so `plan-from-spec`
and `implement` inherit one meaning per term, not whatever each person
assumed.

## When to reach for it

- A spec depends on a term ("active," "owner," "valid") that could mean two
  different things and the difference would change what gets built.
- Different people or messages use different words for what turns out to
  be the same concept, or the same word for different concepts.

## Common questions

**Doesn't this slow down writing a spec?**
Only for the terms that actually matter to a Success Criterion. It's not a
glossary-for-everything exercise — skip terms whose precise meaning
wouldn't change what "done" means.

**Where do the resolved definitions end up?**
In the spec itself, not left in chat history — otherwise `implement` has no
way to inherit them later.

## It's working if

- Nobody discovers mid-implementation that "active" meant something
  different than what they'd assumed.
- The spec's Non-Goals section is easy to write, because the boundary of
  what's in scope is already precise.
