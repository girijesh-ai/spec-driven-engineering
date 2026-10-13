# Code-smell baseline

The twelve smells `review-code` checks in Axis 2 (after Martin Fowler's
*Refactoring* catalogue, as distilled in mattpocock/skills' `code-review`).
Every one is a judgement call, not a rule: report it with the reason it
hurts *this* code, and drop it when a documented repo standard says
otherwise.

| Smell | What it looks like | Usual fix |
|---|---|---|
| Mysterious Name | A name that needs the body read to be understood | Rename until the call site explains itself |
| Duplicated Code | The same logic in two places that must change together | Extract once, call from both |
| Feature Envy | A function that mostly reads another object's data | Move it to the data it uses |
| Data Clumps | The same 3+ values always passed together | Give them a type |
| Primitive Obsession | Strings or ints standing in for a domain concept (money, IDs, states) | A small value type or enum |
| Repeated Switches | The same `switch`/`if type ==` chain in several places | Polymorphism or a lookup table, defined once |
| Shotgun Surgery | One logical change needs edits across many files | Gather the concept into one module |
| Divergent Change | One module changes for several unrelated reasons | Split it by reason to change |
| Speculative Generality | Hooks, parameters, or layers for callers that don't exist | Delete until a second caller appears |
| Message Chains | `a.b().c().d()` — callers know the whole path | Hide the walk behind one method |
| Middle Man | A class that only forwards calls | Call the real target; delete the forwarder |
| Refused Bequest | A subclass that ignores or overrides away most of what it inherits | Replace inheritance with composition |

Overlap with `engineering-standards`: Duplicated Code is DRY, Speculative
Generality is the necessity check, Repeated Switches is Open/Closed. Report
the finding once, under whichever name explains it best.
