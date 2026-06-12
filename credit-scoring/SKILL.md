---
name: credit-scoring
description: Skill para desarrollar, auditar, refactorizar o documentar proyectos de credit scoring con metodologia tipo Naeem Siddiqi. Usar cuando se trabaje con ingesta y definicion de target, integracion de datos, limpieza, feature engineering, WOE/IV, regresion logistica con lrm, validacion OOT, PSI, KS, strategy tables, monitoreo, modelos e informes HTML finales para cliente.
---

# Credit Scoring R Siddiqi

Usar esta skill para proyectos de credit scoring, desde datos crudos hasta un informe HTML final para cliente. Priorizar trazabilidad, validacion, interpretabilidad regulatoria y un pipeline reproducible.

## Principios

- Mantener el flujo modular por scripts numerados y validaciones espejo.
- Separar datos crudos, datos procesados, outputs tecnicos, graficos, modelos, reportes e informe final.
- Documentar decisiones de negocio: definicion de default, ventana de performance, exclusiones, poblacion elegible, fecha de observacion y fecha de maduracion.
- Evitar leakage entre variables explicativas y target.
- Preferir modelos logisticos interpretables con WOE/IV, monotonicidad razonable, estabilidad y sentido de negocio.
- Tratar cada output como auditable: incluir conteos, tasas, fechas, criterios y checks.
- Recomendar mejoras en el proceso toda vez que se detecte alguna oportunidad.

## Estructura Esperada

Trabajar con esta estructura cuando el proyecto no tenga una convencion mejor:

```text
credit_scoring_R/
|-- scripts/
|   |-- 00_config.R
|   |-- 00_run_pipeline.R
|   |-- 01_ingesta_y_target.R
|   |-- 02_bcu_integracion_datos.R
|   |-- 03_limpieza_y_features.R
|   |-- 04_modelizacion.R
|   |-- 05_informe_cliente.R
|   `-- mis_funciones.r
|-- datos/
|-- eda/
|-- modelos/
|-- reportes/
|-- graficos/
`-- informe/
```

Si los scripts reales tienen nombres similares, respetar sus nombres existentes y adaptar el flujo sin romper compatibilidad.

## Flujo De Trabajo

### 1. Configuracion

- Centralizar paths, semillas, fechas de corte, parametros de target, poblaciones, nombres de archivos y librerias en `00_config.R`.
- Usar `00_run_pipeline.R` para ejecutar el proceso completo en orden.
- Hacer que cada script pueda correr de forma independiente despues de cargar la configuracion.

### 2. Ingesta Y Target

En `01_ingesta_y_target.R`:

- Cargar fuentes base y conservar una tabla de auditoria de filas, claves, fechas y duplicados.
- Definir claramente el target: evento malo, ventana de observacion, ventana de performance, exclusiones e indeterminados.
- Crear variables como `target`, `bad`, `good`, `indeterminate`, `sample_flag`, `periodo_obs` y `periodo_perf` cuando apliquen.
- Validar conteos por poblacion, distribucion good/bad/indeterminado, tasa de malos, duplicados y consistencia temporal.

### 3. Integracion De Datos

En `02_bcu_integracion_datos.R`:

- Integrar datos externos o BCU por claves y fechas correctas.
- Evitar usar informacion posterior a la fecha de observacion.
- Mantener trazabilidad de joins, cobertura, registros no matcheados y variables agregadas.
- Validar cobertura por fuente, tasas de match, missingness inducida, duplicacion post-join y consistencia de fechas.

### 4. Limpieza Y Feature Engineering

En `03_limpieza_y_features.R`:

- Estandarizar tipos, unidades, categorias, outliers y valores especiales.
- Crear features con sentido crediticio: antiguedad, mora historica, utilizacion, endeudamiento, capacidad de pago, consultas, comportamiento reciente, saldos, ratios y tendencias.
- Separar variables candidatas, variables excluidas y motivos de exclusion.
- Revisar missingness, rangos, cardinalidad, outliers, distribuciones, estabilidad por periodo y relacion preliminar con target.

### 5. WOE, IV Y Binning

- Construir bins interpretables, estables y con volumen suficiente.
- Buscar monotonicidad razonable del bad rate cuando tenga sentido de negocio.
- Calcular WOE e IV por variable.
- Registrar merges de bins, bins especiales, missing, outliers y justificacion de decisiones.
- Excluir variables por bajo IV, inestabilidad, alta correlacion, leakage, mala interpretacion o debilidad operacional.

### 6. Modelizacion

En `04_modelizacion.R`:

- Separar development, validation y out-of-time si existen fechas suficientes.
- Entrenar una regresion logistica interpretable, preferentemente con `rms::lrm` si el proyecto ya sigue esa convencion.
- Controlar signo esperado, significancia, colinealidad, estabilidad y aporte incremental.
- Guardar modelo `.rds`, transformaciones, metadata de variables, bins y parametros de score.

Reportar como minimo:

- AUC/Gini, KS, matriz de confusion o performance por umbral si aplica.
- Lift o deciles de score.
- Coeficientes, odds ratios o interpretacion de drivers.
- Validar discriminacion con KS, AUC/Gini y deciles.
- Calcular PSI de score y variables relevantes entre desarrollo, validacion, OOT y periodos recientes.

### 7. Validacion, PSI Y Monitoreo

- Revisar calibracion, bad rate por banda, estabilidad de bins y drift de poblacion.
- Preparar strategy tables con bandas de score, tasas de aprobacion, bad rate, odds, volumen, acumulados y tradeoffs.
- Comparacion train/validation/OOT.

### 8. Informe Cliente

En `05_informe_cliente.R` o R Markdown/Quarto:

- Generar un HTML final estilo informe ejecutivo.
- Incluir objetivo, datos, poblacion, definicion de target, metodologia, validaciones, modelo final, drivers, estrategia sugerida, monitoreo y anexos tecnicos.
- Mostrar tablas y graficos que soporten decisiones, no metricas sueltas sin interpretacion.
- Separar conclusiones ejecutivas de anexos tecnicos.

## Funciones Compartidas

Usar `mis_funciones.r` para helpers reutilizables:

- lectura/escritura segura,
- auditorias de tablas,
- calculo de WOE/IV,
- KS/AUC/Gini,
- PSI,
- tablas de estrategia,
- graficos estandar,
- exportacion de reportes.

Evitar duplicar logica entre scripts si puede vivir como funcion clara y testeable.

## Entregables

Al finalizar, producir o dejar preparado:

- pipeline reproducible,
- outputs tecnicos,
- tablas de auditoria,
- graficos,
- modelo `.rds`,
- validacion train/validation/OOT,
- monitoreo PSI/KS,
- strategy tables,
- informe HTML final para cliente.

## Estilo De Respuesta

- Responder en espanol si el usuario trabaja en espanol.
- Ser concreto, tecnico y orientado a negocio.
- Cuando edites codigo, conservar nombres y convenciones existentes.
- Explicar riesgos crediticios o metodologicos con claridad: leakage, mala definicion de target, baja estabilidad, sobreajuste, variables no operables o reglas dificiles de justificar.
