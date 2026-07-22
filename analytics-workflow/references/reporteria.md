# Reportería como producto: KPIs, data contract y QA de cifras

> Parte de la skill `analytics-workflow`. Profundiza el tipo C de `specs-por-tipo.md` (dashboard / reportería). El estándar visual y de narrativa está en `informe-ejecutivo.md` y en la skill `dataviz` — esta referencia cubre lo que hace que un reporte recurrente sea confiable en el tiempo.

Un dashboard que se entrega una vez es un informe. Un reporte **recurrente** es un producto: sus cifras se van a comparar mes contra mes, y cualquier inconsistencia silenciosa destruye la confianza en todo el producto. Estas cuatro piezas son el mantenimiento preventivo.

---

## 1. Diccionario de KPIs (la pieza central)

Un archivo `governance/kpi_dictionary.md` (o tabla equivalente) con un registro por KPI:

```text
kpi | definición exacta (fórmula) | fuente (tabla.campo) | filtros/exclusiones | granularidad | owner de la definición | vigente desde
```

Reglas:

* **Una definición por KPI.** Si ventas lo calcula distinto que finanzas, el reporte usa UNA y lo dice ("venta neta según definición de finanzas, difiere del reporte comercial en X").
* **Definición exacta = fórmula reproducible**, no prosa: "monto facturado − notas de crédito, excluye anulaciones y ventas intercompany, fecha contable" — no "las ventas del mes".
* **Toda definición tiene owner del lado del cliente.** Los cambios de definición los aprueba el owner, no el consultor.

### Versionado de definiciones

El dolor clásico: "la venta neta cambió de definición en marzo y nadie lo registró" — y las series históricas quedan incomparables en silencio. Cada cambio de definición registra:

```markdown
## venta_neta — v2 (vigente desde 2026-03-01)
- Cambio: se excluyen ventas intercompany (antes incluidas)
- Aprobó: [owner], [fecha]
- Efecto: la serie histórica NO se recalcula / SÍ se recalcula desde [fecha]
- El reporte muestra nota de quiebre de serie en los gráficos afectados
```

Un quiebre de definición sin nota visible en el gráfico es un error de entrega, no un detalle.

---

## 2. Data contract con la fuente

Por cada fuente que alimenta el reporte, acordar y documentar:

* Tabla/vista/archivo, campos usados y granularidad esperada.
* Frecuencia y horario de actualización de la fuente (y qué pasa si el reporte corre antes de que la fuente cierre — el clásico "los datos del lunes están incompletos").
* Señal de completitud: cómo se sabe que el período está cerrado (flag, conteo esperado, fecha de última carga).
* Quién avisa si la fuente cambia de estructura, y qué pasa si no avisa (el quality gate de abajo lo detecta).

---

## 3. QA de cifras contra el sistema origen

Antes de la primera entrega y ante cada cambio relevante:

* **Reconciliación**: los totales del reporte contra el sistema origen o el reporte oficial del cliente, con tolerancia definida (idealmente 0; si hay diferencia conocida, documentada y explicada en el reporte).
* **Quality gates automáticos en cada refresh** (patrón de `quality-gates.md`):
  * conteo de filas del período dentro del rango esperado
  * suma de control del KPI principal contra la fuente
  * sin fechas futuras ni períodos faltantes en la serie
  * variación mes contra mes dentro de un rango plausible — si un KPI salta ±X%, el refresh alerta en lugar de publicar en silencio
* Un reporte que publica cifras incorrectas sin alertar es el equivalente en reportería del script que falla silenciosamente.

---

## 4. Refresh y ownership (handover)

Definido antes de la entrega, en el acta de cierre (`engagement.md`):

* Quién corre el refresh (cliente o consultor), con qué frecuencia, con qué instrucciones.
* Qué hacer cuando un quality gate falla: a quién se avisa, se publica o no se publica.
* Vigencia: cuándo se revisan las definiciones y el layout (ej. semestral), y qué dispara una revisión anticipada (cambio de fuente, cambio de negocio).

---

## Checklist específico de reportería (además del genérico)

* [ ] Diccionario de KPIs completo, con owner y fórmula reproducible por KPI
* [ ] Cambios de definición versionados y con nota de quiebre visible en los gráficos afectados
* [ ] Data contract documentado por fuente, con señal de completitud
* [ ] Reconciliación inicial contra sistema origen registrada
* [ ] Quality gates automáticos en el refresh (conteos, sumas de control, saltos implausibles)
* [ ] Refresh y ownership definidos en el acta de cierre
* [ ] Fecha de corte y fuente visibles en cada vista (estándar `informe-ejecutivo.md`)
