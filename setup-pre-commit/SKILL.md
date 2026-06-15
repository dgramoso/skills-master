# setup-pre-commit

Configure Husky pre-commit hooks with lint-staged and Prettier.

## What gets installed

- **Husky** — git hook manager
- **lint-staged** — runs Prettier on staged files only
- **Prettier** — code formatter (config created if missing)
- **typecheck + test** — run at commit time (if scripts exist in package.json)

## Steps

### 1. Detect package manager

Check for lock files: `package-lock.json` (npm), `pnpm-lock.yaml` (pnpm), `yarn.lock` (yarn), `bun.lockb` (bun). Default to npm if unclear.

### 2. Install dependencies

```bash
<pm> install -D husky lint-staged prettier
```

### 3. Initialize Husky

```bash
npx husky init
```

Creates `.husky/` and adds `prepare: "husky"` to `package.json`.

### 4. Create `.husky/pre-commit`

```
npx lint-staged
npm run typecheck
npm run test
```

Adapt `npm` to the detected package manager. Omit `typecheck` or `test` lines if those scripts don't exist in `package.json` — tell the user.

### 5. Create `.lintstagedrc`

```json
{ "*": "prettier --ignore-unknown --write" }
```

### 6. Create `.prettierrc` (if missing)

```json
{
  "useTabs": false,
  "tabWidth": 2,
  "printWidth": 80,
  "singleQuote": false,
  "trailingComma": "es5",
  "semi": true,
  "arrowParens": "always"
}
```

### 7. Verify

- [ ] `.husky/pre-commit` exists and is executable
- [ ] `.lintstagedrc` exists
- [ ] `prepare` script in `package.json` is `"husky"`
- [ ] Prettier config exists
- [ ] `npx lint-staged` runs without error

### 8. Commit

Stage all created/changed files and commit:
`Add pre-commit hooks (husky + lint-staged + prettier)`

This runs through the new hooks — smoke test that everything works.

## Notes

- Husky v9+ doesn't need shebangs in hook files
- `prettier --ignore-unknown` skips files Prettier can't parse
- lint-staged runs first (fast, staged-only), then full typecheck and tests
