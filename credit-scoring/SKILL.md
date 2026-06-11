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
