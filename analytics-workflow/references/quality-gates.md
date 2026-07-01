# Quality Gates y reglas anti-leakage

> Parte de la skill `analytics-workflow`. Ver `SKILL.md` para el flujo general.

---

## Quality Gates

Patrón estándar:

```r
stopifnot(
  "archivo input ausente" = file.exists(PATH_INPUT),
  "target ausente" = TARGET %in% names(datos)
)

if (alguna_condicion_critica) {
  stop("Quality Gate: descripción del problema")
}
```

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
