# Reproducibilidad: config, pipeline y renv

> Parte de la skill `analytics-workflow`. Plantilla copiable en `templates/00_config.r`.

---

## `00_config.r`

Centraliza todo parámetro que puede cambiar entre proyectos. Ver `templates/00_config.r` para el archivo copiable.

Contenido mínimo:

```r
# paths
PATH_RAW        <- "datos/raw/archivo.csv"
PATH_PROCESSED  <- "datos/processed/"
PATH_EDA        <- "EDA/"
PATH_MODELOS    <- "modelos/"
PATH_REPORTES   <- "reportes/"
PATH_LOGS       <- "logs/"

# reproducibilidad
SEED <- 42
set.seed(SEED)

# proyecto
PROJECT_NAME <- "nombre_proyecto"
MODEL_VERSION <- "v1"

# definición de target si aplica
TARGET     <- "nombre_variable_target"
DEF_TARGET <- "descripción de qué significa el evento positivo"

# umbrales de calidad
MISSING_MAX <- 0.80
AUC_MIN     <- 0.60
PSI_ALERT   <- 0.25

# variables
VARS_CAT        <- c()
VARS_NUM        <- c()
VARS_DESCARTAR  <- c()
VARS_ID         <- c()

# lectura
CSV_SEP <- ";"
CSV_DEC <- "."
CSV_ENCODING <- "UTF-8"
```

Regla:

```text
Todo parámetro que puede cambiar entre proyectos vive en 00_config.r.
```

Los scripts no deben tener valores hardcodeados salvo constantes internas obvias.

---

## `00_run_pipeline.r`

Debe ejecutar todo el pipeline en orden:

```r
source("scripts/00_config.r")

source("scripts/01_ingesta.r")
source("scripts/02_features.r")
source("scripts/03_modelizacion.r")
source("scripts/04_validacion.r")
source("scripts/05_informe.r")
```

Reglas:

* debe correr desde cero
* no debe requerir clicks
* no debe depender de objetos en memoria
* debe fallar ruidosamente si algo está mal
* debe guardar logs o mensajes suficientes para auditoría

---

## renv

`set.seed()` garantiza reproducibilidad del muestreo, pero no protege contra cambios en paquetes.

```r
install.packages("renv")
renv::init()
renv::snapshot()
renv::restore()
```

Qué se commitea:

```text
renv.lock sí.
renv/library/ no.
```

Agregar `renv/library/` a `.gitignore`.

Registrar en `CONTEXT.md`:

* versión de R
* sistema operativo si importa
* paquetes críticos
* versión de paquetes si hay riesgo de incompatibilidad
