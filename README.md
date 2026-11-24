# Correction du TD4 : Algorithmes évolutionnaires et métaheuristiques

Faculté des Sciences de Sfax

Contenu du dossier :
- `README.md` : la correction des exercices 1 à 4 (ce fichier)
- `sac_a_dos_aco.py` : programme Python du sac à dos par colonie de fourmis

**Théorème des schèmes** utilisé dans les exercices 1 et 2 :

```
m(H,t+1) >= m(H,t) * f(H)/f_moy * [ 1 - pc*δ(H)/(l-1) - o(H)*pm ]
```

où δ(H) est la longueur utile, o(H) l'ordre du schéma et l la longueur des chaînes.

---

## Exercice 1

Somme des adaptations = 20 + 10 + 5 + 15 = 50, donc f_moy = 12,5.
Ici l = 5, pc = 0,1 et pm = 0,01.

### a) H1 = 1****
- Instances : 10001 (20) et 11100 (10), donc m = 2 et f(H1) = 15.
- δ = 0 et o = 1.
- m(H1,1) >= 2 × (15/12,5) × [1 − 0 − 0,01] = 2 × 1,2 × 0,99 ≈ **2,376**

### b) H2 = 0**10
- Instance : 01110 (15) uniquement, donc m = 1 et f(H2) = 15.
- δ = 5 − 1 = 4 et o = 3.
- Probabilité de survie : 1 − 0,1 × 4/4 − 3 × 0,01 = 0,87.
- m(H2,1) >= 1 × 1,2 × 0,87 ≈ **1,044**

---

## Exercice 2

Somme des adaptations = 80, donc f_moy = 20.
Ici l = 6, pc = 0,6 et pm = 0,01.

### 1) Instances
- H1 = 1*0**1 : **110001** et **110111**
- H2 = 0**0** : **011001** et **000010**

### 2) Longueur utile
- δ(H1) = 6 − 1 = **5**
- δ(H2) = 4 − 1 = **3**

### 3) Bornes du nombre de schémas
Une chaîne de longueur 6 est instance de 2^6 = 64 schémas. La population contient 4 chaînes.
- Borne inférieure : 2^6 = **64** (toutes les chaînes identiques)
- Borne supérieure : 4 × 2^6 = **256** (aucun schéma en commun)

### 4) H1
- m = 2, f(H1) = (20 + 30)/2 = 25 et o = 3.
- Probabilité de survie : 1 − 0,6 × 5/5 − 3 × 0,01 = 0,37.
- m(H1,1) >= 2 × (25/20) × 0,37 ≈ **0,925**

### 5) H2
- m = 2, f(H2) = (16 + 14)/2 = 15 et o = 2.
- Probabilité de survie : 1 − 0,6 × 3/5 − 2 × 0,01 = 0,62.
- m(H2,1) >= 2 × (15/20) × 0,62 ≈ **0,93**

### 6) Disparition de H2 (pc et pm négligeables)
On a m(H2,t+1) = m(H2,t) × f(H2)/f_moy, avec f(H2)/f_moy = 0,75 < 1.
Donc m(H2,t) = 2 × 0,75^t, soit 1,5 ; 1,125 ; 0,84 ; …
- À partir de **t = 3**, le nombre attendu est inférieur à 1 : H2 disparaît en pratique.
- Il tombe sous 0,5 (arrondi à 0) vers t = 5.
- f_moy augmente au fil des générations, donc la disparition est en réalité encore plus rapide.

---

## Exercice 3 : PSO

f(x) = −x² + 4x, avec x ∈ [−5, 5].
f(2) = 4, f(4) = 0 et f(−1) = −5.

### 1a) pbest
Au départ pbest_i = x_i, donc pbest1 = 2, pbest2 = 4 et pbest3 = −1.

### 1b) gbest
La meilleure adaptation est f(2) = 4, donc **gbest = 2**.

### 1c) Première itération
Formules :
```
v_i(1) = c1*v_i + c2*r1*(pbest_i - x_i) + c3*r2*(gbest - x_i)
x_i(1) = x_i + v_i(1)
```
Comme v = 0, le premier terme est nul. On prend r1 = r2 = 0,5.

| Particule | v(1) | x(1) |
|---|---|---|
| 1 | 0 (car x1 = gbest et pbest1 = x1) | 2 |
| 2 | 2 × 0,5 × (2 − 4) = −2 | 2 |
| 3 | 2 × 0,5 × (2 + 1) = 3 | 2 |

- Toutes les particules sont en x = 2, avec f = 4.
- pbest1 = pbest2 = pbest3 = 2 et **gbest(1) = 2**.
- Le maximum de f est bien en x = 2, avec f(2) = 4.

### 2a) Initialisation
```
Algorithme Init(n)
  gbest <- None ; f_gbest <- -inf
  Pour i = 1 à n
      xi <- aléatoire dans [-5, 5]
      vi <- aléatoire dans [-vmax, vmax]
      pbest_i <- xi ; f_pbest_i <- f(xi)
      Si f_pbest_i > f_gbest alors gbest <- pbest_i ; f_gbest <- f_pbest_i
  Fin Pour
```

### 2b) Complexité
La boucle fait n tours, avec un tirage et une évaluation de f en O(1) à chaque tour. La complexité est **O(n)**.

### 2c) PSO complet
```
Init(n)                                  // O(n)
Pour t = 1 à Tmax
    Pour i = 1 à n
        r1, r2 <- aléatoires dans [0,1]
        vi <- c1*vi + c2*r1*(pbest_i - xi) + c3*r2*(gbest - xi)
        xi <- xi + vi
        xi <- borner(xi, -5, 5)
        Si f(xi) > f(pbest_i) alors pbest_i <- xi
        Si f(pbest_i) > f(gbest) alors gbest <- pbest_i
    Fin Pour
Fin Pour
Retourner gbest, f(gbest)
```
Complexité totale : O(Tmax × n).

---

## Exercice 4 : Sac à dos par colonie de fourmis

### 1) Représentation binaire
Une solution est un vecteur x = (x1, …, xn) avec xi ∈ {0,1}, où xi = 1 si l'objet Oi est dans le sac.
Nombre de solutions candidates : **2^n** (dont une partie seulement est réalisable).

### 2) Formulation mathématique
```
max  Σ Vi * xi
s.c. Σ pi * xi <= C
     xi ∈ {0,1},  i = 1..n
```

### 3) Les fourmis
- On utilise m fourmis (par exemple m = n, une par objet de départ, ou un paramètre choisi).
- Chaque fourmi construit une solution :
  1. Elle part d'un objet.
  2. Elle choisit l'objet suivant parmi ceux qui ne sont pas déjà pris et qui respectent la capacité, avec la probabilité
     `P(i→j) = [τij]^α [ηj]^β / Σk [τik]^α [ηk]^β`.
  3. Elle s'arrête quand plus aucun objet ne rentre.
  4. Elle calcule la valeur totale obtenue.
- Ensuite, la phéromone est mise à jour : évaporation, puis dépôt proportionnel à la valeur de la solution.

### 4) Distance entre objets
Heuristique : `ηj = Vj / pj` (rapport valeur/poids).
Distance : **dij = pj / Vj = 1 / ηj**, donc un objet au bon rapport est « proche ».
Autre option : `dij = |Vi/pi − Vj/pj|`.

### 5) Algorithme
```
Initialiser τij <- τ0 pour tout i,j ; calculer ηj = Vj/pj
Répéter Tmax fois
    Pour chaque fourmi k = 1..m
        Sk <- ∅ ; charge <- 0 ; i <- objet de départ
        Tant qu'il existe j ∉ Sk avec charge + pj <= C
            choisir j avec P(i→j) ∝ τij^α * ηj^β
            Sk <- Sk ∪ {j} ; charge <- charge + pj ; i <- j
        Fin Tant que
        valeur(Sk) <- Σ Vi (i ∈ Sk)
    Fin Pour
    Mémoriser la meilleure solution
    τij <- (1 - ρ) * τij                                  // évaporation
    Pour chaque fourmi k : τij <- τij + Q * valeur(Sk)/valeur_max   // dépôt
Fin Répéter
Retourner la meilleure solution
```

### Programme Python
Voir `sac_a_dos_aco.py`. Pour l'exécuter :

```bash
python3 sac_a_dos_aco.py
```

Sur l'exemple de 8 objets (capacité 60), l'ACO trouve la valeur 280, qui est l'optimum exact (vérifié par programmation dynamique).
