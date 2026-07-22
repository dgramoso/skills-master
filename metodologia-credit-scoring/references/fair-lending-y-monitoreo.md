# Fair lending, PSI, monitoreo y governance

> Parte de la skill `metodologia-credit-scoring`. Versionado de modelos y columnas genéricas de `model_registry.csv`: ver `analytics-workflow/references/governance.md` — esta referencia agrega solo lo específico de crédito.

---

## 1. Fair lending y reason codes

### Variables prohibidas y proxies

Mantener lista explícita de variables prohibidas por regulación o política (género, edad, estado civil, nacionalidad — según jurisdicción) y de sus proxies potenciales (geografía como proxy socioeconómico, tipo de ocupación). Si un proxy entra al modelo, documentar la justificación de negocio y el riesgo asumido.

### Impacto dispar

Test básico: comparar approval rate y score medio entre los grupos protegidos observables. Diferencias materiales sin justificación de negocio son un hallazgo a reportar, no a silenciar.

### Reason codes (adverse action)

Para cada solicitante rechazado, generar las 3-4 variables que más puntos le restaron respecto al máximo posible del scorecard. Es requisito regulatorio en mercados desarrollados y buena práctica en todos.

Guardar `EDA/fairness_summary.csv`, `EDA/reason_codes.csv`.

---

## 2. PSI y monitoreo

Calcular: PSI de score, PSI por variable relevante, drift de población, drift de target, drift por bandas de score.

Función genérica `calcular_psi` ya está en `analytics-workflow/templates/mis_funciones.r` y `utils.py` — no reimplementar.

Interpretación estándar:

```text
PSI < 0.10          → Estable
0.10 <= PSI < 0.25  → Monitorear
PSI >= 0.25         → Investigar / considerar recalibración
```

Generar `EDA/psi_summary.csv`, `EDA/top_drift_variables.csv`.

### Monitoreo continuo

Preparar framework para seguimiento mensual de: PSI de score, KS, bad rate por cohorte, calibración.

Generar `EDA/monitoring_dashboard.csv`.

### Test de paridad dev-prod

Antes de dar por implementado el modelo: scorear una muestra idéntica en desarrollo y en producción y verificar coincidencia exacta (o desvío menor a una tolerancia definida). Un scorecard mal transcripto es el modo de falla de implementación más común.

Guardar `EDA/score_parity_test.csv`.

### Triggers de acción

Cada umbral de monitoreo tiene acción y responsable definidos, no solo color:

| Señal | Acción | Decide |
|---|---|---|
| PSI de score >= 0.25 | Investigar causa en 30 días; si es estructural, recalibrar | Model owner |
| KS cae > 10 puntos vs desarrollo | Revisión completa del modelo | Model owner + negocio |
| Bad rate por banda fuera del rango predicho 3 meses seguidos | Revisar calibración y cutoffs | Negocio |

---

## 3. Model governance

Versionado de modelos y columnas genéricas de `governance/model_registry.csv`: ver `analytics-workflow/references/governance.md`.

Columnas adicionales específicas de credit scoring (extienden las genéricas — `target_definition`, `population` y las ventanas ya están en la lista genérica):

```text
oot_auc | oot_ks | reject_inference_method
```

### Marco regulatorio según uso del modelo

Identificar el uso al inicio del proyecto y documentarlo en `specs/00_proyecto.md` — el mismo modelo requiere gobernanza distinta según para qué se use:

| Uso del modelo | Marco de referencia | Implicancia principal |
|---|---|---|
| Originación / decisión de crédito | Model Risk Management (tipo SR 11-7) | Validación independiente, inventario de modelos, documentación completa |
| Provisiones contables | IFRS 9 (ECL) | PD 12 meses vs lifetime, staging, componente forward-looking |
| Capital regulatorio (bancos) | Basilea II/III | Definición de default regulatoria, márgenes de conservadurismo |
