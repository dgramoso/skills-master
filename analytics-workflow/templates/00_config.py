# 00_config.py — plantilla de la skill analytics-workflow
# Centraliza todo parametro que puede cambiar entre proyectos.
# Los scripts no deben tener valores hardcodeados salvo constantes internas obvias.

import random

import numpy as np

# paths
PATH_RAW = "datos/raw/archivo.csv"
PATH_PROCESSED = "datos/processed/"
PATH_EDA = "EDA/"
PATH_MODELOS = "modelos/"
PATH_REPORTES = "reportes/"
PATH_LOGS = "logs/"

# reproducibilidad
SEED = 42
random.seed(SEED)
np.random.seed(SEED)

# proyecto
PROJECT_NAME = "nombre_proyecto"
MODEL_VERSION = "v1"

# definicion de target si aplica
TARGET = "nombre_variable_target"
DEF_TARGET = "descripcion de que significa el evento positivo"

# umbrales de calidad
MISSING_MAX = 0.80
AUC_MIN = 0.60
PSI_ALERT = 0.25

# variables
VARS_CAT: list[str] = []
VARS_NUM: list[str] = []
VARS_DESCARTAR: list[str] = []
VARS_ID: list[str] = []

# lectura
CSV_SEP = ";"
CSV_DEC = "."
CSV_ENCODING = "UTF-8"
