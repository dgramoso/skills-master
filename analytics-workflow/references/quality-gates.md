# Quality Gates y reglas anti-leakage

> Parte de la skill `analytics-workflow`. Ver `SKILL.md` para el flujo general.

---

## Quality Gates

Patrón estándar (ejemplo en R; equivalente Python abajo):

```r
stopifnot(
  "archivo input ausente" = file.exists(PATH_INPUT),
  "target ausente" = TARGET %in% names(datos)
)

if (alguna_condicion_critica) {
  stop("Quality Gate: descripción del problema")
}
```

Equivalente en Python:

```python
assert PATH_INPUT.exists(), "Quality Gate: archivo input ausente"
assert TARGET in datos.columns, "Quality Gate: target ausente"

if alguna_condicion_critica:
    raise ValueError("Quality Gate: descripción del problema")
```

> En Python, no uses `assert` para gates críticos que deban correr en producción: `python -O` los elimina. Para gates que nunca deben desactivarse, preferí `if ...: raise`.

Regla:

```text
Un script que termina sin error pero con datos incorrectos es peor que uno que falla.
```

Quality gates típicos:

* archivo input existe
* columnas obligatorias existen
* claves no tienen duplicados indebidos
* target no tiene valores inválidos
* fechas están dentro de rango esperado
* no hay leakage temporal
* outputs no están vacíos
* porcentajes que deben sumar 100 efectivamente suman 100
* número de filas está dentro del rango esperado
* bad rate está dentro de rango plausible
* variables críticas no superan missing máximo
* no se generan NAs nuevos inesperados

---

## Reglas anti-leakage

Para modelos predictivos:

```text
Ninguna variable puede usar información posterior a la fecha de corte.
```

Reglas:

* La ventana de observación ocurre antes de la ventana de performance.
* El target se mide después de la fecha de corte.
* Features, imputaciones, bins, escaladores y selección de variables se aprenden solo en train.
* Los parámetros aprendidos en train se congelan y se aplican a test/OOT/producción.
* Variables con IV > 1 deben reportarse como sospechosas de leakage.
* Performance demasiado alta debe investigarse antes de celebrarse.

Error común:

```text
Aprender transformaciones usando train + test.
```

Corrección:

```text
Fit en train. Apply en test/OOT/producción.
```

---

## QA pre-entrega (obligatorio)

Pase de QA con "sombrero de validador" antes de generar el informe final. Es la versión default y liviana del challenge independiente — la validación formal + MDD sigue siendo un módulo opcional (ver `modulos-opcionales.md`). Checklist copiable en `templates/qa_pre_entrega.md.tmpl`.

1. **Reproducción en limpio:** copiar/clonar el repo a un directorio limpio y correr `00_run_pipeline` de punta a punta, sin objetos en memoria ni pasos manuales.
2. **Verificación de cifras:** cada número del informe se verifica contra los outputs generados.
3. **Baseline:** el modelo supera al baseline naive / status quo documentado en la spec de modeling.
4. **Revisión final de leakage:** variables con IV > 1 o performance sospechosamente alta investigadas y resueltas.
5. **Sensibilidad básica:** métricas estables ante variación razonable (seed, período, subpoblación).
6. **Consistencia:** mismas cifras en exec summary, cuerpo y anexos; redondeo consistente (ver `informe-ejecutivo.md`).
7. **Registro:** resultado del QA (fecha, hallazgos, correcciones) documentado; hallazgos relevantes al decision log si afectan lo acordado con el cliente.

Reglas:

```text
Nada se entrega sin QA pre-entrega.
/code-review ultra revisa el código; el QA pre-entrega verifica números y metodología. Son complementarios.
```
