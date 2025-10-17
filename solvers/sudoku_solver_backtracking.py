#!/usr/bin/env python3
"""
Algorithme de résolution de Sudoku par backtracking
Ce fichier contient uniquement la logique de résolution pour une compréhension facile
"""

from typing import Tuple, Optional


class SudokuSolver:
    """Solveur de Sudoku utilisant l'algorithme de backtracking"""
    
    def __init__(self, grid: list):
        """
        Initialise le solveur avec une grille
        
        Args:
            grid: Grille de Sudoku (liste de listes)
        """
        self.grid = grid
        self.size = len(grid)
        self.box_size = int(self.size**0.5)
    
    def is_valid(self, row: int, col: int, num: int) -> bool:
        """
        Vérifie si un nombre peut être placé à une position donnée
        
        Args:
            row: Ligne
            col: Colonne
            num: Nombre à placer
            
        Returns:
            True si le placement est valide, False sinon
        """
        # Vérifier la ligne
        for c in range(self.size):
            if self.grid[row][c] == num:
                return False
        
        # Vérifier la colonne
        for r in range(self.size):
            if self.grid[r][col] == num:
                return False
        
        # Vérifier le sous-carré
        start_row = (row // self.box_size) * self.box_size
        start_col = (col // self.box_size) * self.box_size
        
        for r in range(start_row, start_row + self.box_size):
            for c in range(start_col, start_col + self.box_size):
                if self.grid[r][c] == num:
                    return False
        
        return True
    
    def find_empty_cell(self) -> Optional[Tuple[int, int]]:
        """
        Trouve la première cellule vide dans la grille
        
        Returns:
            Tuple (row, col) de la première cellule vide, ou None si la grille est complète
        """
        for row in range(self.size):
            for col in range(self.size):
                if self.grid[row][col] == 0:
                    return (row, col)
        return None
    
    def solve(self) -> bool:
        """
        Résout la grille avec l'algorithme de backtracking
        
        Principe:
        1. Trouver une cellule vide
        2. Essayer tous les nombres possibles (1 à size)
        3. Si un nombre est valide, le placer et continuer récursivement
        4. Si aucune solution n'est trouvée, revenir en arrière (backtrack)
        
        Returns:
            True si la grille est résolue, False sinon
        """
        # Trouver la première cellule vide
        empty_cell = self.find_empty_cell()
        
        # Si pas de cellule vide, la grille est complète
        if not empty_cell:
            return True
        
        row, col = empty_cell
        
        # Essayer tous les nombres de 1 à size
        for num in range(1, self.size + 1):
            # Vérifier si le nombre est valide à cette position
            if self.is_valid(row, col, num):
                # Placer le nombre
                self.grid[row][col] = num
                
                # Continuer récursivement
                if self.solve():
                    return True
                
                # Backtrack: annuler le placement
                self.grid[row][col] = 0
        
        # Aucune solution trouvée
        return False
