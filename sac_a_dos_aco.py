"""
Problème du sac à dos 0/1 résolu par colonie de fourmis (ACO).

Représentation : x = [x1..xn], xi = 1 si l'objet Oi est dans le sac.
Heuristique    : eta_j = V_j / p_j  (distance d_ij = p_j / V_j = 1/eta_j)
Pheromone      : matrice tau[i][j] sur les "arêtes" entre objets.
"""
import random


def aco_knapsack(values, weights, C, n_ants=None, n_iter=100,
                 alpha=1.0, beta=2.0, rho=0.1, Q=1.0, seed=None):
    rnd = random.Random(seed)
    n = len(values)
    n_ants = n_ants or n                       # une fourmi par objet
    eta = [values[j] / weights[j] for j in range(n)]
    tau = [[1.0] * n for _ in range(n)]        # phéromone initiale

    best_x, best_val = [0] * n, 0

    for _ in range(n_iter):
        solutions = []
        for k in range(n_ants):
            x = [0] * n
            cur = k % n if n_ants >= n else rnd.randrange(n)  # départ
            load, val = 0, 0
            if weights[cur] <= C:
                x[cur], load, val = 1, weights[cur], values[cur]
            while True:
                # objets encore faisables
                cand = [j for j in range(n)
                        if x[j] == 0 and load + weights[j] <= C]
                if not cand:
                    break
                w = [(tau[cur][j] ** alpha) * (eta[j] ** beta) for j in cand]
                j = rnd.choices(cand, weights=w)[0]
                x[j] = 1
                load += weights[j]
                val += values[j]
                cur = j
            solutions.append((x, val))
            if val > best_val:
                best_x, best_val = x[:], val

        # évaporation
        for i in range(n):
            for j in range(n):
                tau[i][j] *= (1 - rho)

        # dépôt : chaque fourmi dépose proportionnellement à la valeur obtenue
        for x, val in solutions + [(best_x, best_val)]:   # + élitisme
            items = [i for i in range(n) if x[i]]
            for a, b in zip(items, items[1:]):
                tau[a][b] += Q * val / (best_val or 1)
                tau[b][a] += Q * val / (best_val or 1)

    return best_x, best_val


def dp_knapsack(values, weights, C):
    """Optimum exact (programmation dynamique) pour vérifier."""
    dp = [0] * (C + 1)
    for v, w in zip(values, weights):
        for c in range(C, w - 1, -1):
            dp[c] = max(dp[c], dp[c - w] + v)
    return dp[C]


if __name__ == "__main__":
    V = [60, 100, 120, 80, 30, 50, 70, 40]
    P = [10, 20, 30, 25, 5, 15, 22, 12]
    C = 60

    x, val = aco_knapsack(V, P, C, n_iter=100, seed=1)
    print("Solution ACO :", x)
    print("Valeur       :", val)
    print("Poids        :", sum(p for p, xi in zip(P, x) if xi), "/", C)
    print("Optimum exact:", dp_knapsack(V, P, C))
