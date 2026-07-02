---
name: lecciones-aprendidas
description: >
  Guía al usuario a documentar lecciones aprendidas al cierre de un proyecto o sesión
  importante, mediante un flujo conversacional por secciones. Aprovecha el contexto de la
  sesión (conversación, git log) para proponer borradores en vez de preguntar en frío.
  Guarda el resultado en un archivo markdown acumulativo y opcionalmente actualiza
  CLAUDE.md y la memoria persistente. Use when the user finishes a project, sprint, or
  important session and wants to capture what went well, what went wrong, key decisions,
  and reusable patterns. Triggered by /lecciones-aprendidas, "lecciones aprendidas",
  "retrospectiva", "qué aprendimos", or "cierre de proyecto".
---

# lecciones-aprendidas

## Modos

**Modo completo** (default): flujo conversacional por secciones, descrito abajo. Para cierres de proyecto o retrospectivas donde el usuario quiere reflexionar.

**Modo rápido**: si el usuario pasa `rapido` como argumento, o si la skill se invoca como parte del cierre de sesión (ej: antes de compactar contexto), no hagas las preguntas una por una. Generá la entrada completa desde el contexto de la sesión (ver "Usar el contexto" abajo), mostrala al usuario y pedí una sola confirmación o corrección antes de guardar. Después seguí directo al paso 7.

## Usar el contexto

Antes de preguntar, revisá la evidencia disponible de la sesión o proyecto:

- La conversación actual: qué se intentó, qué falló, qué decisiones se tomaron
- `git log --oneline` reciente del proyecto, si es un repo
- Errores, reintentos o cambios de dirección que hayan ocurrido

Con eso, **proponé un borrador en cada sección en vez de preguntar en frío**. Por ejemplo: "De lo que vi en la sesión, salió bien X e Y, y hubo fricción con Z — ¿coincidís? ¿Qué agregarías?". El usuario corrige y completa; no redacta desde cero. Si no hay contexto útil (ej: la retro es sobre un proyecto que no está en esta sesión), preguntá en frío como indica cada sección.

## Flujo

Hacé una sección a la vez. Esperá respuesta antes de avanzar. No presentes todas las preguntas juntas.

### 1. Contexto
Preguntá:
> "¿Sobre qué proyecto o sesión estamos haciendo la retrospectiva? Dame un nombre y una línea de descripción."

Si el contexto de la sesión ya lo deja claro, proponelo: "Asumo que es sobre {proyecto}, ¿correcto?"

### 2. Qué salió bien
Preguntá:
> "¿Qué salió bien? Podés mencionar decisiones técnicas, procesos, colaboración, herramientas — lo que quieras destacar."

### 3. Qué salió mal
Preguntá:
> "¿Qué no salió como esperabas? Errores, fricción, cosas que frenaron el avance."

### 4. Qué harías diferente
Preguntá:
> "Si empezaras este proyecto de nuevo, ¿qué cambiarías?"

### 5. Decisiones clave
Preguntá:
> "¿Hubo decisiones importantes que tomaste? Arquitectura, stack, enfoque. ¿Qué las motivó y cómo resultaron?"

### 6. Patrones reutilizables
Preguntá:
> "¿Hay algo de lo que hiciste que valga la pena repetir en futuros proyectos? Puede ser un patrón, una herramienta, un approach."

### 7. Guardar
Una vez completadas las secciones:
1. Guardá el resultado en `lecciones-aprendidas/lecciones-aprendidas.md` (en la raíz del proyecto, creando la carpeta si no existe). Es un único archivo acumulativo: cada retro es una entrada nueva. Usá la plantilla y las reglas de inserción de REFERENCE.md.
2. Preguntá: "¿Querés que actualice el CLAUDE.md del proyecto con alguna de estas lecciones?"
3. Preguntá: "¿Querés que guarde los patrones reutilizables en tu memoria persistente para futuras sesiones?"

## Calidad de las lecciones

Una lección útil es accionable: qué pasó, por qué, y qué hacer distinto la próxima vez. Si el usuario da una respuesta solo descriptiva ("el deploy fue lento"), repreguntá una vez para llegar a la causa y la acción ("el deploy fue lento porque X; la próxima vez, hacer Y"). No insistas más de una vez — si el usuario no quiere profundizar, guardá lo que dio.

Si el usuario no tiene nada para una sección ("no hubo decisiones clave"), omití esa sección de la entrada — no guardes "N/A" ni secciones vacías.

## Tono
- Conversacional, no burocrático
- Breve en las preguntas, generoso en el espacio para responder
- Si el usuario da una respuesta corta, ofrecé un ejemplo o preguntá si quiere profundizar
