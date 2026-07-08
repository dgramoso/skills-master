---
name: skill-cleaner
description: Audit local Claude Code skills - prompt budget estimate, duplicate names/descriptions across personal/project/plugin roots, over-long descriptions, and unused candidates. Use when trimming skill prompt budget, finding duplicate skills, or deciding which skills/plugins to remove.
---

# Skill Cleaner

Adapted from [steipete/agent-scripts](https://github.com/steipete/agent-scripts) `skill-cleaner`, rewritten for Claude Code (the original targets Codex's `debug prompt-input` and `~/.codex` logs, which don't exist here). This version scans Claude Code's actual skill roots directly from the filesystem.

## Workflow

1. Run the analyzer:

```bash
node "$HOME/.claude/skills/skill-cleaner/scripts/skill-cleaner.js" --months 3
```

Variants:

```bash
node .../skill-cleaner.js --no-logs                                  # skip usage scan (faster)
node .../skill-cleaner.js --context-tokens 200000 --budget-percent 2  # tune budget model
node .../skill-cleaner.js --root "/path/to/other/skills"              # include an extra root
```

2. Read the report in this order:
   - **Skill Budget**: rough token estimate (`ceil(utf8_bytes / 4)`) of all skill descriptions vs a configurable % of context window.
   - **Description candidates**: skills with descriptions over 400 chars — candidates for tightening.
   - **Duplicates**: same skill `name` found in more than one root (personal `~/.claude/skills`, project `.claude/skills`, or plugin cache `~/.claude/plugins/cache/**/skills`).
   - **Unused candidates**: skill name never mentioned in session transcripts (`~/.claude/projects/**/*.jsonl`) within the lookback window. Heuristic, not proof — a skill can be used without its name appearing verbatim.
   - **Root summary**: how many skills came from each root.

3. Before deleting or editing anything:
   - Confirm the kept copy is the one actually loaded (plugin skills are usually canonical; a personal-dir duplicate of a plugin skill is the one to drop).
   - Don't delete a skill just because it's "unused" by the heuristic — check if it's new or situational first.

## Notes

- Plain Node (no TypeScript, no deps) — Node 24+ needed for nothing special, works on any recent Node.
- `--self-test` runs a small assert-based smoke check of the frontmatter parser and duplicate detector.
- Token/budget math is a rough estimate, not the real Claude Code prompt renderer — treat the number as directional.

## Output Policy

- Suggest first; only edit/delete when the user explicitly asks.
- Don't delete a skill directory without naming it and confirming with the user first.
