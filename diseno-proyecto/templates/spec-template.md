# Especificación de Feature: [NOMBRE DE LA FEATURE]

**ID de Feature**: [NNN]  
**Rama**: `[NNN]-[nombre-semántico]`  
**Fecha**: [FECHA]  
**Estado**: BORRADOR | EN REVISIÓN | APROBADO  
**Autor**: [AUTOR]

---

## 1. Resumen Ejecutivo

**Problema que resuelve**: [Una oración clara del problema]

**Solución propuesta**: [Una oración de la solución, sin detalles técnicos]

**Usuarios objetivo**: [Quiénes se benefician directamente]

**Valor de negocio**: [Por qué esto importa para el negocio]

---

## 2. Contexto y Motivación

### Situación actual
[Descripción del estado actual sin esta feature. ¿Qué hacen los usuarios hoy?]

### Por qué ahora
[Qué cambio (negocio, mercado, usuario) hace necesario construir esto ahora]

### Métricas de éxito
| Métrica | Valor actual | Objetivo | Plazo |
|---------|-------------|---------|-------|
| [métrica 1] | [valor] | [objetivo] | [plazo] |
| [métrica 2] | [valor] | [objetivo] | [plazo] |

---

## 3. Alcance

### Incluido en esta versión (v1)
- [requisito funcional 1]
- [requisito funcional 2]
- [requisito funcional N]

### Explícitamente EXCLUIDO
- [lo que no haremos y por qué]
- [NECESITA CLARIFICACIÓN: ¿aplica X caso?]

### Dependencias externas
- [sistemas, APIs, equipos que necesitamos]

---

## 4. Historias de Usuario

### Historia 1: [Nombre descriptivo]
```
Como [tipo de usuario]
Quiero [acción o capacidad]
Para [beneficio o resultado]
```

**Criterios de aceptación**:
- [ ] Dado [contexto], cuando [acción], entonces [resultado esperado]
- [ ] Dado [contexto], cuando [acción], entonces [resultado esperado]
- [ ] [NECESITA CLARIFICACIÓN: comportamiento en caso borde X]

**Prioridad**: MUST | SHOULD | COULD  
**Estimación de valor**: ALTA | MEDIA | BAJA

---

### Historia 2: [Nombre descriptivo]
```
Como [tipo de usuario]
Quiero [acción o capacidad]
Para [beneficio o resultado]
```

**Criterios de aceptación**:
- [ ] Dado [contexto], cuando [acción], entonces [resultado esperado]

**Prioridad**: MUST | SHOULD | COULD

---

## 5. Requisitos No Funcionales

### Rendimiento
- [ej: tiempo de respuesta < 200ms para el 95% de requests]
- [NECESITA CLARIFICACIÓN: volumen esperado de usuarios concurrentes]

### Seguridad
- [ej: datos sensibles cifrados en reposo y en tránsito]
- [ej: autenticación requerida para todas las operaciones]

### Disponibilidad
- [ej: uptime 99.9%, sin ventanas de mantenimiento programadas]

### Escalabilidad
- [ej: soportar hasta X usuarios sin cambios de arquitectura]

### Observabilidad
- [ej: logs estructurados para todas las operaciones críticas]
- [ej: métricas de negocio accesibles en tiempo real]

---

## 6. Casos Borde y Escenarios de Error

| Escenario | Comportamiento esperado |
|-----------|------------------------|
| [caso borde 1] | [qué debe pasar] |
| [error externo 1] | [cómo degradar gracefully] |
| [NECESITA CLARIFICACIÓN: ¿qué pasa si X?] | [pendiente] |

---

## 7. Experiencia de Usuario (sin diseño técnico)

### Flujo principal (happy path)
1. El usuario [acción]
2. El sistema [respuesta]
3. El usuario [siguiente acción]
4. El sistema [resultado final]

### Flujos alternativos
- **Si [condición]**: [flujo alternativo]
- **Si [error]**: [cómo se informa al usuario]

---

## 8. Restricciones y Suposiciones

### Restricciones
- [restricción de negocio, legal, o técnica que no podemos cambiar]

### Suposiciones
- [algo que asumimos verdadero; si no lo es, el spec puede cambiar]

---

## 9. Preguntas Abiertas

| # | Pregunta | Responsable | Fecha límite | Respuesta |
|---|---------|-------------|-------------|-----------|
| 1 | [NECESITA CLARIFICACIÓN: pregunta específica] | [persona] | [fecha] | PENDIENTE |
| 2 | [NECESITA CLARIFICACIÓN: otra pregunta] | [persona] | [fecha] | PENDIENTE |

---

## 10. Checklist de Completitud

### Antes de marcar como APROBADO:
- [ ] No quedan marcadores `[NECESITA CLARIFICACIÓN]` sin resolver
- [ ] Todos los criterios de aceptación son testeables
- [ ] Las métricas de éxito son medibles
- [ ] Los casos borde críticos están documentados
- [ ] Las dependencias externas están identificadas
- [ ] No hay especificación de implementación técnica (stack, código, APIs internas)
- [ ] Al menos 2 personas del equipo han revisado

---

## Historial de Cambios

| Versión | Fecha | Cambio | Autor |
|---------|-------|--------|-------|
| 0.1 | [fecha] | Borrador inicial | [autor] |
