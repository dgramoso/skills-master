# 00_config.r — plantilla de la skill analytics-workflow
# Centraliza todo parámetro que puede cambiar entre proyectos.
# Los scripts no deben tener valores hardcodeados salvo constantes internas obvias.

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
PROJECT_NAME  <- "nombre_proyecto"
MODEL_VERSION <- "v1"

# definición de target si aplica
TARGET     <- "nombre_variable_target"
DEF_TARGET <- "descripción de qué significa el evento positivo"

# umbrales de calidad
MISSING_MAX <- 0.80
AUC_MIN     <- 0.60
PSI_ALERT   <- 0.25

# variables
VARS_CAT       <- c()
VARS_NUM       <- c()
VARS_DESCARTAR <- c()
VARS_ID        <- c()

# lectura
CSV_SEP      <- ";"
CSV_DEC      <- "."
CSV_ENCODING <- "UTF-8"
