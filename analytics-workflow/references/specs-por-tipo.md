# Specs obligatorias por tipo de proyecto

> Parte de la skill `analytics-workflow`. Ver `SKILL.md` para el flujo general y `spec-template.md` para el template de cada spec.

Cada spec listada acá debe crearse con el template general y grillarse con `/grill-with-docs` antes de escribir código.

Estas son las specs **por defecto**. Los módulos avanzados (reject inference, validación independiente, fairness, data governance) son **opcionales** y se activan solo si el cliente o el regulador lo exige — ver `modulos-opcionales.md`.

El estándar de entrega de `informe-ejecutivo.md` (pyramid principle, so-what cuantificado, supuestos/limitaciones, consistencia de cifras) aplica a la spec de report de **los tres tipos** de proyecto.

---

## A. Modelo supervisado

Ejemplos: credit scoring, cobranza, churn, fraude, propensión comercial.

Specs mínimas:

```text
specs/
├── 00_prd_reference.md
├── 01_target_outcome.md
├── 02_data_snapshot.md
├── 03_eda.md
├── 04_feature_engineering.md
├── 05_modeling_validation.md
├── 06_deployment_scoring.md
├── 07_monitoring.md
└── 08_report.md
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

### 03_eda.md

Debe definir:

* preguntas / hipótesis que el EDA debe responder
* universo de variables a perfilar (todas o subconjunto)
* análisis de distribuciones (numéricas y categóricas)
* análisis de missing (patrón y % por variable)
* detección de outliers y valores imposibles
* correlaciones y multicolinealidad preliminar
* relación de cada variable con el target (tasa de evento por bin, IV/estadístico preliminar)
* candidatos tempranos a leakage (señal sospechosamente alta)
* outputs esperados en `EDA/` (tablas y gráficos)
* **diagnóstico de calidad de datos compartible con el cliente**: cobertura, missing, consistencia, período útil y veredicto de viabilidad del alcance. Se entrega temprano — genera confianza, protege ("los datos tenían 40% de missing y lo dijimos a tiempo") y detecta proyectos inviables antes de quemar horas
* quality gates (ej.: todas las variables del universo perfiladas, reporte de missing generado, candidatos a leakage listados)

> El EDA informa `04_feature_engineering`: esa spec puede refinarse a partir de los hallazgos. Aprender bins/imputaciones acá es solo exploratorio; los parámetros productivos se fijan en feature engineering (fit en train).

### 04_feature_engineering.md

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

### 05_modeling_validation.md

Debe definir:

* **baseline obligatorio**: regla simple, azar o el modelo/status quo actual del cliente — el modelo final debe superarlo (quality gate); sin lift demostrado vs status quo no hay business case
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

### 06_deployment_scoring.md

Debe definir:

* batch/API/manual
* frecuencia
* tabla o archivo de salida
* columnas finales
* versionado
* consumo operativo
* rollback

### 07_monitoring.md

Debe definir:

* PSI
* drift
* performance real
* alertas
* frecuencia
* responsables
* thresholds
* acciones correctivas

### 08_report.md

Debe definir (estándar completo en `informe-ejecutivo.md`):

* audiencia y piezas del entregable (deck ejecutivo / informe técnico / anexos)
* executive summary autocontenido, ≤ 1 página, respuesta primero (pyramid principle)
* estructura del informe
* so-what cuantificado por hallazgo (hallazgo → implicancia → recomendación → impacto → esfuerzo/owner)
* tablas y gráficos con assertion titles, fuente y fecha de corte
* narrativa ejecutiva
* anexos técnicos
* supuestos, limitaciones y condiciones de uso (obligatorio)
* quality gate: consistencia de cifras entre summary, cuerpo y anexos; cada cifra rastreable a un output

---

## B. Segmentación / clustering

Ejemplos: segmentación de consumo de tarjeta, segmentación RFM, clusters de comercios, perfiles de clientes.

Specs mínimas:

```text
specs/
├── 00_prd_reference.md
├── 01_population_scope.md
├── 02_data_snapshot.md
├── 03_eda.md
├── 04_feature_space.md
├── 05_clustering_validation.md
├── 06_segment_interpretation.md
├── 07_deployment_tagging.md
└── 08_report.md
```

Debe documentarse:

* población
* unidad de análisis
* EDA: distribuciones, missing, outliers y correlaciones de las variables de segmentación (spec `03_eda.md`)
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
