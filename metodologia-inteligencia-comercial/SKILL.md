---
name: metodologia-inteligencia-comercial
description: >
  Use when developing commercial/customer analytics models: churn y retención,
  propensión de compra, cross-sell/next best offer, priorización de cobranza,
  campañas y su medición. Triggers: "churn", "retención", "propensión",
  "cross-sell", "next best action", "next best offer", "campaña", "uplift",
  "priorización de gestión", "cobranza" (no crediticio-regulatorio), "RFM
  con acción comercial". NO usar para credit scoring regulatorio (usar
  metodologia-credit-scoring) ni dashboards puros (analytics-workflow tipo C).
---

# Metodología de Inteligencia Comercial

Espejo liviano de `metodologia-credit-scoring` para modelos comerciales. El **proceso** (SDD, specs, gates, engagement, entrega) es el de `analytics-workflow`; la **ejecución e interpretación** es la de `advanced-analytics`; la **medición del impacto** de toda acción resultante es `advanced-analytics/references/medicion-impacto.md`. Esta skill agrega solo lo específico del dominio comercial. Las rutas a otras skills viven en `~/.claude/skills/`.

**La diferencia central con crédito:** en scoring crediticio el entregable es el score; en inteligencia comercial el entregable es la **acción** (a quién contactar, con qué oferta, con qué prioridad) y su medición. Un modelo comercial sin estrategia de acción ni diseño de medición no es un entregable — es un ranking sin consecuencias.

---

## Definición del evento (el "target" comercial)

Mismo rigor que la definición de malo en crédito (`metodologia-credit-scoring`, sección "Definición de target y ventanas" — ventana de observación, ventana de performance, población elegible, leakage). Lo específico:

| Evento | Trampa típica | Regla |
|---|---|---|
| Churn contractual (baja formal) | Confundir fecha de solicitud de baja con fecha efectiva | El evento es la solicitud (ahí se podía actuar); documentar cuál se usa |
| Churn no contractual (el cliente deja de operar sin avisar) | No existe fecha de baja: hay que **definir** inactividad | "Sin transacciones en N meses" con N justificado empíricamente (distribución de gaps de actividad de clientes que volvieron vs. no volvieron — el equivalente comercial del roll rate) |
| Compra / conversión | Target armado sobre campañas históricas con targeting sesgado | El modelo aprende a quién se contactó, no quién compra. Documentar el sesgo; si hay historia de contactos aleatorios o cuasi-aleatorios, usarla |
| Cura en cobranza | Definir cura como pago total cuando el negocio acepta parciales | Definición de cura con el negocio (pago total / acuerdo / N cuotas al día), misma lógica que la definición de malo |

**Regla:** la definición del evento se justifica con datos y se aprueba con el cliente en un gate, igual que el target crediticio. Va al decision log.

---

## Playbooks por caso de uso

### Churn / retención

* Score de riesgo de fuga **por sí solo no alcanza**: priorizar por `riesgo × valor del cliente` — retener a un cliente de bajo valor con alto riesgo puede costar más de lo que rinde.
* Output operativo: lista priorizada con score, valor, y acción sugerida por segmento (oferta de retención A/B/no contactar).
* La acción de retención se lanza **con grupo de control** — es el caso de manual de `medicion-impacto.md` (los "sure things" y los "do-not-disturb" existen: contactar puede acelerar la baja).

### Propensión / cross-sell / next best offer

* Una propensión por producto + reglas de elegibilidad y prioridad entre ofertas (no ofrecer el producto que ya tiene; margen y límite de contactos como desempate) = next best offer. No hace falta un framework: es una tabla de decisión documentada en la spec.
* Cuidado con el sesgo de targeting histórico (tabla de arriba). Si el modelo solo vio contactados, decirlo en las limitaciones del informe.

### Priorización de cobranza (gestión, no regulatorio)

* Priorizar por `probabilidad de cura × saldo recuperable` (y costo del canal): la gestión cara (llamada) para cuentas donde mueve la aguja, la barata (SMS/mail) para el resto.
* Champion/challenger de **estrategias de contacto** (intensidad, canal, momento), no solo de modelos — con control, vía `medicion-impacto.md`.
* Roll rates, definición de mora y todo lo regulatorio: `metodologia-credit-scoring`.

### Segmentación con acción comercial (RFM y afines)

* Proceso: `analytics-workflow` tipo B (clustering) + `advanced-analytics` (perfilado y accionabilidad).
* Lo que esta skill agrega: cada segmento termina en una fila de la tabla `segmento → acción → owner → medición`. Un segmento sin acción asociada es descriptivo, no comercial.

---

## La acción es el entregable

Toda entrega incluye, además del modelo:

1. **Tabla de acción**: banda de score (o segmento) → acción concreta → canal → capacidad requerida.
2. **Restricción de capacidad operativa**: el call center hace X gestiones/día, el presupuesto de ofertas es $Y — el cutoff operativo sale de la capacidad, no solo del score. Documentar el cutoff económico igual que en `scorecard-y-strategy-tables.md` (versión simplificada: contactos disponibles × conversión incremental esperada × margen − costo).
3. **Diseño de medición**: control, fecha de lectura y métrica de decisión definidos ANTES del lanzamiento (`medicion-impacto.md`). Se entrega junto con el modelo, no después.

---

## Errores comunes del dominio

| Error | Corrección |
|---|---|
| Churn no contractual sin justificar la ventana de inactividad | Justificarla con la distribución de gaps de actividad (gate con el cliente) |
| Propensión entrenada sobre targeting histórico sesgado, leída como propensión poblacional | Documentar el sesgo; buscar contactos aleatorios históricos; considerar uplift en la segunda iteración |
| Priorizar por score ignorando valor del cliente o saldo | Priorización = probabilidad × valor, siempre |
| Lanzar la campaña a todos "para no perder ventas" | Sin control no hay impacto demostrable; decisión del cliente al decision log |
| Cutoff por score ignorando capacidad operativa | El cutoff sale de capacidad y economía, no de la distribución del score |
| Entregar el modelo sin tabla de acción ni diseño de medición | No está terminado: la acción es el entregable |

---

## Flujo y referencia rápida

El flujo es el de `analytics-workflow` (preventa → intake → PRD → specs → grill → implementación → validación → informe → entrega), tipo A (supervisado) o B (clustering) según el caso. Momentos específicos de esta skill:

| Momento | Qué usar |
|---|---|
| Definición del evento y ventanas | Esta skill (tabla de eventos) + gate con cliente, patrón de `metodologia-credit-scoring` |
| Modelado e interpretación | `advanced-analytics` (baseline obligatorio, drivers, so-what) |
| Estrategia de acción y cutoff operativo | Esta skill ("La acción es el entregable") |
| Diseño de medición, antes de lanzar | `advanced-analytics/references/medicion-impacto.md` |
| Lectura del piloto y decisión de escalar | `medicion-impacto.md` (output estándar) + informe según `informe-ejecutivo.md` |
