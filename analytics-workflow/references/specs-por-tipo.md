# Specs obligatorias por tipo de proyecto

> Parte de la skill `analytics-workflow`. Ver `SKILL.md` para el flujo general y `spec-template.md` para el template de cada spec.

Cada spec listada acá debe crearse con el template general y grillarse con `/grill-with-docs` antes de escribir código.

Estas son las specs **por defecto**. Los módulos avanzados (reject inference, validación independiente, fairness, data governance) son **opcionales** y se activan solo si el cliente o el regulador lo exige — ver `modulos-opcionales.md`.

---

## A. Modelo supervisado

Ejemplos: credit scoring, cobranza, churn, fraude, propensión comercial.

Specs mínimas:

```text
specs/
├── 00_prd_reference.md
├── 01_target_outcome.md
├── 02_data_snapshot.md
├── 03_feature_engineering.md
├── 04_modeling_validation.md
├── 05_deployment_scoring.md
├── 06_monitoring.md
└── 07_report.md
```

### 01_target_outcome.md

Debe definir:

* unidad de análisis
* fecha de corte
* evento objetivo
* horizonte de predicción
* ventana de observación
* ventana de performance
* población elegible
* exclusiones
* tratamiento de indeterminados
* bad rate esperado
* riesgos de leakage

### 02_data_snapshot.md

Debe definir:

* fuentes
* tablas
* joins
* granularidad
* claves
* períodos
* criterios de deduplicación
* controles de integridad
* outputs intermedios

### 03_feature_engineering.md

Debe definir:

* familias de variables
* ventanas temporales
* transformaciones
* missing
* winsorización
* categorización
* WOE/binning si aplica
* variables excluidas
* chequeos de leakage

### 04_modeling_validation.md

Debe definir:

* algoritmo baseline
* challengers
* split train/test/OOT
* métricas
* calibración
* estabilidad
* selección de modelo
* interpretación
* umbrales mínimos

> **Opcional — reject inference (originación):** si el modelo es de originación y hay población rechazada significativa, definir si se aplica reject inference y con qué método (reclasificación / parcelling / augmentation / Heckman), y marcarlo explícito en la spec (`reject inference: sí/no + método`). Ver `modulos-opcionales.md`.

### 05_deployment_scoring.md

Debe definir:

* batch/API/manual
* frecuencia
* tabla o archivo de salida
* columnas finales
* versionado
* consumo operativo
* rollback

### 06_monitoring.md

Debe definir:

* PSI
* drift
* performance real
* alertas
* frecuencia
* responsables
* thresholds
* acciones correctivas

### 07_report.md

Debe definir:

* audiencia
* estructura del informe
* tablas
* gráficos
* narrativa ejecutiva
* anexos técnicos
* limitaciones

---

## B. Segmentación / clustering

Ejemplos: segmentación de consumo de tarjeta, segmentación RFM, clusters de comercios, perfiles de clientes.

Specs mínimas:

```text
specs/
├── 00_prd_reference.md
├── 01_population_scope.md
├── 02_data_snapshot.md
├── 03_feature_space.md
├── 04_clustering_validation.md
├── 05_segment_interpretation.md
├── 06_deployment_tagging.md
└── 07_report.md
```

Debe documentarse:

* población
* unidad de análisis
* variables de segmentación
* variables descriptivas no usadas para clusterizar
* normalización
* distancia
* algoritmo
* número de clusters
* estabilidad
* interpretabilidad
* accionabilidad
* forma de asignar nuevos clientes
* monitoreo de tamaño y drift de segmentos

Regla:

```text
No incluir variables sociodemográficas, límite de crédito o calidad de pago en el clustering
salvo que formen parte del objetivo estratégico de segmentación.
```

Pueden usarse como variables descriptivas posteriores para perfilar clusters.

---

## C. Dashboard / reportería

Ejemplos: dashboard de scoring, tablero de cobranza, reporte de actividad comercial, monitoreo mensual de modelo.

Specs mínimas:

```text
specs/
├── 00_prd_reference.md
├── 01_kpi_definition.md
├── 02_data_contract.md
├── 03_transformations.md
├── 04_dashboard_layout.md
├── 05_quality_gates.md
└── 06_refresh_monitoring.md
```

Debe documentarse:

* audiencia
* KPIs
* definiciones exactas
* fuentes
* filtros
* actualización
* reglas de negocio
* layout
* exportables
* validaciones
* interpretación esperada
