# setup-matt-pocock-skills

Configure engineering agent capabilities for this repository. Run this once per repo before using other Matt Pocock skills.

## What this configures

Three things agents need to work effectively in this codebase:

1. **Issue tracker location** — Where work items live: GitHub Issues, GitLab Issues, local markdown files, or another system. Defaults to GitHub but adapts based on the repository's remote URL.

2. **Triage label vocabulary** — Maps five canonical workflow states to your repo's actual label strings:
   - `needs-triage` → needs evaluation
   - `needs-info` → awaiting reporter input
   - `ready-for-agent` → ready for autonomous pickup
   - `ready-for-human` → needs human judgment
   - `wontfix` → won't be addressed

3. **Domain documentation layout** — Whether the project uses a single root `CONTEXT.md` or multiple context files (common in monorepos / bounded context setups).

## Process

1. Explore the current repository state (remote URL, existing labels, existing docs)
2. Present findings with explanations, one section at a time
3. Confirm choices with the user before writing anything
4. Write an `## Agent skills` block to `CLAUDE.md` or `AGENTS.md`
5. Create three supporting docs under `docs/agents/`:
   - `issue-tracker.md` — tracker type and access instructions
   - `triage-labels.md` — label vocabulary mapping
   - `domain-docs.md` — where context files live

## When to run

Run `/setup-matt-pocock-skills` at the start of a project before using `/triage`, `/to-issues`, `/to-prd`, or `/grill-with-docs`. Other skills will prompt you to run this if configuration is missing.
