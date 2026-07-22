# Principios y estructura

> Parte de la skill `metodologia-credit-scoring`. Ver `SKILL.md` para el flujo general. Estructura de carpetas, `00_config` y reproducibilidad genéricos: ver `analytics-workflow/references/reproducibilidad.md`. Esta referencia agrega solo lo específico de credit scoring.

---

## Prioridades

* Interpretabilidad.
* Trazabilidad.
* Reproducibilidad.
* Robustez estadística.
* Justificación de negocio.
* Cumplimiento regulatorio.
* Mantenibilidad en producción.

## Principios

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

## Estructura recomendada

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
|   |-- 00_config.{r,py}
|   |-- 00_run_pipeline.{r,py}
|   |-- 01_ingesta_y_target.{r,py}
|   |-- 02_integracion_datos.{r,py}
|   |-- 03_limpieza_y_features.{r,py}
|   |-- 04_modelizacion.{r,py}
|   |-- 05_validacion_y_monitoreo.{r,py}
|   |-- 06_informe.{r,py}
|   `-- mis_funciones.r / utils.py
|
|-- datos/
|   |-- raw/
|   `-- processed/
|
|-- EDA/
|-- modelos/
|-- reportes/
|-- graficos/
|-- informe/
|-- governance/
`-- logs/
```

Nombres de archivo y extensiones por lenguaje (`.rds` vs `.parquet`/`.pkl`, `renv` vs `venv`/`uv`) — ver la tabla "Equivalentes en Python" en `analytics-workflow/references/reproducibilidad.md`.

Si el proyecto ya posee una estructura consolidada, respetar nombres y convenciones existentes. Adaptar el flujo sin romper compatibilidad.

---

## `00_config` — parámetros específicos de credit scoring

El contenido genérico (paths, seeds, target, `AUC_MIN`, variables, lectura de CSV) está en `analytics-workflow/templates/00_config.r` y `00_config.py` — usar esos como base. Agregar los parámetros propios de scoring que esos templates no cubren:

**R**

```r
# umbrales específicos de credit scoring
DEF_DEFAULT    <- "descripción de la definición de malo (ej: mora >= 90 días en 12 meses)"
BAD_RATE_MIN   <- 0.03
BAD_RATE_MAX   <- 0.40
IV_MIN         <- 0.02
VIF_MAX        <- 10
PSI_ALERT      <- 0.25   # ya en el template genérico; repetido acá por relevancia
N_MALOS_MIN    <- 2000   # regla Siddiqi — ver quality-gates.md

# scorecard
PDO            <- 20     # points to double the odds
BASE_SCORE     <- 600
BASE_ODDS      <- 50
```

**Python**

```python
# umbrales específicos de credit scoring
DEF_DEFAULT = "descripción de la definición de malo (ej: mora >= 90 días en 12 meses)"
BAD_RATE_MIN = 0.03
BAD_RATE_MAX = 0.40
IV_MIN = 0.02
VIF_MAX = 10
PSI_ALERT = 0.25
N_MALOS_MIN = 2000

# scorecard
PDO = 20
BASE_SCORE = 600
BASE_ODDS = 50
```

**Regla:** todo parámetro que puede cambiar entre proyectos vive en `00_config`. Los scripts no tienen valores hardcodeados.
