# to-prd

Turn the current conversation context into a PRD and publish it to the project issue tracker.

The issue tracker and triage label vocabulary should have been provided to you — run `/setup-matt-pocock-skills` if not.

**Do NOT interview the user — just synthesize what you already know.**

## Process

### 1. Explore the codebase

Understand the current state and apply domain glossary vocabulary and any ADRs. Use the project's established terminology throughout the PRD.

### 2. Identify testing seams

Sketch out the seams at which you're going to test the feature. Existing seams should be preferred to new ones.

### 3. Write and publish the PRD

Use the template below. Apply the `ready-for-agent` triage label upon publication.

## PRD Template

### Problem Statement

What problem does this solve, from the user's perspective?

### Solution

High-level description of the solution.

### User Stories

Numbered list using actor/feature/benefit format:
1. As a [user], I can [feature] so that [benefit].
2. ...

(Be extensive — enumerate all meaningful user stories.)

### Implementation Decisions

- Module boundaries and interfaces
- Architectural choices
- Trade-offs made

Do NOT include specific file paths or code snippets. Exception: if a prototype produced a snippet encoding a decision more precisely than prose (state machine, reducer, schema, type shape), inline it briefly.

### Testing Decisions

- Focus on external behavior, not implementation details
- Which seams will be used for testing
- Module coverage

### Out of Scope

What this PRD explicitly does not cover.

### Further Notes

Open questions, risks, follow-up work.
