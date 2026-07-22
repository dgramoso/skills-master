# =====================================================================
# test_mis_funciones.r — tests de la biblioteca semilla (testthat)
# Correr desde este directorio: Rscript test_mis_funciones.r
# =====================================================================

library(testthat)
source("mis_funciones.r")

# ---- calcular_psi ---------------------------------------------------

test_that("PSI de distribuciones idénticas es 0", {
  x <- rep(1:100, 10)
  expect_equal(calcular_psi(x, x), 0)
})

test_that("PSI detecta un shift material (> 0.25)", {
  esperado  <- 1:1000
  observado <- 501:1500
  expect_gt(calcular_psi(esperado, observado), 0.25)
})

test_that("PSI falla con input sin variabilidad", {
  expect_error(calcular_psi(rep(1, 100), 1:100), "variabilidad")
})

# ---- calcular_ks ----------------------------------------------------

test_that("KS con separación perfecta es 1", {
  expect_equal(calcular_ks(c(1, 2, 3, 4), c(0, 0, 1, 1)), 1)
})

test_that("KS de caso intercalado calculado a mano es 0.5", {
  expect_equal(calcular_ks(c(1, 2, 3, 4), c(0, 1, 0, 1)), 0.5)
})

test_that("KS con score constante es 0", {
  expect_equal(calcular_ks(rep(5, 10), rep(c(0, 1), 5)), 0)
})

test_that("KS valida target binario y NA", {
  expect_error(calcular_ks(1:4, c(0, 1, 2, 1)), "0/1")
  expect_error(calcular_ks(c(1, NA, 3, 4), c(0, 1, 0, 1)), "NA")
})

# ---- calcular_auc / calcular_gini -----------------------------------

test_that("AUC perfecta es 1 y Gini 1", {
  expect_equal(calcular_auc(c(1, 2, 3, 4), c(0, 0, 1, 1)), 1)
  expect_equal(calcular_gini(c(1, 2, 3, 4), c(0, 0, 1, 1)), 1)
})

test_that("AUC de caso a mano es 0.75", {
  # pares (malo, bueno): (2,1)+, (2,3)-, (4,1)+, (4,3)+ → 3/4
  expect_equal(calcular_auc(c(1, 2, 3, 4), c(0, 1, 0, 1)), 0.75)
})

test_that("AUC con score constante es 0.5", {
  expect_equal(calcular_auc(rep(7, 10), rep(c(0, 1), 5)), 0.5)
})

# ---- tabla_lift -----------------------------------------------------

test_that("tabla_lift con score perfecto: grupo 1 captura todos los malos", {
  score  <- 100:1
  target <- c(rep(1, 10), rep(0, 90))  # los 10 scores más altos son malos
  tl <- tabla_lift(score, target, n_grupos = 10)

  expect_equal(nrow(tl), 10)
  expect_equal(sum(tl$n), 100)
  expect_equal(tl$bad_rate[1], 1)
  expect_equal(tl$lift[1], 10)          # 100% vs 10% global
  expect_equal(tl$captura_acum[1], 1)   # grupo 1 captura el 100% de los malos
  expect_equal(tl$captura_acum[10], 1)
  expect_equal(tl$pct_pobl_acum[10], 1)
})

test_that("tabla_lift falla con n_grupos inválido", {
  expect_error(tabla_lift(1:5, c(0, 1, 0, 1, 0), n_grupos = 10), "n_grupos")
})

# ---- tabla_estrategia -----------------------------------------------

test_that("tabla_estrategia calcula aprobación y malos evitados", {
  score  <- c(10, 20, 30, 40)
  target <- c(0, 0, 1, 1)
  te <- tabla_estrategia(score, target, cutoffs = 30)

  expect_equal(te$pct_aprobado, 0.5)          # aprueba score < 30
  expect_equal(te$n_aprobados, 2L)
  expect_equal(te$bad_rate_aprobados, 0)
  expect_equal(te$pct_malos_evitados, 1)
})

test_that("tabla_estrategia con cutoff que no aprueba a nadie da NA de bad rate", {
  te <- tabla_estrategia(c(10, 20, 30, 40), c(0, 0, 1, 1), cutoffs = 5)
  expect_equal(te$pct_aprobado, 0)
  expect_true(is.na(te$bad_rate_aprobados))
})

# ---- winsorizar fit/apply -------------------------------------------

test_that("winsorizar aprende en train y aplica congelado en test", {
  lim <- winsorizar_fit(1:100, p_inf = 0.05, p_sup = 0.95)
  expect_equal(lim$inf, quantile(1:100, 0.05, names = FALSE))
  expect_equal(lim$sup, quantile(1:100, 0.95, names = FALSE))

  # en test, valores fuera de los límites de TRAIN quedan capados
  res <- winsorizar_apply(c(-50, 50, 200), lim)
  expect_equal(res, c(lim$inf, 50, lim$sup))
})

test_that("winsorizar valida parámetros", {
  expect_error(winsorizar_fit(1:10, p_inf = 0.9, p_sup = 0.1), "p_inf")
  expect_error(winsorizar_apply(1:10, list(a = 1)), "winsorizar_fit")
})

# ---- woe_fit / woe_apply --------------------------------------------

test_that("WOE e IV de caso categórico calculado a mano (Siddiqi)", {
  # A: 30 buenos / 10 malos; B: 20 buenos / 40 malos
  x      <- c(rep("A", 40), rep("B", 60))
  target <- c(rep(0, 30), rep(1, 10), rep(0, 20), rep(1, 40))
  fit    <- woe_fit(x, target)

  tabla <- fit$tabla[order(fit$tabla$bin), ]
  expect_equal(tabla$woe[tabla$bin == "A"], log(3), tolerance = 1e-10)      # ln(0.6/0.2)
  expect_equal(tabla$woe[tabla$bin == "B"], log(0.5), tolerance = 1e-10)    # ln(0.4/0.8)
  expect_equal(fit$iv_total, 0.4 * log(3) + (-0.4) * log(0.5), tolerance = 1e-10)  # ≈ 0.7167
})

test_that("woe_apply mapea con los bins de train y neutraliza categorías nuevas", {
  x      <- c(rep("A", 40), rep("B", 60))
  target <- c(rep(0, 30), rep(1, 10), rep(0, 20), rep(1, 40))
  fit    <- woe_fit(x, target)

  expect_equal(woe_apply(c("A", "B"), fit), c(log(3), log(0.5)), tolerance = 1e-10)
  expect_warning(res <- woe_apply(c("A", "C"), fit), "sin bin conocido")
  expect_equal(res[2], 0)
})

test_that("woe_fit numérico: fit/apply consistente y MISSING como bin propio", {
  set_x  <- c(1:99, NA)
  target <- rep(c(0, 1), 50)
  fit    <- suppressWarnings(woe_fit(set_x, target, n_bins = 4))

  expect_equal(fit$tipo, "numerico")
  expect_true("MISSING" %in% fit$tabla$bin)
  res <- suppressWarnings(woe_apply(set_x, fit))
  expect_equal(length(res), 100)
  expect_true(!anyNA(res))
})

test_that("woe_fit advierte IV > 0.9 como sospecha de leakage", {
  x      <- c(rep("A", 50), rep("B", 50))
  target <- c(rep(0, 49), 1, rep(1, 49), 0)   # separación casi perfecta
  expect_warning(woe_fit(x, target), "leakage")
})

# ---- validar_porcentajes --------------------------------------------

test_that("validar_porcentajes pasa y falla según corresponde", {
  expect_true(validar_porcentajes(c(50, 30, 20)))
  expect_true(validar_porcentajes(c(0.5, 0.3, 0.2), total = 1))
  expect_error(validar_porcentajes(c(50, 30, 25)), "Quality Gate")
  expect_error(validar_porcentajes(c(50, NA)), "NA")
})

cat("\nTodos los tests de mis_funciones.r pasaron.\n")
