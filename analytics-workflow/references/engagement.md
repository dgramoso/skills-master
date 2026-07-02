# Gestión del engagement

> Parte de la skill `analytics-workflow`. Artefactos cliente-facing del proyecto.
> Templates copiables: `templates/decision_log.md.tmpl`, `templates/minuta.md.tmpl`,
> `templates/status_report.md.tmpl`, `templates/acta_cierre.md.tmpl`.

Todos los artefactos de esta sección viven en `engagement/` dentro del repo del proyecto:

```text
engagement/
├── intake.md            # checklist de kickoff completado
├── decision_log.md      # aprobaciones del cliente, con fecha
├── minutas/             # una por reunión relevante
├── status/              # status semanal o por hito
└── acta_cierre.md       # al terminar
```

---

## Intake / kickoff (estado `kickoff`)

Ningún PRD se escribe sin completar el intake. Capturar en `engagement/intake.md`:

**Negocio**

* Sponsor (quién paga / decide) y usuarios finales del entregable
* Pregunta de negocio en una oración
* Definición de éxito **del cliente** (qué tiene que pasar para que considere el proyecto exitoso)
* Decisiones que se tomarán con el resultado
* Plazo esperado e hitos intermedios

**Datos**

* Fuentes disponibles, quién da acceso y cuándo
* Período de historia disponible
* Restricciones: confidencialidad, datos personales, salida de datos del entorno del cliente
* Evaluación de viabilidad: ¿los datos alcanzan para responder la pregunta? Si hay dudas, condicionar el alcance al diagnóstico de calidad de datos (spec de EDA)

**Expectativas**

* Calibrar expectativas de performance **antes** de ver los datos: no prometer métricas concretas antes del EDA
* Entregables acordados: ¿deck, informe, código, modelo productivo, monitoreo?
* Quién opera el modelo después de la entrega (input para el handover)

**Política de datos del cliente**

* Dónde viven los datos durante el proyecto (máquina del consultor / entorno del cliente / cloud)
* Anonimización o seudonimización requerida
* Qué pasa con los datos al cierre (destrucción, devolución, retención)
* ¿Está permitido enviar métricas agregadas a APIs de terceros (ej. narrativa automática vía Claude API)? Si no está permitido, desactivarla — ver `claude-api.md`

---

## Decision log

`engagement/decision_log.md` — registro cronológico de toda decisión **aprobada por el cliente**. Distinto de CONTEXT.md / specs / ADRs (internos): esto es lo que protege el alcance y evita re-trabajo.

Formato (template en `templates/decision_log.md.tmpl`):

| Fecha | Decisión | Quién aprobó | Contexto / alternativas descartadas |
|---|---|---|---|
| 2026-07-15 | Horizonte de predicción: 90 días | J. Pérez (gerente riesgo) | Se descartó 180 días por madurez de cartera |

Reglas:

* Si el cliente no lo aprobó por escrito (mail, minuta, decision log revisado en reunión), no está aprobado.
* Toda respuesta del cliente durante un grill que fije alcance o metodología entra acá, **además** de su documento interno (spec / CONTEXT / ADR según la tabla de persistencia).

---

## Minutas

Una minuta por reunión que tome decisiones (template en `templates/minuta.md.tmpl`): fecha, asistentes, temas, decisiones (→ decision log), pendientes con responsable y fecha.

Enviar al cliente después de cada reunión. Minuta no observada en N días hábiles (definir N en el intake) se considera aceptada.

---

## Status report

Cadencia semanal o por hito (template en `templates/status_report.md.tmpl`). Una página máximo:

* Avance desde el último status (hecho, no actividad)
* Próximos pasos
* Riesgos y bloqueos
* **Decisiones pendientes del cliente**, con fecha límite — es la sección que más acelera proyectos

---

## Change request liviano

Cuando el cliente pide algo fuera del PRD: registrar qué pide, impacto en plazo/esfuerzo/precio, y decisión (aceptado con ajuste / diferido a fase 2 / rechazado). Va al decision log. Sin este registro, todo pedido "chiquito" es scope creep.

---

## Cierre y handover (estado `handover`)

`engagement/acta_cierre.md` (template en `templates/acta_cierre.md.tmpl`):

* Entregables entregados (lista con versión y fecha)
* Qué queda soportado y qué no (y por cuánto tiempo)
* **Monitoreo:** quién corre el PSI / performance y con qué frecuencia — el cliente con instrucciones entregadas, o el consultor bajo acuerdo de soporte. La spec de monitoring debe ser ejecutable por quien la herede.
* Datos del cliente: destrucción / devolución según la política del intake, con confirmación
* Condiciones de re-engagement (recalibración, v2, nuevas poblaciones)
* Aceptación del cliente
