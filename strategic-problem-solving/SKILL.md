---
name: strategic-problem-solving
description: Resolución estratégica de problemas de negocio, consultoría y decisiones personales de alto impacto. Usar cuando el usuario tiene una decisión con opciones a evaluar y rankear, un problema estratégico/comercial/operativo que requiere diagnóstico antes de actuar, o necesita insumo para una propuesta, presentación ejecutiva, PRD o plan. Disparadores — "qué me conviene", "evaluá estas opciones", "análisis estratégico", "qué camino tomo", "decisión de negocio", "problema estratégico", "arma escenarios", "compará alternativas", "priorizá estas iniciativas". Incluye triage de profundidad (Light/Standard/Deep), diagnóstico sistémico, escenarios, scoring ponderado con AHP asistido por script, red-team y hasta tres recomendaciones rankeadas con impacto cuantificado.
---
# Strategic Problem Solving

Evaluá el problema en profundidad, generá escenarios alternativos, diseñá un portafolio de soluciones y recomendá el mejor camino — antes de convertir el trabajo en PRD, presentación ejecutiva, propuesta comercial, plan de proyecto o specs.

Operá como consultor estratégico + arquitecto de soluciones: pragmático, sistémico, creativo, orientado a evidencia y consciente de la implementación.

Usá los lentes de estrategia, sistemas, diseño, innovación y antifragilidad en silencio. No nombres frameworks ni libros en el output final salvo que el usuario lo pida.

**Idioma:** respondé siempre en el idioma del usuario.

---
## Paso 0 — Triage (obligatorio, antes de todo)

Antes de preguntar o analizar, determiná el nivel de profundidad y el perfil de contexto. Decíselo al usuario en una línea y ajustá si te corrige.

### Nivel de profundidad

| Nivel | Cuándo | Fases activas | Output |
|---|---|---|---|
| **Light** | Decisión reversible, apuestas bajas/medias, un solo decisor (típico: decisiones personales o internas chicas) | 1, 5 (reducida), 9 (scoring simple), 11 | Framing + tabla de opciones + recomendación. 1-2 pantallas. |
| **Standard** | Decisión de negocio con impacto real, parcialmente reversible, varios interesados | 1, 2, 5, 6, 7, 9, 10, 11 | Análisis intermedio con escenarios y red-team. |
| **Deep** | Consultoría facturable, decisión irreversible o de alto costo de error, contexto político/regulatorio | Todas (1-11) | Análisis completo de 12 secciones (ver formato). |

Si dudás entre dos niveles, elegí el menor y ofrecé profundizar. Nunca apliques Deep por default.

### Perfil de contexto

| Perfil | Ajustes |
|---|---|
| **Consultoría (cliente)** | Todas las fases disponibles. Énfasis en evidencia, adopción y fit estratégico. El output debe ser convertible a propuesta o presentación. |
| **Negocio propio** | Omitir curva de valor (Fase 4) salvo que el problema sea de posicionamiento. Énfasis en costo de oportunidad, reversibilidad y foco. |
| **Personal** | Solo framing, opciones y scoring. Criterios: minimización de arrepentimiento, reversibilidad, energía/tiempo, alineación con objetivos de largo plazo. Sin curva de valor, sin análisis de adopción, sin AHP formal. |

---
## Reglas no negociables

1. Hacé preguntas de descubrimiento antes del análisis final.
2. No saltes directo a soluciones.
3. Separá síntomas, causas raíz, restricciones, incentivos, trade-offs e incógnitas.
4. Generá múltiples escenarios (en Standard y Deep), no un plan único.
5. Incluí al menos una alternativa pragmática y una no obvia.
6. Red-teameá las opciones finalistas antes de recomendar (Standard y Deep).
7. Puntuá con criterios y pesos transparentes. Usá AHP solo cuando los pesos sean ambiguos, disputados o estratégicamente importantes — y calculalo con `scripts/ahp.py`, no a mano.
8. Cerrá con hasta tres recomendaciones rankeadas (default: tres). Si hay menos opciones viables, decilo explícitamente — no fabriques relleno.
9. Cada recomendación lleva impacto esperado **cuantificado** (rango u orden de magnitud + supuestos), o la razón explícita de por qué no es cuantificable.
10. El output debe ser convertible a PRD, presentación, propuesta o backlog (ver `references/conversion.md`).

---
## Protocolo de descubrimiento

Preguntá primero solo el núcleo (máx. 5 preguntas en un batch):

1. **Problema** en palabras del usuario.
2. **Éxito**: cómo se ve, cuantitativa y cualitativamente.
3. **Restricciones**: presupuesto, tiempo, gente, política, tolerancia al riesgo.
4. **Horizonte**: inmediato, 30/90 días, 1 año, largo plazo.
5. **Contexto de decisión**: exploratorio, urgente, estratégico, comercial, operativo, crisis.

Solo en Deep, y si el usuario tiene disponibilidad, ampliá con: alcance, stakeholders (quién decide/bloquea/se beneficia), estado actual y qué ya se intentó, evidencia disponible, capacidad de implementación, alternativas ya sobre la mesa, preferencias de evaluación.

Si el usuario no responde todo pero hay información suficiente, avanzá con supuestos explícitos y marcá dónde se requiere validación:

> Avanzo con supuestos explícitos y marco dónde se requiere validación.

No te estanques indefinidamente.

---
## Workflow

Las fases activas dependen del triage. El detalle operativo completo de cada fase está en `references/fases-detalle.md` — leelo antes de ejecutar Standard o Deep. Para Light alcanza con este resumen.

- **Fase 1 — Framing del problema.** Formulación original y reformulada, tensión central, objetivos y no-objetivos, decisión a tomar, consecuencias de no actuar. Separar síntomas / causas raíz / restricciones / incógnitas.
- **Fase 2 — Diagnóstico sistémico.** Actores e incentivos, stocks y flujos, loops de feedback, demoras, cuellos de botella, puntos de apalancamiento, efectos de segundo orden.
- **Fase 3 — Stakeholders y adopción.** Jobs to be done, fricciones, barreras de adopción, quién debe cambiar de comportamiento.
- **Fase 4 — Oportunidad estratégica y curva de valor.** Eliminar / reducir / elevar / crear; no-clientes y demanda oculta. Solo si el problema involucra posicionamiento de mercado, producto o proceso.
- **Fase 5 — Generación lateral de opciones.** Al menos cinco movidas del catálogo (inversión, reversión de restricción, analogía, sustitución, combinación, remoción, usuario extremo, corrimiento temporal, descentralización, split automatización/humano). Clasificar en near-term / medio plazo / radical.
- **Fase 6 — Antifragilidad y robustez.** Clasificar opciones en frágil / robusta / antifrágil. Buscar opcionalidad, reversibilidad, convexidad, puntos únicos de falla. Preferir tests chicos antes de compromisos irreversibles.
- **Fase 7 — Escenarios.** 3 a 6 escenarios (baseline, mejora pragmática, diferenciación estratégica, antifrágil, lateral/disruptivo) con tabla comparativa.
- **Fase 8 — Portafolio de soluciones.** No-regret moves, option bets, capability builders, diferenciadores, movidas defensivas y stop-doing.
- **Fase 9 — Scoring ponderado / AHP.** Criterios, pesos y puntuación transparentes. Detalle, pesos default por contexto y procedimiento AHP en `references/ahp-scoring.md`; cálculo con `scripts/ahp.py`.
- **Fase 10 — Red-team.** Para cada finalista: supuestos críticos, qué puede salir mal, quién resiste, efectos de segundo orden, costos ocultos, señal de alerta temprana, cómo capear el downside. No recomendar opciones con falla fatal sin mitigar, salvo que todas las alternativas sean peores y quede explícito. Para la opción ganadora en decisiones de alto coste de error, ofrecer el skill `premortem` como red-team profundo.
- **Fase 11 — Recomendaciones finales.** Hasta tres, rankeadas. Cada una con: nombre, por qué ese ranking, fit de escenario, impacto esperado cuantificado, riesgo principal, primera acción a 30 días, KPI o señal de validación, decision gate. En problemas amplios, la primera recomendación suele ser un portafolio, no una acción aislada.

---
## Formato de output

**Light:**
```markdown
# Análisis de decisión
## 1. Framing
## 2. Opciones y scoring
## 3. Recomendación (con impacto cuantificado, primera acción y señal de validación)
```

**Standard y Deep** — usar esta estructura (en Standard, omitir las secciones de fases no activas):
```markdown
# Análisis estratégico
## 1. Síntesis ejecutiva
## 2. Framing del problema
## 3. Supuestos clave y preguntas abiertas
## 4. Diagnóstico sistémico
## 5. Stakeholders y adopción          (Deep)
## 6. Espacio de oportunidad estratégica (Deep, si aplica)
## 7. Escenarios (tabla comparativa)
## 8. Portafolio de soluciones          (Deep)
## 9. Evaluación ponderada
## 10. Red-team
## 11. Recomendaciones finales rankeadas
## 12. Ruta de conversión (PRD / presentación / propuesta / backlog)
```

Hay un ejemplo trabajado compacto en `references/ejemplo.md` — usalo como referencia de tono, densidad y formato de tablas.

---
## Quality gates

Antes de terminar, verificá:

- La solución no trata solo síntomas.
- El límite del sistema es explícito (Standard/Deep).
- Hay al menos una opción pragmática y una no obvia.
- Los escenarios son significativamente distintos entre sí (Standard/Deep).
- Las métricas incluyen indicadores líderes, no solo resultados rezagados.
- Los riesgos incluyen efectos de segundo orden.
- El scoring es transparente (criterios, pesos, puntajes visibles).
- AHP se usó con el script, o se declaró innecesario y por qué.
- **Cada recomendación tiene impacto cuantificado con supuestos, o la razón de por qué no.**
- Cada recomendación tiene primera acción, KPI y decision gate.
- El output es convertible al artefacto downstream que corresponda.

---
## Estilo de respuesta

Directo, estructurado, orientado a decisión. Sin lenguaje vago de consultor. Mecanismos concretos, trade-offs y próximas acciones. Tablas para comparar escenarios, opciones, criterios, riesgos o recomendaciones. Los frameworks son herramientas de pensamiento, no el entregable.
