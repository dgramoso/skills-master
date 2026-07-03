---
name: strategic-planning
description: >
  Router de triage para problemas y decisiones estratégicas. No analiza nada por sí
  mismo: hace 1-2 preguntas de diagnóstico y deriva al skill correcto entre
  pensamiento-critico (problema difuso), strategic-problem-solving (opciones a
  evaluar) y premortem (plan ya elegido). Usar cuando el usuario invoca
  /strategic-planning explícitamente, o cuando tiene un problema o decisión
  estratégica pero NO está claro cuál de los tres skills corresponde. NO usar si el
  caso ya encaja de forma evidente en uno de los tres — invocar ese directamente.
---

# Strategic Planning — Router de triage

Este skill no ejecuta análisis. Su único trabajo es identificar en qué etapa de la
decisión está el usuario e invocar el skill correspondiente con el Skill tool.

## Triage

Evaluar en este orden con lo que ya se sabe de la conversación. Si falta información,
hacer **máximo 1-2 preguntas** — nunca un cuestionario.

1. **¿Ya hay un plan o decisión elegida, con coste de error alto?**
   → invocar `premortem`.
2. **¿Hay 2+ opciones concretas a comparar, evaluar o rankear?**
   → invocar `strategic-problem-solving`.
3. **¿El problema está difuso, el usuario está atascado, o hay suposiciones sin
   desafiar y ninguna opción sobre la mesa?**
   → invocar `pensamiento-critico`.

Pregunta de desambiguación típica (si nada de lo anterior es evidente):

> "¿En qué punto estás: (a) todavía no tengo claro el problema, (b) tengo opciones y
> no sé cuál elegir, (c) ya decidí y quiero estresar el plan?"

## Reglas

- Anunciar la derivación en una línea ("Esto es un caso para X porque Y") e invocar
  el skill de inmediato. No duplicar aquí ninguna fase de los skills destino.
- Si el usuario describe el caso con suficiente claridad, derivar sin preguntar nada.
- **Encadenamiento:** al terminar un skill hijo, ofrecer el siguiente paso natural del
  pipeline si aplica — pensamiento-critico produce opciones → ofrecer
  strategic-problem-solving; strategic-problem-solving elige ganadora de alto riesgo
  → ofrecer premortem. Ofrecer, no ejecutar automáticamente.
- Responder siempre en el idioma del usuario.
