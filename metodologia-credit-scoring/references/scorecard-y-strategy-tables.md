# Scorecard, master scale y strategy tables

> Parte de la skill `metodologia-credit-scoring`.

---

## 1. Scorecard

Cuando corresponda generar scorecard, documentar PDO (Points to Double the Odds), Base Score, Base Odds, Factor, Offset.

Conversión de WOE a puntos por bin: `points = -(coef * woe + intercept/n_vars) * factor + offset/n_vars`, con `factor = PDO / ln(2)` y `offset = base_score - factor * ln(base_odds)`.

**R** — `scorecard::scorecard()` a partir del binning y el modelo `glm`:

```r
library(scorecard)
card <- scorecard(bins, model_glm, points0 = 600, odds0 = 1/50, pdo = 20)
```

**Python** — clase `Scorecard` de `optbinning` (a partir del binning + `sklearn`/`statsmodels`), o cálculo manual con la fórmula de arriba a partir de los coeficientes de `statsmodels`:

```python
from optbinning import Scorecard
from sklearn.linear_model import LogisticRegression

scorecard = Scorecard(
    binning_process=bp, estimator=LogisticRegression(),
    scaling_method="pdo_odds",
    scaling_method_params={"pdo": 20, "odds": 50, "scorecard_points": 600},
)
scorecard.fit(X_train, y_train)
tabla_puntos = scorecard.table(style="detailed")
```

Guardar `EDA/scorecard_points.csv` (`variable | bin | woe | points`) y `modelos/scorecard.{rds,pkl}`.

### Master scale

Mapear el score a bandas de rating operables:

```text
banda | score_min | score_max | pd_media | odds | n_obs | uso_sugerido
```

Es como el cliente opera el modelo: las decisiones de crédito, pricing y provisiones se toman por banda, no por punto de score. Ver `modelizacion-y-validacion.md` sobre cómo calcular la PD por banda cuando hay pocos eventos.

Guardar `EDA/master_scale.csv`.

---

## 2. Strategy tables

Generar automáticamente tablas con: banda de score, volumen y porcentaje, bad rate, approval rate / rejection rate, odds, expected loss, acumulados.

Evaluar múltiples cutoffs e identificar perfiles: conservador, comercial, agresivo. Mostrar trade-offs explícitamente.

La función base `tabla_estrategia` (aprobación y bad rate por cutoff) ya está en `analytics-workflow/templates/mis_funciones.r` y `utils.py` — extenderla con expected loss y acumulados según el proyecto.

Guardar `EDA/strategy_tables.csv`.

### Swap set analysis

Cuando existe un esquema vigente (modelo anterior, score de buró o regla), cuantificar quiénes cambian de decisión:

* **Swap-in**: rechazados por el esquema vigente que el modelo nuevo aprueba — estimar su bad rate.
* **Swap-out**: aprobados por el esquema vigente que el modelo nuevo rechaza — estimar la pérdida evitada.
* **Neto en unidades monetarias**: volumen adicional aprobado × margen − pérdida incremental.

Guardar `EDA/swap_set_analysis.csv`.

### Cutoff económico

El cutoff óptimo no se elige solo por bad rate: incorporar ganancia esperada por buen cliente y pérdida esperada por malo (LGD × EAD, o la aproximación disponible). Reportar:

* El cutoff que maximiza beneficio neto, junto a los perfiles conservador / comercial / agresivo.
* El uplift del modelo en unidades monetarias: "X puntos de Gini equivalen a $Y menos de pérdida anual a la misma tasa de aprobación".

Si el cliente no provee datos económicos, usar supuestos explícitos y documentarlos como tales — un supuesto declarado es defendible, uno implícito no.
