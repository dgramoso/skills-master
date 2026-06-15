# Plan de Implementación: [NOMBRE DE LA FEATURE]

**ID de Feature**: [NNN]  
**Spec de referencia**: `specs/[NNN]-[nombre]/spec.md`  
**Fecha**: [FECHA]  
**Estado**: BORRADOR | REVISADO | APROBADO  

---

## Fase -1: Gates de Pre-implementación (OBLIGATORIO)

> ⛔ No avanzar al diseño técnico sin pasar estos gates.

### Gate de Simplicidad
- [ ] ¿Máximo 3 módulos/proyectos?
- [ ] ¿Sin features especulativas o "podría necesitarse"?
- [ ] ¿Sin over-engineering para escala no demostrada?

### Gate Anti-abstracción
- [ ] ¿Se usan frameworks directamente sin wrappers innecesarios?
- [ ] ¿Representación única por entidad (sin modelos duplicados)?

### Gate Integración-primero
- [ ] ¿Contratos de API definidos antes del código?
- [ ] ¿Tests de contrato planificados en fase Red?

### Gate Test-First
- [ ] ¿Tests escritos y aprobados ANTES del código de implementación?
- [ ] ¿Tests confirmados en estado FAIL (Red) antes de implementar?

**Decisiones de complejidad** (completar si algún gate falla con justificación):
> [Documentar aquí cualquier excepción con su razón de negocio o técnica]

---

## 1. Resumen Técnico

**Enfoque general**: [Descripción en 2-3 oraciones del approach técnico]

**Principales desafíos técnicos**:
1. [desafío 1 y cómo se aborda]
2. [desafío 2 y cómo se aborda]

---

## 2. Stack Tecnológico

| Componente | Tecnología | Justificación | Requisito del spec |
|------------|-----------|--------------|-------------------|
| [Backend] | [tech] | [por qué esta y no otra] | [Historia X, RNF Y] |
| [Base de datos] | [tech] | [por qué] | [Historia X] |
| [Frontend] | [tech] | [por qué] | [Historia X] |
| [Infraestructura] | [tech] | [por qué] | [RNF Y] |

> Toda elección tecnológica debe trazar a al menos un requisito del spec.

---

## 3. Arquitectura del Sistema

### Diagrama de componentes (en texto/Mermaid)
```
[Componente A] ──→ [Componente B]
      │                  │
      ↓                  ↓
[Componente C] ←── [Componente D]
```

### Módulos y responsabilidades

**Módulo 1: [Nombre]**
- Responsabilidad: [qué hace y qué NO hace]
- Interfaz pública: [qué expone hacia afuera]
- Dependencias: [de qué otros módulos depende]

**Módulo 2: [Nombre]**
- Responsabilidad: [...]
- Interfaz pública: [...]
- Dependencias: [...]

---

## 4. Modelo de Datos (resumen)

> Detalle completo en `data-model.md`

### Entidades principales
| Entidad | Propósito | Atributos clave |
|---------|-----------|----------------|
| [Entidad1] | [qué representa] | id, [campo1], [campo2] |
| [Entidad2] | [qué representa] | id, [campo1] |

### Relaciones clave
- [Entidad1] 1→N [Entidad2]: [descripción de la relación]

---

## 5. Contratos de API (resumen)

> Detalle completo en `contracts/`

### Endpoints REST
| Método | Ruta | Propósito | Historia |
|--------|------|-----------|---------|
| POST | /api/[recurso] | [qué hace] | Historia X |
| GET | /api/[recurso]/:id | [qué hace] | Historia X |

### Eventos / WebSockets (si aplica)
| Evento | Dirección | Payload | Historia |
|--------|-----------|---------|---------|
| [evento] | server→client | [datos] | Historia X |

---

## 6. Estrategia de Testing

> Orden obligatorio: contrato → integración → e2e → unitario

### Tests de contrato
- [qué contratos se verifican y con qué herramienta]

### Tests de integración
- [escenarios de integración críticos]
- Usar: BD real, servicios reales (sin mocks)

### Tests e2e
- [flujos críticos de usuario a cubrir]

### Tests unitarios
- [lógica de negocio compleja que merece unit test]

---

## 7. Plan de Entrega por Fases

### Fase 0: Fundación (prerequisito para todo lo demás)
**Prerrequisitos**: ninguno  
**Entregables**:
- [ ] Contratos de API definidos y revisados
- [ ] Tests de contrato escritos y en estado FAIL
- [ ] Esquema de base de datos versionado
- [ ] Configuración de entorno de desarrollo

### Fase 1: [Nombre de la fase]
**Prerrequisitos**: Fase 0 completa  
**Requisitos del spec**: [Historia X, Historia Y]  
**Entregables**:
- [ ] [entregable 1]
- [ ] [entregable 2]
- [ ] Tests de integración pasando

### Fase 2: [Nombre de la fase]
**Prerrequisitos**: Fase 1 completa  
**Requisitos del spec**: [Historia Z]  
**Entregables**:
- [ ] [entregable 1]
- [ ] Tests e2e de flujos principales pasando

### Fase Final: Producción
**Prerrequisitos**: Todas las fases anteriores  
**Entregables**:
- [ ] Observabilidad y alertas configuradas
- [ ] Documentación de operaciones
- [ ] Criterios de rollback definidos

---

## 8. Consideraciones de Seguridad

| Riesgo | Mitigación | Fase de implementación |
|--------|-----------|----------------------|
| [riesgo 1] | [cómo se mitiga] | Fase X |

---

## 9. Consideraciones de Rendimiento

| Requisito del spec | Estrategia técnica | Cómo se valida |
|-------------------|-------------------|----------------|
| [RNF de performance] | [approach técnico] | [benchmark/test] |

---

## 10. Guía de Validación Rápida (Quickstart)

Pasos para verificar que la implementación es correcta:

```bash
# 1. [Paso de setup]
[comando]

# 2. [Verificación del happy path]
[comando o acción]

# 3. [Verificación de caso borde crítico]
[comando o acción]
```

**Resultado esperado**: [qué deberías ver]

---

## 11. Registro de Decisiones Técnicas (ADR)

| # | Decisión | Alternativas consideradas | Razón de elección |
|---|---------|--------------------------|------------------|
| 1 | [decisión] | [alt1], [alt2] | [por qué esta] |

---

## Historial de Cambios

| Versión | Fecha | Cambio | Autor |
|---------|-------|--------|-------|
| 0.1 | [fecha] | Borrador inicial | [autor] |
