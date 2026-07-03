---
name: pensamiento-critico
description: >
  Interrogatorio crítico de problemas y decisiones: deconstrucción por primeros
  principios, inversión, 5 porqués, consecuencias de segundo orden y premortem.
  Usar cuando el problema está difuso o mal definido, el usuario está atascado o
  dando vueltas sin avanzar, hay suposiciones sin desafiar, o pide explícitamente
  que lo interroguen. Disparadores — "estoy atascado", "no sé qué hacer con",
  "desafiá mi razonamiento", "ayúdame a pensar esto", "algo no está funcionando
  y no sé por qué", "cuestioná mis suposiciones", "pensamiento crítico".
  NO usar cuando el usuario ya tiene opciones claras a comparar y rankear, ni para
  preguntas directas que se responden sin taller.
---

# Pensamiento Crítico — Deconstrucción desde Primeros Principios

Este skill guía un interrogatorio en 5 fases: deconstruir el problema hasta los hechos demostrables, invertirlo, llegar a la causa raíz, trazar consecuencias de segundo orden y estresar la decisión con un premortem. **No des consejos genéricos.**

---

## Modo de trabajo (elegir al inicio, decírselo al usuario)

| Modo | Cuándo | Cómo opera |
|---|---|---|
| **Taller** (default) | El usuario tiene tiempo y el problema lo amerita | Fase a fase, esperando la respuesta del usuario antes de avanzar. |
| **Exprés** | El usuario tiene poco tiempo, o lo pide | Claude propone respuestas candidatas en cada fase (hechos vs. suposiciones, los porqués, los escenarios) y el usuario solo corrige. Una pasada completa en 2-3 turnos. |

Reglas de flexibilidad:
- Se puede **saltar una fase con justificación explícita** (decirlo en una línea, nunca en silencio). Ejemplos: Fase 0 si el problema ya viene concreto y medible; Fase 4 si todavía no hay decisión candidata (primero pasar por el puente de opciones).
- Si el usuario deja de responder o pide cerrar, completar lo que falte con supuestos marcados y entregar la síntesis y el memo.

---

## FASE 0 — Captura del Problema

**Antes de cualquier análisis, pedir explícitamente:**

> "Para trabajar bien esto, necesito que me respondas dos cosas de forma concreta:
> 1. ¿Cuál es el **problema** exacto? (qué está pasando, qué no está funcionando)
> 2. ¿Cuál es el **objetivo**? (qué resultado específico querés lograr)
>
> Evitá ser vago. Cuanto más concreto, mejor el análisis."

Mientras el usuario responde:
- Si algo suena a **suposición disfrazada de hecho**, señalarlo: *"Eso lo estás dando por sentado. ¿Podés demostrarlo?"*
- Si el objetivo es vago ("tener éxito", "mejorar"), presionar: *"¿Qué significa eso exactamente? ¿Cómo sabrías que lo lograste?"*

---

## FASE 1 — Deconstrucción del Problema

**No construyas sobre arena. Primero, desmontar.**

### 1A. Verdades Innegables
Identificar qué del problema es **verdad demostrable** vs. qué es interpretación, narrativa o suposición. Separar en dos columnas:

| ✅ Hecho demostrable | ❌ Suposición / Interpretación |
|---|---|
| ... | ... |

### 1B. Desafiar Suposiciones
Por cada suposición identificada, preguntar:
> *"¿Qué pasaría si esto fuera completamente falso? ¿Cambia el problema?"*

Si cambia el problema → la suposición es **fatal** y hay que resolverla primero.

### 1C. Reconstrucción desde Cero
Con solo los hechos demostrables, reformular el problema en una sola oración sin adjetivos ni narrativa. Si no se puede hacer, el problema no está bien definido aún.

---

## FASE 2 — Inversión: Garantizar el Fracaso

**No preguntar "¿cómo tengo éxito?" — preguntar "¿cómo GARANTIZO el fracaso?"**

Listar exhaustivamente:
- Todas las formas de arruinar esto
- Las peores decisiones posibles a tomar
- Las suposiciones que, si resultan falsas, lo destruyen todo
- Los comportamientos que llevan al peor resultado
- Los momentos donde podría sabotearse sin darse cuenta

**Formato de output:**

```
MAPA DE FRACASOS
─────────────────────────────────────────────────────
❌ [Forma de fracasar]  →  ✅ [Acción concreta opuesta]
❌ [Forma de fracasar]  →  ✅ [Acción concreta opuesta]
...
```

Cada inversión debe ser **una acción específica**, no un principio vago.

---

## FASE 3 — Los 5 Por Qués

**Profundizar hasta la causa raíz estructural.**

Tomar el problema central o la suposición más peligrosa identificada y ejecutar:

```
PROBLEMA:  [enunciado]
↓ ¿Por qué ocurre eso? (1)  → [respuesta]
↓ ¿Por qué ocurre eso? (2)  → [respuesta]
↓ ¿Por qué ocurre eso? (3)  → [respuesta]
↓ ¿Por qué ocurre eso? (4)  → [respuesta]
↓ ¿Por qué ocurre eso? (5)  → [respuesta]
★ CAUSA RAÍZ ESTRUCTURAL: [síntesis]
```

**Reglas de los 5 Por Qués:**
- Si la respuesta es vaga ("porque así es", "siempre fue así", "no sé"), **no aceptar**. Presionar: *"Eso no es una causa. ¿Qué decisión, sistema o comportamiento concreto lo genera?"*
- Cada respuesta debe ser más profunda que la anterior.
- El objetivo es llegar a algo que, si se resuelve, resuelve el origen — no el síntoma.
- Se puede bifurcar: si una respuesta revela dos causas posibles, explorar ambas.
- **Distinguir causa raíz accionable de restricción.** Si la cadena termina en algo que el usuario no controla ("porque el mercado es así", "porque el regulador lo exige"), eso es una restricción, no una causa raíz útil. Redefinir el problema dentro de la esfera de control del usuario y volver a correr la cadena desde ahí.

---

## PUENTE — Generación de Opciones (solo si no hay decisión sobre la mesa)

La Fase 4 necesita una decisión candidata. Si el usuario llegó sin ella (el caso típico de "estoy atascado"):

1. A partir de la causa raíz, generar **2-3 cursos de acción candidatos**, concretos y distintos entre sí (no variantes cosméticas del mismo movimiento).
2. Presentarlos en una línea cada uno: qué se hace, qué ataca de la causa raíz, costo aproximado de estar equivocado.
3. Pedir al usuario que elija uno (o que proponga el propio).
4. Correr las Fases 4 y 5 sobre esa elección.

Si el usuario ya trae una decisión, saltar este puente y decirlo.

---

## FASE 4 — Consecuencias en 3 Capas

**La mayoría piensa en qué pasa ahora. Los buenos decisores piensan en qué pasa DESPUÉS.**

Confirmar la decisión a analizar (la que trajo el usuario o la elegida en el puente). Luego trazar las consecuencias en **ambos escenarios**, en 3 capas temporales:

### Escenario A: CON la decisión tomada
```
CAPA 1 — ¿Qué pasa inmediatamente?
→ [consecuencias en días/semanas]

CAPA 2 — ¿Qué provoca eso después?
→ [consecuencias en 1-3 meses, derivadas de la capa 1]

CAPA 3 — ¿Qué provoca ESO en 6-12 meses?
→ [consecuencias sistémicas, cambios de estado, puntos de no retorno]
```

### Escenario B: SIN tomar la decisión (status quo)
```
CAPA 1 — ¿Qué pasa inmediatamente?
→ [qué continúa igual, qué se deteriora]

CAPA 2 — ¿Qué provoca eso después?
→ [acumulación de consecuencias por inacción]

CAPA 3 — ¿Qué provoca ESO en 6-12 meses?
→ [costo real del no-hacer]
```

**Ser brutal.** No suavizar los escenarios negativos. El valor está en ver lo que se prefiere no ver.

---

## FASE 5 — Premortem: El Fracaso Ya Ocurrió

> Si el coste de equivocarse es alto (dinero, reputación, irreversibilidad), ofrecer correr el skill `premortem` completo (subagentes paralelos + informe HTML) en lugar de esta versión reducida.

**Asumir que la decisión tomada llevó al fracaso. Han pasado 6 meses.**

> *"Imaginate que tomaste la decisión. Estamos 6 meses después y fracasó. No fue lo que esperabas. Ahora trabajamos hacia atrás."*

### 5A. Escenarios de Fracaso Concretos
Generar mínimo 3 escenarios específicos de cómo pudo fallar:

```
ESCENARIO 1: [Nombre del fracaso]
- ¿Qué salió mal?
- ¿Cuándo se hizo evidente?
- ¿Por qué no se vio venir?

ESCENARIO 2: [Nombre del fracaso]
...

ESCENARIO 3: [Nombre del fracaso]
...
```

### 5B. Plan de Acción Preventiva HOY
Por cada escenario:

```
ESCENARIO 1 → ACCIÓN PREVENTIVA HOY: [qué hacer esta semana para que eso no ocurra]
ESCENARIO 2 → ACCIÓN PREVENTIVA HOY: [...]
ESCENARIO 3 → ACCIÓN PREVENTIVA HOY: [...]
```

**"Hoy" es literal.** No "en algún momento", no "habría que". Una acción con verbo en infinitivo que puede ejecutarse en los próximos 7 días.

---

## CIERRE — Síntesis y memo de decisión

1. **Síntesis ejecutiva** en el chat (5-7 líneas): problema real, causa raíz, decisión recomendada, mayor riesgo y primera acción.
2. **Ofrecer el memo de decisión** como archivo de una página (`memo-decision-<tema>.md` donde el usuario indique, o en el directorio de trabajo):

```markdown
# Memo de decisión — [tema]
Fecha: [fecha]

## Problema reformulado
[una oración, sin adjetivos]

## Hechos vs. suposiciones
| ✅ Hecho | ❌ Suposición (y si es fatal) |

## Causa raíz estructural
[síntesis + si es accionable o restricción]

## Mapa de fracasos (top 3-5)
❌ → ✅

## Consecuencias
- Con la decisión: [capa 3 resumida]
- Sin la decisión: [capa 3 resumida]

## Decisión y primera acción
[decisión] — [acción ejecutable esta semana]

## Acciones preventivas (próximos 7 días)
1. ...
2. ...
3. ...

## Supuestos pendientes de validar
- ...
```

---

## Quality gates

Antes de cerrar, verificar:
- El problema quedó reformulado en una sola oración con solo hechos demostrables.
- Se identificó al menos una suposición fatal, o se declaró explícitamente que no hay.
- La causa raíz es accionable (o se redefinió el problema dentro de la esfera de control).
- Hay ≥3 escenarios de fracaso, cada uno con una acción preventiva ejecutable en ≤7 días.
- Se entregó la síntesis ejecutiva y se ofreció el memo.

---

## Principios de conducción

- **En modo taller, no des el análisis en un solo bloque.** Trabaja fase a fase, esperando la respuesta del usuario antes de avanzar. En modo exprés, proponé y dejá corregir.
- **No suavices.** Este proceso sirve exactamente para ver lo que es incómodo ver.
- **No valides respuestas vagas.** Cada respuesta vaga es una oportunidad perdida de ir más profundo.
- **Presiona por especificidad.** "¿Podés darme un ejemplo concreto?" es una pregunta válida en cualquier fase.
- **Señala cuando algo no suma.** Si el objetivo declarado contradice las acciones descritas, decirlo.
- **Responder siempre en el idioma del usuario.**
