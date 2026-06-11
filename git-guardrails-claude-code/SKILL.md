# git-guardrails-claude-code

Install a PreToolUse hook that prevents Claude from executing dangerous git commands.

## Blocked operations

- `git push` (including force push variants)
- `git reset --hard`
- `git clean` commands
- `git branch -D` (force branch deletion)
- `git checkout` / `git restore` commands that discard changes

## Installation steps

### 1. Choose scope

- **Project-level**: `.claude/settings.json` — blocks only in this repo
- **Global**: `~/.claude/settings.json` — blocks in all projects

### 2. Copy the blocking script

Copy `scripts/block-dangerous-git.sh` to the appropriate hooks directory and make it executable:

```bash
chmod +x .claude/hooks/block-dangerous-git.sh
```

### 3. Add hook configuration

Add to your chosen `settings.json`:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": ".claude/hooks/block-dangerous-git.sh"
          }
        ]
      }
    ]
  }
}
```

Merge into any existing `PreToolUse` array — do not replace it.

### 4. Customize (optional)

Edit `block-dangerous-git.sh` to adjust which patterns are blocked.

### 5. Verify

Test with a sample git push command piped through the script. A successful block returns exit code 2 with a blocked message to stderr.
