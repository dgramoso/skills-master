# Credit Scoring R Siddiqi

Guía técnica de la skill metodologia-credit-scoring. Utilizar para proyectos de credit scoring de punta a punta, desde la ingesta de datos crudos hasta la construcción de scorecards, validación, monitoreo e informes finales para cliente o áreas de riesgo.

Priorizar:

* Interpretabilidad.
* Trazabilidad.
* Reproducibilidad.
* Robustez estadística.
* Justificación de negocio.
* Cumplimiento regulatorio.
* Mantenibilidad en producción.

---

# Principios

* Mantener un pipeline modular y reproducible.
* Evitar leakage en todas las etapas.
* Preservar trazabilidad de cada transformación.
* Documentar todas las decisiones metodológicas.
* Favorecer modelos interpretables salvo indicación explícita.
* Todo output debe ser auditable: incluir conteos, tasas, fechas, criterios y checks.
* Ninguna métrica debe presentarse sin contexto de negocio.
* Todo modelo debe ser explicable para auditoría, validación independiente y áreas comerciales.
* Preservar convenciones existentes del proyecto. No cambiar librerías, estructuras o nomenclaturas sin necesidad.

---

# Estructura Recomendada

```text
credit_scoring/
|
|-- specs/
|   |-- 00_proyecto.md
|   |-- 01_ingesta_y_target.md
|   |-- 02_integracion_datos.md
|   |-- 03_limpieza_y_features.md
|   |-- 04_modelizacion.md
|   `-- 05_validacion_y_monitoreo.md
|
|-- scripts/
|   |-- 00_config.R o 00_config.py
|   |-- 00_run_pipeline.R o
|   |-- 01_ingesta_y_target.R o
|   |-- 02_integracion_datos.R o
|   |-- 03_limpieza_y_features.R o
|   |-- 04_modelizacion.R o
|   |-- 05_validacion_y_monitoreo.R 
|   |-- 06_informe.R
|   `-- mis_funciones.R
|
|-- datos/
|   |-- raw/
|   |-- processed/
|
|-- EDA/
|
|-- modelos/
|
|-- reportes/
|
|-- graficos/
|
|-- informe/
|
|-- governance/
|
`-- logs/
```

Si el proyecto ya posee una estructura consolidada, respetar nombres y convenciones existentes. Adaptar el flujo sin romper compatibilidad.

---

# Specs-Driven Development (SDD)

Antes de implementar cualquier script, crear y completar la spec correspondiente en `specs/`. El código existe para cumplir la spec — no al revés.

**El proceso SDD (qué skill invocar, en qué orden, con qué gates) lo define el SKILL.md de esta skill — no duplicarlo acá.** Esta referencia define los artefactos: el contenido de `specs/00_proyecto.md`, el template de spec por etapa y las specs pre-llenadas.

### `specs/00_proyecto.md` — output del alcance inicial

Generado en la Fase 0 (ver SKILL.md). Contiene:
- Objetivo del modelo y decisión de negocio que habilita
- Población elegible y exclusiones
- Fuentes de datos disponibles
- Definición preliminar de target
- Restricciones regulatorias o de negocio
- Qué queda fuera del alcance
- Preguntas abiertas que `/grill-with-docs` va a resolver

## Template de spec por etapa

```markdown
# Spec — <nombre_script>.R

## Objetivo
[Una oración que describa qué resuelve esta etapa]

## Precondiciones
- [Archivo o condición que debe existir antes de correr]
- [Columnas requeridas del input]

## Postcondiciones
- [Archivos que este script debe producir]
- [Columnas que deben estar presentes en el output]

## Quality Gate — falla si:
- [Condición 1]
- [Condición 2]

## Invariantes
- [Regla que nunca debe romperse, ej: no usar datos posteriores a periodo_obs]

## Decisiones metodológicas
- [Decisión tomada]: [justificación]

## Output esperado
| Archivo | Columnas clave | Filas esperadas |
|---|---|---|
| [nombre] | [columnas] | [estimado] |
```

## Specs pre-llenadas por etapa

### specs/01_ingesta_y_target.md

```markdown
# Spec — 01_ingesta_y_target.R

## Precondiciones
- datos/raw/ contiene el archivo de solicitudes o cartera
- Columnas mínimas: id_cliente, fecha_solicitud o fecha_obs, estado_cuenta

## Postcondiciones
- datos/processed/base_target.rds con columnas:
  id_cliente, target, bad, good, indeterminate,
  sample_flag, periodo_obs, periodo_perf
- EDA/auditoria_target.csv generado
- EDA/roll_rate_analysis.csv y EDA/vintage_analysis.csv generados
  (justificación empírica de la definición de default y la ventana)

## Quality Gate — falla si:
- Duplicados en id_cliente
- bad_rate fuera de [3%, 40%]
- Ventana de performance < 12 meses
- target con NA en población elegible
- Menos de ~2.000 malos en desarrollo sin advertencia documentada
  (regla Siddiqi: por debajo el scorecard es inestable)

## Invariantes
- No usar información posterior a periodo_obs
- Exclusiones documentadas con motivo explícito
```

### specs/02_integracion_datos.md

```markdown
# Spec — 02_integracion_datos.R

## Precondiciones
- datos/processed/base_target.rds existe y cumple su spec
- Fuentes externas disponibles con fecha de snapshot <= periodo_obs

## Postcondiciones
- datos/processed/base_integrada.rds
- EDA/integration_log.csv con cobertura y porcentaje de no-match

## Quality Gate — falla si:
- No-match supera umbral definido en 00_config.R
- Duplicados generados por el join
- Cualquier variable con fecha posterior a periodo_obs

## Invariantes
- Integridad temporal: nunca usar datos posteriores a periodo_obs
```

### specs/03_limpieza_y_features.md

```markdown
# Spec — 03_limpieza_y_features.R

## Precondiciones
- datos/processed/base_integrada.rds existe y cumple su spec

## Postcondiciones
- datos/processed/base_features.rds con candidate_variables
- EDA/exclusion_log.csv con variables descartadas y motivo
- EDA/binning_log.csv con WOE, IV y bad_rate por bin

## Quality Gate — falla si:
- Leakage detectado (variable con fecha > periodo_obs)
- Variable con missing > 80% en candidate_variables
- IV de alguna variable seleccionada < umbral definido

## Invariantes
- Toda exclusión debe tener motivo en exclusion_log
- Monotonicidad documentada si se rompe
```

### specs/04_modelizacion.md

```markdown
# Spec — 04_modelizacion.R

## Precondiciones
- datos/processed/base_features.rds existe y cumple su spec
- EDA/binning_log.csv y EDA/exclusion_log.csv generados

## Postcondiciones
- modelos/modelo_final.rds
- modelos/metadata_modelo.rds
- EDA/model_comparison.csv con champion y challengers
- EDA/performance_summary.csv con AUC, KS, Gini en train/val/OOT
- EDA/calibration_summary.csv

## Quality Gate — falla si:
- AUC < umbral definido en 00_config.R
- Signo de algún coeficiente contradice expectativa de negocio
- VIF > 10 en alguna variable del modelo final
- Convergencia no alcanzada
- Champion no supera al baseline con significancia (DeLong) y no está
  documentada la recomendación de no reemplazar el esquema vigente

## Invariantes
- Documentar trade-off performance vs interpretabilidad si aplica
- Champion seleccionado con justificación explícita
```

### specs/05_validacion_y_monitoreo.md

```markdown
# Spec — 05_validacion_y_monitoreo.R

## Precondiciones
- modelos/modelo_final.rds existe
- Datos de período posterior disponibles para PSI

## Postcondiciones
- EDA/psi_summary.csv
- EDA/top_drift_variables.csv
- EDA/monitoring_dashboard.csv
- governance/model_registry.csv actualizado

## Quality Gate — falla si:
- PSI de score >= 0.25 sin documentación de causa
- KS OOT cae más de 10 puntos respecto a desarrollo

## Invariantes
- PSI < 0.10: estable / 0.10-0.25: monitorear / >= 0.25: investigar
- Todo cambio de estado en model_registry debe tener fecha y responsable
```

---

# Flujo General

## 1. Configuración

Centralizar en `00_config.R`:

* Paths.
* Seeds (`set.seed()` explícito).
* Fechas de observación y performance.
* Definición de target.
* Parámetros de scorecard.
* Umbrales de calidad.
* Librerías.

El pipeline completo debe ejecutarse desde `00_run_pipeline.R`. Cada script debe poder correr de forma independiente después de cargar la configuración.

Ejemplo de contenido mínimo:

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

**Regla:** todo parámetro que puede cambiar entre proyectos vive en `00_config.R`. Los scripts no tienen valores hardcodeados.

---

# Quality Gates

Antes de avanzar entre etapas, validar los controles correspondientes. Si algún control falla:

```r
stop("Quality Gate Failed: <descripción>")
```

Patrón estándar:

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

## Gate: Ingesta

* Sin duplicados de clave principal.
* Target definido.
* Ventanas válidas.
* Tasa de malos razonable.

## Gate: Integración

* Cobertura de joins documentada.
* Porcentaje de no-match controlado.
* Integridad temporal verificada.

## Gate: Features

* Leakage = 0.
* Missing documentados.
* Variables finales identificadas.

## Gate: Modelización

* Convergencia verificada.
* Signos coherentes con expectativas de negocio.
* Performance mínima alcanzada.

---

## 2. Ingesta y Target

En `01_ingesta_y_target.R`.

Documentar:

* Población elegible.
* Exclusiones.
* Fecha de observación.
* Ventana de performance.
* Definición de default.
* Criterios regulatorios.

Crear variables:

```r
target
bad
good
indeterminate
sample_flag
periodo_obs
periodo_perf
```

Validar:

* Conteos por población.
* Bad rate.
* Duplicados.
* Consistencia temporal.
* Distribución de cohortes.

Generar:

```r
EDA/auditoria_target.csv
```

### Justificación empírica del target

La definición de default no se declara: se justifica con datos. Antes de fijarla:

* **Roll rate analysis**: matriz de transición entre buckets de mora (al día → 1-29 → 30-59 → 60-89 → 90+). La definición de malo se fija en el bucket desde el cual la mayoría de las cuentas no cura.
* **Vintage analysis**: curvas de bad rate acumulado por cohorte de originación. La ventana de performance se fija donde las curvas se aplanan.
* **Tamaño muestral**: regla Siddiqi de ~2.000 malos mínimo en desarrollo. Por debajo, documentar el riesgo de inestabilidad y considerar reducir el alcance (menos variables, sin segmentación).

Guardar:

```r
EDA/roll_rate_analysis.csv
EDA/vintage_analysis.csv
```

Es lo primero que revisa un validador independiente: si el target no está justificado empíricamente, el modelo no es defendible.

---

## 3. Integración de Datos

En `02_integracion_datos.R`.

Documentar:

* Fuentes.
* Fecha de snapshot.
* Claves de join.
* Reglas de matching.

Validar:

* Cobertura y porcentaje de no-match.
* Duplicados generados por el join.
* Integridad temporal: nunca usar información posterior a la fecha de observación.

Generar:

```r
EDA/integration_log.csv
```

---

## 4. Limpieza y Feature Engineering

En `03_limpieza_y_features.R`.

Realizar:

* Estandarización de tipos, unidades y categorías.
* Imputación documentada.
* Tratamiento de outliers y valores especiales.
* Consolidación de categorías con bajo volumen.

Construir variables con sentido crediticio:

* Utilización.
* Endeudamiento.
* Capacidad de pago.
* Comportamiento reciente.
* Recencia, frecuencia, tendencias.
* Ratios y antigüedad.
* Concentración, consultas, saldos.
* Mora histórica.

Mantener y guardar:

```r
candidate_variables   # variables que entran al análisis
excluded_variables    # variables descartadas con motivo
```

---

## 5. WOE, IV y Binning

Construir bins:

* Interpretables.
* Estables.
* Con volumen suficiente.

Aplicar monotonicidad cuando tenga sentido crediticio (utilización ↑ ⇒ riesgo ↑, mora ↑ ⇒ riesgo ↑). Si se rompe monotonicidad, documentar el motivo explícitamente.

Calcular WOE, IV y Bad Rate por bin.

Guardar:

```r
EDA/binning_log.csv
```

Columnas:

```text
variable | bin_id | lower | upper | woe | iv | n_obs | bad_rate | decision_note
```

---

### Exclusion Log

Documentar todas las variables excluidas en:

```r
EDA/exclusion_log.csv
```

Columnas:

```text
variable | reason | iv | stability_metric | correlation | business_justification
```

Motivos típicos:

* Leakage.
* IV bajo.
* Inestabilidad.
* Correlación alta con otra variable seleccionada.
* No operable en producción.
* Sin justificación de negocio.

---

## Segmentación de Scorecards

Antes de modelizar, decidir explícitamente si conviene un scorecard único o varios (ej: con/sin historial en buró, cliente nuevo/conocido, persona física/jurídica).

Criterio de decisión:

* Segmentar solo si hay interacciones fuertes (la misma variable predice distinto por segmento) o poblaciones estructuralmente distintas (thin files vs thick files).
* La segmentación se justifica si el uplift de performance supera el costo de desarrollar, validar y mantener N modelos.
* Cada segmento debe conservar volumen suficiente (~2.000 malos por scorecard).

Documentar la decisión — segmentar o no — con evidencia en:

```r
EDA/segmentation_analysis.csv
```

---

## 6. Champion vs Challenger

Nunca evaluar un único modelo cuando sea posible. Comparar al menos:

* **Baseline obligatorio**: el esquema vigente del cliente — modelo anterior, score de buró o regla simple (ej: peor calificación). El modelo nunca se evalúa en el vacío.
* Logistic WOE.
* Logistic sin WOE.
* Árbol de decisión.
* Random Forest.
* XGBoost interpretable.

Regla de decisión: si el champion no supera al baseline por un margen material y estadísticamente significativo (test de DeLong), la recomendación honesta es no reemplazar el esquema vigente. Documentarlo como hallazgo, no ocultarlo.

Seleccionar el champion considerando:

* Performance (AUC, KS, Gini).
* Interpretabilidad para negocio y auditoría.
* Estabilidad temporal.
* Gobernanza y cumplimiento regulatorio.

Guardar:

```r
EDA/model_comparison.csv
```

---

## 7. Reject Inference

Cuando se trate de originación, documentar:

* Volumen de aprobados, rechazados y tasa de aceptación.

Evaluar los enfoques disponibles:

* Parceling.
* Reweighting.
* Fuzzy Augmentation.

Si no se realiza reject inference, documentar explícitamente las limitaciones y el sesgo potencial.

---

## 8. Modelización

En `04_modelizacion.R`.

Si el proyecto ya usa una función específica (`glm`, `rms::lrm`, `scorecard::lr_model`), usarla para preservar convenciones. Si no existe convención, usar por defecto:

```r
rms::lrm()
```

Validar:

* Signo esperado por variable.
* Significancia estadística.
* Colinealidad y VIF.
* Estabilidad de coeficientes.

Guardar:

```r
modelos/modelo_final.rds
modelos/metadata_modelo.rds
```

---

### Validaciones Mínimas

Calcular en train, validation y OOT:

* AUC / Gini.
* KS.
* Lift y Gain.
* Deciles de score.
* Odds por banda.

Rigor estadístico:

* Intervalos de confianza bootstrap (95%) para AUC, KS y Gini — nunca reportar métricas puntuales sin IC.
* Test de DeLong para comparar AUC entre champion, challengers y baseline: "0.74 > 0.72" no es evidencia sin significancia.
* Si los IC del champion y del baseline se solapan, decirlo explícitamente en el informe.

Guardar:

```r
EDA/performance_summary.csv
```

---

### Calibración

Además de discriminación, calcular:

* Calibration Curve.
* Brier Score.
* Test de Hosmer-Lemeshow.
* Predicted vs Observed Bad Rate por banda.
* Ajuste a central tendency: alinear la PD promedio del modelo con la tasa de malos de largo plazo del portafolio, no solo con la de la muestra de desarrollo (que puede ser un punto atípico del ciclo). Documentar el ajuste si se aplica.

Guardar:

```r
EDA/calibration_summary.csv
```

---

## 9. Scorecard

Cuando corresponda generar scorecard, documentar:

* PDO (Points to Double the Odds).
* Base Score.
* Base Odds.
* Factor.
* Offset.

Guardar:

```r
EDA/scorecard_points.csv
```

Columnas:

```text
variable | bin | woe | points
```

Guardar también:

```r
modelos/scorecard.rds
```

### Master Scale

Mapear el score a bandas de rating operables:

```text
banda | score_min | score_max | pd_media | odds | n_obs | uso_sugerido
```

Es como el cliente opera el modelo: las decisiones de crédito, pricing y provisiones se toman por banda, no por punto de score.

Guardar:

```r
EDA/master_scale.csv
```

---

## 10. Strategy Tables

Generar automáticamente tablas con:

* Banda de score.
* Volumen y porcentaje.
* Bad rate.
* Approval rate / Rejection rate.
* Odds.
* Expected loss.
* Acumulados.

Evaluar múltiples cutoffs e identificar perfiles:

* Conservador.
* Comercial.
* Agresivo.

Mostrar trade-offs explícitamente.

Guardar:

```r
EDA/strategy_tables.csv
```

### Swap Set Analysis

Cuando existe un esquema vigente (modelo anterior, score de buró o regla), cuantificar quiénes cambian de decisión:

* **Swap-in**: rechazados por el esquema vigente que el modelo nuevo aprueba — estimar su bad rate.
* **Swap-out**: aprobados por el esquema vigente que el modelo nuevo rechaza — estimar la pérdida evitada.
* **Neto en unidades monetarias**: volumen adicional aprobado × margen − pérdida incremental.

Guardar:

```r
EDA/swap_set_analysis.csv
```

### Cutoff económico

El cutoff óptimo no se elige solo por bad rate: incorporar ganancia esperada por buen cliente y pérdida esperada por malo (LGD × EAD, o la aproximación disponible). Reportar:

* El cutoff que maximiza beneficio neto, junto a los perfiles conservador / comercial / agresivo.
* El uplift del modelo en unidades monetarias: "X puntos de Gini equivalen a $Y menos de pérdida anual a la misma tasa de aprobación".

Si el cliente no provee datos económicos, usar supuestos explícitos y documentarlos como tales — un supuesto declarado es defendible, uno implícito no.

---

## Fair Lending y Reason Codes

### Variables prohibidas y proxies

Mantener lista explícita de variables prohibidas por regulación o política (género, edad, estado civil, nacionalidad — según jurisdicción) y de sus proxies potenciales (geografía como proxy socioeconómico, tipo de ocupación). Si un proxy entra al modelo, documentar la justificación de negocio y el riesgo asumido.

### Impacto dispar

Test básico: comparar approval rate y score medio entre los grupos protegidos observables. Diferencias materiales sin justificación de negocio son un hallazgo a reportar, no a silenciar.

### Reason codes (adverse action)

Para cada solicitante rechazado, generar las 3-4 variables que más puntos le restaron respecto al máximo posible del scorecard. Es requisito regulatorio en mercados desarrollados y buena práctica en todos.

Guardar:

```r
EDA/fairness_summary.csv
EDA/reason_codes.csv
```

---

## 11. Validación OOT

Si existen períodos suficientes, separar:

```text
Development / Validation / OOT
```

Si no existe OOT: documentarlo explícitamente, ejecutar K-Fold Cross Validation como control alternativo, e indicar "OOT pendiente" en el informe.

---

## 12. PSI y Monitoreo

En `05_validacion_y_monitoreo.R`.

Calcular:

* PSI de score.
* PSI por variable relevante.
* Drift de población.
* Drift de target.
* Drift por bandas de score.

Interpretación estándar:

```text
PSI < 0.10          → Estable
0.10 <= PSI < 0.25  → Monitorear
PSI >= 0.25         → Investigar / considerar recalibración
```

Generar:

```r
EDA/psi_summary.csv
EDA/top_drift_variables.csv
```

---

## 13. Monitoreo Continuo

Preparar framework para seguimiento mensual de:

* PSI de score.
* KS.
* Bad Rate por cohorte.
* Calibración.

Generar:

```r
EDA/monitoring_dashboard.csv
```

### Test de paridad dev-prod

Antes de dar por implementado el modelo: scorear una muestra idéntica en desarrollo y en producción y verificar coincidencia exacta (o desvío menor a una tolerancia definida). Un scorecard mal transcripto es el modo de falla de implementación más común.

Guardar:

```r
EDA/score_parity_test.csv
```

### Triggers de acción

Cada umbral de monitoreo tiene acción y responsable definidos, no solo color:

| Señal | Acción | Decide |
|---|---|---|
| PSI de score >= 0.25 | Investigar causa en 30 días; si es estructural, recalibrar | Model owner |
| KS cae > 10 puntos vs desarrollo | Revisión completa del modelo | Model owner + negocio |
| Bad rate por banda fuera del rango predicho 3 meses seguidos | Revisar calibración y cutoffs | Negocio |

---

## 14. Model Governance

Mantener registro en:

```r
governance/model_registry.csv
```

Columnas:

```text
model_name | version | build_date | developer | business_owner | target_definition |
population | variables_finales | auc | ks | oot_auc | oot_ks | deployment_date | status
```

Ciclo de vida de `status`: `desarrollo` → `validación` → `producción` → `deprecado`.

Registrar nuevas versiones, recalibraciones y reemplazos.

### Marco regulatorio según uso del modelo

Identificar el uso al inicio del proyecto y documentarlo en `specs/00_proyecto.md` — el mismo modelo requiere gobernanza distinta según para qué se use:

| Uso del modelo | Marco de referencia | Implicancia principal |
|---|---|---|
| Originación / decisión de crédito | Model Risk Management (tipo SR 11-7) | Validación independiente, inventario de modelos, documentación completa |
| Provisiones contables | IFRS 9 (ECL) | PD 12 meses vs lifetime, staging, componente forward-looking |
| Capital regulatorio (bancos) | Basilea II/III | Definición de default regulatoria, márgenes de conservadurismo |

---

## 15. Informe Cliente

En `06_informe.R`.

Generar informe HTML ejecutivo con diseño:

* Minimalista, estilo macOS / suizo.
* Amplio espacio en blanco.
* Tipografía del sistema:

```css
-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif
```

* SF Mono o equivalente para tablas y datos numéricos.
* Colores neutros, contrastes suaves. Evitar colores brillantes o fondos oscuros.

---

### Contenido Ejecutivo

Incluir:

* Objetivo y contexto.
* Datos utilizados y población.
* Definición de target.
* Metodología.
* Variables relevantes y drivers.
* Performance (train / validation / OOT) con intervalos de confianza.
* Benchmark contra el esquema vigente y uplift económico (swap set).
* Strategy Tables, cutoff económico y cutoffs recomendados.
* Calibración y master scale.
* Fair lending y reason codes (si aplica).
* Recomendaciones.
* Riesgos metodológicos.
* Próximos pasos y monitoreo.

---

### Separación Ejecutivo / Técnico

* **Sección ejecutiva**: para negocio y alta dirección. Foco en insights, estrategia y recomendaciones.
* **Anexos técnicos**: para riesgo, auditoría y validación independiente. Incluye binning, exclusion log, coeficientes, PSI, calibración y governance.

---

### Gráficos

Estilo BBC / The Economist:

* Minimalistas.
* Etiquetas claras.
* Sin gridlines innecesarios.
* Foco en storytelling e interpretación.

Evitar colores estridentes o decoraciones que distraigan del mensaje.

---

# Funciones Compartidas

Usar `mis_funciones.R` para helpers reutilizables:

* Lectura/escritura segura.
* Auditorías de tablas.
* Cálculo de WOE/IV.
* KS, AUC, Gini, Lift.
* PSI.
* Strategy Tables.
* Scorecard.
* Exportaciones.
* Interpretaciones automáticas vía Claude API (`llamar_claude()`).

### `llamar_claude()` — interpretación automática en el informe

Incluir en `mis_funciones.R` para generar narrativa dinámica en `06_informe.R`:

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

Secciones a generar automáticamente en el informe:
- **Performance**: interpretación del Gini/AUC/KS en función de las variables reales
- **Calibración**: si el modelo está bien calibrado y dónde hay mayor desvío
- **PSI**: estabilidad e implicancias para producción
- **Recomendaciones**: cutoffs, mejoras y monitoreo con los números reales del modelo

La función devuelve `""` si no hay API key, sin romper el pipeline. Configurar `ANTHROPIC_API_KEY` en `.Renviron` para que cargue automáticamente en cada sesión de R.

**Importante:** Antes de generar código que use `source("mis_funciones.R")`, confirmar que el archivo existe. Si no existe, incluir la función inline con una nota o solicitar su creación previa. No duplicar lógica entre scripts si puede vivir como función clara y testeable.

---

# Entregables Esperados

Al finalizar, producir o dejar preparado:

* Pipeline reproducible (`00_run_pipeline.R`).
* Auditorías y logs (`auditoria_target`, `integration_log`, `binning_log`, `exclusion_log`).
* Justificación empírica del target (`roll_rate_analysis.csv`, `vintage_analysis.csv`).
* Decisión de segmentación con evidencia (`segmentation_analysis.csv`).
* Comparación de modelos contra baseline (`model_comparison.csv`).
* Modelo champion y challengers (`.rds`).
* Scorecard (`scorecard.rds`, `scorecard_points.csv`) y master scale (`master_scale.csv`).
* Strategy tables, swap set y cutoff económico (`strategy_tables.csv`, `swap_set_analysis.csv`).
* Validación train / validation / OOT con IC bootstrap (`performance_summary.csv`).
* Calibración (`calibration_summary.csv`).
* Fair lending y reason codes (`fairness_summary.csv`, `reason_codes.csv`).
* PSI y monitoreo (`psi_summary.csv`, `monitoring_dashboard.csv`).
* Test de paridad dev-prod (`score_parity_test.csv`).
* Governance (`model_registry.csv`) con marco regulatorio identificado.
* Informe HTML ejecutivo con anexos técnicos.

---

# Estilo de Respuesta

* Responder en el idioma del usuario.
* Mantener tono técnico y orientado a negocio.
* Preservar convenciones existentes del proyecto.
* No cambiar librerías, estructuras o nomenclaturas sin necesidad explícita.
* Explicar claramente riesgos metodológicos: leakage, mala definición de target, baja estabilidad, sobreajuste, variables no operables.
* Cuando exista conflicto entre performance y explicabilidad, documentar explícitamente el trade-off y justificar la decisión.
* Todo resultado debe poder ser defendido frente a negocio, auditoría, validación independiente y regulador.
