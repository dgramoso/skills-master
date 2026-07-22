# =====================================================================
# mis_funciones.r — biblioteca semilla del analytics-workflow
# Copiar a scripts/mis_funciones.r del proyecto. Tests: test_mis_funciones.r
# =====================================================================
# Convenciones:
#   - target: vector 0/1 donde 1 = evento ("malo").
#   - score:  mayor score = mayor riesgo. Si tu scorecard es al revés
#     (mayor puntaje = mejor), pasar -score o invertir la lectura de cutoffs.
#   - Anti-leakage: las funciones *_fit aprenden parámetros (SOLO con train);
#     las *_apply aplican parámetros congelados (test / OOT / producción).
#   - WOE con convención Siddiqi: WOE = ln(dist_buenos / dist_malos);
#     IV = sum((dist_buenos - dist_malos) * WOE).
#   - En tabla_lift, empates de score en el borde de un grupo se reparten
#     por orden de aparición.
# Sin dependencias fuera de base R.
# =====================================================================

# ---- validadores internos -------------------------------------------

.validar_target <- function(target) {
  if (anyNA(target)) stop("target contiene NA")
  if (!all(target %in% c(0, 1))) stop("target debe ser 0/1 (1 = evento)")
  if (length(unique(target)) < 2) stop("target necesita ambas clases (0 y 1)")
  invisible(TRUE)
}

.validar_score <- function(score, target) {
  if (!is.numeric(score)) stop("score debe ser numérico")
  if (anyNA(score)) stop("score contiene NA")
  if (length(score) != length(target)) stop("score y target tienen largo distinto")
  invisible(TRUE)
}

# ---- estabilidad ----------------------------------------------------

# PSI entre una distribución esperada (desarrollo) y una observada (actual).
# Bins por deciles de la distribución esperada. > 0.25 = cambio material.
calcular_psi <- function(esperado, observado, n_bins = 10, min_prop = 1e-4) {
  if (!is.numeric(esperado) || !is.numeric(observado)) stop("calcular_psi: inputs deben ser numéricos")
  esperado  <- esperado[!is.na(esperado)]
  observado <- observado[!is.na(observado)]
  if (!length(esperado) || !length(observado)) stop("calcular_psi: vector vacío tras remover NA")

  cortes <- unique(quantile(esperado, probs = seq(0, 1, length.out = n_bins + 1), names = FALSE))
  if (length(cortes) < 3) stop("calcular_psi: variabilidad insuficiente en 'esperado' para binear")
  cortes[1] <- -Inf
  cortes[length(cortes)] <- Inf

  k <- length(cortes) - 1
  p_esp <- tabulate(cut(esperado,  cortes, labels = FALSE), nbins = k) / length(esperado)
  p_obs <- tabulate(cut(observado, cortes, labels = FALSE), nbins = k) / length(observado)
  p_esp <- pmax(p_esp, min_prop)  # evita log(0) en bins vacíos
  p_obs <- pmax(p_obs, min_prop)

  sum((p_obs - p_esp) * log(p_obs / p_esp))
}

# ---- discriminación -------------------------------------------------

# KS: máxima distancia entre las ECDF de malos y buenos sobre el score.
calcular_ks <- function(score, target) {
  .validar_target(target); .validar_score(score, target)
  malos  <- score[target == 1]
  buenos <- score[target == 0]
  puntos <- sort(unique(score))
  max(abs(ecdf(malos)(puntos) - ecdf(buenos)(puntos)))
}

# AUC vía Mann-Whitney (equivale a P(score_malo > score_bueno), empates a medias).
calcular_auc <- function(score, target) {
  .validar_target(target); .validar_score(score, target)
  r  <- rank(score)
  n1 <- sum(target == 1)
  n0 <- sum(target == 0)
  (sum(r[target == 1]) - n1 * (n1 + 1) / 2) / (n1 * n0)
}

calcular_gini <- function(score, target) 2 * calcular_auc(score, target) - 1

# ---- tablas de negocio ----------------------------------------------

# Tabla de lift/gain por grupos de score (grupo 1 = mayor riesgo).
tabla_lift <- function(score, target, n_grupos = 10) {
  .validar_target(target); .validar_score(score, target)
  n <- length(score)
  if (n_grupos < 2 || n < n_grupos) stop("tabla_lift: n_grupos inválido para el tamaño de la muestra")

  orden  <- order(-score)
  grupo  <- ceiling(seq_len(n) * n_grupos / n)
  t_sort <- target[orden]
  malos  <- tapply(t_sort, grupo, sum)
  casos  <- tapply(t_sort, grupo, length)
  bad_rate_global <- mean(target)

  out <- data.frame(
    grupo         = as.integer(names(casos)),
    n             = as.integer(casos),
    malos         = as.integer(malos),
    bad_rate      = as.numeric(malos / casos),
    lift          = as.numeric((malos / casos) / bad_rate_global),
    captura_acum  = as.numeric(cumsum(malos) / sum(target)),
    pct_pobl_acum = as.numeric(cumsum(casos) / n),
    row.names     = NULL
  )
  if (sum(out$n) != n) stop("Quality Gate: tabla_lift — los grupos no cubren toda la muestra")
  out
}

# Strategy table: aprobación y bad rate por cutoff.
# Convención: mayor score = mayor riesgo → se aprueba score < cutoff.
tabla_estrategia <- function(score, target, cutoffs) {
  .validar_target(target); .validar_score(score, target)
  if (!length(cutoffs)) stop("tabla_estrategia: cutoffs vacío")

  total_malos <- sum(target)
  filas <- lapply(sort(cutoffs), function(k) {
    aprobado <- score < k
    data.frame(
      cutoff             = k,
      n_aprobados        = sum(aprobado),
      pct_aprobado       = mean(aprobado),
      bad_rate_aprobados = if (any(aprobado)) mean(target[aprobado]) else NA_real_,
      pct_malos_evitados = sum(target[!aprobado]) / total_malos
    )
  })
  do.call(rbind, filas)
}

# ---- transformaciones fit/apply -------------------------------------

# Winsorización: fit aprende límites en train; apply los aplica congelados.
winsorizar_fit <- function(x, p_inf = 0.01, p_sup = 0.99) {
  if (!is.numeric(x)) stop("winsorizar_fit: x debe ser numérico")
  if (p_inf >= p_sup) stop("winsorizar_fit: p_inf debe ser < p_sup")
  q <- quantile(x, probs = c(p_inf, p_sup), na.rm = TRUE, names = FALSE)
  list(inf = q[1], sup = q[2])
}

winsorizar_apply <- function(x, limites) {
  if (!all(c("inf", "sup") %in% names(limites))) stop("winsorizar_apply: limites debe venir de winsorizar_fit")
  pmin(pmax(x, limites$inf), limites$sup)
}

# WOE/IV: fit binea (numérico por cuantiles; categórico por categoría) y
# calcula WOE e IV con suavizado 0.5 en bins sin buenos o sin malos.
# Missing es un bin propio ("MISSING"). Advierte si IV > 0.9 (posible leakage).
woe_fit <- function(x, target, n_bins = 5) {
  .validar_target(target)
  if (length(x) != length(target)) stop("woe_fit: x y target de largo distinto")

  if (is.numeric(x)) {
    tipo   <- "numerico"
    cortes <- unique(quantile(x, probs = seq(0, 1, length.out = n_bins + 1), na.rm = TRUE, names = FALSE))
    if (length(cortes) < 3) stop("woe_fit: variabilidad insuficiente para binear")
    cortes[1] <- -Inf
    cortes[length(cortes)] <- Inf
    bin <- as.character(cut(x, cortes))
  } else {
    tipo   <- "categorico"
    cortes <- NULL
    bin    <- as.character(x)
  }
  bin[is.na(bin)] <- "MISSING"

  malos  <- tapply(target, bin, sum)
  casos  <- tapply(target, bin, length)
  buenos <- casos - malos

  ajuste   <- (malos == 0 | buenos == 0) * 0.5
  malos_a  <- malos  + ajuste
  buenos_a <- buenos + ajuste

  dist_malos  <- malos_a  / sum(malos_a)
  dist_buenos <- buenos_a / sum(buenos_a)
  woe <- log(dist_buenos / dist_malos)          # convención Siddiqi
  iv  <- (dist_buenos - dist_malos) * woe

  tabla <- data.frame(
    bin         = names(casos),
    n           = as.integer(casos),
    malos       = as.integer(malos),
    buenos      = as.integer(buenos),
    dist_malos  = as.numeric(dist_malos),
    dist_buenos = as.numeric(dist_buenos),
    woe         = as.numeric(woe),
    iv          = as.numeric(iv),
    row.names   = NULL
  )
  iv_total <- sum(tabla$iv)
  if (iv_total > 0.9) warning(sprintf("woe_fit: IV = %.3f > 0.9 — sospechosa de leakage, investigar", iv_total))

  list(tipo = tipo, cortes = cortes, tabla = tabla, iv_total = iv_total)
}

# Aplica un woe_fit congelado. Categorías nuevas o MISSING no visto en train
# reciben WOE 0 (neutral) con warning.
woe_apply <- function(x, ajuste_woe) {
  if (!all(c("tipo", "tabla") %in% names(ajuste_woe))) stop("woe_apply: ajuste_woe debe venir de woe_fit")

  if (ajuste_woe$tipo == "numerico") {
    if (!is.numeric(x)) stop("woe_apply: x debe ser numérico para un fit numérico")
    bin <- as.character(cut(x, ajuste_woe$cortes))
  } else {
    bin <- as.character(x)
  }
  bin[is.na(bin)] <- "MISSING"

  idx <- match(bin, ajuste_woe$tabla$bin)
  woe <- ajuste_woe$tabla$woe[idx]
  sin_match <- is.na(idx)
  if (any(sin_match)) {
    warning(sprintf("woe_apply: %d valores sin bin conocido — se asigna WOE 0 (neutral)", sum(sin_match)))
    woe[sin_match] <- 0
  }
  woe
}

# ---- quality gates --------------------------------------------------

# Falla si los porcentajes no suman el total esperado (default 100).
validar_porcentajes <- function(x, total = 100, tolerancia = 0.01) {
  if (anyNA(x)) stop("validar_porcentajes: hay NA")
  if (abs(sum(x) - total) > tolerancia)
    stop(sprintf("Quality Gate: los porcentajes suman %.4f, se esperaba %s (±%s)", sum(x), total, tolerancia))
  invisible(TRUE)
}
