# Lista de Tareas: [NOMBRE DE LA FEATURE]

**ID de Feature**: [NNN]  
**Plan de referencia**: `specs/[NNN]-[nombre]/plan.md`  
**Fecha de generación**: [FECHA]  
**Estado**: PENDIENTE | EN PROGRESO | COMPLETADO  

---

## Leyenda

- `[P]` — Tarea paralelizable (sin dependencias bloqueantes dentro del grupo)
- `[S]` — Tarea secuencial (debe ejecutarse en orden)
- `[B]` — Bloqueante para el siguiente grupo

---

## Grupo 0: Fundación 🏗️
> Prerequisito para todos los grupos siguientes.

```
[T000] [S][B] Definir y revisar contratos de API
  - Descripción: Crear archivos en contracts/ con especificaciones OpenAPI/AsyncAPI
  - Entradas: spec.md (sección Historias de Usuario + Criterios de Aceptación)
  - Salidas: contracts/api.yaml, contracts/events.yaml
  - Dependencias: ninguna

[T001] [S][B] Crear tests de contrato (estado FAIL)
  - Descripción: Implementar tests que validen los contratos definidos en T000
  - Entradas: contracts/
  - Salidas: tests/contract/ con todos los tests en estado FAIL confirmado
  - Dependencias: T000

[T002] [P] Crear esquema de base de datos v1
  - Descripción: Migraciones iniciales con todas las entidades del data-model.md
  - Entradas: data-model.md
  - Salidas: migrations/001_initial.sql (o equivalente del ORM)
  - Dependencias: T000

[T003] [P] Configurar entorno de desarrollo
  - Descripción: Docker compose / scripts de setup para desarrollo local
  - Entradas: plan.md (sección Stack Tecnológico)
  - Salidas: docker-compose.yml, .env.example, README de setup
  - Dependencias: ninguna
```

**Estado del grupo**: [ ] Completo (continuar solo cuando T001 y T002 estén done)

---

## Grupo 1: [Nombre de la Fase 1] 🔨
> Prerequisito: Grupo 0 completo.

```
[T010] [S] [Nombre de tarea]
  - Descripción: [qué hace exactamente]
  - Entradas: [qué necesita]
  - Salidas: [qué produce]
  - Dependencias: T001, T002

[T011] [P] [Nombre de tarea paralelizable]
  - Descripción: [qué hace]
  - Entradas: [qué necesita]
  - Salidas: [qué produce]
  - Dependencias: T010

[T012] [P] [Otra tarea paralelizable]
  - Descripción: [qué hace]
  - Entradas: [qué necesita]
  - Salidas: [qué produce]
  - Dependencias: T010

[T019] [S][B] Tests de integración - Grupo 1
  - Descripción: Verificar integración de todos los componentes del grupo 1
  - Entradas: componentes T010-T012
  - Salidas: tests/integration/grupo1/ todos en PASS
  - Dependencias: T010, T011, T012
```

**Estado del grupo**: [ ] Completo

---

## Grupo 2: [Nombre de la Fase 2] ⚙️
> Prerequisito: Grupo 1 completo.

```
[T020] [S] [Nombre de tarea]
  - Descripción: [...]
  - Entradas: [...]
  - Salidas: [...]
  - Dependencias: T019

[T021] [P] [Nombre de tarea]
  - Descripción: [...]
  - Entradas: [...]
  - Salidas: [...]
  - Dependencias: T020

[T029] [S][B] Tests e2e - Flujos principales
  - Descripción: Verificar flujos end-to-end de las historias de usuario principales
  - Entradas: entorno completo del Grupo 2
  - Salidas: tests/e2e/ todos en PASS
  - Dependencias: T020, T021
```

**Estado del grupo**: [ ] Completo

---

## Grupo Final: Producción 🚀
> Prerequisito: Todos los grupos anteriores completos + revisión de seguridad.

```
[T900] [P] Configurar observabilidad
  - Descripción: Logs estructurados, métricas, alertas según RNF del spec
  - Entradas: plan.md (sección Consideraciones de Rendimiento)
  - Salidas: configuración de monitoring activa
  - Dependencias: T029

[T901] [P] Documentación de operaciones
  - Descripción: Runbook, guía de rollback, playbook de incidentes
  - Entradas: plan.md (sección Guía de Validación)
  - Salidas: docs/operations.md
  - Dependencias: T029

[T999] [S] Validación final con criterios del spec
  - Descripción: Ejecutar todos los criterios de aceptación del spec.md manualmente
  - Entradas: spec.md (todos los Criterios de Aceptación)
  - Salidas: checklist de aceptación firmada
  - Dependencias: T900, T901
```

**Estado del grupo**: [ ] Completo

---

## Resumen de Paralelización

```
Grupo 0: T000 → T001,T002,T003 (T001 y T002 en paralelo)
                      ↓
Grupo 1: T010 → T011,T012 (paralelo) → T019
                      ↓
Grupo 2: T020 → T021 → T029
                      ↓
Final:   T900,T901 (paralelo) → T999
```

---

## Métricas de Progreso

| Grupo | Total tareas | Completadas | % |
|-------|-------------|-------------|---|
| Grupo 0 | [N] | 0 | 0% |
| Grupo 1 | [N] | 0 | 0% |
| Grupo 2 | [N] | 0 | 0% |
| Final | [N] | 0 | 0% |
| **Total** | **[N]** | **0** | **0%** |
