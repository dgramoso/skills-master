# Template general de spec

> Parte de la skill `analytics-workflow`. Usar este template para toda spec analítica. Ver `specs-por-tipo.md` para qué specs crear según el tipo de proyecto.

```markdown
# Spec — [nombre_componente]

## Estado
Draft / Grillada / Aprobada / Implementada / Deprecada

## Relación con PRD
- PRD padre:
- User stories relacionadas:
- Decisiones del PRD que esta spec implementa:

## Objetivo
[Una oración clara que describa qué resuelve esta etapa.]

## Alcance

### Incluye
- ...

### No incluye
- ...

## Precondiciones
- Archivo/fuente requerida:
- Columnas requeridas:
- Parámetros requeridos:
- Supuestos de disponibilidad:

## Diseño metodológico
- Unidad de análisis:
- Granularidad:
- Fecha de corte:
- Ventana de observación:
- Ventana de performance:
- Transformaciones:
- Reglas de exclusión:
- Tratamiento de missing:
- Riesgos de leakage:

## Postcondiciones
- Archivos generados:
- Tablas generadas:
- Columnas obligatorias:
- Metadata generada:
- Logs generados:

## Quality Gates — falla con stop() si:
- ...
- ...
- ...

## Invariantes
- ...
- ...

## Decisiones metodológicas
| Decisión | Justificación | Documento destino |
|---|---|---|
|  |  |  |

## Riesgos
- Riesgo de leakage:
- Riesgo de sesgo:
- Riesgo de baja cobertura:
- Riesgo operativo:
- Riesgo de interpretación:

## Preguntas abiertas
- [ ] ...

## Output esperado
| Archivo | Columnas clave | Filas esperadas | Observaciones |
|---|---|---|---|
|  |  |  |  |

## Acceptance criteria
- [ ] La spec fue grillada.
- [ ] No quedan preguntas bloqueantes.
- [ ] Los quality gates son verificables.
- [ ] Los outputs esperados están definidos.
- [ ] La implementación puede hacerse sin decisiones implícitas.
```
