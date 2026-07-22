# =====================================================================
# utils.py — biblioteca semilla del analytics-workflow (equivalente de
# mis_funciones.r). Copiar a scripts/utils.py del proyecto.
# Tests: test_utils.py (correr con `python test_utils.py`; también compatible pytest)
# =====================================================================
# Convenciones (idénticas a la versión R):
#   - target: array 0/1 donde 1 = evento ("malo").
#   - score:  mayor score = mayor riesgo. Si tu scorecard es al revés
#     (mayor puntaje = mejor), pasar -score o invertir la lectura de cutoffs.
#   - Anti-leakage: las funciones *_fit aprenden parámetros (SOLO con train);
#     las *_apply aplican parámetros congelados (test / OOT / producción).
#   - WOE con convención Siddiqi: WOE = ln(dist_buenos / dist_malos);
#     IV = sum((dist_buenos - dist_malos) * WOE).
#   - Gates críticos con raise (no assert: `python -O` los elimina).
# Dependencias: numpy y pandas.
# =====================================================================

import warnings

import numpy as np
import pandas as pd

# ---- validadores internos -------------------------------------------


def _validar_target(target):
    target = np.asarray(target)
    if pd.isna(target).any():
        raise ValueError("target contiene NA")
    if not np.isin(target, [0, 1]).all():
        raise ValueError("target debe ser 0/1 (1 = evento)")
    if len(np.unique(target)) < 2:
        raise ValueError("target necesita ambas clases (0 y 1)")
    return target.astype(int)


def _validar_score(score, target):
    score = np.asarray(score, dtype=float)
    if np.isnan(score).any():
        raise ValueError("score contiene NA")
    if len(score) != len(target):
        raise ValueError("score y target tienen largo distinto")
    return score


# ---- estabilidad ----------------------------------------------------


def calcular_psi(esperado, observado, n_bins=10, min_prop=1e-4):
    """PSI entre distribución esperada (desarrollo) y observada (actual).

    Bins por deciles de la esperada. > 0.25 = cambio material.
    """
    esperado = np.asarray(esperado, dtype=float)
    observado = np.asarray(observado, dtype=float)
    esperado = esperado[~np.isnan(esperado)]
    observado = observado[~np.isnan(observado)]
    if len(esperado) == 0 or len(observado) == 0:
        raise ValueError("calcular_psi: vector vacío tras remover NA")

    cortes = np.unique(np.quantile(esperado, np.linspace(0, 1, n_bins + 1)))
    if len(cortes) < 3:
        raise ValueError("calcular_psi: variabilidad insuficiente en 'esperado' para binear")
    internos = cortes[1:-1]  # bins (a, b] como cut() de R, extremos abiertos a ±inf
    k = len(internos) + 1

    def _props(x):
        idx = np.searchsorted(internos, x, side="left")
        return np.bincount(idx, minlength=k) / len(x)

    p_esp = np.maximum(_props(esperado), min_prop)  # evita log(0) en bins vacíos
    p_obs = np.maximum(_props(observado), min_prop)
    return float(np.sum((p_obs - p_esp) * np.log(p_obs / p_esp)))


# ---- discriminación -------------------------------------------------


def calcular_ks(score, target):
    """KS: máxima distancia entre las ECDF de malos y buenos sobre el score."""
    target = _validar_target(target)
    score = _validar_score(score, target)
    malos = np.sort(score[target == 1])
    buenos = np.sort(score[target == 0])
    puntos = np.unique(score)
    f_malos = np.searchsorted(malos, puntos, side="right") / len(malos)
    f_buenos = np.searchsorted(buenos, puntos, side="right") / len(buenos)
    return float(np.max(np.abs(f_malos - f_buenos)))


def calcular_auc(score, target):
    """AUC vía Mann-Whitney (P(score_malo > score_bueno), empates a medias)."""
    target = _validar_target(target)
    score = _validar_score(score, target)
    r = pd.Series(score).rank().to_numpy()  # empates a rango medio, como rank() de R
    n1 = int(target.sum())
    n0 = len(target) - n1
    return float((r[target == 1].sum() - n1 * (n1 + 1) / 2) / (n1 * n0))


def calcular_gini(score, target):
    return 2 * calcular_auc(score, target) - 1


# ---- tablas de negocio ----------------------------------------------


def tabla_lift(score, target, n_grupos=10):
    """Tabla de lift/gain por grupos de score (grupo 1 = mayor riesgo).

    Empates de score en el borde de un grupo se reparten por orden de aparición.
    """
    target = _validar_target(target)
    score = _validar_score(score, target)
    n = len(score)
    if n_grupos < 2 or n < n_grupos:
        raise ValueError("tabla_lift: n_grupos inválido para el tamaño de la muestra")

    orden = np.argsort(-score, kind="stable")
    grupo = np.ceil(np.arange(1, n + 1) * n_grupos / n).astype(int)
    df = pd.DataFrame({"grupo": grupo, "target": target[orden]})
    agg = df.groupby("grupo")["target"].agg(n="count", malos="sum").reset_index()

    bad_rate_global = target.mean()
    agg["bad_rate"] = agg["malos"] / agg["n"]
    agg["lift"] = agg["bad_rate"] / bad_rate_global
    agg["captura_acum"] = agg["malos"].cumsum() / target.sum()
    agg["pct_pobl_acum"] = agg["n"].cumsum() / n

    if agg["n"].sum() != n:
        raise ValueError("Quality Gate: tabla_lift — los grupos no cubren toda la muestra")
    return agg


def tabla_estrategia(score, target, cutoffs):
    """Strategy table: aprobación y bad rate por cutoff.

    Convención: mayor score = mayor riesgo → se aprueba score < cutoff.
    """
    target = _validar_target(target)
    score = _validar_score(score, target)
    cutoffs = np.atleast_1d(np.asarray(cutoffs, dtype=float))
    if len(cutoffs) == 0:
        raise ValueError("tabla_estrategia: cutoffs vacío")

    total_malos = target.sum()
    filas = []
    for k in np.sort(cutoffs):
        aprobado = score < k
        filas.append(
            {
                "cutoff": k,
                "n_aprobados": int(aprobado.sum()),
                "pct_aprobado": float(aprobado.mean()),
                "bad_rate_aprobados": float(target[aprobado].mean()) if aprobado.any() else np.nan,
                "pct_malos_evitados": float(target[~aprobado].sum() / total_malos),
            }
        )
    return pd.DataFrame(filas)


# ---- transformaciones fit/apply -------------------------------------


def winsorizar_fit(x, p_inf=0.01, p_sup=0.99):
    """Aprende límites de winsorización en train (np.quantile ≡ quantile type 7 de R)."""
    if p_inf >= p_sup:
        raise ValueError("winsorizar_fit: p_inf debe ser < p_sup")
    x = np.asarray(x, dtype=float)
    x = x[~np.isnan(x)]
    q = np.quantile(x, [p_inf, p_sup])
    return {"inf": float(q[0]), "sup": float(q[1])}


def winsorizar_apply(x, limites):
    """Aplica límites congelados (aprendidos en train)."""
    if not {"inf", "sup"} <= set(limites):
        raise ValueError("winsorizar_apply: limites debe venir de winsorizar_fit")
    return np.clip(np.asarray(x, dtype=float), limites["inf"], limites["sup"])


def woe_fit(x, target, n_bins=5):
    """WOE/IV: binea (numérico por cuantiles; categórico por categoría) sobre TRAIN.

    Suavizado 0.5 en bins sin buenos o sin malos. Missing es bin propio
    ("MISSING"). Advierte si IV > 0.9 (posible leakage).
    """
    target = _validar_target(target)
    x = pd.Series(x).reset_index(drop=True)
    if len(x) != len(target):
        raise ValueError("woe_fit: x y target de largo distinto")

    if pd.api.types.is_numeric_dtype(x):
        tipo = "numerico"
        cortes = np.unique(np.quantile(x.dropna(), np.linspace(0, 1, n_bins + 1)))
        if len(cortes) < 3:
            raise ValueError("woe_fit: variabilidad insuficiente para binear")
        cortes[0], cortes[-1] = -np.inf, np.inf
        bin_ = pd.cut(x, cortes).astype(str)  # right=True ≡ cut() de R: (a, b]
    else:
        tipo = "categorico"
        cortes = None
        bin_ = x.astype(str)
    bin_[x.isna()] = "MISSING"

    df = pd.DataFrame({"bin": bin_, "target": target})
    agg = df.groupby("bin")["target"].agg(n="count", malos="sum").reset_index()
    agg["buenos"] = agg["n"] - agg["malos"]

    ajuste = ((agg["malos"] == 0) | (agg["buenos"] == 0)) * 0.5
    malos_a = agg["malos"] + ajuste
    buenos_a = agg["buenos"] + ajuste

    agg["dist_malos"] = malos_a / malos_a.sum()
    agg["dist_buenos"] = buenos_a / buenos_a.sum()
    agg["woe"] = np.log(agg["dist_buenos"] / agg["dist_malos"])  # convención Siddiqi
    agg["iv"] = (agg["dist_buenos"] - agg["dist_malos"]) * agg["woe"]

    iv_total = float(agg["iv"].sum())
    if iv_total > 0.9:
        warnings.warn(f"woe_fit: IV = {iv_total:.3f} > 0.9 — sospechosa de leakage, investigar")

    return {"tipo": tipo, "cortes": cortes, "tabla": agg, "iv_total": iv_total}


def woe_apply(x, ajuste_woe):
    """Aplica un woe_fit congelado. Categorías nuevas o MISSING no visto en
    train reciben WOE 0 (neutral) con warning."""
    if not {"tipo", "tabla"} <= set(ajuste_woe):
        raise ValueError("woe_apply: ajuste_woe debe venir de woe_fit")

    x = pd.Series(x).reset_index(drop=True)
    if ajuste_woe["tipo"] == "numerico":
        if not pd.api.types.is_numeric_dtype(x):
            raise ValueError("woe_apply: x debe ser numérico para un fit numérico")
        bin_ = pd.cut(x, ajuste_woe["cortes"]).astype(str)
    else:
        bin_ = x.astype(str)
    bin_[x.isna()] = "MISSING"

    mapa = dict(zip(ajuste_woe["tabla"]["bin"], ajuste_woe["tabla"]["woe"]))
    woe = bin_.map(mapa)
    sin_match = woe.isna()
    if sin_match.any():
        warnings.warn(
            f"woe_apply: {int(sin_match.sum())} valores sin bin conocido — se asigna WOE 0 (neutral)"
        )
        woe[sin_match] = 0.0
    return woe.astype(float).to_numpy()


# ---- quality gates --------------------------------------------------


def validar_porcentajes(x, total=100, tolerancia=0.01):
    """Falla si los porcentajes no suman el total esperado (default 100)."""
    x = np.asarray(x, dtype=float)
    if np.isnan(x).any():
        raise ValueError("validar_porcentajes: hay NA")
    if abs(x.sum() - total) > tolerancia:
        raise ValueError(
            f"Quality Gate: los porcentajes suman {x.sum():.4f}, se esperaba {total} (±{tolerancia})"
        )
    return True
