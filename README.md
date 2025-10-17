# Résolution de Problèmes Combinatoires - Sudoku

## 🎯 Le Projet

Ce projet explore différentes approches algorithmiques pour résoudre des problèmes combinatoires, en utilisant le Sudoku comme cas d'application. L'objectif principal est de **comprendre et comparer** comment différentes stratégies influencent les performances de résolution.

Nous implémentons plusieurs versions d'algorithmes, de la plus simple (backtracking naïf) à des approches plus sophistiquées, afin d'observer concrètement l'impact des optimisations sur les temps de calcul et la capacité à traiter des problèmes de grande taille.

## 📁 Architecture du Projet

Le code est organisé de manière modulaire pour faciliter la compréhension et l'évolution :

```
├── sudoku_solver_v1.py        # Algorithme de résolution V1 (backtracking simple)
├── main.py                    # Interface d'utilisation (CLI)
├── utils.py                   # Utilitaires (chargement, sauvegarde, affichage)
├── sudoku_generator.py        # Générateur de grilles de test
├── data/
│   ├── raw/                  # Grilles à résoudre
│   └── resolved/             # Solutions générées
└── README.md
```

### Séparation des responsabilités

- **`sudoku_solver_v1.py`** : Contient **uniquement** l'algorithme de backtracking (~100 lignes). Code volontairement simple et commenté pour une compréhension immédiate de la logique de résolution.

- **`utils.py`** : Fonctions utilitaires réutilisables (chargement/sauvegarde de fichiers, représentation de la grille, affichage).

- **`main.py`** : Point d'entrée du programme, orchestre les modules et gère l'interaction utilisateur.

Cette architecture permet d'ajouter facilement de nouvelles versions d'algorithmes (v2, v3...) sans modifier le reste du code.

## 📊 Version 1 : Backtracking Simple

### Algorithme utilisé

La V1 implémente un **backtracking pur** sans aucune optimisation. C'est l'approche la plus intuitive pour résoudre un Sudoku :

```
1. Trouver la première cellule vide
2. Essayer tous les nombres de 1 à N
3. Pour chaque nombre :
   - Vérifier s'il respecte les contraintes (ligne, colonne, bloc)
   - Si oui : placer le nombre et continuer récursivement
   - Si la récursion réussit : problème résolu
   - Sinon : retirer le nombre (backtrack) et essayer le suivant
4. Si aucun nombre ne fonctionne : retour arrière
```

### Performances observées

| Taille de grille | Temps de résolution | Statut |
|------------------|---------------------|---------|
| **4×4**          | < 1 seconde        | ✅ Excellent |
| **9×9**          | < 5 secondes       | ✅ Acceptable |
| **16×16**        | > 1 minute         | ⚠️ Lent |
| **25×25**        | Plusieurs heures   | ❌ Impraticable |

### Limitations

Le backtracking simple explore **toutes les possibilités** de manière aveugle, ce qui génère un arbre de recherche exponentiel. Sans heuristiques ni propagation de contraintes, l'algorithme teste énormément de combinaisons invalides avant de trouver la solution.

Ces limitations sont **volontaires** : elles démontrent la nécessité d'approches plus intelligentes pour traiter des problèmes de grande taille. Les versions futures introduiront des optimisations progressives.

## � Utilisation

```bash
# Mode interactif
python3 main.py

# Résoudre une grille directement
python3 main.py data/raw/exemple_9x9.txt
```

**Format des fichiers** : un point `.` pour les cases vides, les chiffres pour les valeurs.

Exemple 4×4 :
```
1...
.3.2
2...
...4
```