# Versionado de modelos y governance

> Parte de la skill `analytics-workflow`. Plantilla de changelog en `templates/CHANGELOG.md.tmpl`.

---

## Versionado de modelos

Sin MLflow por defecto. Usar Git + carpetas versionadas.

```text
modelos/
  v1/
    modelo_final.rds
    metadata_modelo.rds
    scorecard.rds
    CHANGELOG.md
  v2/
    ...
```

`CHANGELOG.md` mínimo (ver `templates/CHANGELOG.md.tmpl`):

```markdown
# v1 — AAAA-MM-DD

## Motivo
Modelo baseline inicial.

## Variables
- ...

## Métricas
- AUC train:
- AUC test:
- Gini test:
- KS test:
- PSI:

## Cambios relevantes
- ...

## Limitaciones
- ...
```

---

## `model_registry.csv`

Un registro por modelo relevante en `governance/model_registry.csv`.

Columnas mínimas:

```text
model_name
version
build_date
developer
target_definition
population
observation_window
performance_window
variables_finales
auc_train
auc_test
gini_test
ks_test
psi
deployment_date
status
notes
```

Estados:

```text
desarrollo → validación → producción → deprecado
```
