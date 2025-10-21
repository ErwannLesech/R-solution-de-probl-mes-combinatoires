#!/usr/bin/env python3
"""
Utilitaires pour parser des grille de sudoku depuis l'extérieur
Permet de sauvegarder et d'enrichir les grilles de sudoku

Format attendu en entrée:

x lignes correspondant à x grilles de sudoku, chaque ligne contenant:
9..8...........5............2..1...3.1.....6....4...7.7.86.........3.1..4.....2..

Chaque caractère représente une cellule:
- '1'-'9' pour les valeurs 1 à 9
- '.' pour une cellule vide
- 'A'-'Z' pour les valeurs 10 à 35 (pour les grilles plus grandes)

Il faut que la taille de la grille soit un carré parfait (4, 9, 16, 25, etc.)
"""
import os
import sys
import math
from typing import List, Tuple, Optional
from utils import SudokuGrid, char_to_value, save_grid_to_file


def parse_line_to_grid(line: str) -> Tuple[SudokuGrid, int]:
    """
    Parse une ligne de texte en grille de sudoku
    
    Args:
        line: Ligne contenant la grille (ex: "9..8...........5............")
        
    Returns:
        Tuple (grille, taille) ou lève une exception si la ligne est invalide
    """
    # Nettoyer la ligne
    line = line.strip().replace(' ', '')
    
    if not line:
        raise ValueError("Ligne vide")
    
    # Déterminer la taille de la grille
    total_cells = len(line)
    size = int(math.sqrt(total_cells))
    
    if size * size != total_cells:
        raise ValueError(f"La ligne contient {total_cells} cellules, ce n'est pas un carré parfait")
    
    # Vérifier que la taille est elle-même un carré parfait
    box_size = int(math.sqrt(size))
    if box_size * box_size != size:
        raise ValueError(f"La taille {size} n'est pas un carré parfait valide pour un sudoku")
    
    # Créer la grille
    grid = SudokuGrid(size)
    
    # Remplir la grille
    for i in range(size):
        for j in range(size):
            idx = i * size + j
            char = line[idx]
            try:
                value = char_to_value(char)
                if value < 0 or value > size:
                    raise ValueError(f"Valeur {value} hors limites pour une grille {size}x{size}")
                grid.grid[i][j] = value
            except ValueError as e:
                raise ValueError(f"Caractère invalide '{char}' à la position {idx+1}: {e}")
    
    return grid, size


def parse_grids_from_file(input_file: str, output_dir: str = "data/raw", base_name: Optional[str] = None) -> List[str]:
    """
    Parse toutes les grilles d'un fichier et les sauvegarde dans le dossier de sortie
    
    Args:
        input_file: Fichier contenant les grilles (une par ligne)
        output_dir: Dossier de destination (par défaut "data/raw")
        base_name: Nom de base pour les fichiers de sortie (optionnel)
        
    Returns:
        Liste des noms de fichiers créés
    """
    if not os.path.exists(input_file):
        raise FileNotFoundError(f"Le fichier {input_file} n'existe pas")
    
    # Créer le dossier de sortie s'il n'existe pas
    os.makedirs(output_dir, exist_ok=True)
    
    # Lire toutes les lignes
    with open(input_file, 'r') as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]
    
    if not lines:
        raise ValueError("Le fichier est vide")
    
    print(f"Parsing de {len(lines)} grille(s) depuis {input_file}...")
    
    # Déterminer le nom de base si non fourni
    if base_name is None:
        base_name = os.path.splitext(os.path.basename(input_file))[0]
    
    saved_files = []
    
    # Parser chaque ligne
    for idx, line in enumerate(lines, 1):
        try:
            grid, size = parse_line_to_grid(line)
            
            # Générer le nom du fichier de sortie
            if len(lines) == 1:
                output_filename = f"{output_dir}/{base_name}.txt"
            else:
                output_filename = f"{output_dir}/{base_name}_{idx}.txt"
            
            # Sauvegarder la grille
            save_grid_to_file(grid, output_filename)
            saved_files.append(output_filename)
            
            print(f"✓ Grille {idx}/{len(lines)} ({size}x{size}) sauvegardée: {output_filename}")
            
        except Exception as e:
            print(f"✗ Erreur lors du parsing de la grille {idx}: {e}")
            continue
    
    print(f"\nTerminé ! {len(saved_files)}/{len(lines)} grille(s) sauvegardée(s) avec succès.")
    return saved_files


def main():
    """Point d'entrée principal du script"""
    if len(sys.argv) < 2:
        print("Usage: python parse_grid.py <fichier_entree> [dossier_sortie] [nom_de_base]")
        print()
        print("Arguments:")
        print("  fichier_entree  : Fichier contenant les grilles à parser (une par ligne)")
        print("  dossier_sortie  : Dossier de destination (défaut: data/raw)")
        print("  nom_de_base     : Nom de base pour les fichiers (défaut: nom du fichier d'entrée)")
        print()
        print("Exemple:")
        print("  python parse_grid.py grilles.txt")
        print("  python parse_grid.py grilles.txt data/raw sudoku_9x9")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "data/raw"
    base_name = sys.argv[3] if len(sys.argv) > 3 else None
    
    try:
        saved_files = parse_grids_from_file(input_file, output_dir, base_name)
        
        if saved_files:
            print("\nFichiers créés:")
            for file in saved_files:
                print(f"  - {file}")
    
    except Exception as e:
        print(f"Erreur: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

