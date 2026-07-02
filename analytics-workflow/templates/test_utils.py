# =====================================================================
# test_utils.py — tests de la biblioteca semilla (paridad con
# test_mis_funciones.r). Correr: python test_utils.py
# También compatible con pytest si está instalado.
# =====================================================================

import math
import warnings

import numpy as np

from utils import (
    calcular_auc,
    calcular_gini,
    calcular_ks,
    calcular_psi,
    tabla_estrategia,
    tabla_lift,
    validar_porcentajes,
    winsorizar_apply,
    winsorizar_fit,
    woe_apply,
    woe_fit,
)


def _espera_error(fn, fragmento):
    try:
        fn()
    except ValueError as e:
        if fragmento not in str(e):
            raise AssertionError(f"error esperado con '{fragmento}', vino: {e}")
        return
    raise AssertionError(f"se esperaba ValueError con '{fragmento}' y no falló")


# ---- calcular_psi ---------------------------------------------------


def test_psi_distribuciones_identicas_es_0():
    x = np.tile(np.arange(1, 101), 10)
    assert calcular_psi(x, x) == 0


def test_psi_detecta_shift_material():
    assert calcular_psi(np.arange(1, 1001), np.arange(501, 1501)) > 0.25


def test_psi_falla_sin_variabilidad():
    _espera_error(lambda: calcular_psi(np.ones(100), np.arange(100)), "variabilidad")


# ---- calcular_ks ----------------------------------------------------


def test_ks_separacion_perfecta_es_1():
    assert calcular_ks([1, 2, 3, 4], [0, 0, 1, 1]) == 1


def test_ks_caso_a_mano_es_0_5():
    assert calcular_ks([1, 2, 3, 4], [0, 1, 0, 1]) == 0.5


def test_ks_score_constante_es_0():
    assert calcular_ks([5] * 10, [0, 1] * 5) == 0


def test_ks_valida_target_y_na():
    _espera_error(lambda: calcular_ks([1, 2, 3, 4], [0, 1, 2, 1]), "0/1")
    _espera_error(lambda: calcular_ks([1, np.nan, 3, 4], [0, 1, 0, 1]), "NA")


# ---- calcular_auc / calcular_gini -----------------------------------


def test_auc_perfecta_es_1_y_gini_1():
    assert calcular_auc([1, 2, 3, 4], [0, 0, 1, 1]) == 1
    assert calcular_gini([1, 2, 3, 4], [0, 0, 1, 1]) == 1


def test_auc_caso_a_mano_es_0_75():
    # pares (malo, bueno): (2,1)+, (2,3)-, (4,1)+, (4,3)+ → 3/4
    assert calcular_auc([1, 2, 3, 4], [0, 1, 0, 1]) == 0.75


def test_auc_score_constante_es_0_5():
    assert calcular_auc([7] * 10, [0, 1] * 5) == 0.5


# ---- tabla_lift -----------------------------------------------------


def test_tabla_lift_score_perfecto():
    score = np.arange(100, 0, -1)
    target = np.array([1] * 10 + [0] * 90)  # los 10 scores más altos son malos
    tl = tabla_lift(score, target, n_grupos=10)

    assert len(tl) == 10
    assert tl["n"].sum() == 100
    assert tl["bad_rate"].iloc[0] == 1
    assert tl["lift"].iloc[0] == 10  # 100% vs 10% global
    assert tl["captura_acum"].iloc[0] == 1
    assert tl["captura_acum"].iloc[9] == 1
    assert tl["pct_pobl_acum"].iloc[9] == 1


def test_tabla_lift_falla_n_grupos_invalido():
    _espera_error(lambda: tabla_lift([1, 2, 3, 4, 5], [0, 1, 0, 1, 0], n_grupos=10), "n_grupos")


# ---- tabla_estrategia -----------------------------------------------


def test_tabla_estrategia_caso_a_mano():
    te = tabla_estrategia([10, 20, 30, 40], [0, 0, 1, 1], cutoffs=30)
    assert te["pct_aprobado"].iloc[0] == 0.5  # aprueba score < 30
    assert te["n_aprobados"].iloc[0] == 2
    assert te["bad_rate_aprobados"].iloc[0] == 0
    assert te["pct_malos_evitados"].iloc[0] == 1


def test_tabla_estrategia_sin_aprobados_da_nan():
    te = tabla_estrategia([10, 20, 30, 40], [0, 0, 1, 1], cutoffs=5)
    assert te["pct_aprobado"].iloc[0] == 0
    assert math.isnan(te["bad_rate_aprobados"].iloc[0])


# ---- winsorizar fit/apply -------------------------------------------


def test_winsorizar_fit_apply_train_test():
    x = np.arange(1, 101)
    lim = winsorizar_fit(x, p_inf=0.05, p_sup=0.95)
    assert lim["inf"] == np.quantile(x, 0.05)
    assert lim["sup"] == np.quantile(x, 0.95)

    # en test, valores fuera de los límites de TRAIN quedan capados
    res = winsorizar_apply([-50, 50, 200], lim)
    assert list(res) == [lim["inf"], 50, lim["sup"]]


def test_winsorizar_valida_parametros():
    _espera_error(lambda: winsorizar_fit(np.arange(10), p_inf=0.9, p_sup=0.1), "p_inf")
    _espera_error(lambda: winsorizar_apply(np.arange(10), {"a": 1}), "winsorizar_fit")


# ---- woe_fit / woe_apply --------------------------------------------


def _caso_categorico():
    # A: 30 buenos / 10 malos; B: 20 buenos / 40 malos
    x = ["A"] * 40 + ["B"] * 60
    target = [0] * 30 + [1] * 10 + [0] * 20 + [1] * 40
    return x, target


def test_woe_iv_caso_a_mano_siddiqi():
    x, target = _caso_categorico()
    fit = woe_fit(x, target)
    tabla = fit["tabla"].set_index("bin")

    assert abs(tabla.loc["A", "woe"] - math.log(3)) < 1e-10  # ln(0.6/0.2)
    assert abs(tabla.loc["B", "woe"] - math.log(0.5)) < 1e-10  # ln(0.4/0.8)
    esperado_iv = 0.4 * math.log(3) + (-0.4) * math.log(0.5)  # ≈ 0.7167
    assert abs(fit["iv_total"] - esperado_iv) < 1e-10


def test_woe_apply_mapea_y_neutraliza_categorias_nuevas():
    x, target = _caso_categorico()
    fit = woe_fit(x, target)

    res = woe_apply(["A", "B"], fit)
    assert abs(res[0] - math.log(3)) < 1e-10
    assert abs(res[1] - math.log(0.5)) < 1e-10

    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        res = woe_apply(["A", "C"], fit)
        assert any("sin bin conocido" in str(wi.message) for wi in w)
    assert res[1] == 0


def test_woe_numerico_fit_apply_y_missing():
    x = list(range(1, 100)) + [np.nan]
    target = [0, 1] * 50
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        fit = woe_fit(x, target, n_bins=4)
        assert fit["tipo"] == "numerico"
        assert "MISSING" in set(fit["tabla"]["bin"])
        res = woe_apply(x, fit)
    assert len(res) == 100
    assert not np.isnan(res).any()


def test_woe_advierte_iv_mayor_a_1_leakage():
    x = ["A"] * 50 + ["B"] * 50
    target = [0] * 49 + [1] + [1] * 49 + [0]  # separación casi perfecta
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        woe_fit(x, target)
        assert any("leakage" in str(wi.message) for wi in w)


# ---- validar_porcentajes --------------------------------------------


def test_validar_porcentajes_pasa_y_falla():
    assert validar_porcentajes([50, 30, 20])
    assert validar_porcentajes([0.5, 0.3, 0.2], total=1)
    _espera_error(lambda: validar_porcentajes([50, 30, 25]), "Quality Gate")
    _espera_error(lambda: validar_porcentajes([50, np.nan]), "NA")


# ---- runner sin pytest ----------------------------------------------

if __name__ == "__main__":
    import sys
    import traceback

    fallas = 0
    tests = sorted(k for k in list(globals()) if k.startswith("test_"))
    for nombre in tests:
        try:
            globals()[nombre]()
            print(f"OK   {nombre}")
        except Exception:
            fallas += 1
            print(f"FAIL {nombre}")
            traceback.print_exc()
    print(f"\n{len(tests) - fallas}/{len(tests)} tests pasaron.")
    sys.exit(1 if fallas else 0)
