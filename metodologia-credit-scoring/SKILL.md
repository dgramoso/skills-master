---
name: metodologia-credit-scoring
description: Metodología completa SDD + Ponytail + Skills para proyectos de credit scoring con Claude Code. Cubre flujo de trabajo, orden de skills, estructura de carpetas, specs, quality gates, reproducibilidad, governance e informe con interpretaciones automáticas vía Claude API. Invocar al inicio de cualquier proyecto de credit scoring o modelo predictivo.
---

# Metodología de Trabajo: SDD + Ponytail + Skills para Proyectos de Credit Scoring

**Aplicable a:** proyectos de analítica con Claude Code (credit scoring, modelos predictivos, dashboards)

---

## Filosofía base

Tres principios que se aplican siempre, en orden de prioridad:

1. **SDD (Specs-Driven Development)**: toda etapa empieza con una spec escrita y grillada. El código existe para cumplir la spec — no al revés.
2. **Ponytail**: mínimo código que funciona. No construir para el futuro. No abstracciones sin justificación. El primer script que pasa los quality gates es el correcto.
3. **Claude como pair programmer permanente**: Claude no reemplaza el juicio analítico, lo amplifica. Las decisiones de negocio y metodológicas son del analista. Claude implementa.

---

## Estructura de carpetas (estándar para todo proyecto)

```
nombre_proyecto/
├── CLAUDE.md              ← contexto del proyecto para Claude (leer en cada sesión)
├── CONTEXT.md             ← dominio, variables, glosario, decisiones tomadas
├── METODOLOGIA_credit_scoring.md
│
├── specs/                 ← una spec por etapa, ANTES de escribir código
│   ├── 00_proyecto.md     ← alcance validado con cliente
│   ├── 01_exploracion.md
│   ├── 02_feature_engineering.md
│   ├── 03_modelizacion.md
│   ├── 04_scorecard_validacion.md
│   └── 05_informe.md
│
├── scripts/
│   ├── 00_config.r        ← paths, seeds, umbrales, parámetros centralizados
│   ├── 00_run_pipeline.r  ← corre todo en orden
│   ├── mis_funciones.r    ← funciones compartidas (WOE, métricas, llamar_claude)
│   └── 01_...05_...r
│
├── datos/
│   ├── raw/               ← datos originales, nunca modificar
│   └── processed/         ← outputs de scripts (.rds)
│
├── EDA/                   ← todos los CSVs de auditoría y logs
├── modelos/               ← modelo_final.rds, scorecard.rds, metadata
│   └── v1/
├── reportes/              ← informe HTML para el cliente
├── governance/            ← model_registry.csv
├── graficos/
└── logs/
```

**Regla:** `datos/raw/` es inmutable. Nunca sobrescribir datos originales.

---

## Skills y orden de invocación

```
Inicio de proyecto:
  /setup-matt-pocock-skills   ← una sola vez, configura el repo

Definición de alcance (una sola vez, antes de cualquier spec):
  /to-prd                     ← dump libre del proyecto → genera specs/00_proyecto.md
  /grill-with-docs            ← cuestiona el alcance, actualiza CONTEXT.md con decisiones de negocio

Por cada etapa del pipeline:
  1. /to-prd                  ← convierte tu descripción en spec borrador
  2. /grill-with-docs         ← cuestiona la spec antes del código
  3. (opcional) /to-issues    ← genera backlog en GitHub si el proyecto dura semanas
  4. código                   ← Claude implementa siguiendo la spec
  5. /code-review             ← revisa el script antes de avanzar

Al modelizar:
  /credit-scoring             ← guía metodológica Siddiqi de punta a punta
  /advanced-analytics         ← complementa con enfoque de negocio

Transversal durante todo el proyecto:
  ponytail (activo por default) ← modo de trabajo, se declara al inicio de sesión

Al finalizar el pipeline:
  /code-review ultra           ← revisión profunda multi-agente antes de entregar al cliente
  /improve-codebase-architecture ← detecta duplicaciones y refactoriza
  /graphify                    ← genera grafo del codebase para navegación
```

---

## Referencia de cada skill

**`/to-prd`** — convierte descripción en lenguaje natural en spec estructurada (objetivo, precondiciones, postcondiciones, quality gates, invariantes). Usar antes de cada etapa y al inicio para definir alcance con el cliente.

**`/grill-with-docs`** — lee la spec y CONTEXT.md, hace preguntas críticas una por una, actualiza CONTEXT.md con las decisiones que emergen. Responder una pregunta a la vez. Nunca saltar al código sin grilear la spec. **Diferencia clave:** no actualiza specs, actualiza CONTEXT.md con conocimiento de dominio (el "por qué").

**`/credit-scoring`** — guía metodológica completa Siddiqi: WOE/IV, binning, champion vs challengers, calibración, PSI, scorecard, strategy tables, governance e informe.

**`/advanced-analytics`** — exige que cada resultado técnico tenga traducción práctica de negocio. Usar junto a `/credit-scoring`.

**`ponytail`** — modo de trabajo, no skill invocable. Activo durante toda la sesión. Marca el código deliberadamente simplificado con `# ponytail: <razón>`.

**`/improve-codebase-architecture`** — solo al final, cuando todos los scripts funcionan. Detecta duplicaciones y propone refactor.

**`/code-review` / `/code-review ultra`** — `/code-review` después de cada script. `/code-review ultra` una sola vez antes de entregar.

**`/to-issues`** — solo si hay equipo o el cliente quiere visibilidad del backlog.

**`/graphify`** — cuando hay ≥ 3 scripts relacionados. Útil al retomar proyectos o para onboarding.

**`/tdd`** — solo para funciones reutilizables en `mis_funciones.r`. Los `stop()` en los scripts ya son TDD implícita.

---

## Definición de target y ventanas

El error más caro en credit scoring no está en el código — está en cómo se define a quién se predice y sobre qué período. Documentar en `CONTEXT.md` **antes** de la spec 01.

| Decisión | Qué definir | Dónde se documenta |
|---|---|---|
| Definición de malo | Días de mora y severidad (ej: mora ≥ 30, ≥ 90, default Basilea) | `CONTEXT.md` + `DEF_DEFAULT` en `00_config.r` |
| Ventana de observación | Fecha/período en que se "fotografía" al cliente | `CONTEXT.md` |
| Ventana de performance | Período posterior en que se observa si cae en mora (típico 12 meses) | `CONTEXT.md` |
| Población elegible | Quién entra y quién se excluye, con motivo explícito | `CONTEXT.md` + `exclusion_log` |
| Indeterminados | Clientes ni claramente buenos ni malos: ¿se excluyen o se asignan? | `CONTEXT.md` |

**Invariante crítico:** ninguna variable puede contener información posterior a la ventana de observación. Si una variable "ve el futuro", es leakage y el modelo no sirve en producción aunque el AUC sea alto.

**Vintage / cohortes:** si hay datos de varios períodos, analizar la tasa de malo por cohorte antes de mezclar todo.

> Estas cinco decisiones son las que un validador independiente o auditor revisa primero. Si no están documentadas con justificación, el modelo no es defendible.

---

## Template de spec (usar siempre)

```markdown
# Spec — nombre_script.r

## Objetivo
[Una oración que describa qué resuelve esta etapa]

## Precondiciones
- [Archivo que debe existir antes de correr]
- [Columnas o condiciones requeridas del input]

## Postcondiciones
- [Archivos que este script debe producir]
- [Columnas que deben estar presentes en el output]

## Quality Gates — falla con stop() si:
- [Condición 1]
- [Condición 2]

## Invariantes
- [Regla que nunca debe romperse]

## Decisiones metodológicas
- [Decisión]: [justificación]

## Output esperado
| Archivo | Columnas clave | Filas esperadas |
|---|---|---|
| EDA/nombre.csv | col1, col2 | estimado |
```

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
   → commit: "spec: 00_proyecto — alcance validado"

Para cada etapa del pipeline:

1. /to-prd
   → describís la etapa en lenguaje natural
   → Claude genera spec borrador

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

5. /code-review (opcional por etapa)
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

## `00_config.r` — qué debe contener siempre

```r
# paths
PATH_RAW       <- "datos/raw/archivo.csv"
PATH_PROCESSED <- "datos/processed/"
PATH_EDA       <- "EDA/"
PATH_MODELOS   <- "modelos/"

# reproducibilidad
set.seed(42)

# definición de target
TARGET         <- "nombre_variable_target"
DEF_DEFAULT    <- "descripción de la definición de malo"

# umbrales de calidad
BAD_RATE_MIN   <- 0.03
BAD_RATE_MAX   <- 0.40
MISSING_MAX    <- 0.80
IV_MIN         <- 0.02
AUC_MIN        <- 0.60

# variables categóricas y a descartar
VARS_CAT       <- c("var1", "var2")
VARS_DESCARTAR <- c("var_sin_variabilidad")

# parámetros de lectura
CSV_SEP <- ";"
CSV_DEC <- "."
```

**Regla:** todo parámetro que puede cambiar entre proyectos vive en `00_config.r`. Los scripts no tienen valores hardcodeados.

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

El script de informe puede llamar a Claude directamente para generar narrativa analítica con los números reales de cada corrida.

### Función `llamar_claude()` en `mis_funciones.r`

```r
llamar_claude <- function(prompt, max_tokens = 400) {
  api_key <- Sys.getenv("ANTHROPIC_API_KEY")
  if (!nzchar(api_key)) {
    warning("ANTHROPIC_API_KEY no configurada — saltando interpretación automática")
    return("")
  }
  tryCatch({
    resp <- httr2::request("https://api.anthropic.com/v1/messages") |>
      httr2::req_headers(
        "x-api-key"         = api_key,
        "anthropic-version" = "2023-06-01",
        "content-type"      = "application/json"
      ) |>
      httr2::req_body_json(list(
        model      = "claude-haiku-4-5-20251001",
        max_tokens = max_tokens,
        messages   = list(list(role = "user", content = prompt))
      )) |>
      httr2::req_perform() |>
      httr2::resp_body_json()
    resp$content[[1]]$text
  }, error = function(e) {
    warning("Error llamando a Claude API: ", e$message)
    ""
  })
}
```

### Secciones a generar automáticamente en `05_informe.r`

| Sección | Qué interpreta Claude |
|---|---|
| Performance | Gini/AUC/KS en función de variables reales y bad rate |
| Calibración | Si el modelo está bien calibrado y dónde hay mayor desvío |
| PSI | Estabilidad e implicancias para producción |
| Recomendaciones | Cutoffs, mejoras y monitoreo con números reales del modelo |

### Configuración

Agregar en `~/.Renviron`:
```
ANTHROPIC_API_KEY=sk-ant-...
```

La función devuelve `""` si no hay API key, sin romper el pipeline.

---

## Quality Gates: patrón estándar

```r
stopifnot(
  "archivo input ausente" = file.exists(PATH_INPUT),
  "target ausente"        = TARGET %in% names(datos)
)

bad_rate <- mean(datos[[TARGET]])
if (bad_rate < BAD_RATE_MIN || bad_rate > BAD_RATE_MAX)
  stop(sprintf("Quality Gate: bad rate %.1f%% fuera del rango esperado", bad_rate * 100))
```

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

```
model_name | version | build_date | developer | target_definition |
population | variables_finales | auc_train | auc_test | gini_test |
ks_test | pdo | base_score | base_odds | deployment_date | status
```

`status`: `desarrollo` → `validación` → `producción` → `deprecado`.

---

## Checklist de entrega al cliente

- [ ] `00_run_pipeline.r` corre de punta a punta sin intervención manual
- [ ] Todos los quality gates pasan
- [ ] `CONTEXT.md` refleja todas las decisiones tomadas
- [ ] `governance/model_registry.csv` actualizado
- [ ] `/code-review ultra` ejecutado y hallazgos resueltos
- [ ] `reportes/informe_*.html` generado y revisado
- [ ] Commit final con tag de versión: `git tag v1.0`

---

## Errores comunes a evitar

| Error | Corrección |
|---|---|
| Escribir código antes de tener la spec | Siempre spec primero, aunque sea pequeña |
| Calcular WOE sobre toda la población antes de splitear | Split primero, WOE solo en train |
| Breaks de bins que generan NAs en test | Usar `-Inf`/`Inf` en extremos de los breaks |
| Hardcodear parámetros en los scripts | Todo en `00_config.r` |
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
         reportes governance graficos logs

# 3. copiar datos a datos/raw/ (nunca modificar)

# 4. en Claude Code:
#    - declarar ponytail activo
#    - /setup-matt-pocock-skills
#    - crear CLAUDE.md y CONTEXT.md
#    - crear scripts/00_config.r

# 5. definir alcance: /to-prd → /grill-with-docs → commit specs/00_proyecto.md

# 6. por cada etapa: /to-prd → /grill-with-docs → código → /code-review → commit

# 7. al finalizar: /code-review ultra → /improve-codebase-architecture → /graphify
```

---

## Referencia rápida de skills por momento

| Momento | Skills |
|---|---|
| Inicio del proyecto | `/setup-matt-pocock-skills` |
| Definición de alcance | `/to-prd` → `/grill-with-docs` |
| Antes de cada etapa | `/to-prd` |
| Después de la spec | `/grill-with-docs` |
| Al modelizar | `/credit-scoring` + `/advanced-analytics` |
| Después de cada script | `/code-review` |
| Proyecto con equipo / cliente | `/to-issues` |
| Pipeline completo | `/code-review ultra` → `/improve-codebase-architecture` → `/graphify` |
| Cerrar sesión / transferir trabajo | `/handoff` o `/handoff "próximo objetivo"` |
| Retomar proyecto pausado | `graphify query "<pregunta>"` |
| Funciones reutilizables | `/tdd` |
| Modo de trabajo permanente | `ponytail full` |
