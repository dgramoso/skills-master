# Medición de impacto de acciones comerciales

> Parte de la skill `advanced-analytics`. Cierra el loop `recomendación → acción → ¿funcionó?`. Aplica a campañas, estrategias de cobranza, cambios de pricing, pilotos de retención y cualquier acción cuyo impacto haya que demostrar.

**Principio:** ningún resultado de una acción se reporta comparando contra el pasado o contra nada. Se compara contra el contrafactual: qué hubiera pasado sin la acción. Sin contrafactual no hay impacto — hay anécdota.

---

## El diseño se define ANTES de lanzar

La decisión más importante se toma antes de ejecutar la acción, no al analizarla:

* **Grupo de control aleatorio**: una fracción de la población objetivo que NO recibe la acción, seleccionada al azar. Es la única fuente de contrafactual limpio.
* **Tamaño del control**: suficiente para detectar el efecto mínimo que justificaría la acción (ver tamaño muestral abajo). Típico: 10-20% de la población objetivo; con poblaciones chicas, 50/50.
* **Duración predefinida**: fecha de lectura fijada antes de lanzar. Prohibido leer antes y parar cuando el resultado "da bien" (peeking).
* **Contaminación**: verificar que el control no recibe la acción por otro canal (otra campaña simultánea, gestión manual del comercial que "no quiere perder al cliente").

Si el negocio no acepta dejar un control sin tratar ("no podemos no gestionar a nadie"), documentarlo como decisión del cliente en el decision log — y el informe dirá "impacto no medible con rigor" en lugar de inventar una cifra.

---

## Jerarquía de evidencia

Usar el método más alto que el contexto permita, y **declarar cuál se usó**:

| Nivel | Método | Cuándo |
|---|---|---|
| 1 | Test/control aleatorizado | Siempre que se pueda. Default. |
| 2 | Cuasi-experimento: difference-in-differences, matching por score de propensión, regresión con controles | El control aleatorio no fue posible pero existe un grupo comparable no tratado |
| 3 | Pre-post (antes vs después) | Último recurso. Reportar SIEMPRE con la limitación explícita: no distingue el efecto de la acción de la tendencia, estacionalidad o cualquier otro cambio simultáneo |

Error dominante del nivel 3: atribuir a la campaña lo que era tendencia ("la mora bajó tras la campaña" — la mora venía bajando de antes).

---

## Tamaño muestral y lectura

* Regla práctica para proporciones: para detectar un lift de `d` puntos porcentuales sobre una tasa base `p`, se necesitan aproximadamente `n ≈ 16 · p(1−p) / d²` casos **por grupo** (α=5%, potencia 80%). Ej.: tasa base 5%, detectar +1 pp → `16 · 0.05·0.95 / 0.0001 ≈ 7.600` por grupo.
* Si la población disponible no alcanza para detectar el efecto mínimo relevante, decirlo antes de lanzar — correr el piloto igual solo si el cliente acepta que la lectura será direccional, no concluyente.
* La lectura respeta la fecha predefinida y reporta el intervalo de confianza de la diferencia, no solo el punto.

---

## Métricas de impacto

```text
conversión incremental   = tasa_tratados − tasa_control
volumen incremental      = conversión_incremental × n_tratados
costo por incremental    = costo_total_acción / volumen_incremental
ROI de la acción         = (margen × volumen_incremental − costo_total) / costo_total
```

* El costo por conversión **incremental** es la métrica honesta: la campaña "generó" 500 ventas, pero si el control convierte parecido, las incrementales pueden ser 40 — y el costo por venta real es 12 veces el reportado.
* Reportar lift absoluto (pp) y relativo (%) con su IC. "La retención subió 2,1 pp (IC 95%: 0,8–3,4) sobre una base de 84%".

---

## Errores comunes

| Error | Corrección |
|---|---|
| Leer el experimento antes de la fecha y parar cuando da bien | Fecha de lectura predefinida; una sola lectura confirmatoria |
| Sin grupo de control ("se gestionó a todos") | Decisión del cliente al decision log; reportar como no medible o usar cuasi-experimento |
| Control contaminado por otra campaña o gestión manual | Verificar exposición del control antes de leer; excluir contaminados documentándolo |
| Comparar tratados vs no-tratados cuando el targeting no fue aleatorio | Eso mide el sesgo de selección, no el impacto. Usar matching o declarar la limitación |
| Pescar segmentos ganadores post-hoc ("funcionó en mujeres 25-34 del interior") | Los subgrupos se definen antes del experimento; lo demás es hipótesis para el próximo test |
| Atribuir a la acción una mejora que era tendencia | Nivel 3 de evidencia: mostrar la serie previa completa, no solo el antes/después |
| Celebrar el lift sin costo | Siempre costo por incremental y ROI; un lift caro es una pérdida |

---

## Output estándar de una medición

1. Diseño usado (nivel de evidencia) y sus limitaciones.
2. Lift absoluto y relativo con IC, sobre la métrica de decisión acordada.
3. Costo por conversión incremental y ROI.
4. Recomendación: escalar / ajustar y re-testear / descontinuar — con el umbral económico que la justifica.
5. Próximo experimento: qué hipótesis quedó abierta y cómo se testearía.

---

## Uplift modeling (opcional)

Targeting por incrementalidad — a quién la acción le **cambia** el comportamiento, no quién convierte de todos modos (persuadibles vs. sure things / lost causes / do-not-disturb). Requiere historia de experimentos con control aleatorio para entrenar. No arrancar por acá: primero medir bien con test/control simple; el uplift modeling es la segunda iteración cuando ya hay cultura de experimentación.
