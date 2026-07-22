# WOE/IV/binning, segmentación y reject inference

> Parte de la skill `metodologia-credit-scoring`.

---

## 1. WOE, IV y binning

Construir bins interpretables, estables, con volumen suficiente.

Aplicar monotonicidad cuando tenga sentido crediticio (utilización ↑ ⇒ riesgo ↑, mora ↑ ⇒ riesgo ↑). Si se rompe monotonicidad, documentar el motivo explícitamente.

Calcular WOE, IV y bad rate por bin.

Guardar `EDA/binning_log.csv`:

```text
variable | bin_id | lower | upper | woe | iv | n_obs | bad_rate | decision_note
```

### R vs Python: cómo se fuerza la monotonicidad

Diferencia real entre ecosistemas, no solo de sintaxis:

**R (`scorecard::woebin()`)** no garantiza monotonicidad por optimización — el método por defecto (`method = "tree"`) suele acercarse, pero si un bin sale no monótono la corrección es semi-manual con `woebin_adj()` (ajuste interactivo) o iterando `bin_num_limit`/`stop_limit`. El paquete `monobin` es una alternativa dedicada a binning monótono (heurísticas tipo isotonic regression), pero menos usado y sin la restricción de tamaño/IV simultánea.

```r
library(scorecard)
bins <- woebin(datos_train, y = "target", x = "antiguedad_laboral")
# si no sale monótono:
bins_ajustado <- woebin_adj(datos_train, y = "target", bins = bins)
```

**Python (`optbinning`)** plantea el binning como un problema de optimización (CP/MIP) que maximiza IV sujeto a restricciones simultáneas: monotonicidad declarada, tamaño mínimo por bin, máximo de bins. La monotonicidad es una restricción del solver, no un ajuste posterior.

```python
from optbinning import OptimalBinning, BinningProcess

optb = OptimalBinning(
    name="antiguedad_laboral", dtype="numerical",
    monotonic_trend="ascending",  # o "descending", "auto", "peak", "valley", None
    min_bin_size=0.05, max_n_bins=6,
)
optb.fit(x_train, y_train)
tabla = optb.binning_table.build()          # bin, count, event rate, WOE, IV
x_woe = optb.transform(x_nueva, metric="woe")

# para todo el dataset a la vez, con ranking de IV por variable:
bp = BinningProcess(list(X_train.columns), min_bin_size=0.05, max_n_bins=6)
bp.fit(X_train, y_train)
bp.summary()
```

Si el proyecto exige monotonicidad forzada y matemáticamente garantizada por variable (común cuando el validador o el regulador lo pide explícito), esto pesa a favor de Python. Con R, la vía es aceptar el ajuste semi-manual de `woebin_adj()`, usar `reticulate` para llamar a `optbinning` desde R, o hacer el binning en Python y el resto del pipeline en R (frontera limpia: exportar la tabla de bins/WOE).

**Anti-leakage:** fit del binning solo en train; `transform`/`woebin_apply` aplica los cortes congelados a test/OOT/producción. Extremos abiertos (`-Inf`/`Inf` en R, comportamiento por defecto en `optbinning`) para que valores fuera de rango en producción no generen NA.

Funciones genéricas `woe_fit`/`woe_apply` (binning por cuantiles, sin monotonicidad forzada) ya están en `analytics-workflow/templates/mis_funciones.r` y `utils.py` — usarlas para variables donde la monotonicidad no es un requisito duro; usar `optbinning`/`scorecard` cuando sí lo es.

---

## 2. Segmentación de scorecards

Antes de modelizar, decidir explícitamente si conviene un scorecard único o varios (ej: con/sin historial en buró, cliente nuevo/conocido, persona física/jurídica).

Criterio de decisión:

* Segmentar solo si hay interacciones fuertes (la misma variable predice distinto por segmento) o poblaciones estructuralmente distintas (thin files vs thick files).
* La segmentación se justifica si el uplift de performance supera el costo de desarrollar, validar y mantener N modelos.
* Cada segmento debe conservar volumen suficiente (~2.000 malos por scorecard).
* Si un segmento no junta eventos suficientes para estimar bandas de PD con precisión aceptable, no amerita modelo propio — se pliega al modelo único o se fusiona con otro segmento.

Documentar la decisión — segmentar o no — con evidencia en `EDA/segmentation_analysis.csv`.

---

## 3. Reject inference

Cuando se trate de originación, documentar volumen de aprobados, rechazados y tasa de aceptación.

Evaluar los enfoques disponibles:

* **Parceling**: los rechazados se distribuyen entre buenos/malos según la proporción observada en aprobados de score similar, con reponderación.
* **Reweighting**: los aprobados de cada banda de score reciben un peso que representa también a los rechazados de esa banda.
* **Fuzzy Augmentation**: cada rechazado se duplica en un registro "bueno" y uno "malo", ambos con peso fraccionario según la probabilidad estimada.

Si no se realiza reject inference, documentar explícitamente las limitaciones y el sesgo potencial (el modelo solo aprendió de la población aprobada — sesgo de selección).

**Interacción con weighting por desbalance:** si además se aplica un esquema de balanceo de clases (ver `modelizacion-y-validacion.md`), documentar con precisión el peso final combinado de cada registro en train — es lo primero que un auditor va a querer reconstruir cuando hay dos reponderaciones apiladas (reject inference + balanceo).
