# Interpretaciones automáticas vía Claude API

> Parte de la skill `analytics-workflow`. Opcional — el pipeline no debe romperse si no hay API key.

El script de informe puede llamar a Claude directamente para generar narrativa analítica con los números reales de cada corrida, en lugar de usar textos hardcodeados.

## Función `llamar_claude()` en `mis_funciones.r`

```r
llamar_claude <- function(prompt, max_tokens = 400) {
  api_key <- Sys.getenv("ANTHROPIC_API_KEY")

  if (!nzchar(api_key)) {
    warning("ANTHROPIC_API_KEY no configurada — saltando interpretación automática")
    return("")
  }

  tryCatch({
    resp <- httr2::request("https://api.anthropic.com/v1/messages") |>
      httr2::req_headers(
        "x-api-key"         = api_key,
        "anthropic-version" = "2023-06-01",
        "content-type"      = "application/json"
      ) |>
      httr2::req_body_json(list(
        model      = "claude-haiku-4-5-20251001",
        max_tokens = max_tokens,
        messages   = list(list(role = "user", content = prompt))
      )) |>
      httr2::req_perform() |>
      httr2::resp_body_json()

    resp$content[[1]]$text

  }, error = function(e) {
    warning("Error llamando a Claude API: ", e$message)
    ""
  })
}
```

## Secciones típicas a generar automáticamente en el informe

| Sección         | Qué interpreta Claude                                                 |
| --------------- | --------------------------------------------------------------------- |
| Performance     | Métricas del modelo en función de variables reales y bad rate         |
| Calibración     | Si el modelo está bien calibrado y dónde hay mayor desvío             |
| Estabilidad     | PSI e implicancias para producción                                    |
| Recomendaciones | Cutoffs, mejoras y monitoreo con números reales                       |
| Segmentos       | Lectura de clusters, perfiles y accionabilidad                        |
| Alertas         | Señales de drift, leakage, baja cobertura o resultados inconsistentes |

## Configuración

Agregar en `~/.Renviron`:

```text
ANTHROPIC_API_KEY=sk-ant-...
```

La función devuelve `""` si no hay API key, sin romper el pipeline.

Reglas:

* No enviar datos personales innecesarios.
* No enviar información sensible si no es imprescindible.
* Preferir prompts con métricas agregadas, no datasets completos.
* La narrativa generada debe revisarse antes de entregar al cliente.
* El informe debe seguir siendo reproducible aunque la API no responda.
