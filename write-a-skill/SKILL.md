# write-a-skill

Create a new Claude Code skill with proper structure and documentation.

## Process

1. **Gather requirements** — what domain, what use cases, what trigger conditions
2. **Draft the skill** — SKILL.md plus any supporting files
3. **Review with user** — confirm completeness before saving

## File structure

```
<skill-name>/
  SKILL.md          # required — main instructions (keep under 100 lines)
  REFERENCE.md      # optional — longer reference content
  EXAMPLES.md       # optional — concrete examples
  scripts/          # optional — deterministic utility scripts
```

Split into separate files when SKILL.md exceeds 100 lines or when content covers distinct domains.

Add scripts only for deterministic operations (validation, formatting) that would otherwise generate repeated code.

## Critical: the description

The description is **the only thing your agent sees** when deciding which skill to load. It must:
- Fit within 1024 characters
- Be written in third person
- Include specific trigger conditions: "Use when [context]"
- Clearly distinguish this skill from alternatives

**Strong description format:**
```
[What the skill does]. Use when [specific trigger 1], [trigger 2], or user mentions [keywords].
```

**Example:**
```
Extract text and tables from PDF files, fill forms, merge documents.
Use when working with PDF files or when user mentions PDFs, forms, or document extraction.
```

## Review checklist

- [ ] Description includes trigger conditions
- [ ] SKILL.md is under 100 lines (or content is split)
- [ ] Examples are concrete, not abstract
- [ ] References stay one level deep (no chains)
- [ ] Scripts handle only deterministic operations
