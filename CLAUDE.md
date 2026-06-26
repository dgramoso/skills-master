# CLAUDE.md — nombre_proyecto

## Contexto
[Una oración describiendo el proyecto. Ver CONTEXT.md para detalle.]

## Lenguaje
[R / Python / SQL + R / etc.]

## Metodología
SDD + Ponytail. Cada etapa tiene su spec en specs/. Arrancar siempre por la spec antes de escribir código.

## Estructura de specs
- specs/00_proyecto.md → alcance validado con cliente
- specs/01_... → [qué hace]
- specs/02_... → [qué hace]
- specs/03_... → [qué hace]

## Versionado de modelos
modelos/vN/ — cada versión tiene modelo + CHANGELOG.md

## Ponytail
Activo (full). No construir abstracciones no pedidas.

## Agent skills
- Issue tracker: local markdown (specs/ actúa como backlog)
- Context files: CONTEXT.md (dominio), specs/*.md (tareas activas)

## Cierre de sesión
Antes de cerrar, correr `/handoff "descripción de lo que sigue"`.
