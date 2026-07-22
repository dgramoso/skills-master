# Funciones compartidas

> Parte de la skill `metodologia-credit-scoring`.

---

## Biblioteca semilla genérica

`analytics-workflow/templates/mis_funciones.r` y `utils.py` (con sus tests) ya cubren, testeadas:

* PSI (`calcular_psi`)
* KS, AUC, Gini (`calcular_ks`, `calcular_auc`, `calcular_gini`)
* Lift/gain (`tabla_lift`)
* Strategy table base (`tabla_estrategia`)
* Winsorización fit/apply (`winsorizar_fit`, `winsorizar_apply`)
* WOE/IV fit/apply (`woe_fit`, `woe_apply`) — binning por cuantiles sin monotonicidad forzada

Copiar esos archivos como base de `scripts/mis_funciones.r` o `scripts/utils.py` del proyecto. No reimplementar estas funciones en credit scoring.

Para binning con monotonicidad forzada (requisito frecuente en scorecards), usar `optbinning` (Python) o `scorecard`/`monobin` (R) — ver `binning-segmentacion-reject-inference.md`.

---

## Funciones específicas de credit scoring (no están en la biblioteca genérica)

Agregar a `mis_funciones.r`/`utils.py` del proyecto cuando el pipeline las necesite:

* **Conversión WOE → puntos de scorecard** (PDO/odds/factor/offset) — ver fórmula y ejemplos en `scorecard-y-strategy-tables.md`.
* **Generador de reason codes**: para cada solicitante, ranking de las variables que más puntos restaron respecto al máximo del scorecard — ver `fair-lending-y-monitoreo.md`.
* **Swap set analysis**: cálculo de swap-in/swap-out contra un esquema vigente — ver `scorecard-y-strategy-tables.md`.

**Importante:** antes de generar código que use `source("mis_funciones.r")` o `import utils`, confirmar que el archivo existe. Si no existe, incluir la función inline con una nota o solicitar su creación previa. No duplicar lógica entre scripts si puede vivir como función clara y testeable.

---

## Interpretaciones automáticas vía Claude API

La función `llamar_claude()` (o el equivalente en Python) y las reglas de uso (privacidad, revisión antes de entregar, no romper el pipeline sin API key) están definidas en `analytics-workflow/references/claude-api.md` — no duplicar acá.

Las secciones que ese documento lista como típicas para generar automáticamente (Performance, Calibración, Estabilidad, Recomendaciones) aplican directo a `06_informe` de credit scoring, con las métricas propias del scorecard (AUC, KS, PSI, calibración por banda) como input al prompt.
