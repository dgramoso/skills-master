# Plantilla de salida

El archivo `lecciones-aprendidas/lecciones-aprendidas.md` es acumulativo. Cada invocación agrega una nueva entrada al final, separada por `---`.

```markdown
# Lecciones Aprendidas

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

---
```

Si el archivo ya existe, NO reescribir el encabezado `# Lecciones Aprendidas`. Solo agregar la nueva entrada `## {fecha} — {nombre}` al final, antes del último `---` o al final del archivo.

## Dónde guardar

Siempre guardar en la raíz del proyecto actual:
`lecciones-aprendidas/<nombre>-<fecha>.md`

Crear la carpeta si no existe. Si no hay proyecto activo (ej: directorio home), preguntar al usuario dónde guardar.

## Qué va a memoria persistente

Solo los patrones reutilizables que sean generalizables a otros proyectos — no detalles específicos del proyecto actual. Guardar como memoria tipo `project` o `feedback` según corresponda.
