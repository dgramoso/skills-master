# Módulos avanzados opcionales

> Parte de la skill `analytics-workflow`. **NO** son parte del flujo por defecto.
> Se activan solo cuando el cliente o el regulador lo exige. Un proyecto estándar
> no los necesita — no generar esta documentación "por las dudas" (Ponytail).

Grado-buró (Equifax/Experian, consultora internacional, MRM tipo SR 11-7) no es
producir burocracia por defecto: es adoptar la **sustancia** cuando corresponde. Este
archivo captura ese estándar como conocimiento disponible; el uso se gatilla por
necesidad explícita, no automáticamente.

---

## Cómo se decide: triage en el intake / PRD

Al crear el PRD (`/to-spec`), responder 4 preguntas. Cada "sí" activa su módulo; registrar
la decisión (qué se activa y por qué) en el PRD. Si ninguna aplica, el flujo por defecto alcanza.

1. ¿El cliente es una entidad regulada, o el modelo es material (decisiones de crédito a escala)?
   → **Validación independiente + MDD**
2. ¿El modelo decide sobre personas y hay exposición legal / grupos protegidos?
   → **Fairness + adverse action / reason codes**
3. ¿Es un modelo de originación y hay población rechazada significativa?
   → **Reject inference**
4. ¿El entregable debe poder ser auditado o reproducido por un tercero?
   → **Data governance + hash de snapshot + change control**

---

## Catálogo de módulos

### 1. Reject inference (originación)

* **Qué:** corrige el sesgo de selección de modelar solo sobre aprobados, infiriendo el
  comportamiento de los rechazados (through-the-door population).
* **Activar si:** originación / acquisition + población rechazada relevante.
* **NO hace falta si:** modelo comportamental, cartera existente, o población completa observada.
* **Qué agrega:** en `05_modeling_validation.md`, definir método (reclasificación / parcelling /
  augmentation / Heckman) y su validación. Marcar explícito: `reject inference: sí/no + método`.
* **Esfuerzo:** bajo-medio (una sección en la spec de modeling; sin etapa nueva).

### 2. Validación independiente + MDD

* **Qué:** challenge independiente del desarrollo (solidez conceptual, backtesting, benchmarking,
  sensibilidad, estabilidad OOT/vintage) + Model Development Document formal.
* **Activar si:** cliente regulado, modelo material, o exige documentación auditable.
* **NO hace falta si:** uso interno, exploratorio, o cliente que solo quiere el resultado de negocio.
* **Qué agrega:** spec `0N_model_validation.md` + Validation Report + MDD (separados del informe de negocio).
* **Frontera con el default:** el QA pre-entrega (`quality-gates.md`) es obligatorio en todo
  proyecto y ya cubre el pase disciplinado con sombrero de validador + `/code-review ultra`.
  Este módulo agrega encima la validación **formal**: Validation Report + MDD + effective
  challenge documentado por alguien (o un pase) distinto del desarrollo — no autovalidación.
* **Esfuerzo:** alto.

### 3. Fairness + adverse action / reason codes

* **Qué:** test de impacto dispar por grupos protegidos + generación de razones de rechazo explicables.
* **Activar si:** el modelo decide sobre personas y hay requisito legal (ECOA/FCRA o equivalente
  local) o riesgo reputacional.
* **NO hace falta si:** segmentación descriptiva, dashboards, uso interno sin decisión sobre individuos.
* **Qué agrega:** spec `0N_fairness.md` + quality gate de impacto dispar en la etapa de validación +
  tabla de reason codes derivada del scorecard.
* **Esfuerzo:** medio.

### 4. Data governance + hash de snapshot + change control

* **Qué:** diccionario de datos, linaje fuente→modelo, dimensiones de calidad, hash/checksum del
  `datos/raw/`, y workflow de PR con `main` protegida.
* **Activar si:** el entregable debe poder ser auditado o reproducido por un tercero, o entorno regulado.
* **NO hace falta si:** proyecto exploratorio o de una persona sin requisito de auditoría
  (`renv` + `00_config.r` + git directo alcanza).
* **Qué agrega:** un `references/data-governance.md` (a crear si se activa), hash del snapshot en la
  metadata del pipeline, y control de cambios vía branch → PR → merge.
* **Esfuerzo:** medio.

---

## Principio

Capturar el estándar como conocimiento disponible; gatillar su uso por necesidad explícita.
Ningún módulo entra "por las dudas". El flujo por defecto queda liviano.
