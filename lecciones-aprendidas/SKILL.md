# lecciones-aprendidas

Guía al usuario a documentar lecciones aprendidas al cierre de un proyecto o sesión importante, mediante un flujo conversacional por secciones. Guarda el resultado en un archivo markdown y opcionalmente actualiza CLAUDE.md y la memoria persistente.

Use when the user finishes a project, sprint, or important session and wants to capture what went well, what went wrong, key decisions, and reusable patterns. Triggered by `/lecciones-aprendidas`, "lecciones aprendidas", "retrospectiva", "qué aprendimos", or "cierre de proyecto".

## Flujo

Hacé una sección a la vez. Esperá respuesta antes de avanzar. No presentes todas las preguntas juntas.

### 1. Contexto
Preguntá:
> "¿Sobre qué proyecto o sesión estamos haciendo la retrospectiva? Dame un nombre y una línea de descripción."

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
1. Guardá el resultado en `lecciones-aprendidas/lecciones-aprendidas.md` (en la raíz del proyecto, creando la carpeta si no existe). Si el archivo ya existe, agregá la nueva entrada al final. Cada entrada va precedida por su fecha como encabezado. Usá la plantilla de REFERENCE.md
2. Preguntá: "¿Querés que actualice el CLAUDE.md del proyecto con alguna de estas lecciones?"
3. Preguntá: "¿Querés que guarde los patrones reutilizables en tu memoria persistente para futuras sesiones?"

## Tono
- Conversacional, no burocrático
- Breve en las preguntas, generoso en el espacio para responder
- Si el usuario da una respuesta corta, ofrecé un ejemplo o preguntá si quiere profundizar
