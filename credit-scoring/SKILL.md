---
name: credit-scoring
description: Skill para desarrollar, auditar, refactorizar, validar, monitorear o documentar proyectos de credit scoring con metodología tipo Naeem Siddiqi. Utilizar cuando se trabaje con definición de target, integración de datos, feature engineering, WOE/IV, scorecards, regresión logística, validación OOT, PSI, monitoreo, strategy tables, governance, modelos .rds e informes ejecutivos para negocio o riesgo.
---

# Credit Scoring R Siddiqi

Utilizar esta skill para proyectos de credit scoring de punta a punta, desde la ingesta de datos crudos hasta la construcción de scorecards, validación, monitoreo e informes finales para cliente o áreas de riesgo.

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
|   |-- 00_config.R
|   |-- 00_run_pipeline.R
|   |-- 01_ingesta_y_target.R
|   |-- 02_integracion_datos.R
|   |-- 03_limpieza_y_features.R
|   |-- 04_modelizacion.R
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

## Flujo obligatorio

```
1. Completar specs/<etapa>.md        ← ANTES de escribir código
2. Confirmar con el usuario si hay decisiones metodológicas abiertas
3. Implementar el script             ← cumpliendo precondiciones y postcondiciones
4. Incluir quality gates como código ejecutable que falla explícitamente
```

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

## Quality Gate — falla si:
- Duplicados en id_cliente
- bad_rate fuera de [3%, 40%]
- Ventana de performance < 12 meses
- target con NA en población elegible

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

---

# Quality Gates

Antes de avanzar entre etapas, validar los controles correspondientes. Si algún control falla:

```r
stop("Quality Gate Failed: <descripción>")
```

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

## 6. Champion vs Challenger

Nunca evaluar un único modelo cuando sea posible. Comparar al menos:

* Logistic WOE.
* Logistic sin WOE.
* Árbol de decisión.
* Random Forest.
* XGBoost interpretable.

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

Registrar nuevas versiones, recalibraciones y reemplazos.

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
* Performance (train / validation / OOT).
* Strategy Tables y cutoffs recomendados.
* Calibración.
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
* Comparación de modelos (`model_comparison.csv`).
* Modelo champion y challengers (`.rds`).
* Scorecard (`scorecard.rds`, `scorecard_points.csv`).
* Strategy tables (`strategy_tables.csv`).
* Validación train / validation / OOT (`performance_summary.csv`).
* Calibración (`calibration_summary.csv`).
* PSI y monitoreo (`psi_summary.csv`, `monitoring_dashboard.csv`).
* Governance (`model_registry.csv`).
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
