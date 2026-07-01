---
name: analytics-workflow
description: Workflow SDD para proyectos de analítica, machine learning, scoring, segmentación, dashboards y reportería. Define el flujo PRD → specs → grill → issues → código → validación → entrega, con Ponytail, trazabilidad metodológica, reproducibilidad e interpretabilidad.
disable-model-invocation: true
---

# Analytics Workflow — SDD + Ponytail + Skills

Metodología para proyectos de analítica con Claude Code: credit scoring, cobranza inteligente, churn, fraude, segmentación/clustering, dashboards, reportería, modelos supervisados y no supervisados, y pipelines de datos para inteligencia comercial.

**Prioridades permanentes:**

1. **Trazabilidad** — toda decisión metodológica importante queda documentada.
2. **Reproducibilidad** — el pipeline corre de punta a punta sin intervención manual.
3. **Interpretabilidad** — los resultados pueden explicarse a negocio, auditoría o regulador.
4. **Ponytail** — mínimo código que funciona; sin abstracciones ni infraestructura futura innecesaria.
5. **Separación documental** — PRD, specs, issues, CONTEXT.md y ADRs cumplen roles distintos.

---

## Archivos de referencia

Este `SKILL.md` es el núcleo navegable. El detalle operativo vive en archivos aparte. **Cuando la tarea entre en uno de los casos de abajo, leé el archivo correspondiente con Read antes de responder** — no trabajes de memoria ni improvises lo que ya está documentado.

| Cuándo lo necesitás | Archivo |
|---|---|
| Detalle y prompts de cada skill (`/to-prd`, grill, issues, code-review…) | `references/skills-detalle.md` |
| Specs mínimas por tipo de proyecto (supervisado / clustering / dashboard) | `references/specs-por-tipo.md` |
| Template general de spec | `references/spec-template.md` |
| Patrones de quality gates + reglas anti-leakage | `references/quality-gates.md` |
| `00_config.r`, `00_run_pipeline.r`, renv | `references/reproducibilidad.md` |
| Versionado de modelos, CHANGELOG, `model_registry.csv` | `references/governance.md` |
| Narrativa automática vía Claude API (`llamar_claude()`) | `references/claude-api.md` |
| Módulos avanzados **opcionales** (reject inference, validación independiente, fairness, data governance) — activar solo si el cliente/regulador lo exige | `references/modulos-opcionales.md` |
| Plantillas copiables | `templates/00_config.r`, `templates/CLAUDE.md.tmpl`, `templates/CHANGELOG.md.tmpl` |

---

## Filosofía base

Tres principios en orden de prioridad.

**1. Specs-Driven Development.** Toda etapa relevante empieza con una spec escrita y grillada antes del código. El código existe para cumplir la spec; no se reconstruye la spec después de mirar el código.

```text
No spec → no código.
Spec sin grill → no código productivo.
Código que no cumple la spec → código incorrecto.
```

**2. Ponytail.** Usar el mínimo código que cumple el objetivo y pasa los quality gates. No anticipar necesidades futuras, no refactorizar prematuramente, no crear frameworks salvo duplicación real. Niveles: `full` (default), `lite` (algo más de estructura si el proyecto crecerá), `ultra` (máxima austeridad; scripts simples y directos).

**3. Claude como pair programmer.** Claude implementa, revisa y documenta. El analista decide: problema de negocio, target, población, horizonte, exclusiones, metodología, trade-offs y criterios de aceptación. Claude no inventa decisiones de negocio ni metodológicas críticas.

---

## Jerarquía documental

Cinco niveles con roles distintos:

- **PRD** — documento padre de una iniciativa. Define problema, solución, usuarios, user stories, alcance, fuera de alcance, criterios de éxito y specs hijas. Uno por iniciativa importante (`/to-prd`). No reemplaza a las specs. Ej: nuevo motor de scoring, sistema de cobranza inteligente, dashboard ejecutivo de riesgo.
- **Specs** — documentos operativos: cómo se implementa un componente analítico concreto (target, data snapshot, feature engineering, modeling/validation, deployment, monitoring, report). Cada spec se grilla antes de codear.
- **Issues** — unidades ejecutables derivadas de specs aprobadas. Opcionales: solo con equipo, backlog visible, ejecución por agentes o trazabilidad con cliente.
- **CONTEXT.md** — memoria estable del dominio: glosario, reglas de negocio persistentes, definiciones reutilizables, convenciones. No es basurero de decisiones transitorias.
- **ADRs** (`docs/adr/`) — decisiones arquitectónicas duraderas. Ej: batch vs real-time, scorecard interpretable vs black-box, Git + `modelos/vN/` como registry liviano.

### Persistencia de decisiones

Durante `/grill-with-docs`, clasificar cada respuesta del analista **antes** de documentarla:

| Tipo de decisión | Documento destino | Ejemplo |
|---|---|---|
| Regla estable de negocio/dominio | `CONTEXT.md` | "El score operativo se expresa de 1 a 1000." |
| Decisión específica de una feature/modelo | Spec activa | "Para este modelo v1 se usará horizonte de 90 días." |
| Decisión arquitectónica duradera | `docs/adr/` | "El scoring será batch diario y no real-time." |
| Trabajo ejecutable | Issue tracker | "Implementar cálculo mensual de PSI." |
| Hallazgo exploratorio | `EDA/` o informe técnico | "La variable X tiene 42% de missing." |

Regla: **CONTEXT.md no es un basurero de decisiones.** Solo contiene conocimiento reutilizable por futuras features y agentes.

---

## Estructura estándar de carpetas

```text
nombre_proyecto/
├── CLAUDE.md
├── CONTEXT.md
├── METODOLOGIA_<tipo>.md
│
├── docs/
│   ├── agents/            # issue-tracker.md, triage-labels.md, domain.md
│   └── adr/               # 0001-decision-template.md
│
├── specs/                 # 00_prd_reference.md, 01_…07_…md
├── scripts/               # 00_config.r, 00_run_pipeline.r, mis_funciones.r, 01_…07_…r
│
├── datos/
│   ├── raw/               # INMUTABLE
│   └── processed/
│
├── EDA/
├── modelos/
│   └── v1/                # modelo_final.rds, metadata_modelo.rds, CHANGELOG.md
│
├── reportes/
├── governance/            # model_registry.csv
├── graficos/
└── logs/
```

Reglas:

* `datos/raw/` es inmutable. Nunca sobrescribir datos originales.
* Todo output reproducible va a `datos/processed/`, `EDA/`, `modelos/`, `reportes/`, `graficos/` o `logs/`.
* Todo parámetro que puede cambiar entre proyectos vive en `scripts/00_config.r`.
* Ningún script depende de pasos manuales invisibles.

---

## Workflow por estados

Cada proyecto avanza por estados. No saltar un estado salvo decisión explícita documentada.

```text
intake → prd_created → specs_generated → specs_grilled
  → issues_created (opcional) → implementation → validation
  → report → delivery → monitoring
```

| Transición | Condición para avanzar |
|---|---|
| `intake` → `prd_created` | PRD documentado y alcance aprobado |
| `prd_created` → `specs_generated` | Specs hijas identificadas y creadas |
| `specs_generated` → `specs_grilled` | Cada spec crítica cuestionada con `/grill-with-docs` |
| `specs_grilled` → `implementation` | No quedan preguntas bloqueantes |
| `implementation` → `validation` | Pipeline corre punta a punta |
| `validation` → `report` | Quality gates y métricas mínimas pasan |
| `report` → `delivery` | Informe revisado, reproducible y entendible |
| `delivery` → `monitoring` | Registry, changelog y monitoreo definidos |

---

## Flujo por cada etapa del pipeline

```text
1. Crear o actualizar spec        → references/spec-template.md
2. Grill con /grill-with-docs     → clasificar decisiones (tabla de persistencia)
3. Commit de spec                 → git commit -m "spec: 0N_nombre"
4. Implementar script             → sin funcionalidad fuera de spec
5. Ejecutar script desde cero     → outputs a datos/processed, EDA, etc.
6. Verificar outputs y quality gates
7. /code-review                   → resolver hallazgos críticos
8. Commit de script               → git commit -m "feat: script 0N_nombre — descripción"
```

Al terminar el pipeline completo, una sola vez: `/code-review ultra` → informe → delivery → monitoring.

---

## Skills: cuándo invocar cada una

Tabla de routing. El detalle de uso y los prompts recomendados están en `references/skills-detalle.md`.

| Momento | Skill / acción | Notas |
|---|---|---|
| Configurar repo (1 vez) | `/setup-matt-pocock-skills` | Issue tracker, labels, docs de dominio |
| Crear PRD padre (1 vez/iniciativa) | `/to-prd` | No usar antes de cada script |
| Crear spec analítica | `/analytics-spec` o prompt manual | Una por componente crítico |
| Cuestionar spec | `/grill-with-docs` | Habilita implementación |
| Crear backlog | `/to-issues` | Solo con equipo / trazabilidad / agentes |
| Metodología credit scoring | `/credit-scoring` | Solo proyectos crediticios |
| Interpretación de negocio | `/advanced-analytics` | Traducir métricas a decisiones |
| Implementar | `ponytail full` | Modo permanente, no se invoca |
| Funciones reutilizables | `/tdd` | Solo para `mis_funciones.r` |
| Revisar script | `/code-review` | Después de cada script |
| Revisar entrega completa | `/code-review ultra` | Una sola vez al final |
| Refactor final | `/improve-codebase-architecture` | Solo cuando todo funciona |
| Grafo del codebase | `/graphify` | ≥ 3 scripts o al retomar |
| Cerrar sesión | `/handoff "próximo objetivo"` | Toda sesión larga cierra con handoff |

---

## Interpretabilidad

Todo resultado técnico debe tener traducción de negocio. Usar `/advanced-analytics` cuando haga falta.

No alcanza con `AUC = 0.72`. Debe decirse:

> El modelo tiene capacidad razonable de ordenar clientes por riesgo. Es útil para priorización y estrategia, pero no debería interpretarse como predicción exacta individual.

No alcanza con `PSI = 0.31`. Debe decirse:

> La población actual difiere materialmente de la población de desarrollo. Antes de usar el modelo para decisiones automáticas, se recomienda revisar drift por variable y performance reciente.

---

## Checklist de entrega

* [ ] PRD padre creado o documentado
* [ ] Specs críticas creadas y grilladas
* [ ] No quedan preguntas bloqueantes
* [ ] `00_run_pipeline.r` corre de punta a punta
* [ ] Todos los quality gates pasan
* [ ] `CONTEXT.md` contiene solo decisiones estables del dominio
* [ ] Cada spec contiene sus decisiones específicas
* [ ] ADRs creados para decisiones arquitectónicas duraderas
* [ ] `renv.lock` actualizado si aplica
* [ ] `governance/model_registry.csv` y `modelos/vN/CHANGELOG.md` actualizados si hay modelo
* [ ] Informe generado y revisado (narrativa automática revisada si se usó Claude API)
* [ ] `/code-review ultra` ejecutado y hallazgos críticos resueltos
* [ ] Commit final y tag de versión si corresponde (`git tag v1.0`)

---

## Errores comunes

| Error | Corrección |
|---|---|
| Usar `/to-prd` para cada script | `/to-prd` crea el PRD padre. Las etapas usan specs. |
| Escribir código antes de tener spec | Crear spec, grillarla y recién después implementar. |
| Mandar todas las decisiones a `CONTEXT.md` | Clasificar: contexto, spec, ADR o issue. |
| Mezclar PRD con spec | PRD define qué y por qué. Spec define cómo. |
| Calcular target sin fecha de corte clara | Definir observación, performance y población elegible. |
| Aprender bins/imputaciones con train + test | Fit en train, apply en test/OOT/producción. |
| Variables con información futura | Eliminar; es leakage. |
| Hardcodear parámetros en scripts | Pasar a `00_config.r`. |
| Scripts que fallan silenciosamente | Quality gates con `stop()`. |
| Reportar métricas sin interpretación | Traducir siempre a implicancias de negocio. |
| Refactorizar antes de que funcione | Ponytail: primero mínimo código correcto. |
| Usar `/improve-codebase-architecture` en el medio | Solo al final. |
| Mezclar cohortes sin vintage analysis | Analizar métricas por cohorte/vintage cuando aplique. |
| Crear issues demasiado grandes | Dividir por tarea ejecutable y acceptance criteria. |
| Llamar a Claude API con datos sensibles innecesarios | Enviar métricas agregadas y revisar narrativa. |
| Confiar en paquetes sin versionar | Usar `renv` si el proyecto debe reproducirse. |

---

## Inicio rápido en proyecto nuevo

```bash
mkdir nombre_proyecto && cd nombre_proyecto && git init

mkdir -p docs/agents docs/adr specs scripts datos/raw datos/processed \
         EDA modelos/v1 reportes governance graficos logs
```

En Claude Code:

```text
Trabajemos con ponytail full activo.

/setup-matt-pocock-skills

Crear CLAUDE.md, CONTEXT.md y scripts/00_config.r para este proyecto.
Luego /to-prd para crear el PRD padre.
```

Después: crear specs hijas según el tipo de proyecto (ver `references/specs-por-tipo.md`), grillarlas una por una, implementar scripts, correr pipeline, code review.

---

## Principio final

El workflow correcto no es `idea → código → arreglar documentación`. Es:

```text
idea → PRD → specs → grill → issues (opcional) → código → validación → informe → monitoreo
```

* Si una decisión no está documentada, no existe.
* Si el pipeline no corre de punta a punta, no está terminado.
* Si el resultado no puede explicarse a negocio, no está listo para entregar.
