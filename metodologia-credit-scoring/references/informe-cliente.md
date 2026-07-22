# Informe cliente

> Parte de la skill `metodologia-credit-scoring`. El estándar genérico (pyramid principle, so-what, piezas del entregable, checklist) está en `analytics-workflow/references/informe-ejecutivo.md` — usar esa versión. Esta referencia agrega solo lo específico de credit scoring: estilo visual y contenido ejecutivo propio del scorecard.

---

## Estilo visual

Generar informe HTML ejecutivo con diseño:

* Minimalista, estilo macOS / suizo.
* Amplio espacio en blanco.
* Tipografía del sistema: `-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif`.
* SF Mono o equivalente para tablas y datos numéricos.
* Colores neutros, contrastes suaves. Evitar colores brillantes o fondos oscuros.

Gráficos estilo BBC / The Economist: minimalistas, etiquetas claras, sin gridlines innecesarios, foco en storytelling e interpretación. Evitar colores estridentes o decoraciones que distraigan del mensaje. Assertion titles (ver `analytics-workflow/informe-ejecutivo.md`).

---

## Contenido ejecutivo específico de credit scoring

Además de la estructura genérica (respuesta primero, so-what por hallazgo, supuestos/limitaciones), el informe de un scorecard incluye:

* Definición de target y su justificación empírica (roll rate, vintage).
* Metodología (binning, reject inference si aplica, segmentación si aplica).
* Variables relevantes y drivers, con signo e interpretación de negocio.
* Performance (train/validation/OOT) con intervalos de confianza.
* Benchmark contra el esquema vigente y uplift económico (swap set).
* Strategy tables, cutoff económico y cutoffs recomendados.
* Calibración y master scale.
* Fair lending y reason codes, si aplica.
* Riesgos metodológicos propios del proyecto (ej. reject inference no realizado, sin OOT disponible).

## Separación ejecutivo / técnico

* **Sección ejecutiva**: para negocio y alta dirección. Foco en insights, estrategia y recomendaciones.
* **Anexos técnicos**: para riesgo, auditoría y validación independiente. Incluye binning, exclusion log, coeficientes, PSI, calibración y governance.
