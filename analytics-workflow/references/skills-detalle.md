# Detalle operativo de cada skill del workflow

> Parte de la skill `analytics-workflow`. El `SKILL.md` tiene la tabla de routing (cuándo usar qué); acá está el detalle de uso y los prompts recomendados de cada una.

---

## `/setup-matt-pocock-skills` — inicio del repo

Ejecutar una sola vez por repo. Objetivo:

* configurar issue tracker
* configurar triage labels
* configurar docs de dominio
* crear o actualizar `CLAUDE.md` / `AGENTS.md`
* crear `docs/agents/*.md`

---

## `/to-prd` — definición de iniciativa

Ejecutar una vez por iniciativa importante. El PRD es padre; las specs son hijas.

```text
/to-prd

Crear un PRD padre para [nombre de la iniciativa] usando lo conversado y el estado actual del repo.

El PRD debe:
- definir problema
- solución propuesta
- usuarios
- user stories
- alcance
- fuera de alcance
- criterios generales de éxito
- specs hijas necesarias

No crear código.
No crear todavía issues técnicos salvo que se pida explícitamente.
```

Ejemplos:

```text
/to-prd

Crear un PRD para un sistema de cobranza inteligente.
Debe identificar specs hijas para target, datos, features, modelo, estrategia de acción, monitoreo y reporte.
```

```text
/to-prd

Crear un PRD para un nuevo motor de scoring de originación de tarjeta.
Debe contemplar riesgo, aprobación, explicabilidad, validación, deployment batch y monitoreo.
```

Regla:

```text
/to-prd no se usa antes de cada script. Crea el PRD padre, no las etapas.
```

---

## Generación de specs analíticas

Si existe skill específica: `/analytics-spec`. Si no, usar prompt manual equivalente:

```text
Crear la spec [nombre] para el PRD [nombre].

La spec debe definir:
- relación con el PRD padre
- objetivo
- alcance
- precondiciones
- diseño metodológico
- postcondiciones
- quality gates
- invariantes
- riesgos
- preguntas abiertas
- outputs esperados

Guardar en specs/[archivo].md.
No escribir código todavía.
```

Ejemplo:

```text
Crear la spec "Target & Outcome Definition" para el PRD de cobranza inteligente.

Debe definir:
- unidad de análisis
- fecha de corte
- horizonte de predicción
- evento objetivo
- outcomes secundarios
- población elegible
- exclusiones
- indeterminados
- riesgos de leakage
- quality gates

Guardar en specs/01_target_outcome.md.
No escribir código.
```

---

## `/grill-with-docs` — grill de specs

Después de crear cada spec crítica:

```text
/grill-with-docs specs/01_target_outcome.md

Leé la spec activa, CONTEXT.md y ADRs relevantes.

Haceme preguntas críticas una por una.

Después de cada respuesta:
- si es regla estable del dominio, actualizá CONTEXT.md
- si es decisión específica de esta etapa, actualizá la spec activa
- si es decisión arquitectónica duradera, proponé o actualizá ADR
- si es tarea ejecutable, registrala como issue o TODO según corresponda

No avances al código hasta que no queden preguntas bloqueantes.
```

Regla:

```text
Una spec no grillada no habilita implementación.
```

Ver `SKILL.md` para la tabla de persistencia de decisiones (dónde va cada respuesta del grill).

---

## `/to-issues` — backlog

Ejecutar solo cuando:

* hay equipo
* hay backlog visible para cliente
* el proyecto dura varias semanas
* se delegará implementación a agentes
* se necesita trazabilidad PRD → specs → tasks

Cada issue debe incluir:

```markdown
## Context
Spec relacionada: specs/...

## Task
Qué hay que implementar.

## Acceptance criteria
- [ ] ...
- [ ] ...

## Out of scope
- ...

## Validation
Cómo se verifica que está correcto.
```

Labels recomendados:

* `needs-triage`
* `needs-info`
* `ready-for-agent`
* `ready-for-human`
* `wontfix`

Issue AFK-ready:

```text
Un agente puede tomarlo sin pedir contexto humano adicional.
```

---

## `/credit-scoring`

Invocar si el proyecto es credit scoring o riesgo crediticio. Debe guiar:

* definición de bueno/malo
* WOE/IV
* binning
* scorecard
* logística
* champion/challenger
* KS
* Gini
* AUC
* calibración
* strategy tables
* cutoff analysis
* PSI
* governance
* explicabilidad
* monitoreo

No usar mecánicamente en segmentación, dashboards o modelos no crediticios.

---

## `/advanced-analytics`

Invocar cuando el resultado técnico necesite interpretación de negocio. Especialmente útil para:

* clusters
* estrategia comercial
* cobranzas
* originación
* dashboards ejecutivos
* recomendaciones accionables
* traducción de métricas a decisiones

---

## `/tdd`

Usar TDD formal solo para funciones reutilizables en `mis_funciones.r`:

* función de PSI
* función de WOE
* función de lift/gain
* función de strategy table
* función de winsorización
* función de validación de porcentajes

Para scripts lineales, los `stop()` y quality gates son TDD implícita.

---

## `/code-review`

Después de cada script:

```text
/code-review
```

Antes de entregar:

```text
/code-review ultra
```

Si hay disponibilidad:

```text
/codex:review
```

Regla:

```text
/code-review ultra se ejecuta una sola vez al final, no en medio del desarrollo.
```

Debe revisar: cumplimiento de spec, reproducibilidad, errores silenciosos, duplicaciones, leakage, hardcoding, claridad, outputs, quality gates, riesgos metodológicos.

---

## `/improve-codebase-architecture`

Ejecutar solo al final, cuando todo funciona:

* detectar duplicaciones
* mover funciones repetidas a `mis_funciones.r`
* limpiar estructura
* mejorar mantenibilidad

No usar durante exploración inicial ni antes de que el pipeline corra punta a punta.

---

## `/graphify`

Invocar cuando hay al menos 3 scripts relacionados o al retomar un proyecto:

```text
graphify query "cómo se calcula el target"
graphify query "dónde se genera el dataset final"
graphify query "qué scripts dependen de 02_features.r"
```

---

## `/handoff`

Al cerrar sesión:

```text
/handoff "próximo objetivo"
```

Debe resumir: estado actual, specs creadas, decisiones tomadas, scripts implementados, pendientes, riesgos y próximo paso recomendado.

Regla:

```text
Toda sesión larga debe cerrar con handoff.
```
