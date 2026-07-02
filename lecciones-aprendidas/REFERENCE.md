# Plantilla de salida

El archivo `lecciones-aprendidas/lecciones-aprendidas.md` es único y acumulativo. Cada invocación agrega una nueva entrada, separada por `---`.

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

## Reglas de inserción

- Si el archivo no existe, crearlo con el encabezado `# Lecciones Aprendidas` seguido de la primera entrada.
- Si ya existe, NO reescribir el encabezado. Insertar la nueva entrada **inmediatamente después del encabezado**, antes de las entradas existentes — el archivo queda en orden cronológico descendente (lo más reciente arriba).
- Cada entrada empieza y termina con una línea `---`.
- Omitir las secciones para las que el usuario no aportó nada — no incluir secciones vacías ni "N/A".

## Dónde guardar

Siempre en la raíz del proyecto actual: `lecciones-aprendidas/lecciones-aprendidas.md`. Crear la carpeta si no existe. Si no hay proyecto activo (ej: directorio home), preguntar al usuario dónde guardar.

## Qué va a memoria persistente

Solo los patrones reutilizables que sean generalizables a otros proyectos — no detalles específicos del proyecto actual. Guardar como memoria tipo `project` o `feedback` según corresponda, con las líneas **Why:** y **How to apply:** para que la lección sea accionable en futuras sesiones.
