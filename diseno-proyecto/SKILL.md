---
name: diseno-proyecto
description: >
  Implementa la metodología Spec-Driven Development (SDD) para diseñar proyectos de software.
  Usar SIEMPRE que el usuario quiera arrancar un proyecto nuevo, diseñar una feature, crear un PRD,
  documentar requisitos, planificar una implementación técnica, o cuando diga frases como
  "quiero construir X", "necesito diseñar el proyecto Y", "ayúdame a planificar esta app",
  "crea el spec de", "hagamos el diseño de", "necesito el PRD de", "planifica esta feature",
  "diseñemos la arquitectura de". También disparar cuando el usuario tenga una idea vaga
  y quiera convertirla en un plan ejecutable concreto.
---

# Skill: Diseño de Proyecto (SDD)

Implementa **Spec-Driven Development**: las especificaciones son la fuente de verdad.
El código sirve a la especificación, no al revés.

## Filosofía Central

```
Idea → PRD (spec) → Plan de implementación → Lista de tareas → Código
```

El código es el *último* artefacto, no el primero. Cambiar un requisito significa
actualizar el spec, no parchear código.

---

## Flujo de trabajo según el punto de entrada

Detectar dónde está el usuario y saltar a esa fase:

| Punto de entrada del usuario | Fase a ejecutar |
|---|---|
| Idea vaga / "quiero construir X" | → **Fase 1: Especificación (PRD)** |
| Tiene idea clara / descripción detallada | → **Fase 1** acelerada |
| Ya tiene PRD o spec | → **Fase 2: Plan de implementación** |
| Ya tiene plan | → **Fase 3: Lista de tareas** |
| Quiere revisar / actualizar | → Actualización bidireccional |

---

## Fase 1: Especificación (PRD)

### Objetivo
Convertir una idea en un PRD completo, preciso y ejecutable.

### Proceso

**1. Entrevista de descubrimiento** (hacer solo las preguntas necesarias, no todas a la vez)

Preguntas clave:
- ¿Qué problema resuelve este producto para quién?
- ¿Cuál es el flujo principal del usuario (happy path)?
- ¿Qué es lo que definitivamente NO hace la primera versión?
- ¿Hay restricciones técnicas o de negocio que deba conocer?
- ¿Cómo se ve el éxito? ¿Qué métricas importan?

**2. Generar el PRD** usando la plantilla → `templates/spec-template.md`

**3. Marcar ambigüedades** con `[NECESITA CLARIFICACIÓN: pregunta específica]`

**4. Entregar el PRD** y pedir revisión antes de avanzar a Fase 2.

### Reglas del PRD
- ✅ Enfocarse en QUÉ necesita el usuario y POR QUÉ
- ❌ Nunca especificar CÓMO implementar (sin stack tech, sin estructura de código)
- ✅ Cada requisito debe ser testeable y tener criterios de aceptación medibles
- ✅ Marcar explícitamente lo que está fuera de alcance

---

## Fase 2: Plan de Implementación

### Objetivo
Traducir el PRD en decisiones técnicas concretas con trazabilidad a requisitos.

### Proceso

**1. Analizar el PRD** completo antes de escribir el plan

**2. Validar las Gates de Pre-implementación** (ver sección Gates más abajo)

**3. Generar el Plan** usando la plantilla → `templates/plan-template.md`

El plan debe incluir:
- Stack tecnológico con justificación (trazada a requisito específico)
- Arquitectura del sistema (módulos/servicios y sus responsabilidades)
- Modelo de datos con entidades principales
- Contratos de API (endpoints / eventos)
- Estrategia de testing (contract → integración → e2e → unitario)
- Fases de entrega con dependencias claras

**4. Separar el detalle excesivo** a archivos auxiliares:
- `data-model.md` → esquemas detallados
- `contracts/` → especificaciones de API
- `research.md` → decisiones y comparativas técnicas

### Gates de Pre-implementación (OBLIGATORIAS)

Antes de avanzar, verificar cada gate:

**Gate de Simplicidad**
- [ ] ¿Máximo 3 módulos/proyectos en la implementación inicial?
- [ ] ¿Sin "future-proofing" (no arquitectura para requisitos inexistentes)?
- [ ] ¿Complejidad adicional documentada y justificada?

**Gate Anti-abstracción**
- [ ] ¿Se usan los frameworks directamente sin capas de envoltura innecesarias?
- [ ] ¿Representación única de cada entidad (sin duplicación de modelos)?

**Gate de Integración-primero**
- [ ] ¿Contratos de API definidos antes del código?
- [ ] ¿Tests de contrato planificados antes de la implementación?

Si algún gate falla → documentar justificación en sección "Decisiones de complejidad"
del plan antes de continuar.

---

## Fase 3: Lista de Tareas

### Objetivo
Convertir el plan en tareas atómicas y ejecutables, listas para un agente o desarrollador.

### Proceso

**1. Leer**: `plan.md` (obligatorio) + `data-model.md`, `contracts/`, `research.md` si existen

**2. Derivar tareas** desde:
- Contratos de API → tareas de implementación de endpoints
- Entidades del modelo → tareas de migración/esquema
- Escenarios de test → tareas de testing
- Fases del plan → grupos de tareas ordenados

**3. Formato de cada tarea**:
```
[ID] [P?] Título breve
  - Descripción: qué hace exactamente
  - Entradas: qué necesita para ejecutarse
  - Salidas: qué produce cuando termina
  - Dependencias: IDs de tareas previas
```
`[P]` = tarea paralelizable (sin dependencias bloqueantes)

**4. Agrupar en fases** con prerrequisitos explícitos entre grupos

**5. Generar** `tasks.md` usando la plantilla → `templates/tasks-template.md`

---

## Principio de Retroalimentación Bidireccional

Los specs no son documentos muertos. Actualizar cuando:

| Evento | Acción en el spec |
|---|---|
| Métricas de producción muestran problema | Nuevo requisito no-funcional en PRD |
| Incidente de seguridad | Nueva restricción en PRD + propagación al plan |
| Cambio de requisito de negocio | Actualizar PRD → regenerar secciones afectadas del plan |
| Deuda técnica identificada | Refactoring en el plan como tarea explícita |

---

## Constitución Arquitectónica (Principios Inmutables)

Estos principios se aplican en TODA implementación:

1. **Library-First**: Cada feature nace como módulo/librería independiente
2. **CLI Mandate**: Toda librería expone funcionalidad vía CLI (stdin/stdout/JSON)
3. **Test-First**: Ningún código de implementación antes de que los tests estén aprobados y fallen (fase Red)
4. **Simplicidad**: Máximo 3 proyectos iniciales; complejidad adicional requiere justificación documentada
5. **Anti-abstracción**: Usar frameworks directamente; no envolver lo que ya funciona
6. **Integración-primero**: Tests con entornos reales (no mocks); BD real, servicios reales

---

## Plantillas y Referencias

- `templates/spec-template.md` → Plantilla completa del PRD
- `templates/plan-template.md` → Plantilla del plan de implementación
- `templates/tasks-template.md` → Plantilla de lista de tareas
- `references/sdd-principles.md` → Principios SDD extendidos y ejemplos

Leer la plantilla relevante antes de generar cada artefacto.

---

## Formato de entrega

Siempre entregar en bloques de código Markdown con nombre de archivo sugerido:

```markdown
<!-- specs/001-nombre-feature/spec.md -->
[contenido del spec]
```

Crear rama semántica sugerida: `NNN-nombre-feature` (ej: `001-chat-sistema`)
