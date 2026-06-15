# scaffold-exercises

Create exercise directory structures for course sections that pass linting validation.

## Naming conventions

- Sections: `XX-section-name/` inside `exercises/`
- Exercises: `XX.YY-exercise-name/` inside their section
- All names: dash-case, lowercase

Example: `exercises/01-retrieval-skill-building/01.03-retrieval-with-bm25/`

## Required structure

Each exercise needs at least one variant subfolder: `problem/`, `solution/`, or `explainer/`.

Default to `explainer/` when stubbing unless specifications say otherwise.

Each variant subfolder must contain a non-empty `readme.md` with at minimum a title and description.

A readme-only exercise is fine during stubbing.

## Workflow

1. Parse the exercise plan
2. Create directories with `mkdir -p`
3. Generate stub readmes (title + brief description)
4. Run `pnpm ai-hero-cli internal lint` to validate
5. Fix any errors and re-lint until clean

## Validation checks

The linter verifies:
- Required subfolders exist
- `readme.md` files are non-empty
- No `.gitkeep` files
- Internal links are valid
- Proper folder structure and naming

## Moving exercises

Use `git mv` (not `mv`) when reorganizing to preserve version control history.
