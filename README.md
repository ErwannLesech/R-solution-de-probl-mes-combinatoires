# Générateur et Solveur de Sudoku

Ce projet permet de générer et résoudre des grilles de Sudoku de différentes tailles.

## Fonctionnalités

1. **Génération de grilles** : Création de grilles Sudoku solvables de différentes tailles (4x4, 9x9, 16x16, etc.)
2. **Résolution par force brute** : Algorithme de backtracking pour résoudre les grilles
3. **Import/Export de fichiers** : Lecture et écriture de grilles au format texte

## Format des fichiers

Les grilles sont stockées dans des fichiers texte avec le format suivant :
- Un point (`.`) représente une case vide
- Les chiffres représentent les valeurs remplies
- Chaque ligne du fichier représente une ligne de la grille

Exemple pour une grille 4x4 :
```
1...
.3.2
2...
...4
```

Exemple pour une grille 9x9 :
```
53..7....
6..195...
.98....6.
8...6...3
4..8.3..1
7...2...6
.6....28.
...419..5
....8..79
```

## Utilisation

### Script principal
```bash
python3 sudoku_solver_v1.py
```

Le script propose un menu interactif avec les options suivantes :
1. Générer une nouvelle grille de Sudoku
2. Résoudre une grille depuis un fichier
3. Quitter

### Génération de grilles de test
```bash
python3 generate_test_grids.py
```

Ce script génère automatiquement des grilles de test de différentes tailles et difficultés.

## Limitations

⚠️ **Attention** : L'algorithme de force brute devient très lent pour les grandes grilles (16x16 et plus). Il est conçu pour être basique et sera impraticable pour les grosses dimensions, comme demandé.

## Structure du projet

```
├── sudoku_solver_v1.py        # Script principal
├── generate_test_grids.py     # Générateur de grilles de test
├── data/                      # Dossier contenant les grilles
│   ├── exemple_4x4.txt       # Exemple de grille 4x4
│   ├── exemple_9x9.txt       # Exemple de grille 9x9
│   └── (grilles générées)
└── README.md                  # Ce fichier
```

## Exemples d'utilisation

1. **Générer une grille 9x9 de difficulté moyenne** :
   - Lancer le script principal
   - Choisir option 1
   - Entrer 9 comme dimension
   - Choisir "medium" comme difficulté

2. **Résoudre la grille d'exemple** :
   - Lancer le script principal
   - Choisir option 2
   - Entrer "data/exemple_9x9.txt" comme fichier

## Classes principales

- `SudokuGrid` : Représente une grille de Sudoku avec méthodes de validation et résolution
- `SudokuGenerator` : Génère des grilles complètes et crée des puzzles
- Fonctions utilitaires pour charger/sauvegarder les fichiers