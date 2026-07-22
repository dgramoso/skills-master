# Quality Gates específicos de credit scoring

> Parte de la skill `metodologia-credit-scoring`. El patrón genérico (`stopifnot()`/`assert`, cómo fallar ruidosamente) está en `analytics-workflow/references/quality-gates.md` — usar esa versión. Esta referencia solo lista los **umbrales y controles propios del dominio crediticio**.

---

## Gate: Ingesta

* Sin duplicados de clave principal.
* Target definido.
* Ventanas válidas (performance >= 12 meses).
* Bad rate dentro de `[BAD_RATE_MIN, BAD_RATE_MAX]` (default 3%-40%).
* Al menos ~2.000 malos en desarrollo (regla Siddiqi) — por debajo, documentar el riesgo de inestabilidad y considerar reducir alcance (menos variables, sin segmentación).

## Gate: Integración

* Cobertura de joins documentada.
* Porcentaje de no-match controlado (umbral en `00_config`).
* Integridad temporal verificada: ninguna fuente con fecha de snapshot posterior a `periodo_obs`.

## Gate: Features

* Leakage = 0 (ninguna variable con fecha posterior a `periodo_obs`).
* Missing documentado; variables con missing > 80% se excluyen o se justifica su inclusión.
* IV de cada variable candidata seleccionada >= `IV_MIN` (default 0.02); IV > 1 se marca como sospechosa de leakage.
* Variables finales identificadas con `exclusion_log` completo.

## Gate: Modelización

* Convergencia verificada.
* Signos de coeficientes coherentes con expectativa de negocio (ej: utilización ↑ ⇒ riesgo ↑).
* AUC >= umbral mínimo definido en `00_config`.
* VIF <= 10 en todas las variables del modelo final.
* Champion supera al baseline con significancia estadística (test de DeLong) — si no, documentar la recomendación de no reemplazar el esquema vigente.

## Gate: Validación / Monitoreo

* PSI de score < 0.25 sin investigación pendiente.
* KS OOT no cae más de 10 puntos respecto a desarrollo.
* Calibración: PD predicha vs. bad rate observado por banda dentro de tolerancia (ver `modelizacion-y-validacion.md`).

Ejemplo de gate específico (patrón genérico en `analytics-workflow/quality-gates.md`):

**R**
```r
bad_rate <- mean(datos[[TARGET]])
if (bad_rate < BAD_RATE_MIN || bad_rate > BAD_RATE_MAX)
  stop(sprintf("Quality Gate: bad rate %.1f%% fuera del rango esperado", bad_rate * 100))
```

**Python**
```python
bad_rate = datos[TARGET].mean()
if not (BAD_RATE_MIN <= bad_rate <= BAD_RATE_MAX):
    raise ValueError(f"Quality Gate: bad rate {bad_rate:.1%} fuera del rango esperado")
```
