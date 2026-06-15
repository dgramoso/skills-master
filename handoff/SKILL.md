# handoff

Compact the current conversation into a handoff document for agent-to-agent transfer.

## Output location

Save to the OS temporary directory (not the workspace). Do not write to the project.

## Required sections

1. **Conversation summary** — what was discussed, decided, and done
2. **Suggested skills** — which agent skills the next session should load
3. **References** — pointers to existing artifacts (PRDs, plans, ADRs, issues, commits, diffs). Reference rather than duplicate their content.

## Rules

- **Redact sensitive data**: API keys, passwords, PII — never include in handoff docs
- **Incorporate user arguments** as context for the next session's focus (the user may pass an argument describing what the next session should accomplish)
- **Do not reproduce content from other artifacts** — link or reference instead
- Keep it compact enough that an agent can read it in one pass without losing important context

## Usage

`/handoff` — compact current session for transfer
`/handoff <next session goal>` — tailor the handoff toward a specific next objective
