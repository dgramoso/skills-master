---
name: metodologia-credit-scoring
description: >
  Use when starting any credit scoring or predictive risk model project, and when
  developing, auditing, validating, monitoring, or documenting scorecards. Triggers:
  "credit scoring", "scorecard", "modelo de riesgo", WOE, IV, binning, PSI, KS,
  master scale, strategy tables, reject inference, fair lending, roll rates, vintage,
  validación OOT, SR 11-7, IFRS 9, Basilea, metodología Siddiqi.
---

# Metodología de Trabajo: SDD + Ponytail + Skills para Proyectos de Credit Scoring

**Aplicable a:** proyectos de analítica con Claude Code (credit scoring, modelos predictivos, dashboards)

> **Guía técnica embebida:** `references/credit-scoring.md` contiene la metodología Siddiqi completa (estructura canónica, specs pre-llenadas por etapa, quality gates, WOE/IV, scorecard, strategy tables, fair lending, governance, informe). Este SKILL.md define el **proceso**; la referencia define la **técnica**. Leerla al armar la estructura, al escribir cada spec y al modelizar.

---

## Filosofía base

Tres principios que se aplican siempre, en orden de prioridad:

1. **SDD (Specs-Driven Development)**: toda etapa empieza con una spec escrita y grillada. El código existe para cumplir la spec — no al revés.
2. **Ponytail**: mínimo código que funciona. No construir para el futuro. No abstracciones sin justificación. El primer script que pasa los quality gates es el correcto.
3. **Claude como pair programmer permanente**: Claude no reemplaza el juicio analítico, lo amplifica. Las decisiones de negocio y metodológicas son del analista. Claude implementa.

---

## Fases del engagement (con gates de aprobación del cliente)

```
Fase 0 — Kickoff y alcance
  /to-prd → /grill-with-docs → /premortem
  GATE: cliente valida specs/00_proyecto.md (objetivo, target preliminar, datos comprometidos)

Fase 1 — Data audit (go / no-go)
  Evaluar los datos recibidos ANTES de comprometer el modelo
  GATE: decisión go / no-go / go con alcance reducido, comunicada al cliente

Fase 2 — Desarrollo
  Pipeline por etapas según references/credit-scoring.md
  GATE: cliente valida definición de target y ventanas ANTES de modelizar

Fase 3 — Validación
  Validación independiente + /code-review ultra
  GATE: hallazgos resueltos o aceptados por escrito

Fase 4 — Entrega e implementación
  Informe + paquete de handover + test de paridad dev-prod
  GATE: checklist de entrega completo
```

**Regla:** ningún gate se pasa implícitamente. Cada aprobación queda en el decision log con fecha y quién la dio. El gate de la Fase 2 es el que evita el "eso no era lo que pedimos" en la semana 8.

---

## Fase 1: Data audit (go / no-go)

Antes de la spec 01, evaluar formalmente los datos recibidos:

| Dimensión | Pregunta | Semáforo |
|---|---|---|
| Completitud | ¿Llegaron todas las fuentes comprometidas? ¿% de missing en variables clave? | 🟢 🟡 🔴 |
| Profundidad histórica | ¿Alcanza para ventana de performance + OOT? | 🟢 🟡 🔴 |
| Volumen de malos | ¿≥ ~2.000 malos? (regla Siddiqi, ver `references/credit-scoring.md`) | 🟢 🟡 🔴 |
| Consistencia | ¿Claves únicas, fechas coherentes, snapshots a la fecha correcta? | 🟢 🟡 🔴 |
| Linkage | ¿Las fuentes se pueden unir con cobertura aceptable? | 🟢 🟡 🔴 |

Resultado: **go / no-go / go con alcance reducido**, documentado en `EDA/data_audit.md` y comunicado al cliente antes de modelar. Un rojo descubierto en la semana 6 cuesta el proyecto; descubierto en la semana 1, es una conversación de alcance.

Es también la protección contractual del consultor: lo que se entrega depende de la calidad de lo que se recibe, y eso queda establecido por escrito al inicio.

---

## Estructura de carpetas (estándar para todo proyecto)

La estructura canónica de carpetas, scripts y specs está definida en `references/credit-scoring.md` (etapas `01_ingesta_y_target` → `05_validacion_y_monitoreo` + `06_informe`). No duplicarla acá: usar siempre esa versión.

Esta metodología agrega sobre esa estructura:

```
nombre_proyecto/
├── CLAUDE.md              ← contexto del proyecto para Claude (leer en cada sesión)
├── CONTEXT.md             ← dominio, variables, glosario, decisiones tomadas
├── modelos/
│   └── v1/                ← versionado: cada versión con su CHANGELOG.md
└── (resto según references/credit-scoring.md)
```

**Regla:** `datos/raw/` es inmutable. Nunca sobrescribir datos originales.

---

## Definición de target y ventanas

El error más caro en credit scoring no está en el código — está en cómo se define a quién se predice y sobre qué período. Documentar en `CONTEXT.md` **antes** de la spec 01.

| Decisión | Qué definir | Dónde se documenta |
|---|---|---|
| Definición de malo | Días de mora y severidad (ej: mora ≥ 30, ≥ 90, default Basilea) | `CONTEXT.md` + `DEF_DEFAULT` en `00_config.R` |
| Ventana de observación | Fecha/período en que se "fotografía" al cliente | `CONTEXT.md` |
| Ventana de performance | Período posterior en que se observa si cae en mora (típico 12 meses) | `CONTEXT.md` |
| Población elegible | Quién entra y quién se excluye, con motivo explícito | `CONTEXT.md` + `exclusion_log` |
| Indeterminados | Clientes ni claramente buenos ni malos: ¿se excluyen o se asignan? | `CONTEXT.md` |

**Invariante crítico:** ninguna variable puede contener información posterior a la ventana de observación. Si una variable "ve el futuro", es leakage y el modelo no sirve en producción aunque el AUC sea alto.

**Vintage / cohortes:** si hay datos de varios períodos, analizar la tasa de malo por cohorte antes de mezclar todo.

> Estas cinco decisiones son las que un validador independiente o auditor revisa primero. Si no están documentadas con justificación, el modelo no es defendible.

---

## Decision log (formato de auditoría)

Las decisiones en `CONTEXT.md` se registran con formato defendible ante auditoría:

```markdown
## [AAAA-MM-DD] Definición de malo: mora >= 90 días en ventana de 12 meses
- Alternativas consideradas: mora >= 30 (ruido de cura alto), mora >= 60
- Evidencia: roll rate — 78% de las cuentas en mora 90 no cura
- Decidió: cliente (gerencia de riesgo), reunión del AAAA-MM-DD
```

El campo **"Decidió"** es el que importa: separa las decisiones metodológicas del consultor de las decisiones de negocio del cliente. Cuando el modelo se cuestione un año después, ese registro es la defensa. Los gates de fase aprobados también se registran acá.

---

## Template de spec (usar siempre)

El template de spec y las specs pre-llenadas por etapa (`01_ingesta_y_target` a `05_validacion_y_monitoreo`) están en `references/credit-scoring.md`. No duplicar acá: usar siempre esa versión.

---

## Flujo completo por etapa

```
Una sola vez al inicio del proyecto:

0. Definición de alcance
   /to-prd
   → dump libre del proyecto en lenguaje natural (objetivo, datos, población, restricciones)
   → Claude genera specs/00_proyecto.md con alcance, fuera de alcance y preguntas abiertas
   → con cliente presente: el cliente valida el borrador antes de salir de la reunión

   /grill-with-docs sobre specs/00_proyecto.md
   → Claude cuestiona el alcance una pregunta a la vez
   → cada respuesta actualiza CONTEXT.md (target, ventanas, población, restricciones)
   → diferencia clave: no actualiza specs — actualiza CONTEXT.md con el conocimiento
     de dominio (el "por qué"). Nunca saltar al código sin grilear la spec.
   → commit: "spec: 00_proyecto — alcance validado"

   /premortem sobre el plan
   → asume que el proyecto falló a los 6 meses y lista los motivos
   → modos de falla típicos en scoring: datos peores de lo prometido,
     target indefendible, cliente sin capacidad de implementar el score
   → riesgos y mitigaciones quedan en CONTEXT.md
   → los riesgos que dependen del cliente (calidad de datos, implementación)
     se comunican en el kickoff, no cuando se materializan

Para cada etapa del pipeline:

1. /to-prd
   → describís la etapa en lenguaje natural
   → Claude genera spec borrador (objetivo, precondiciones, postcondiciones,
     quality gates, invariantes)

2. /grill-with-docs
   → Claude lee la spec y CONTEXT.md
   → hace preguntas críticas una por una
   → vos respondés
   → CONTEXT.md se actualiza con cada decisión

3. Commit de la spec
   → git commit -m "spec: 0N_nombre"

4. Implementación
   → Claude escribe el script siguiendo la spec
   → el script corre sin errores desde cero
   → outputs en EDA/ o datos/processed/

5. /code-review
   → revisa el script antes de avanzar a la siguiente etapa

   Al finalizar el pipeline completo (una sola vez):
   → /code-review ultra   ← revisión profunda multi-agente antes de entregar al cliente

6. Commit del script
   → git commit -m "feat: script 0N_nombre — descripción breve"

7. /handoff (al cerrar la sesión)
   → compacta la conversación en un documento de transferencia
   → la próxima sesión lo lee para retomar sin perder contexto
   → útil también para pasar trabajo a otro miembro del equipo
   → /handoff "próximo objetivo" para orientar la transferencia
```

---

## `00_config.R` — qué debe contener siempre

El contenido canónico de `00_config.R` (paths, seeds, target, umbrales de calidad, ejemplo completo) está en `references/credit-scoring.md`.

**Regla:** todo parámetro que puede cambiar entre proyectos vive en `00_config.R`. Los scripts no tienen valores hardcodeados.

---

## Reproducibilidad: renv + versión de R

`set.seed()` garantiza reproducibilidad del muestreo pero no protege contra cambios de API de paquetes.

> **Caso real:** una actualización de `xgboost` renombró parámetros (`eta` → `learning_rate`, `data` → `x`). El mismo código que corría dejó de correr. `set.seed` no evita esto; `renv` sí.

```r
install.packages("renv")
renv::init()        # al arrancar el proyecto
renv::snapshot()    # después de cada cambio en dependencias
renv::restore()     # al clonar o retomar
```

**Qué se commitea:** `renv.lock` sí. La carpeta `renv/library/` no (va a `.gitignore`).
Registrar la versión de R en `CONTEXT.md` (ej: R 4.5.1).

---

## Interpretaciones automáticas vía Claude API

El script de informe (`06_informe.R`) puede llamar a Claude directamente para generar narrativa analítica con los números reales de cada corrida.

La función `llamar_claude()` (vive en `mis_funciones.R`) y las secciones del informe que genera automáticamente (performance, calibración, PSI, recomendaciones) están definidas en `references/credit-scoring.md`. No duplicar la función acá.

Configuración: agregar `ANTHROPIC_API_KEY=sk-ant-...` en `~/.Renviron`. La función devuelve `""` si no hay API key, sin romper el pipeline.

---

## Quality Gates

El patrón estándar (`stopifnot()` / `stop()`) y los gates por etapa están definidos en `references/credit-scoring.md`.

**El script debe fallar ruidosamente.** Un script que termina sin error pero con datos incorrectos es peor que uno que falla.

---

## CLAUDE.md — contenido mínimo por proyecto

```markdown
# CLAUDE.md — nombre_proyecto

## Contexto
[Una oración describiendo el proyecto. Ver CONTEXT.md para detalle.]

## Lenguaje
R. / SQL + R.

## Metodología
SDD + Ponytail. Cada etapa tiene su spec en specs/. Arrancar siempre por la spec.

## Estructura de specs
- specs/00_proyecto.md → alcance validado
- specs/01_... → [qué hace]

## Versionado de modelos
modelos/vN/ — cada versión tiene modelo + CHANGELOG.md

## Ponytail
Activo (full). No construir abstracciones no pedidas.

## Agent skills
- Issue tracker: local markdown (specs/ actúa como backlog)
- Context files: CONTEXT.md (dominio), specs/*.md (tareas activas)

## Cierre de sesión
Antes de cerrar, correr `/handoff "descripción de lo que sigue"`.
```

---

## Versionado de modelos

```
modelos/
  v1/
    modelo_final.rds
    scorecard.rds
    metadata_modelo.rds
    CHANGELOG.md
  v2/
    ...
```

`CHANGELOG.md` mínimo:
```markdown
# v1 — AAAA-MM-DD
- Variables: [lista]
- Gini test: X% | AUC: 0.XXX | KS: X%
- Motivo: modelo baseline inicial
```

---

## Governance: `model_registry.csv`

Las columnas canónicas de `governance/model_registry.csv` y el ciclo de vida de `status` (`desarrollo` → `validación` → `producción` → `deprecado`) están definidos en `references/credit-scoring.md`.

---

## Validación independiente (segunda línea)

Quien valida no puede ser quien desarrolló. Trabajando solo, la versión práctica:

1. `/code-review ultra` sobre el pipeline completo.
2. Una sesión de Claude **nueva** con rol de validador adversarial: lee solo `specs/`, `EDA/` y `modelos/` — sin el historial del desarrollo — y responde:
   - ¿La definición de target está justificada con evidencia (roll rates, vintage)?
   - ¿Hay leakage? ¿La integridad temporal se puede verificar desde los logs?
   - ¿El champion supera al baseline con significancia estadística?
   - ¿Las métricas OOT sostienen las conclusiones del informe?
   - ¿El pipeline corre desde cero con `renv::restore()`?
3. Cada hallazgo se resuelve o se acepta por escrito en el decision log — no se ignora.

---

## Checklist de entrega al cliente

**Pipeline y calidad:**

- [ ] `00_run_pipeline.R` corre de punta a punta sin intervención manual
- [ ] Todos los quality gates pasan
- [ ] `/code-review ultra` ejecutado y validación independiente con hallazgos resueltos
- [ ] Test de paridad dev-prod ejecutado (ver `references/credit-scoring.md`)

**Documentación y governance:**

- [ ] `CONTEXT.md` / decision log refleja todas las decisiones con quién las tomó
- [ ] `governance/model_registry.csv` actualizado
- [ ] `EDA/data_audit.md` y registro de riesgos del premortem incluidos como anexos

**Paquete de handover:**

- [ ] MDD (Model Development Document): metodología, decisiones, resultados y limitaciones en documento formal
- [ ] Diccionario de variables del modelo: definición, fuente, tratamiento aplicado
- [ ] Manual de uso del score: master scale, cutoffs, política de excepciones
- [ ] Runbook de monitoreo: qué se corre, con qué frecuencia, umbrales y acción/responsable por umbral
- [ ] `reportes/informe_*.html` generado y revisado

**Cierre:**

- [ ] Commit final con tag de versión: `git tag v1.0`

---

## Errores comunes a evitar

| Error | Corrección |
|---|---|
| Escribir código antes de tener la spec | Siempre spec primero, aunque sea pequeña |
| Calcular WOE sobre toda la población antes de splitear | Split primero, WOE solo en train |
| Breaks de bins que generan NAs en test | Usar `-Inf`/`Inf` en extremos de los breaks |
| Hardcodear parámetros en los scripts | Todo en `00_config.R` |
| Scripts que fallan silenciosamente | Quality gates con `stop()` explícito |
| Documentar el "qué" en lugar del "por qué" | CONTEXT.md es para decisiones, no para describir el código |
| Correr `/improve-codebase-architecture` en el medio del desarrollo | Solo al final |

---

## Inicio rápido en un proyecto nuevo

```bash
# 1. crear carpeta y git
mkdir nombre_proyecto && cd nombre_proyecto && git init

# 2. estructura
mkdir -p specs scripts datos/raw datos/processed EDA modelos/v1 \
         reportes informe governance graficos logs

# 3. copiar datos a datos/raw/ (nunca modificar)

# 4. en Claude Code:
#    - declarar ponytail activo
#    - /setup-matt-pocock-skills
#    - crear CLAUDE.md y CONTEXT.md
#    - crear scripts/00_config.R

# 5. definir alcance: /to-prd → /grill-with-docs → commit specs/00_proyecto.md

# 6. por cada etapa: /to-prd → /grill-with-docs → código → /code-review → commit

# 7. al finalizar: /code-review ultra → /improve-codebase-architecture → /graphify
```

---

## Referencia rápida de skills por momento

| Momento | Skills | Nota |
|---|---|---|
| Inicio del proyecto (una vez) | `/setup-matt-pocock-skills` + leer `references/credit-scoring.md` | Configura el repo; la referencia define estructura, specs y gates |
| Definición de alcance (una vez) | `/to-prd` → `/grill-with-docs` → `/premortem` | Ver "Flujo completo por etapa", paso 0 |
| Antes de cada etapa | `/to-prd` → `/grill-with-docs` | Spec borrador, cuestionada antes del código |
| Al modelizar | `references/credit-scoring.md` + `/advanced-analytics` | La referencia da la técnica Siddiqi; advanced-analytics exige traducción de negocio de cada métrica |
| Después de cada script | `/code-review` | Obligatorio antes del commit del script |
| Proyecto con equipo / cliente | `/to-issues` | Solo si hay equipo o el cliente quiere visibilidad del backlog |
| Pipeline completo (una vez) | `/code-review ultra` → `/improve-codebase-architecture` → `/graphify` | improve-codebase solo cuando todos los scripts funcionan; graphify útil con ≥ 3 scripts relacionados y al retomar u onboardear |
| Cerrar sesión / transferir trabajo | `/handoff "próximo objetivo"` | Compacta la sesión en un documento de transferencia |
| Retomar proyecto pausado | `graphify query "<pregunta>"` | |
| Funciones reutilizables | `/tdd` | Solo para `mis_funciones.R`; los `stop()` de los scripts ya son TDD implícita |
| Modo de trabajo permanente | `ponytail` (full) | No es skill invocable: se declara al inicio de sesión; marcar simplificaciones con `# ponytail: <razón>` |
