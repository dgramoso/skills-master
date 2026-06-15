# migrate-to-shoehorn

Migrate test files from TypeScript `as` type assertions to `@total-typescript/shoehorn`.

Shoehorn lets you pass partial data in tests while keeping TypeScript happy. **Test code only. Never use shoehorn in production code.**

## Installation

```bash
npm i @total-typescript/shoehorn
```

## Migration patterns

### Pattern 1: Large objects with minimal needed properties

Replace verbose object creation or `as Type` with `fromPartial()`:

```typescript
// Before
const user = { id: 1, name: "Alice" } as User;

// After
import { fromPartial } from "@total-typescript/shoehorn";
const user = fromPartial<User>({ id: 1, name: "Alice" });
```

### Pattern 2: Intentionally incorrect data

Replace `as unknown as Type` with `fromAny()` when testing error scenarios:

```typescript
// Before
const bad = "not-a-user" as unknown as User;

// After
const bad = fromAny("not-a-user");
```

### Pattern 3: Enforce complete objects

Use `fromExact()` when you need to ensure all fields are specified.

## Function reference

| Function | Purpose |
|----------|---------|
| `fromPartial<T>()` | Type-checked partial data — TypeScript autocomplete, missing fields allowed |
| `fromAny()` | Intentionally incorrect data with autocomplete — for error scenario tests |
| `fromExact<T>()` | Enforce complete object specification |

## Steps

1. Identify test files containing `as` assertions
2. Install the package
3. Replace assertions with the appropriate shoehorn function
4. Add imports
5. Verify with type checking (`tsc --noEmit`)
