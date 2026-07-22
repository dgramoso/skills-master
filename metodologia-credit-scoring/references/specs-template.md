# Specs — template y specs pre-llenadas por etapa

> Parte de la skill `metodologia-credit-scoring`. El proceso SDD (qué skill invocar, en qué orden, con qué gates) lo define `SKILL.md` — no duplicarlo acá. Esta referencia define los artefactos.

---

## `specs/00_proyecto.md` — output del alcance inicial

Generado en la Fase 0 (ver `SKILL.md`). Contiene:
- Objetivo del modelo y decisión de negocio que habilita
- Población elegible y exclusiones
- Fuentes de datos disponibles
- Definición preliminar de target
- Restricciones regulatorias o de negocio
- Qué queda fuera del alcance
- Preguntas abiertas que `/grill-with-docs` va a resolver

---

## Template de spec por etapa

```markdown
# Spec — <nombre_etapa>

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

---

## Specs pre-llenadas por etapa

### `specs/01_ingesta_y_target.md`

```markdown
# Spec — 01_ingesta_y_target

## Precondiciones
- datos/raw/ contiene el archivo de solicitudes o cartera
- Columnas mínimas: id_cliente, fecha_solicitud o fecha_obs, estado_cuenta

## Postcondiciones
- datos/processed/base_target.{rds,parquet} con columnas:
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

### `specs/02_integracion_datos.md`

```markdown
# Spec — 02_integracion_datos

## Precondiciones
- datos/processed/base_target.{rds,parquet} existe y cumple su spec
- Fuentes externas disponibles con fecha de snapshot <= periodo_obs

## Postcondiciones
- datos/processed/base_integrada.{rds,parquet}
- EDA/integration_log.csv con cobertura y porcentaje de no-match

## Quality Gate — falla si:
- No-match supera umbral definido en 00_config
- Duplicados generados por el join
- Cualquier variable con fecha posterior a periodo_obs

## Invariantes
- Integridad temporal: nunca usar datos posteriores a periodo_obs
```

### `specs/03_limpieza_y_features.md`

```markdown
# Spec — 03_limpieza_y_features

## Precondiciones
- datos/processed/base_integrada.{rds,parquet} existe y cumple su spec

## Postcondiciones
- datos/processed/base_features.{rds,parquet} con candidate_variables
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

### `specs/04_modelizacion.md`

```markdown
# Spec — 04_modelizacion

## Precondiciones
- datos/processed/base_features.{rds,parquet} existe y cumple su spec
- EDA/binning_log.csv y EDA/exclusion_log.csv generados

## Postcondiciones
- modelos/modelo_final.{rds,pkl}
- modelos/metadata_modelo.{rds,json}
- EDA/model_comparison.csv con champion y challengers
- EDA/performance_summary.csv con AUC, KS, Gini en train/val/OOT
- EDA/calibration_summary.csv

## Quality Gate — falla si:
- AUC < umbral definido en 00_config
- Signo de algún coeficiente contradice expectativa de negocio
- VIF > 10 en alguna variable del modelo final
- Convergencia no alcanzada
- Champion no supera al baseline con significancia (DeLong) y no está
  documentada la recomendación de no reemplazar el esquema vigente

## Invariantes
- Documentar trade-off performance vs interpretabilidad si aplica
- Champion seleccionado con justificación explícita
```

### `specs/05_validacion_y_monitoreo.md`

```markdown
# Spec — 05_validacion_y_monitoreo

## Precondiciones
- modelos/modelo_final.{rds,pkl} existe
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
