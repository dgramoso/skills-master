# teach

Multi-session skill instruction framework using workspace state. Teaches users new concepts through stateful, progressive lessons grounded in their real-world goals.

## Workspace structure

```
MISSION.md              # why the user wants to learn this — grounds all instruction
RESOURCES.md            # curated high-quality external sources
NOTES.md                # scratchpad for user preferences and working notes
lessons/                # primary teaching units (HTML, one concept each)
reference/              # compressed quick-lookup materials
learning-records/       # non-obvious insights, like ADRs for learning
```

## Teaching philosophy

Effective learning requires three elements:
- **Knowledge** — from trusted, cited external sources (never rely solely on parametric knowledge)
- **Skills** — through interactive lessons with tight feedback loops
- **Wisdom** — from real-world community engagement

## Key principles

- Teach **ONE concept per lesson** — completable very quickly, tangible win
- Always operate within the learner's zone of proximal development
- Ground every lesson in `MISSION.md` — why does this matter to them?
- **Never trust parametric knowledge** — source and cite external resources
- Use learning records to capture non-obvious insights and drive future instruction
- Support lessons with thoroughly-cited reference materials

## Session flow

1. Read `MISSION.md` and recent `learning-records/` to calibrate
2. Identify the next appropriate concept (zone of proximal development)
3. Find high-quality external resources — cite them in the lesson
4. Write a focused HTML lesson to `lessons/`
5. Update `learning-records/` with any non-obvious insights from the session
