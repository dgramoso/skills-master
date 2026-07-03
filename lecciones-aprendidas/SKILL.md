---
name: lecciones-aprendidas
description: >
  Use when the user finishes a project, sprint, or important session and wants
  to capture lessons learned — what went well, what went wrong, key decisions,
  and reusable patterns. Triggered by /lecciones-aprendidas, "lecciones
  aprendidas", "retrospectiva", "qué aprendimos", or "cierre de proyecto".
---

# lecciones-aprendidas

## Modos

**Modo completo** (default): flujo conversacional por secciones, descrito abajo. Para cierres de proyecto o retrospectivas donde el usuario quiere reflexionar.

**Modo rápido**: solo si el usuario pasa `rapido` como argumento. No hagas las preguntas una por una: generá la entrada completa desde el contexto de la sesión (ver "Usar el contexto" abajo), mostrala al usuario y pedí una sola confirmación o corrección antes de guardar. Después seguí directo al paso 7. Si no hay contexto de sesión útil para generar el borrador, avisale al usuario y caé al modo completo — no inventes una entrada.

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
1. Guardá el resultado según "Plantilla y guardado" abajo.
2. Preguntá: "¿Querés que actualice el CLAUDE.md del proyecto con alguna de estas lecciones?"
3. Preguntá: "¿Querés que guarde los patrones reutilizables en tu memoria persistente para futuras sesiones?"

## Calidad de las lecciones

Una lección útil es accionable: qué pasó, por qué, y qué hacer distinto la próxima vez. Si el usuario da una respuesta solo descriptiva ("el deploy fue lento"), repreguntá una vez para llegar a la causa y la acción ("el deploy fue lento porque X; la próxima vez, hacer Y"). No insistas más de una vez — si el usuario no quiere profundizar, guardá lo que dio.

Si el usuario no tiene nada para una sección ("no hubo decisiones clave"), omití esa sección de la entrada — no guardes "N/A" ni secciones vacías.

## Tono
- Conversacional, no burocrático
- Breve en las preguntas, generoso en el espacio para responder
- Si el usuario da una respuesta corta, ofrecé un ejemplo o preguntá si quiere profundizar

## Plantilla y guardado

El archivo `lecciones-aprendidas/lecciones-aprendidas.md` (en la raíz del proyecto actual, creando la carpeta si no existe) es único y acumulativo: cada invocación agrega una nueva entrada. Si no hay proyecto activo (ej: directorio home), preguntá al usuario dónde guardar.

Formato de cada entrada — `{YYYY-MM-DD}` es la fecha de hoy:

```markdown
---

## {YYYY-MM-DD} — {nombre-proyecto}

**Descripción:** {una línea}

### Qué salió bien

{respuesta del usuario}

### Qué salió mal

{respuesta del usuario}

### Qué haría diferente

{respuesta del usuario}

### Decisiones clave

{respuesta del usuario}

### Patrones reutilizables

{respuesta del usuario}
```

Reglas de inserción:

- Cada entrada **empieza** con una línea `---` y **no** lleva `---` de cierre — el `---` de la entrada siguiente hace de separador.
- Si el archivo no existe, crearlo con el encabezado `# Lecciones Aprendidas` seguido de la primera entrada.
- Si ya existe, NO reescribir el encabezado. Insertar la nueva entrada **inmediatamente después del encabezado**, antes de las entradas existentes — el archivo queda en orden cronológico descendente (lo más reciente arriba).
- Omitir las secciones para las que el usuario no aportó nada — no incluir secciones vacías ni "N/A".

## Qué va a memoria persistente

Solo los patrones reutilizables que sean generalizables a otros proyectos — no detalles específicos del proyecto actual. Guardar como memoria tipo `project` o `feedback` según corresponda, con las líneas **Why:** y **How to apply:** para que la lección sea accionable en futuras sesiones.
