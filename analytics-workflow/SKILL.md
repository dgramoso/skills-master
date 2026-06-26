# Analytics Workflow: SDD + Ponytail + Skills

Metodología de trabajo para proyectos de analítica con Claude Code: carga de datos, ingeniería de atributos, modelización, validación y deployment. Aplica a cualquier proyecto predictivo (credit scoring, churn, fraude, segmentación, dashboards).

Prioridades permanentes:
- **Trazabilidad**: toda decisión metodológica queda documentada.
- **Reproducibilidad**: el pipeline corre de punta a punta sin intervención manual.
- **Interpretabilidad**: los resultados pueden ser explicados a negocio, auditoría o regulador.
- **Mínimo código que funciona** (Ponytail): no construir para el futuro.

---

## Filosofía base

Tres principios en orden de prioridad:

1. **SDD (Specs-Driven Development)**: toda etapa empieza con una spec escrita y grillada antes del código. El código existe para cumplir la spec — no al revés.
2. **Ponytail**: mínimo código que funciona. El primer script que pasa los quality gates es el correcto.
3. **Claude como pair programmer**: Claude implementa. Las decisiones de negocio y metodológicas son del analista.

---

## Estructura de carpetas (estándar)

```
nombre_proyecto/
├── CLAUDE.md              ← contexto del proyecto para Claude (leer cada sesión)
├── CONTEXT.md             ← dominio, variables, glosario, decisiones tomadas
├── METODOLOGIA_<tipo>.md  ← referencia metodológica específica del proyecto
│
├── specs/                 ← una spec por etapa, ANTES de escribir código
│   ├── 01_ingesta.md
│   ├── 02_features.md
│   ├── 03_modelizacion.md
│   ├── 04_validacion.md
│   └── 05_informe.md
│
├── scripts/
│   ├── 00_config.r        ← paths, seeds, umbrales, parámetros centralizados
│   ├── 00_run_pipeline.r  ← ejecuta todo en orden con un solo comando
│   ├── mis_funciones.r    ← funciones compartidas entre scripts
│   └── 01_...05_...r
│
├── datos/
│   ├── raw/               ← datos originales, NUNCA modificar
│   └── processed/         ← outputs de scripts (.rds / .parquet / .csv)
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

## Skills y cuándo invocarlas

### Orden en un proyecto típico

```
Inicio del proyecto:
  /setup-matt-pocock-skills   ← una sola vez, configura el repo

Por cada etapa del pipeline:
  1. /to-prd                  ← convierte descripción en spec borrador
  2. /grill-with-docs         ← cuestiona la spec antes del código
  3. (opcional) /to-issues    ← genera backlog si el proyecto dura semanas
  4. código                   ← Claude implementa siguiendo la spec
  5. /code-review             ← revisa el script antes de avanzar

Al modelizar:
  /credit-scoring             ← metodología Siddiqi (si es credit scoring)
  /advanced-analytics         ← enfoque de negocio e interpretación

Transversal:
  ponytail (activo permanente) ← se declara al inicio de sesión, no se invoca

Al finalizar el pipeline:
  /code-review ultra          ← revisión profunda multi-agente antes de entregar
  /improve-codebase-architecture ← detecta duplicaciones y refactoriza
  /graphify                   ← grafo del codebase para navegación
```

### Referencia de cada skill

**`/to-prd`** — convierte lenguaje natural en spec estructurada (objetivo, precondiciones, postcondiciones, quality gates, invariantes). Usar antes de cada etapa.

**`/grill-with-docs`** — lee la spec y el CONTEXT.md, hace preguntas críticas una por una, actualiza CONTEXT.md con las decisiones que emergen. Responder una pregunta a la vez. Nunca saltar al código sin grilear la spec.

**`/advanced-analytics`** — exige que cada resultado técnico tenga traducción práctica de negocio. Útil junto a `/credit-scoring` o como guía standalone para proyectos no-crediticios.

**`/credit-scoring`** — guía metodológica completa (Siddiqi): WOE/IV, binning, champion vs challengers, calibración, PSI, scorecard, strategy tables, governance. Solo para proyectos de credit scoring.

**`ponytail`** — modo de trabajo, no skill invocable. Se activa al inicio de sesión: "trabajemos con ponytail activo". Niveles: `full` (default), `lite`, `ultra`.

**`/improve-codebase-architecture`** — revisa el codebase completo al final. Detecta duplicaciones, funciones que deberían ir a `mis_funciones.r`, inconsistencias. Solo cuando todos los scripts están funcionando.

**`/code-review` / `/code-review ultra`** — `/code-review` después de cada script. `/code-review ultra` una sola vez antes de entregar al cliente.

**`/to-issues`** — convierte specs en issues de GitHub. Solo si hay equipo o el cliente quiere visibilidad del backlog.

**`/graphify`** — construye grafo de conocimiento del codebase. Invocar cuando hay ≥ 3 scripts relacionados. Útil al retomar proyectos o para onboarding.

**`/tdd`** — TDD formal solo para funciones reutilizables en `mis_funciones.r`. Los `stop()` en los scripts son TDD implícita.

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
```

---

## `00_config.r` — contenido mínimo

```r
# paths
PATH_RAW       <- "datos/raw/archivo.csv"
PATH_PROCESSED <- "datos/processed/"
PATH_EDA       <- "EDA/"
PATH_MODELOS   <- "modelos/"

# reproducibilidad
set.seed(42)

# definición de target (si aplica)
TARGET         <- "nombre_variable_target"
DEF_TARGET     <- "descripción de qué significa el evento positivo"

# umbrales de calidad (ajustar por proyecto)
MISSING_MAX    <- 0.80
AUC_MIN        <- 0.60

# variables categóricas y a descartar
VARS_CAT       <- c()
VARS_DESCARTAR <- c()

# parámetros de lectura
CSV_SEP <- ";"
CSV_DEC <- "."
```

**Regla:** todo parámetro que puede cambiar entre proyectos vive aquí. Los scripts no tienen valores hardcodeados.

---

## Interpretaciones automáticas vía Claude API

El script de informe puede llamar a Claude directamente para generar narrativa analítica
con los números reales de cada corrida, en lugar de textos hardcodeados.

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

### Secciones típicas a generar automáticamente en el informe

| Sección | Qué interpreta Claude |
|---|---|
| Performance | Métricas del modelo en función de variables reales y bad rate |
| Calibración | Si el modelo está bien calibrado y dónde hay mayor desvío |
| Estabilidad | PSI e implicancias para producción |
| Recomendaciones | Cutoffs, mejoras y monitoreo con números reales |

### Configuración

Agregar en `~/.Renviron` (carga automáticamente en toda sesión R):
```
ANTHROPIC_API_KEY=sk-ant-...
```

La función devuelve `""` si no hay API key, **sin romper el pipeline**.

---

## Quality Gates: patrón estándar

```r
# al inicio de cada script
stopifnot(
  "archivo input ausente" = file.exists(PATH_INPUT),
  "target ausente"        = TARGET %in% names(datos)
)

# validaciones de negocio
if (alguna_condicion_critica)
  stop("Quality Gate: descripción del problema")
```

**Regla:** el script debe fallar ruidosamente si algo está mal. Un script que termina sin error pero con datos incorrectos es peor que uno que falla.

---

## Reproducibilidad: renv

`set.seed()` garantiza reproducibilidad del muestreo pero no protege contra cambios de API de paquetes. `renv` fija las versiones exactas.

```r
install.packages("renv")
renv::init()        # al arrancar el proyecto
# ... instalar paquetes normalmente ...
renv::snapshot()    # después de cada cambio en dependencias
# al clonar / retomar:
renv::restore()
```

**Qué se commitea:** `renv.lock` sí. La carpeta `renv/library/` no (va a `.gitignore`).

Registrar la versión de R en `CONTEXT.md` (ej: R 4.5.1).

---

## CLAUDE.md — contenido mínimo por proyecto

```markdown
# CLAUDE.md — nombre_proyecto

## Contexto
[Una oración describiendo el proyecto. Ver CONTEXT.md para detalle.]

## Lenguaje
[R / Python / SQL + R / etc.]

## Metodología
SDD + Ponytail. Cada etapa tiene su spec en specs/. Arrancar siempre por la spec.

## Estructura de specs
- specs/01_... → [qué hace]
- specs/02_... → [qué hace]

## Ponytail
Activo (full). No construir abstracciones no pedidas.

## Agent skills
- Issue tracker: [GitHub Issues / local markdown]
- Context files: CONTEXT.md (dominio), specs/*.md (tareas activas)
```

---

## Versionado de modelos

Sin MLflow. Git + carpetas versionadas:

```
modelos/
  v1/
    modelo_final.rds
    metadata_modelo.rds
    CHANGELOG.md      ← fecha, variables, métricas clave, motivo del cambio
  v2/
    ...
```

`CHANGELOG.md` mínimo:
```markdown
# v1 — AAAA-MM-DD
- Variables: [lista]
- AUC test: 0.XXX | Gini: XX% | KS: XX%
- Motivo: modelo baseline inicial
```

---

## Governance: `model_registry.csv`

Un registro por modelo productivo:

```
model_name | version | build_date | developer | target_definition |
population | variables_finales | auc_train | auc_test | gini_test |
ks_test | deployment_date | status
```

`status`: `desarrollo` → `validación` → `producción` → `deprecado`.

---

## Definición de target y ventanas (para modelos predictivos)

Antes de modelar, documentar en `CONTEXT.md`:

| Decisión | Qué definir |
|---|---|
| Definición del evento | Qué condición define el positivo (ej: mora ≥ 30d, churn en 90d) |
| Ventana de observación | Fecha/período en que se "fotografía" al cliente (las variables) |
| Ventana de performance | Período posterior en que se observa el evento |
| Población elegible | Quién entra y quién se excluye, con motivo explícito |
| Indeterminados | Casos ambiguos: ¿se excluyen o se asignan? |

**Invariante crítico:** ninguna variable puede contener información posterior a la ventana de observación. Si una variable "ve el futuro", es leakage y el modelo no sirve en producción aunque el AUC sea alto.

---

## Checklist de entrega

- [ ] `00_run_pipeline.r` corre de punta a punta sin intervención manual
- [ ] Todos los quality gates pasan
- [ ] `CONTEXT.md` refleja todas las decisiones tomadas
- [ ] `governance/model_registry.csv` actualizado
- [ ] `/code-review ultra` ejecutado y hallazgos resueltos
- [ ] Informe HTML generado y revisado
- [ ] Commit final con tag: `git tag v1.0`

---

## Errores comunes

| Error | Corrección |
|---|---|
| Escribir código antes de tener la spec | Siempre spec primero |
| Calcular features sobre toda la población antes de splitear | Split primero, features solo en train |
| Breaks de bins que generan NAs en test | Usar `-Inf`/`Inf` en extremos de los breaks |
| Hardcodear parámetros en los scripts | Todo en `00_config.r` |
| Scripts que fallan silenciosamente | Quality gates con `stop()` explícito |
| Documentar el "qué" en lugar del "por qué" | CONTEXT.md es para decisiones, no para describir el código |
| Correr `/improve-codebase-architecture` en el medio del desarrollo | Solo al final |
| Mezclar cohortes sin analizar vintage | Analizar bad rate por cohorte antes de modelar |

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

# 5. por cada etapa: /to-prd → /grill-with-docs → código → /code-review → commit

# 6. al finalizar: /code-review ultra → /improve-codebase-architecture → /graphify
```

---

## Referencia rápida de skills por momento

| Momento | Skills |
|---|---|
| Inicio del proyecto | `/setup-matt-pocock-skills` |
| Antes de cada etapa | `/to-prd` |
| Después de la spec | `/grill-with-docs` |
| Al modelizar | `/credit-scoring` + `/advanced-analytics` |
| Después de cada script | `/code-review` |
| Proyecto con equipo | `/to-issues` |
| Pipeline completo | `/code-review ultra` → `/improve-codebase-architecture` → `/graphify` |
| Retomar proyecto pausado | `graphify query "<pregunta>"` |
| Funciones reutilizables | `/tdd` |
| Modo de trabajo permanente | `ponytail full` |
