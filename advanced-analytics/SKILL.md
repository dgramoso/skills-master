---
name: advanced-analytics
description: Usar cuando hay que analizar un dataset (CSV, SQL, Excel), hacer EDA, construir o evaluar modelos (regresión, clasificación, clustering, forecasting, segmentación, scoring), identificar drivers, o traducir métricas técnicas (AUC, KS, PSI, IV, R², MAPE) a decisiones de negocio y recomendaciones ejecutivas. Estándar de consultora internacional (McKinsey/EY/Experian). Complementa a analytics-workflow (proceso SDD) y metodologia-credit-scoring (metodología crediticia).
---

# Advanced Analytics — Ejecución e Interpretación

Skill de **ejecución técnica e interpretación** para proyectos de analítica: convierte datos crudos en conclusiones listas para decidir, con el rigor metodológico y el estándar de comunicación de una consultora internacional.

## Rol dentro del ecosistema

Esta skill define **cómo se hace y cómo se interpreta un análisis**. No define el proceso del proyecto ni el formato del entregable final — eso vive en otras skills. No duplicar sus contenidos: referenciarlos.

| Necesidad | Dónde vive |
|---|---|
| Proceso del proyecto: PRD, specs, grill, estados, engagement, entrega, handover | `analytics-workflow` (SKILL.md + `references/`) |
| Estándar del informe ejecutivo: pyramid principle, piezas del entregable | `analytics-workflow/references/informe-ejecutivo.md` |
| QA pre-entrega del proyecto completo y quality gates de pipeline | `analytics-workflow/references/quality-gates.md` |
| Metodología crediticia completa (WOE/IV, scorecard, OOT, strategy tables) | `metodologia-credit-scoring` (+ su `references/credit-scoring.md`) |
| Funciones ya testeadas (PSI, KS, AUC/Gini, lift, WOE/IV fit-apply) | `analytics-workflow/templates/mis_funciones.r` · `utils.py` |
| Diseño de gráficos y dashboards | skills del plugin data: `data:create-viz` · `data:data-visualization` |

**Cuándo se invoca esta skill:** análisis exploratorio o modelado dentro de una etapa del pipeline, driver analysis, o cuando hay resultados técnicos que traducir a decisiones de negocio.

---

## Principios operativos

1. **Guiado por hipótesis, no por curiosidad.** Antes de tocar los datos, descomponer la pregunta de negocio en un árbol de hipótesis MECE (mutuamente excluyentes, colectivamente exhaustivas). Cada análisis prueba o descarta una hipótesis; lo que no responde a ninguna es exploración residual y se marca como tal.
2. **80/20.** Identificar primero las 2-3 variables o segmentos que concentran la mayor parte del efecto. Profundizar solo donde el impacto potencial lo justifica.
3. **Baseline obligatorio.** Ningún modelo ni recomendación se reporta sin comparación contra el status quo del cliente o una regla naive. La complejidad se justifica solo si mejora la decisión de negocio de forma material.
4. **Separación epistémica.** Todo output distingue explícitamente: **hecho** (observado en datos), **estimación** (salida de modelo con incertidumbre), **supuesto** (declarado, no verificado) y **recomendación** (juicio). Nunca mezclarlos en una misma frase sin etiqueta.
5. **Materialidad antes que significancia.** Un efecto estadísticamente significativo pero económicamente irrelevante no es un hallazgo. Un segmento se reporta solo si es accionable y tiene tamaño mínimo (default: ≥ 5% de la población o n ≥ 100, lo que sea mayor; ajustar en la spec).
6. **Riesgos de primera clase:** leakage, sesgo de muestreo, fechas de corte, definición de target, población de desarrollo vs población de aplicación, paradoja de Simpson al agregar. Se verifican, no se asumen.
7. **Reproducibilidad.** Código modular y rerunnable: parámetros en `00_config`, fit en train / apply en test, outputs a carpetas del proyecto (`EDA/`, `datos/processed/`, `reportes/`). Preferir Python (`pandas`, `numpy`, `scikit-learn`) o R según el proyecto; SQL para transformaciones pesadas en warehouse.

---

## Workflow técnico

### 0. Encuadre (antes de tocar datos)

Dejar por escrito, en la spec de la etapa o al inicio del análisis:

- Pregunta de negocio y **decisión que habilita** (si ninguna decisión cambia con el resultado, replantear el análisis).
- Audiencia y nivel de detalle esperado.
- Unidad de análisis (grano), población, ventana temporal, exclusiones.
- Métrica de éxito y umbral de "suficientemente bueno".
- Árbol de hipótesis inicial (3-7 hipótesis MECE con su test asociado).

### 1. Diagnóstico de datos

- Cargar solo lo necesario. Inspeccionar: shape, schema, tipos, nulos, cardinalidad, rangos, cobertura temporal, disponibilidad del target.
- Identificar claves de entidad y tiempo, joins, unidad de observación e independencia de registros.
- **Gates que frenan el análisis** (escalar al analista antes de seguir):
  - Claves duplicadas en el grano declarado.
  - Variable candidata a leakage (información posterior a la fecha de decisión).
  - Población de datos ≠ población sobre la que se decidirá.
  - Variable crítica con missing > 40% sin explicación de negocio.
- Producir un resumen de calidad de datos (tabla: variable, tipo, % nulos, rango/valores, anomalías) — es parte del entregable, no un paso interno.

### 2. Preparación

- Política de missing **declarada** por variable: preservar como señal, imputar, excluir o flag de missingness. Nunca imputar en silencio.
- Estandarizar categorías, fechas, unidades y booleanos; conservar etiquetas interpretables para reporting antes de encodear.
- Features derivadas que reflejen mecanismos de negocio: tenure, RFM, utilización, crecimiento, lags, ratios.
- Split train/test **respetando el tiempo** si el uso es forward-looking; todo fit (bins, imputaciones, escalado, WOE) se aprende en train y se aplica en test/OOT.

### 3. EDA guiado por hipótesis

- Cada gráfico o tabla responde una hipótesis del árbol; su título es la afirmación del hallazgo (assertion title), no una descripción.
- Comparar tasas del target entre segmentos con intervalos o tamaños muestrales visibles.
- Revisar correlaciones, monotonicidad, estacionalidad, cohortes/vintages e interacciones.
- Antes de reportar un agregado, verificar que no se invierte al desagregar (Simpson).
- Mantener dos listas separadas: **hallazgos confirmados** y **sorpresas por verificar**. Una sorpresa no confirmada no entra al informe.

### 4. Modelado (cuando aporta a la decisión)

Elegir el modelo más simple que responde la pregunta. Por tipo:

| Tipo | Baseline mínimo | Métricas a reportar |
|---|---|---|
| Regresión | Media / valor del período anterior | RMSE, MAE, patrón de residuos, **error en unidades de negocio** |
| Clasificación | Prevalencia / regla actual del cliente | AUC, KS, precision/recall, lift por decil, calibración, trade-offs de umbral |
| Clustering | Segmentación vigente del negocio | Tamaño y perfil de cada cluster en variables de negocio, estabilidad |
| Series de tiempo | Naive estacional | MAPE/sMAPE por horizonte, comparación vs naive |
| Credit scoring | Regla vigente / score anterior | Derivar a la skill `metodologia-credit-scoring` |

- Reportar siempre la comparación contra baseline y el veredicto: ¿la complejidad extra mejora la decisión lo suficiente?
- **Disparadores de sospecha** (auditar antes de reportar): una variable con IV > 0.9 (leakage casi seguro), R² > 0.95 en datos de negocio, una feature con > 50% de la importancia total, performance en test mejor que en train.

### 5. Driver analysis

- Métodos según el caso: coeficientes, permutation importance, SHAP, partial dependence, deltas por segmento.
- **Asociación ≠ causalidad.** Solo afirmar causalidad si el diseño lo soporta (experimento, quasi-experimento, variación exógena); si no, el lenguaje es "asociado a", nunca "causa".
- Agrupar drivers en categorías de negocio (perfil, engagement, uso de producto, pricing, operaciones, riesgo, canal) — un ranking de 30 variables técnicas no es un entregable.
- Cuantificar cada driver en unidades entendibles: puntos de conversión, probabilidad de churn, ingreso esperado, costo evitado.

### 6. Interpretación para negocio

Ningún hallazgo se reporta suelto. La cadena completa es obligatoria:

```text
hallazgo → implicancia → recomendación → impacto estimado ($ o volumen) → esfuerzo/owner
```

Si el impacto no puede cuantificarse, decir explícitamente por qué y qué dato faltó. El formato del entregable final sigue `analytics-workflow/references/informe-ejecutivo.md` (pyramid principle: respuesta primero, evidencia después).

---

## Traducción estándar de métricas

Usar estos rangos como lenguaje por defecto al comunicar a negocio. Son heurísticos: si el contexto del cliente exige otros umbrales, se fijan en la spec.

| Métrica | Rango | Lectura de negocio |
|---|---|---|
| AUC | < 0.60 | Apenas mejor que el azar; no usar para decidir |
| | 0.60–0.70 | Ordena con capacidad modesta; útil solo para priorización gruesa |
| | 0.70–0.80 | Ordena bien; apto para priorización y estrategia, no para decisión individual automática |
| | > 0.80 | Discriminación fuerte; antes de celebrar, revisar el IV de cada variable — IV > 0.9 indica leakage |
| KS | < 20 | Separación débil |
| | 20–40 | Separación aceptable a buena |
| | 40–50 | Separación fuerte; verificar variables antes de reportar |
| | > 50 | Sospechar leakage o target mal definido |
| PSI | < 0.10 | Población estable |
| | 0.10–0.25 | Drift moderado; monitorear y revisar variables |
| | > 0.25 | La población cambió materialmente; no automatizar decisiones sin revalidar |
| MAPE | Comparar siempre vs naive | "El modelo reduce el error del pronóstico actual de X% a Y%" |
| Silhouette / estabilidad | — | Los clusters valen por su accionabilidad y perfil de negocio, no por el score interno |

Regla general: **la métrica nunca viaja sola** — siempre acompañada de qué permite y qué no permite hacer.

---

## QA analítico (antes de mostrar resultados)

Checklist propio de cada análisis — complementa (no reemplaza) el QA pre-entrega del proyecto:

- [ ] Los totales del análisis reconcilian con la fuente (filas, sumas de montos, conteos por período).
- [ ] Las cifras citadas en texto y títulos coinciden con las tablas/outputs que las respaldan.
- [ ] Cada conclusión sobrevive a un cambio razonable de supuesto clave (sensibilidad mínima: cutoff de fechas, tratamiento de outliers, definición de target).
- [ ] Los segmentos reportados cumplen el tamaño mínimo de materialidad.
- [ ] Métricas de modelo calculadas sobre datos que el modelo no vio (test/OOT), con split temporal si aplica.
- [ ] El código corre de punta a punta desde datos crudos sin pasos manuales.
- [ ] Hechos, estimaciones, supuestos y recomendaciones están separados en el texto.

---

## Errores comunes de análisis

| Error | Corrección |
|---|---|
| Metric dump: reportar AUC/RMSE sin interpretación | Toda métrica con su lectura de negocio y su baseline |
| "Insight" que es una descripción ("las ventas suben en diciembre") | Un insight cambia una decisión; si no, es contexto |
| Explorar sin hipótesis y reportar todo lo encontrado | Árbol MECE primero; reportar solo lo que responde hipótesis |
| Promediar sobre poblaciones heterogéneas | Desagregar por segmento antes de afirmar; chequear Simpson |
| Celebrar AUC 0.95 | Auditar leakage revisando el IV por variable: IV > 0.9 es el diagnóstico más probable |
| Recomendar sobre un segmento de n = 12 | Aplicar umbral de materialidad |
| Afirmar causalidad desde correlación | Lenguaje de asociación salvo diseño causal |
| Imputar o excluir nulos en silencio | Política de missing declarada y reportada |
| Fit de transformaciones con train + test juntos | Fit en train, apply en test/OOT |
| Gráficos decorativos o títulos descriptivos | Cada visual responde una pregunta; assertion titles |
| Comparar cohortes con maduración incompleta | Vintage analysis con ventanas comparables |
| Reportar la sorpresa sin verificarla | Lista separada; se confirma o no entra |

---

## Estándar de output

Todo análisis entrega, en este orden:

1. **Respuesta a la pregunta de negocio** (2-5 líneas, autocontenida, con el so-what cuantificado).
2. **Hallazgos** con la cadena completa (hallazgo → implicancia → recomendación → impacto → esfuerzo/owner).
3. **Resumen de calidad de datos** y limitaciones que condicionan las conclusiones.
4. **Evidencia**: tablas y gráficos con assertion titles, cada uno ligado a una hipótesis.
5. **Código reproducible** (Python, R o SQL) con parámetros en `00_config`, salvo que se pida solo revisión conceptual.
6. **Próximas mediciones**: qué dato o experimento reduciría más la incertidumbre.

Nunca entregar un volcado de métricas sin interpretación, ni una recomendación sin la evidencia que la sostiene.
