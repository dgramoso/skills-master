# Pipeline: ingesta, target, integración y features

> Parte de la skill `metodologia-credit-scoring`. Cubre las etapas 1-3 del pipeline (`01_ingesta_y_target`, `02_integracion_datos`, `03_limpieza_y_features`). Specs en `specs-template.md`, quality gates en `quality-gates.md`.

---

## 1. Ingesta y target

Documentar en `CONTEXT.md` antes de codear (ver también `SKILL.md`, sección "Definición de target y ventanas"):

* Población elegible.
* Exclusiones.
* Fecha de observación.
* Ventana de performance.
* Definición de default.
* Criterios regulatorios.

Crear variables:

```text
target
bad
good
indeterminate
sample_flag
periodo_obs
periodo_perf
```

Validar: conteos por población, bad rate, duplicados, consistencia temporal, distribución de cohortes.

Generar: `EDA/auditoria_target.csv`.

### Justificación empírica del target

La definición de default no se declara: se justifica con datos. Antes de fijarla:

* **Roll rate analysis**: matriz de transición entre buckets de mora (al día → 1-29 → 30-59 → 60-89 → 90+). La definición de malo se fija en el bucket desde el cual la mayoría de las cuentas no cura.
* **Vintage analysis**: curvas de bad rate acumulado por cohorte de originación. La ventana de performance se fija donde las curvas se aplanan.
* **Tamaño muestral**: regla Siddiqi de ~2.000 malos mínimo en desarrollo. Por debajo, documentar el riesgo de inestabilidad y considerar reducir el alcance (menos variables, sin segmentación).

Guardar: `EDA/roll_rate_analysis.csv`, `EDA/vintage_analysis.csv`.

Es lo primero que revisa un validador independiente: si el target no está justificado empíricamente, el modelo no es defendible.

---

## 2. Integración de datos

Documentar: fuentes, fecha de snapshot, claves de join, reglas de matching.

Validar: cobertura y porcentaje de no-match, duplicados generados por el join, integridad temporal (nunca usar información posterior a la fecha de observación).

Generar: `EDA/integration_log.csv`.

---

## 3. Limpieza y feature engineering

Realizar:

* Estandarización de tipos, unidades y categorías.
* Imputación documentada.
* Tratamiento de outliers y valores especiales (ver `winsorizar_fit`/`winsorizar_apply` en `analytics-workflow/templates/mis_funciones.r` y `utils.py`).
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

Mantener y guardar: `candidate_variables` (entran al análisis), `excluded_variables` (descartadas con motivo).

### Exclusion log

Documentar todas las variables excluidas en `EDA/exclusion_log.csv`:

```text
variable | reason | iv | stability_metric | correlation | business_justification
```

Motivos típicos: leakage, IV bajo, inestabilidad, correlación alta con otra variable seleccionada, no operable en producción, sin justificación de negocio.

**Anti-leakage:** fit de imputaciones, winsorización y binning solo en train — aplicar congelado en test/OOT/producción. Regla general y patrón `*_fit`/`*_apply` en `analytics-workflow/references/quality-gates.md`.
