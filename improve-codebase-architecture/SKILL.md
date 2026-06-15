# improve-codebase-architecture

Surface architectural friction and propose deepening opportunities — refactors that increase module depth (leverage at the interface) while improving testability and maintainability.

## Core vocabulary (use consistently)

- **Module**: anything with an interface and an implementation
- **Depth**: behavioral leverage behind a compact interface — a lot of behaviour behind a small interface
- **Seam**: where an interface lives; a place behaviour can be altered without editing in place
- **Locality**: what maintainers get from depth: change, bugs, knowledge concentrated in one place
- **Leverage**: what callers gain from depth

## Phase 1 — Explore

Read domain glossary (`CONTEXT.md`) and ADRs before touching anything.

Walk the codebase organically, noting friction points:
- Bouncing between many small modules to understand one concept
- Shallow interfaces (the "deletion test": would removing this module force its callers to duplicate its logic, or just inline a pass-through?)
- Sections with poor testability or untested behavior
- Tight coupling that hides seams

Apply the **deletion test**: if removing a module just pushes its code to callers without concentrating complexity, it's a pass-through, not a deep module.

## Phase 2 — Report

Generate a self-contained HTML report (written to OS temp directory, timestamped) presenting each candidate as a card with:
- Files involved
- Problem statement
- Proposed solution
- Before/after diagrams (Mermaid)
- Recommendation strength badge
- Expected benefits

Use Tailwind and Mermaid CDN for visuals. Open the report for the user after generating it.

Present candidates without proposing final interfaces — that comes in Phase 3.

## Phase 3 — Grilling loop

For each candidate the user selects, engage in exploratory conversation:
- Constraints and existing dependencies
- What the deepened module interface should look like
- Update `CONTEXT.md` with new domain terms as they emerge
- Update `LANGUAGE.md` clarifications as needed
- Offer ADRs when a rejection carries architectural weight worth documenting for future readers

## Critical discipline

- Use domain language from `CONTEXT.md` throughout
- Consult existing ADRs before suggesting refactors
- Only surface ADR contradictions when friction is genuine enough to warrant reopening the decision
- Do not reopen ADRs pre-emptively
