---
name: analytics-workflow
description: Usar cuando arranca un proyecto de analítica, machine learning, credit scoring, cobranza, churn, fraude, segmentación, clustering, dashboard o reportería; cuando hay que estructurar el PRD, las specs, el pipeline o la entrega de un engagement de datos; o cuando el usuario pide metodología, workflow o SDD para un proyecto analítico.
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
| Detalle y prompts de cada skill (`/to-spec`, grill, issues, code-review…) | `references/skills-detalle.md` |
| Specs mínimas por tipo de proyecto (supervisado / clustering / dashboard) | `references/specs-por-tipo.md` |
| Template general de spec | `references/spec-template.md` |
| Patrones de quality gates + reglas anti-leakage | `references/quality-gates.md` |
| `00_config.r`, `00_run_pipeline.r`, renv | `references/reproducibilidad.md` |
| Versionado de modelos, CHANGELOG, `model_registry.csv` | `references/governance.md` |
| Narrativa automática vía Claude API (`llamar_claude()`) | `references/claude-api.md` |
| Gestión del engagement: preventa/propuesta, intake, decision log, minutas, status, change request, cierre/handover, política de datos | `references/engagement.md` |
| Reportería recurrente: diccionario de KPIs versionado, data contract, QA de cifras, refresh/ownership | `references/reporteria.md` |
| Estándar de informe ejecutivo: pyramid principle, so-what, visualización, piezas del entregable | `references/informe-ejecutivo.md` |
| Módulos avanzados **opcionales** (reject inference, validación formal + MDD, fairness, data governance) — activar solo si el cliente/regulador lo exige | `references/modulos-opcionales.md` |
| Plantillas copiables (config R/Python, CLAUDE.md, CHANGELOG, artefactos de engagement/entrega) | `templates/` |
| Biblioteca semilla de funciones **testeada** (PSI, KS, AUC/Gini, lift/gain, strategy table, winsorización, WOE/IV, validación de porcentajes) | `templates/mis_funciones.r` + tests (R) · `templates/utils.py` + tests (Python) |

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

Seis niveles con roles distintos:

- **PRD** — documento padre de una iniciativa. Define problema, solución, usuarios, user stories, alcance, fuera de alcance, criterios de éxito y specs hijas. Uno por iniciativa importante (`/to-spec`). No reemplaza a las specs. Ej: nuevo motor de scoring, sistema de cobranza inteligente, dashboard ejecutivo de riesgo.
- **Specs** — documentos operativos: cómo se implementa un componente analítico concreto (target, data snapshot, feature engineering, modeling/validation, deployment, monitoring, report). Cada spec se grilla antes de codear.
- **Issues** — unidades ejecutables derivadas de specs aprobadas. Opcionales: solo con equipo, backlog visible, ejecución por agentes o trazabilidad con cliente.
- **CONTEXT.md** — memoria estable del dominio: glosario, reglas de negocio persistentes, definiciones reutilizables, convenciones. No es basurero de decisiones transitorias.
- **ADRs** (`docs/adr/`) — decisiones arquitectónicas duraderas. Ej: batch vs real-time, scorecard interpretable vs black-box, Git + `modelos/vN/` como registry liviano.
- **Decision log** (`engagement/decision_log.md`) — registro **cliente-facing** de toda decisión aprobada por el cliente, con fecha. Complementa a los documentos internos; protege el alcance. Ver `references/engagement.md`.

### Persistencia de decisiones

Durante `/grill-with-docs`, clasificar cada respuesta del analista **antes** de documentarla:

| Tipo de decisión | Documento destino | Ejemplo |
|---|---|---|
| Regla estable de negocio/dominio | `CONTEXT.md` | "El score operativo se expresa de 1 a 1000." |
| Decisión específica de una feature/modelo | Spec activa | "Para este modelo v1 se usará horizonte de 90 días." |
| Decisión arquitectónica duradera | `docs/adr/` | "El scoring será batch diario y no real-time." |
| Trabajo ejecutable | Issue tracker | "Implementar cálculo mensual de PSI." |
| Hallazgo exploratorio | `EDA/` o informe técnico | "La variable X tiene 42% de missing." |
| Decisión aprobada por el cliente | `engagement/decision_log.md` (además del destino interno) | "Cliente aprobó horizonte de 90 días (2026-07-15)." |

Regla: **CONTEXT.md no es un basurero de decisiones.** Solo contiene conocimiento reutilizable por futuras features y agentes.

---

## Estructura estándar de carpetas

```text
nombre_proyecto/
├── CLAUDE.md
├── CONTEXT.md
│
├── docs/
│   ├── agents/            # issue-tracker.md, triage-labels.md, domain.md
│   └── adr/               # 0001-decision-template.md
│
├── specs/                 # 00_prd_reference.md + specs numeradas según references/specs-por-tipo.md
├── scripts/               # 00_config.r, 00_run_pipeline.r, mis_funciones.r, 01_…0N_…r
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
├── engagement/            # intake.md, decision_log.md, minutas/, status/, acta_cierre.md
├── graficos/
└── logs/
```

Reglas:

* `datos/raw/` es inmutable. Nunca sobrescribir datos originales.
* Todo output reproducible va a `datos/processed/`, `EDA/`, `modelos/`, `reportes/`, `graficos/` o `logs/`.
* Todo parámetro que puede cambiar entre proyectos vive en `scripts/00_config.r` (o `00_config.py`).
* Ningún script depende de pasos manuales invisibles.
* La numeración y contenido de las specs (`01_…07_`) por tipo de proyecto está definida en `references/specs-por-tipo.md`.

> **Nombres por lenguaje.** Los nombres de archivo de esta skill están en R (`00_config.r`, `mis_funciones.r`, `.rds`); en Python usar los equivalentes `.py` (`00_config.py`, `utils.py`, `.parquet`/`.pkl`). La metodología es idéntica — ver la sección "Equivalentes en Python" en `references/reproducibilidad.md`.

---

## Workflow por estados

Cada proyecto avanza por estados. No saltar un estado salvo decisión explícita documentada. Antes de `kickoff` puede existir una fase de **preventa** (propuesta aceptada) — ver `references/engagement.md`.

```text
kickoff → prd_created → specs_generated → specs_grilled
  → issues_created (opcional) → implementation → validation
  → qa_delivery → report → delivery → handover
```

Dentro de `implementation`, el orden interno es: **datos → EDA → features → modelo**.

| Transición | Condición para avanzar |
|---|---|
| `kickoff` → `prd_created` | Intake completo (`engagement/intake.md`: sponsor, pregunta de negocio, viabilidad de datos, política de datos, expectativas calibradas) y PRD aprobado por el cliente |
| `prd_created` → `specs_generated` | Specs hijas identificadas y creadas |
| `specs_generated` → `specs_grilled` | Cada spec crítica cuestionada con `/grill-with-docs` |
| `specs_grilled` → `implementation` | No quedan preguntas bloqueantes |
| `implementation` → `validation` | Pipeline corre punta a punta |
| `validation` → `qa_delivery` | Quality gates y métricas mínimas pasan; el modelo supera al baseline |
| `qa_delivery` → `report` | Checklist de QA pre-entrega completo (ver `references/quality-gates.md`) |
| `report` → `delivery` | Informe cumple `references/informe-ejecutivo.md`: exec summary autocontenido, so-what cuantificado, cifras consistentes |
| `delivery` → `handover` | Acta de cierre, monitoreo asignado (cliente o consultor), decision log entregado, registry y changelog al día |

### EDA — exploración entre datos y features

El EDA es una **etapa de primera clase**: tiene su propia spec (`03_eda.md`), se grilla con `/grill-with-docs` y sigue el mismo flujo por etapa que el resto (spec → grill → commit → implementar → correr → verificar quality gates → code-review → commit). Su spec define qué preguntas debe responder, qué outputs produce en `EDA/` y sus quality gates verificables.

Ubicación en el pipeline: **después** del data snapshot y **antes** de feature engineering. Sus hallazgos (distribuciones, missing, outliers, correlaciones, señales tempranas de leakage) informan la spec de features, que puede refinarse a partir de ellos. Los hallazgos estables del dominio se registran en `CONTEXT.md`; los específicos de esta iteración, en la spec correspondiente.

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

Al terminar el pipeline completo, una sola vez: QA pre-entrega (`references/quality-gates.md`) + `/code-review ultra` → informe → delivery → handover.

---

## Skills: cuándo invocar cada una

Tabla de routing. El detalle de uso y los prompts recomendados están en `references/skills-detalle.md`.

| Momento | Skill / acción | Notas |
|---|---|---|
| Configurar repo (1 vez) | `/setup-matt-pocock-skills` | Issue tracker, labels, docs de dominio |
| Crear PRD padre (1 vez/iniciativa) | `/to-spec` | No usar antes de cada script |
| Estresar el plan tras el PRD | `/premortem` | Asumir que el proyecto falló a los 6 meses; riesgos y mitigaciones a `CONTEXT.md`, los que dependen del cliente se comunican en el kickoff |
| Crear spec analítica | Prompt manual (ver `references/skills-detalle.md`) | Una por componente crítico |
| Cuestionar spec | `/grill-with-docs` | Habilita implementación |
| Crear backlog | `/to-tickets` | Solo con equipo / trazabilidad / agentes |
| Metodología credit scoring | `/metodologia-credit-scoring` | Solo proyectos crediticios |
| Metodología modelos comerciales | `/metodologia-inteligencia-comercial` | Churn, propensión, cross-sell, priorización de cobranza, campañas |
| Interpretación de negocio | `/advanced-analytics` | Traducir métricas a decisiones |
| Implementar | Ponytail full (modo permanente, no es una skill que se invoca) | Mínimo código que pasa quality gates |
| Funciones reutilizables | `/tdd` | Arrancar de la biblioteca semilla (`templates/mis_funciones.r` / `utils.py`, ya testeada); `/tdd` solo para funciones nuevas |
| Revisar script | `/code-review` | Después de cada script |
| Revisar entrega completa | `/code-review ultra` | Una sola vez al final; la tipea el usuario (revisión cloud facturada, Claude no puede lanzarla solo) |
| Refactor final | `/improve-codebase-architecture` | Solo cuando todo funciona |
| Grafo del codebase | `/graphify` | ≥ 3 scripts o al retomar |
| Cerrar sesión | `/handoff "próximo objetivo"` | Toda sesión larga cierra con handoff |
| Cierre de proyecto (handover) | `/lecciones-aprendidas` | Retro del engagement; los patrones reutilizables van a memoria persistente |

---

## Interpretabilidad y so-what

Todo resultado técnico debe tener traducción de negocio. Usar `/advanced-analytics` cuando haga falta.

En el informe final, el estándar es más exigente (detalle en `references/informe-ejecutivo.md`): ningún hallazgo se reporta suelto —

```text
hallazgo → implicancia → recomendación → impacto estimado → esfuerzo/owner
```

El impacto se cuantifica en plata o volumen cuando los datos lo permiten; si no, se dice explícito por qué no.

No alcanza con `AUC = 0.72`. Debe decirse:

> El modelo tiene capacidad razonable de ordenar clientes por riesgo. Es útil para priorización y estrategia, pero no debería interpretarse como predicción exacta individual.

No alcanza con `PSI = 0.31`. Debe decirse:

> La población actual difiere materialmente de la población de desarrollo. Antes de usar el modelo para decisiones automáticas, se recomienda revisar drift por variable y performance reciente.

---

## Checklist de entrega

* [ ] Intake completo (`engagement/intake.md`) y decision log al día — toda aprobación del cliente con fecha
* [ ] PRD padre creado o documentado
* [ ] Specs críticas creadas y grilladas
* [ ] No quedan preguntas bloqueantes
* [ ] Spec de EDA (`03_eda.md`) creada, grillada y ejecutada; hallazgos en `EDA/` antes de feature engineering
* [ ] `00_run_pipeline.r` corre de punta a punta
* [ ] Todos los quality gates pasan
* [ ] Modelo comparado contra baseline naive / status quo del cliente — y lo supera
* [ ] `CONTEXT.md` contiene solo decisiones estables del dominio
* [ ] Cada spec contiene sus decisiones específicas
* [ ] ADRs creados para decisiones arquitectónicas duraderas
* [ ] `renv.lock` actualizado si aplica
* [ ] `governance/model_registry.csv` y `modelos/vN/CHANGELOG.md` actualizados si hay modelo
* [ ] QA pre-entrega ejecutado: pipeline reproducido en limpio, cifras del informe verificadas contra outputs (`templates/qa_pre_entrega.md.tmpl`)
* [ ] Informe cumple `references/informe-ejecutivo.md`: responde la pregunta de negocio del PRD, exec summary autocontenido, so-what cuantificado por hallazgo, supuestos/limitaciones/condiciones de uso, cifras consistentes (narrativa automática revisada si se usó Claude API)
* [ ] `/code-review ultra` ejecutado y hallazgos críticos resueltos
* [ ] Acta de cierre y handover de monitoreo definidos (quién lo corre, con qué instrucciones)
* [ ] Commit final y tag de versión si corresponde (`git tag v1.0`)

---

## Errores comunes

| Error | Corrección |
|---|---|
| Usar `/to-spec` para cada script | `/to-spec` crea el PRD padre. Las etapas usan specs. |
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
| Prometer métricas concretas antes del EDA | Calibrar expectativas recién después del diagnóstico de datos. |
| Título de gráfico que describe en vez de afirmar | Assertion titles: el título es el hallazgo. |

---

## Inicio rápido en proyecto nuevo

```bash
mkdir nombre_proyecto && cd nombre_proyecto && git init

mkdir -p docs/agents docs/adr specs scripts datos/raw datos/processed \
         EDA modelos/v1 reportes governance engagement/minutas engagement/status \
         graficos logs
```

En Claude Code:

```text
Trabajemos con ponytail full activo.

/setup-matt-pocock-skills

Crear CLAUDE.md, CONTEXT.md y scripts/00_config.r para este proyecto.
Completar engagement/intake.md con el checklist de references/engagement.md.
Luego /to-spec para crear el PRD padre.
```

Después: crear specs hijas según el tipo de proyecto (ver `references/specs-por-tipo.md`), grillarlas una por una, implementar scripts, correr pipeline, code review.

---

## Principio final

* Si una decisión no está documentada, no existe.
* Si el cliente no lo aprobó por escrito, no está aprobado.
* Si el pipeline no corre de punta a punta, no está terminado.
* Si el resultado no puede explicarse a negocio —con su so-what cuantificado—, no está listo para entregar.
