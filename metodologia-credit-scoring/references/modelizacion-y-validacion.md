# Champion/challenger, modelización, validación y calibración

> Parte de la skill `metodologia-credit-scoring`. Cubre la etapa 4 del pipeline (`04_modelizacion`) y la validación OOT.

---

## 1. Champion vs challenger

Nunca evaluar un único modelo cuando sea posible. Comparar al menos:

* **Baseline obligatorio**: el esquema vigente del cliente — modelo anterior, score de buró o regla simple (ej: peor calificación). El modelo nunca se evalúa en el vacío.
* Logistic WOE.
* Logistic sin WOE.
* Árbol de decisión.
* Random Forest.
* XGBoost interpretable.

Regla de decisión: si el champion no supera al baseline por un margen material y estadísticamente significativo (test de DeLong), la recomendación honesta es no reemplazar el esquema vigente. Documentarlo como hallazgo, no ocultarlo.

Seleccionar el champion considerando: performance (AUC, KS, Gini), interpretabilidad para negocio y auditoría, estabilidad temporal, gobernanza y cumplimiento regulatorio.

Guardar `EDA/model_comparison.csv`.

---

## 2. Modelización

Si el proyecto ya usa una función específica, usarla para preservar convenciones. Si no existe convención:

**R** — por defecto `rms::lrm()` (diagnósticos inferenciales completos: significancia, deviance, C-index). Alternativa liviana: `glm(family = binomial)`.

```r
modelo <- rms::lrm(target ~ ., data = datos_woe_train, x = TRUE, y = TRUE)
```

**Python** — por defecto `statsmodels` (da los diagnósticos inferenciales que `sklearn` no da por defecto: p-values, IC de coeficientes, deviance).

```python
import statsmodels.api as sm

X_const = sm.add_constant(X_train_woe)
modelo = sm.Logit(y_train, X_const).fit()
print(modelo.summary())
```

`scikit-learn` (`LogisticRegression`) es aceptable para el fit rápido o para challengers de ML (Random Forest, XGBoost), pero no reemplaza a `statsmodels` para el modelo final cuando se necesita defender significancia estadística ante un validador.

Validar: signo esperado por variable, significancia estadística, colinealidad y VIF, estabilidad de coeficientes.

Guardar `modelos/modelo_final.{rds,pkl}`, `modelos/metadata_modelo.{rds,json}`.

### Desbalance de clases

El bad rate típico de originación (3%-40%) rara vez amerita técnicas de balanceo — las métricas de scoring (KS, AUC/Gini, lift) son de ordenamiento y no se degradan por desbalance moderado, y el weighting artificial (`class_weight="balanced"`, SMOTE) distorsiona el intercepto y rompe la calibración de las PDs si estas se toman directo del modelo.

Si se decide muestrear (ej. por volumen computacional, conservando el 100% de los malos y muestreando buenos), reponderar el muestreo con pesos (`freq_weights` en `statsmodels`, `sample_weight` en `optbinning`/`sklearn`) para restaurar los odds poblacionales, y verificar la calibración final contra la tasa de malo observada en una muestra no ponderada.

Es válido y recomendable correr un experimento champion (desbalance natural) vs. challenger (con weighting) cuando las PD finales se toman de la tabla de performance empírica en test/OOT (no del output crudo del modelo) — en ese esquema el weighting no puede distorsionar la calibración, porque la calibración no depende de él. Definir el criterio de desempate (ej. diferencia mínima de KS) antes de correr el experimento, y documentar la elección en el decision log.

---

## 3. Validaciones mínimas

Calcular en train, validation y OOT: AUC/Gini, KS, lift y gain, deciles de score, odds por banda.

Rigor estadístico:

* Intervalos de confianza bootstrap (95%) para AUC, KS y Gini — nunca reportar métricas puntuales sin IC.
* Test de DeLong para comparar AUC entre champion, challengers y baseline: "0.74 > 0.72" no es evidencia sin significancia.
* Si los IC del champion y del baseline se solapan, decirlo explícitamente en el informe.

Guardar `EDA/performance_summary.csv`.

Funciones genéricas `calcular_ks`, `calcular_auc`, `calcular_gini`, `tabla_lift` ya están en `analytics-workflow/templates/mis_funciones.r` y `utils.py` — no reimplementar.

---

## 4. Calibración

Además de discriminación, calcular: calibration curve, Brier score, test de Hosmer-Lemeshow, predicted vs. observed bad rate por banda.

**Ajuste a central tendency**: alinear la PD promedio del modelo con la tasa de malos de largo plazo del portafolio, no solo con la de la muestra de desarrollo (que puede ser un punto atípico del ciclo). Documentar el ajuste si se aplica.

**Bandas con pocos eventos**: la PD empírica de una banda con 0 (o pocos) malos observados no es 0% — es una estimación con alta incertidumbre relativa (regla del 3: cota superior ≈ 3/n con IC 95%). No usar la tasa cruda en esos casos; usar un piso (floor), fusionar la banda con la contigua, o suavizar con una curva de calibración (log-odds vs. score) ajustada sobre toda la muestra. Es un problema de inferencia en la capa de calibración, no un defecto del binning — un bucket con 0 malos es evidencia de buena discriminación, no un error.

Guardar `EDA/calibration_summary.csv`.

---

## 5. Validación OOT

Si existen períodos suficientes, separar `Development / Validation / OOT`.

Si no existe OOT: documentarlo explícitamente, ejecutar K-Fold Cross Validation como control alternativo, e indicar "OOT pendiente" en el informe.
