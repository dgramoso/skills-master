# Scoring ponderado y AHP

Referencia para la Fase 9. Usar scoring para toda comparación seria. Usar AHP solo cuando los pesos o las comparaciones sean ambiguos, subjetivos, disputados o estratégicamente importantes — y calcularlo con `scripts/ahp.py`, nunca a mano.

---
## Escala de puntuación

Escala 1-5 salvo que el usuario provea otra:
- 1 = débil / desfavorable.
- 3 = moderado / incierto.
- 5 = fuerte / favorable.

Para costo, riesgo y esfuerzo, invertir el puntaje para que 5 sea favorable:
- Control de riesgo: 5 = riesgo bajo o manejable.
- Eficiencia de costo: 5 = costo bajo relativo al valor.
- Factibilidad: 5 = fácil de ejecutar con las capacidades actuales.

---
## Criterios default

1. Potencial de impacto.
2. Fit estratégico.
3. Factibilidad.
4. Velocidad al valor.
5. Eficiencia de costo.
6. Control de riesgo.
7. Probabilidad de adopción.
8. Apalancamiento sistémico.
9. Opcionalidad.
10. Antifragilidad.
11. Innovación/diferenciación.
12. Fuerza de la evidencia.

## Pesos provisionales default (si el usuario no da ninguno)

```text
Potencial de impacto: 15%
Fit estratégico: 10%
Factibilidad: 10%
Velocidad al valor: 8%
Eficiencia de costo: 7%
Control de riesgo: 10%
Probabilidad de adopción: 8%
Apalancamiento sistémico: 10%
Opcionalidad: 7%
Antifragilidad: 7%
Innovación/diferenciación: 5%
Fuerza de la evidencia: 3%
```

## Ajustes de pesos por contexto

- **Crisis**: subir velocidad, control de riesgo, factibilidad.
- **Innovación**: subir diferenciación, opcionalidad, apalancamiento sistémico.
- **Propuesta comercial**: subir impacto, adopción, factibilidad, fit estratégico.
- **Contexto regulado**: subir control de riesgo, fuerza de evidencia, factibilidad.
- **Iniciativa de analytics/IA**: subir fuerza de evidencia, factibilidad, adopción, control de riesgo, apalancamiento sistémico.
- **Negocio propio**: subir costo de oportunidad (usar velocidad al valor + eficiencia de costo como proxy), reversibilidad (opcionalidad) y foco; bajar adopción e innovación salvo que apliquen.
- **Personal (Light)**: no usar esta lista. Criterios simples: minimización de arrepentimiento, reversibilidad, energía/tiempo requerido, alineación con objetivos de largo plazo. Pesos a ojo, transparentes, sin AHP.

---
## Procedimiento AHP

1. Definir criterios (3 a 9; más de 9 vuelve inconsistentes las comparaciones).
2. Pedir comparaciones de a pares al usuario si su participación es necesaria.
3. Escala de Saaty: 1 igual, 3 moderado, 5 fuerte, 7 muy fuerte, 9 extremo; 2/4/6/8 intermedios. Recíprocos para la dirección opuesta.
4. Armar la matriz de comparaciones y **correr `scripts/ahp.py`** para obtener pesos y ratio de consistencia (CR):

```bash
python scripts/ahp.py --criteria "Impacto,Factibilidad,Riesgo,Velocidad" --matrix "1,3,5,3; 0.333,1,3,1; 0.2,0.333,1,0.5; 0.333,1,2,1"
```

   El script devuelve los pesos normalizados y el CR. Si CR > 0.10, las comparaciones son inconsistentes: mostrar al usuario los dos pares más contradictorios y pedir que revise.
5. Puntuar alternativas contra criterios (escala 1-5 de arriba).
6. Calcular puntaje ponderado (el script también lo hace con `--scores`).
7. Stress-test: verificar si el ranking cambia bajo variaciones plausibles de pesos (±20% en los 2-3 pesos más altos). Si el ranking es inestable, decirlo — es información, no un defecto.

Si AHP frenaría demasiado la tarea, usar pesos provisionales, decirlo, y recomendar validar los pesos después.

---
## Presentación del resultado

Mostrar siempre: tabla con criterios, pesos, puntajes por alternativa, puntaje ponderado total y ranking. Agregar una línea de notas de sensibilidad (qué tendría que cambiar para que el #2 pase al #1).
