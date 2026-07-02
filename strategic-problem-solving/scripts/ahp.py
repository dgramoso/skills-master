"""AHP: pesos de criterios y ratio de consistencia desde una matriz de comparaciones de a pares.

Uso:
    python ahp.py --criteria "Impacto,Factibilidad,Riesgo" --matrix "1,3,5; 0.333,1,3; 0.2,0.333,1"
    python ahp.py --criteria "A,B,C" --matrix "..." --scores "OpcionX:4,3,5; OpcionY:2,5,3"

La matriz se da por filas separadas con ';' y valores con ','. Debe ser cuadrada,
recíproca (m[j][i] ~= 1/m[i][j]) y con diagonal 1. Solo stdlib, sin numpy.

Salida: pesos normalizados por criterio, lambda_max, CI y CR. Con --scores,
además el puntaje ponderado y ranking de cada alternativa.
CR > 0.10 => comparaciones inconsistentes: revisar los pares señalados.
"""

import argparse
import sys

# Índice aleatorio de Saaty (n=1..15)
RANDOM_INDEX = {1: 0.0, 2: 0.0, 3: 0.58, 4: 0.90, 5: 1.12, 6: 1.24, 7: 1.32,
                8: 1.41, 9: 1.45, 10: 1.49, 11: 1.51, 12: 1.54, 13: 1.56,
                14: 1.57, 15: 1.58}

RECIPROCAL_TOLERANCE = 0.05  # tolerancia relativa al validar m[j][i] ~= 1/m[i][j]
CR_THRESHOLD = 0.10


def parse_matrix(text):
    rows = [r.strip() for r in text.split(";") if r.strip()]
    matrix = []
    for r in rows:
        try:
            matrix.append([float(v) for v in r.split(",")])
        except ValueError:
            sys.exit(f"error: fila no numérica: {r!r}")
    n = len(matrix)
    if any(len(row) != n for row in matrix):
        sys.exit("error: la matriz debe ser cuadrada (filas separadas con ';', valores con ',')")
    for i in range(n):
        if abs(matrix[i][i] - 1.0) > 1e-9:
            sys.exit(f"error: la diagonal debe ser 1 (fila {i + 1})")
        for j in range(n):
            if matrix[i][j] <= 0:
                sys.exit("error: todos los valores deben ser positivos")
    return matrix


def check_reciprocity(matrix, criteria):
    problems = []
    n = len(matrix)
    for i in range(n):
        for j in range(i + 1, n):
            expected = 1.0 / matrix[i][j]
            if abs(matrix[j][i] - expected) / expected > RECIPROCAL_TOLERANCE:
                problems.append(
                    f"  {criteria[j]} vs {criteria[i]}: {matrix[j][i]:.3f} "
                    f"(esperado ~{expected:.3f} como recíproco de {matrix[i][j]:.3f})"
                )
    return problems


def compute_weights(matrix):
    """Pesos por normalización de columnas + promedio de filas (aproximación estándar)."""
    n = len(matrix)
    col_sums = [sum(matrix[i][j] for i in range(n)) for j in range(n)]
    weights = [sum(matrix[i][j] / col_sums[j] for j in range(n)) / n for i in range(n)]
    return weights


def consistency(matrix, weights):
    n = len(matrix)
    # lambda_max: promedio de (A·w)_i / w_i
    aw = [sum(matrix[i][j] * weights[j] for j in range(n)) for i in range(n)]
    lambda_max = sum(aw[i] / weights[i] for i in range(n)) / n
    ci = (lambda_max - n) / (n - 1) if n > 1 else 0.0
    ri = RANDOM_INDEX.get(n)
    if ri is None:
        return lambda_max, ci, None
    cr = ci / ri if ri > 0 else 0.0
    return lambda_max, ci, cr


def worst_pairs(matrix, weights, criteria, top=2):
    """Pares cuya comparación más se desvía del ratio de pesos implícito."""
    devs = []
    n = len(matrix)
    for i in range(n):
        for j in range(i + 1, n):
            implied = weights[i] / weights[j]
            dev = abs(matrix[i][j] - implied) / implied
            devs.append((dev, i, j, implied))
    devs.sort(reverse=True)
    lines = []
    for dev, i, j, implied in devs[:top]:
        lines.append(
            f"  {criteria[i]} vs {criteria[j]}: dijiste {matrix[i][j]:.2f}, "
            f"los pesos implican ~{implied:.2f}"
        )
    return lines


def parse_scores(text, n_criteria):
    alternatives = []
    for chunk in text.split(";"):
        chunk = chunk.strip()
        if not chunk:
            continue
        if ":" not in chunk:
            sys.exit(f"error: alternativa sin nombre: {chunk!r} (formato Nombre:s1,s2,...)")
        name, values = chunk.split(":", 1)
        try:
            scores = [float(v) for v in values.split(",")]
        except ValueError:
            sys.exit(f"error: puntajes no numéricos en {name.strip()!r}")
        if len(scores) != n_criteria:
            sys.exit(f"error: {name.strip()!r} tiene {len(scores)} puntajes, se esperaban {n_criteria}")
        alternatives.append((name.strip(), scores))
    return alternatives


def main():
    parser = argparse.ArgumentParser(description="Pesos AHP + ratio de consistencia")
    parser.add_argument("--criteria", required=True, help="nombres separados por coma")
    parser.add_argument("--matrix", required=True, help="filas con ';', valores con ','")
    parser.add_argument("--scores", help="alternativas: 'Nombre:s1,s2,...; Nombre2:...'")
    args = parser.parse_args()

    criteria = [c.strip() for c in args.criteria.split(",") if c.strip()]
    matrix = parse_matrix(args.matrix)
    if len(criteria) != len(matrix):
        sys.exit(f"error: {len(criteria)} criterios pero matriz de {len(matrix)}x{len(matrix)}")

    reciprocity_problems = check_reciprocity(matrix, criteria)
    if reciprocity_problems:
        print("ADVERTENCIA: la matriz no es recíproca en:")
        print("\n".join(reciprocity_problems))
        print()

    weights = compute_weights(matrix)
    lambda_max, ci, cr = consistency(matrix, weights)

    print("Pesos:")
    for name, w in sorted(zip(criteria, weights), key=lambda x: -x[1]):
        print(f"  {name}: {w:.4f} ({w * 100:.1f}%)")
    print(f"\nlambda_max = {lambda_max:.4f} | CI = {ci:.4f}", end="")
    if cr is None:
        print(" | CR no disponible (n fuera de tabla RI)")
    else:
        print(f" | CR = {cr:.4f}")
        if cr > CR_THRESHOLD:
            print(f"\nINCONSISTENTE (CR > {CR_THRESHOLD}). Pares más contradictorios:")
            print("\n".join(worst_pairs(matrix, weights, criteria)))
        else:
            print("Consistencia aceptable.")

    if args.scores:
        alternatives = parse_scores(args.scores, len(criteria))
        results = [(name, sum(w * s for w, s in zip(weights, scores)))
                   for name, scores in alternatives]
        results.sort(key=lambda x: -x[1])
        print("\nRanking ponderado:")
        for rank, (name, total) in enumerate(results, 1):
            print(f"  {rank}. {name}: {total:.3f}")


if __name__ == "__main__":
    main()
