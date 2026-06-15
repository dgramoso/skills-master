# grill-with-docs

A conversational workflow that stress-tests plans against a project's domain model and documentation.

## Core approach

Interview the user systematically about each aspect of their plan, moving through design decisions one at a time. For each question, offer a recommended answer. When possible, validate claims against the actual codebase rather than relying on description alone.

## Key practices

**Challenge terminology mismatches.** If existing `CONTEXT.md` defines a term differently than the user is employing it, flag the conflict immediately.

**Push back on vagueness.** When language is imprecise or overloaded, propose a sharper canonical term and let the user confirm or correct.

**Stress-test with scenarios.** Use concrete examples to expose edge cases and force precision about concept boundaries.

**Verify against code.** When the user describes how something works, check whether the implementation agrees. Surface contradictions.

**Update CONTEXT.md live.** Capture glossary decisions as they're resolved, not in batches. Keep it free of implementation detail—it's a glossary, not a spec.

**Create ADRs selectively.** Only document a decision if it's hard to reverse, surprising without context, and the result of a genuine trade-off. Skip the ADR otherwise.

## File structure awareness

Look for `CONTEXT.md` and `docs/adr/` in standard locations. If `CONTEXT-MAP.md` exists, the codebase has multiple bounded contexts. Create documentation files lazily when needed.
