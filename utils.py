#!/usr/bin/env python3
"""
Utilitaires pour les grilles de Sudoku
Classes et fonctions communes de sauvegarde, chargement et manipulation
"""

import os


def char_to_value(char: str) -> int:
    """
    Convertit un caractère en valeur numérique
    '.' -> 0, '1'-'9' -> 1-9, 'A'-'Z' -> 10-35
    
    Args:
        char: Caractère à convertir
        
    Returns:
        Valeur numérique correspondante
    """
    if char == '.':
        return 0
    elif char.isdigit():
        return int(char)
    elif char.upper() in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
        return ord(char.upper()) - ord('A') + 10
    else:
        raise ValueError(f"Caractère invalide: '{char}'")


def value_to_char(value: int) -> str:
    """
    Convertit une valeur numérique en caractère
    0 -> '.', 1-9 -> '1'-'9', 10-35 -> 'A'-'Z'
    
    Args:
        value: Valeur numérique à convertir
        
    Returns:
        Caractère correspondant
    """
    if value == 0:
        return '.'
    elif 1 <= value <= 9:
        return str(value)
    elif 10 <= value <= 35:
        return chr(ord('A') + value - 10)
    else:
        raise ValueError(f"Valeur invalide: {value}")


class SudokuGrid:
    """Classe pour représenter et manipuler une grille de Sudoku"""
    
    def __init__(self, size: int = 9):
        """
        Initialise une grille de Sudoku
        
        Args:
            size: Taille de la grille (doit être un carré parfait : 4, 9, 16, 25, etc.)
        """
        if int(size**0.5)**2 != size:
            raise ValueError(f"La taille {size} n'est pas un carré parfait")
        
        self.size = size
        self.box_size = int(size**0.5)  # Taille des sous-carrés
        self.grid = [[0 for _ in range(size)] for _ in range(size)]
    
    def copy(self):
        """Crée une copie de la grille"""
        new_grid = SudokuGrid(self.size)
        new_grid.grid = [row[:] for row in self.grid]
        return new_grid
    
    def find_empty_cell(self):
        """
        Trouve la première cellule vide dans la grille
        
        Returns:
            Tuple (row, col) de la cellule vide ou None si la grille est complète
        """
        for i in range(self.size):
            for j in range(self.size):
                if self.grid[i][j] == 0:
                    return (i, j)
        return None
    
    def is_valid(self, row: int, col: int, num: int) -> bool:
        """
        Vérifie si un nombre peut être placé à une position donnée
        
        Args:
            row: Ligne de la cellule
            col: Colonne de la cellule
            num: Nombre à vérifier
            
        Returns:
            True si le placement est valide, False sinon
        """
        # Vérifier la ligne
        if num in self.grid[row]:
            return False
        
        # Vérifier la colonne
        for i in range(self.size):
            if self.grid[i][col] == num:
                return False
        
        # Vérifier le sous-carré
        box_row = (row // self.box_size) * self.box_size
        box_col = (col // self.box_size) * self.box_size
        
        for i in range(box_row, box_row + self.box_size):
            for j in range(box_col, box_col + self.box_size):
                if self.grid[i][j] == num:
                    return False
        
        return True
    
    def display(self):
        """Affiche la grille de manière lisible"""
        print(f"\nGrille Sudoku {self.size}x{self.size}:")
        
        # Calculer la largeur d'une cellule (2 pour <=9, 3 pour >=10)
        cell_width = 3 if self.size > 9 else 2
        separator_width = self.size * cell_width + self.box_size + 1
        
        print("-" * separator_width)
        
        for i in range(self.size):
            if i > 0 and i % self.box_size == 0:
                print("-" * separator_width)
            
            row_str = "|"
            for j in range(self.size):
                if j > 0 and j % self.box_size == 0:
                    row_str += "|"
                
                cell_char = value_to_char(self.grid[i][j])
                if self.size > 9:
                    row_str += f" {cell_char:>2}"
                else:
                    row_str += f" {cell_char}"
            
            row_str += "|"
            print(row_str)
        
        print("-" * separator_width)


def load_grid_from_file(filename: str) -> SudokuGrid:
    """
    Charge une grille de Sudoku depuis un fichier
    
    Args:
        filename: Nom du fichier à charger
        
    Returns:
        Grille de Sudoku chargée
    """
    if not os.path.exists(filename):
        raise FileNotFoundError(f"Le fichier {filename} n'existe pas")
    
    with open(filename, 'r') as file:
        lines = [line.strip() for line in file.readlines() if line.strip()]
    
    if not lines:
        raise ValueError("Le fichier est vide")
    
    # Déterminer la taille de la grille
    size = len(lines)
    
    # Vérifier que c'est un carré parfait
    if int(size**0.5)**2 != size:
        raise ValueError(f"La taille {size} n'est pas un carré parfait")
    
    grid = SudokuGrid(size)
    
    for i, line in enumerate(lines):
        # Supprimer les espaces et traiter chaque caractère
        chars = line.replace(' ', '')
        
        if len(chars) != size:
            raise ValueError(f"Ligne {i+1} a une longueur incorrecte: {len(chars)} au lieu de {size}")
        
        for j, char in enumerate(chars):
            try:
                num = char_to_value(char)
                if num < 0 or num > size:
                    raise ValueError(f"Nombre invalide {num} à la position ({i+1}, {j+1})")
                grid.grid[i][j] = num
            except ValueError as e:
                raise ValueError(f"Caractère invalide '{char}' à la position ({i+1}, {j+1}): {e}")
    
    return grid


def save_grid_to_file(grid: SudokuGrid, filename: str):
    """
    Sauvegarde une grille de Sudoku dans un fichier
    
    Args:
        grid: Grille à sauvegarder
        filename: Nom du fichier de destination
    """
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    
    with open(filename, 'w') as file:
        for row in grid.grid:
            line = ""
            for cell in row:
                line += value_to_char(cell)
            file.write(line + "\n")
    
    print(f"Grille sauvegardée dans {filename}")


def get_solution_filename(original_filename: str) -> str:
    """
    Génère le nom du fichier de solution à partir du fichier original
    
    Args:
        original_filename: Nom du fichier original
        
    Returns:
        Nom du fichier de solution dans data/resolved/
    """
    base_name = os.path.basename(original_filename)
    name_without_ext = os.path.splitext(base_name)[0]
    return f"data/resolved/{name_without_ext}_solution.txt"


def find_file_in_raw(filename: str) -> str:
    """
    Cherche un fichier dans data/raw/ si il n'existe pas au chemin donné
    
    Args:
        filename: Nom du fichier à chercher
        
    Returns:
        Chemin du fichier trouvé
    """
    # Si le fichier existe déjà au chemin donné
    if os.path.exists(filename):
        return filename
    
    # Si ce n'est pas un chemin absolu et ne commence pas par data/
    if not os.path.isabs(filename) and not filename.startswith('data/'):
        test_filename = f"data/raw/{filename}"
        if os.path.exists(test_filename):
            return test_filename
    
    # Retourner le nom original si rien n'est trouvé
    return filename