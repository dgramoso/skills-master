# Principios SDD — Referencia Extendida

## La Inversión de Poder

En el desarrollo tradicional:
```
Código = fuente de verdad
Spec = documentación del código (siempre desactualizada)
```

En SDD:
```
Spec = fuente de verdad
Código = expresión de la spec en un lenguaje/framework
```

**Consecuencia práctica**: Cuando hay contradicción entre spec y código, el spec gana.
El código se regenera; el spec se actualiza con intención consciente.

---

## El Ciclo de Vida SDD

```
0 → 1: Idea → PRD → Plan → Tareas → Código (primera implementación)
1 → N: Cambio en spec → Actualización del plan → Regeneración del código afectado
```

No hay "finalización" del spec. Evoluciona con el producto.

---

## Los 3 Artefactos Centrales

### 1. PRD (Product Requirements Document) — spec.md
- **Qué es**: La intención del negocio/usuario en lenguaje natural
- **Qué NO es**: Una descripción técnica de cómo implementar
- **Quién lo mantiene**: Product manager / líder de negocio
- **Cuándo cambia**: Cuando cambian los requisitos de negocio

### 2. Plan de Implementación — plan.md
- **Qué es**: Traducción técnica del PRD con trazabilidad explícita
- **Qué NO es**: Código ni pseudocódigo detallado
- **Quién lo mantiene**: Arquitecto / tech lead
- **Cuándo cambia**: Cuando cambia el PRD o se descubren mejores decisiones técnicas

### 3. Lista de Tareas — tasks.md
- **Qué es**: Instrucciones atómicas y ejecutables para un agente o desarrollador
- **Qué NO es**: El código en sí
- **Quién lo mantiene**: Tech lead / agente de desarrollo
- **Cuándo cambia**: Cuando cambia el plan

---

## Regla de Trazabilidad

Cada elemento del plan debe citar el requisito del spec que lo origina.
Cada tarea debe citar la sección del plan que la genera.

```
spec.md (Historia 3, CA-2)
    ↓
plan.md (Endpoint POST /api/orders → justificado por Historia 3)
    ↓
tasks.md (T025: Implementar POST /api/orders → derivado de plan sección 5)
    ↓
código (orders_controller.py → implementa T025)
```

Si no puedes trazar la cadena, algo falta o sobra.

---

## Marcadores de Ambigüedad

Usar explícitamente en specs y planes cuando algo no está definido:

```
[NECESITA CLARIFICACIÓN: pregunta específica sobre X]
```

**Por qué importa**: Evita que el LLM (o el desarrollador) asuma silenciosamente.
Una suposición no marcada es una deuda oculta.

**Regla**: Un spec con marcadores `[NECESITA CLARIFICACIÓN]` es mejor que un spec
sin ellos pero con suposiciones incorrectas embebidas.

---

## Branching y Versionado

Estructura de ramas sugerida:
```
main
├── 001-auth-sistema
├── 002-perfil-usuario
├── 003-chat-tiempo-real
└── NNN-nombre-feature
```

Estructura de archivos por feature:
```
specs/
└── NNN-nombre-feature/
    ├── spec.md          ← PRD
    ├── plan.md          ← Plan de implementación
    ├── tasks.md         ← Lista de tareas
    ├── data-model.md    ← Esquemas detallados (si aplica)
    ├── research.md      ← Decisiones técnicas y comparativas
    ├── quickstart.md    ← Guía de validación rápida
    └── contracts/
        ├── api.yaml
        └── events.yaml
```

---

## Retroalimentación desde Producción

Incidentes y métricas de producción no son solo problemas operativos.
Son inputs para actualizar los specs:

| Evento de producción | Actualización del spec |
|---------------------|----------------------|
| Latencia alta en endpoint X | Nuevo RNF de performance en PRD |
| Vulnerabilidad de seguridad | Nueva restricción en PRD + propagación al plan |
| Feature nunca usada | Candidata para eliminación del próximo ciclo |
| Confusión de usuarios | Clarificación en criterios de aceptación |

---

## Anti-patrones SDD

### ❌ Spec como formalidad
Escribir el spec después del código para "documentar lo que se hizo".
→ El spec debe preceder al código, siempre.

### ❌ Over-speccing
Especificar implementación técnica en el PRD (frameworks, nombres de funciones, estructura de carpetas).
→ El PRD describe QUÉ y POR QUÉ. El plan describe CÓMO.

### ❌ Spec desactualizado
Implementar un cambio de negocio directamente en código sin actualizar el spec primero.
→ Actualizar spec → derivar cambios al plan → ejecutar tareas.

### ❌ Tareas monolíticas
Tareas que hacen demasiado, sin entradas/salidas definidas.
→ Cada tarea debe ser atómica: una persona o agente puede ejecutarla en aislamiento.

### ❌ Mocks en lugar de integración
Tests que mockean la BD, servicios externos, etc.
→ Usar entornos reales. Los mocks ocultan problemas de integración.

---

## SDD y Exploración / Experimentos

SDD soporta la exploración explícitamente:

**Experimento de implementación**:
Un mismo spec puede generar múltiples planes con diferentes trade-offs:
- Plan A: optimizado para performance
- Plan B: optimizado para mantenibilidad
- Plan C: optimizado para costo de infraestructura

Comparar implementaciones de forma sistemática y elegir con evidencia.

**What-if de negocio**:
"Si necesitamos pivotar de B2C a B2B, ¿qué cambia?"
→ Crear rama del spec → modificar PRD → derivar nuevo plan → comparar delta de tareas

---

## Escala: Cuándo usar cada nivel de detalle

| Tamaño del cambio | PRD | Plan | Tasks | Contratos |
|-------------------|-----|------|-------|-----------|
| Bugfix | No | No | Sí (1-2 tareas) | No |
| Feature pequeña | Sí (mínimo) | Sí | Sí | Sí si hay API |
| Feature mediana | Sí (completo) | Sí | Sí | Sí |
| Feature grande / épica | Sí + sub-specs | Sí + sub-planes | Sí por sub-feature | Sí, con versioning |
| Nuevo producto | Sí (detallado) | Sí (detallado) | Sí (priorizado) | Sí |
