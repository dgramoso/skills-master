# Estándar de informe ejecutivo

> Parte de la skill `analytics-workflow`. Aplica a los tres tipos de proyecto (supervisado, clustering, dashboard). Template copiable en `templates/informe_ejecutivo.md.tmpl`.

Un informe técnicamente correcto pero consultivamente plano no está listo para entregar. Este estándar es obligatorio para todo entregable cliente-facing.

---

## Pyramid principle: respuesta primero

El informe empieza por la respuesta a la pregunta de negocio, no por la metodología.

* **Executive summary ≤ 1 página, autocontenido**: un gerente debe poder leer solo esa página y saber qué se encontró, qué se recomienda y qué impacto tiene. Sin jerga técnica.
* Estructura del summary: Situación → Complicación → Resolución (SCR), o directamente respuesta → 3-5 argumentos de soporte.
* La metodología va después (o en anexo). El cliente no compra el método, compra la decisión informada.

---

## Estándar de recomendación (so-what)

Ningún hallazgo se reporta suelto. Cadena obligatoria:

```text
hallazgo → implicancia → recomendación → impacto estimado → esfuerzo/owner
```

Ejemplo:

> **Hallazgo:** la mora se concentra en el segmento sin historia crediticia (bad rate 12% vs 4% general).
> **Implicancia:** el cutoff actual aprueba a este segmento igual que al resto.
> **Recomendación:** cutoff diferencial de 680 para clientes sin historia.
> **Impacto estimado:** reducción de ~18% de la mora esperada de originación, al costo de ~6% de aprobación (strategy table, anexo B).
> **Esfuerzo:** cambio de parámetro en el motor de decisión; owner: equipo de riesgo.

El impacto se estima en plata o volumen siempre que los datos lo permitan. Si no, decirlo explícito: "no cuantificable con los datos disponibles porque X".

---

## Piezas del entregable

Tres piezas con audiencias distintas (acordadas en el intake):

| Pieza | Audiencia | Contenido |
|---|---|---|
| Deck ejecutivo | Sponsor / gerencia | Respuesta, recomendaciones, impacto. 10-15 slides máx. |
| Informe técnico | Analistas / riesgo del cliente | Metodología, validación, decisiones, limitaciones |
| Anexos | Auditoría / quien herede el modelo | Tablas completas, diccionario, specs, reproducibilidad |

En proyectos chicos, deck e informe pueden ser un solo documento con el exec summary como primera sección — pero la lógica de audiencias se mantiene.

---

## Supuestos, limitaciones y condiciones de uso (obligatorio)

Sección propia en el informe técnico, siempre:

* Supuestos metodológicos (población, ventanas, exclusiones, representatividad)
* Limitaciones de datos (missing, historia corta, sesgos conocidos)
* **Condiciones de uso**: para qué sirve el resultado y para qué NO ("no debe usarse para decisiones individuales automáticas sin revisión", "no aplica a la población X")
* Vigencia esperada y disparadores de recalibración

Protege al cliente (uso correcto) y al consultor (responsabilidad acotada).

---

## Estándar de visualización

* **Assertion titles**: el título del gráfico afirma el hallazgo ("La mora se concentra en el segmento joven-digital"), no describe el eje ("Mora por segmento").
* Una idea por gráfico. Si necesita explicación oral, está mal diseñado.
* Fuente y fecha de corte en cada gráfico y tabla.
* Paleta consistente en todo el entregable; el color señala, no decora.
* Orden con intención: barras ordenadas por valor, salvo que el orden natural (tiempo, bins) importe.

---

## Quality gate: consistencia de cifras

Parte del QA pre-entrega (ver `quality-gates.md`):

* Mismo número en exec summary, cuerpo y anexos.
* Redondeo consistente (definir la regla: ej. métricas con 2 decimales, porcentajes con 1).
* Cada cifra del informe es rastreable a un output del pipeline.

---

## Checklist del informe

* [ ] Executive summary autocontenido, ≤ 1 página, respuesta primero
* [ ] El informe responde la pregunta de negocio del PRD
* [ ] Cada hallazgo clave con so-what cuantificado (o "no cuantificable porque X")
* [ ] Sección de supuestos, limitaciones y condiciones de uso
* [ ] Assertion titles + fuente y fecha de corte en cada gráfico/tabla
* [ ] Cifras consistentes y rastreables a outputs
* [ ] Narrativa automática (Claude API) revisada por el analista, si se usó
