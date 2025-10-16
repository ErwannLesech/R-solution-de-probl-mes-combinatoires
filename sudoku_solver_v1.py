#!/usr/bin/env python3
"""
Générateur et solveur de Sudoku
Permet de générer des grilles de Sudoku solvables et de les résoudre avec un algorithme de force brute.
"""

import random
import os
import sys
from typing import List, Tuple, Optional


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
            Tuple (row, col) de la première cellule vide, ou None si aucune
        """
        for row in range(self.size):
            for col in range(self.size):
                if self.grid[row][col] == 0:
                    return (row, col)
        return None
    
    def solve_bruteforce(self) -> bool:
        """
        Résout la grille avec un algorithme de force brute (backtracking)
        
        Returns:
            True si la grille est résolue, False sinon
        """
        empty_cell = self.find_empty_cell()
        if not empty_cell:
            return True  # Grille complète
        
        row, col = empty_cell
        
        for num in range(1, self.size + 1):
            if self.is_valid(row, col, num):
                self.grid[row][col] = num
                
                if self.solve_bruteforce():
                    return True
                
                # Backtrack
                self.grid[row][col] = 0
        
        return False
    
    def copy(self):
        """Crée une copie de la grille"""
        new_grid = SudokuGrid(self.size)
        new_grid.grid = [row[:] for row in self.grid]
        return new_grid
    
    def display(self):
        """Affiche la grille de manière lisible"""
        print(f"\nGrille Sudoku {self.size}x{self.size}:")
        print("-" * (self.size * 2 + self.box_size + 1))
        
        for i in range(self.size):
            if i > 0 and i % self.box_size == 0:
                print("-" * (self.size * 2 + self.box_size + 1))
            
            row_str = "|"
            for j in range(self.size):
                if j > 0 and j % self.box_size == 0:
                    row_str += "|"
                
                if self.grid[i][j] == 0:
                    row_str += " ."
                else:
                    row_str += f" {self.grid[i][j]}"
            
            row_str += "|"
            print(row_str)
        
        print("-" * (self.size * 2 + self.box_size + 1))


class SudokuGenerator:
    """Générateur de grilles de Sudoku"""
    
    def __init__(self, size: int = 9):
        self.size = size
    
    def generate_complete_grid(self) -> SudokuGrid:
        """
        Génère une grille de Sudoku complète et valide
        
        Returns:
            Grille de Sudoku complètement remplie
        """
        grid = SudokuGrid(self.size)
        self._fill_grid(grid)
        return grid
    
    def _fill_grid(self, grid: SudokuGrid) -> bool:
        """
        Remplit récursivement la grille avec des nombres valides
        """
        empty_cell = grid.find_empty_cell()
        if not empty_cell:
            return True
        
        row, col = empty_cell
        numbers = list(range(1, self.size + 1))
        random.shuffle(numbers)
        
        for num in numbers:
            if grid.is_valid(row, col, num):
                grid.grid[row][col] = num
                
                if self._fill_grid(grid):
                    return True
                
                grid.grid[row][col] = 0
        
        return False
    
    def create_puzzle(self, difficulty: str = "medium") -> SudokuGrid:
        """
        Crée un puzzle en supprimant des cellules d'une grille complète
        
        Args:
            difficulty: Niveau de difficulté ("easy", "medium", "hard")
            
        Returns:
            Grille de Sudoku avec des cellules vides
        """
        complete_grid = self.generate_complete_grid()
        
        # Définir le nombre de cellules à supprimer selon la difficulté
        if difficulty == "easy":
            cells_to_remove = self.size * 4
        elif difficulty == "medium":
            cells_to_remove = self.size * 5
        else:  # hard
            cells_to_remove = self.size * 6
        
        # S'assurer de ne pas supprimer trop de cellules
        cells_to_remove = min(cells_to_remove, self.size * self.size - self.size)
        
        # Supprimer aléatoirement des cellules
        positions = [(i, j) for i in range(self.size) for j in range(self.size)]
        random.shuffle(positions)
        
        for i in range(cells_to_remove):
            row, col = positions[i]
            complete_grid.grid[row][col] = 0
        
        return complete_grid


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
            if char == '.':
                grid.grid[i][j] = 0
            else:
                try:
                    num = int(char)
                    if 1 <= num <= size:
                        grid.grid[i][j] = num
                    else:
                        raise ValueError(f"Nombre invalide {num} à la position ({i+1}, {j+1})")
                except ValueError:
                    raise ValueError(f"Caractère invalide '{char}' à la position ({i+1}, {j+1})")
    
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
                if cell == 0:
                    line += "."
                else:
                    line += str(cell)
            file.write(line + "\n")
    
    print(f"Grille sauvegardée dans {filename}")


def main():
    """Fonction principale avec menu interactif"""
    print("=== Générateur et Solveur de Sudoku ===")
    
    while True:
        print("\nOptions disponibles:")
        print("1. Générer une nouvelle grille de Sudoku")
        print("2. Résoudre une grille depuis un fichier")
        print("3. Quitter")
        
        choice = input("\nVotre choix (1-3): ").strip()
        
        if choice == "1":
            # Génération d'une nouvelle grille
            try:
                size = int(input("Entrez la dimension de la grille (4, 9, 16, 25, etc.): "))
                if int(size**0.5)**2 != size:
                    print("Erreur: La dimension doit être un carré parfait (4, 9, 16, 25, etc.)")
                    continue
                
                print("Génération de la grille...")
                generator = SudokuGenerator(size)
                
                difficulty = input("Difficulté (easy/medium/hard) [medium]: ").strip().lower()
                if difficulty not in ["easy", "medium", "hard"]:
                    difficulty = "medium"
                
                puzzle = generator.create_puzzle(difficulty)
                puzzle.display()
                
                # Sauvegarder la grille
                filename = f"data/sudoku_{size}x{size}_{difficulty}.txt"
                save_grid_to_file(puzzle, filename)
                
            except ValueError as e:
                print(f"Erreur: {e}")
            except Exception as e:
                print(f"Erreur inattendue: {e}")
        
        elif choice == "2":
            # Résolution d'une grille depuis un fichier
            filename = input("Entrez le nom du fichier à résoudre: ").strip()
            
            try:
                print("Chargement de la grille...")
                grid = load_grid_from_file(filename)
                
                print("Grille originale:")
                grid.display()
                
                # Créer une copie pour la résolution
                solver_grid = grid.copy()
                
                print("\nRésolution en cours (algorithme de force brute)...")
                if solver_grid.solve_bruteforce():
                    print("Grille résolue avec succès!")
                    solver_grid.display()
                    
                    # Proposer de sauvegarder la solution
                    save_solution = input("\nVoulez-vous sauvegarder la solution? (o/n): ").strip().lower()
                    if save_solution in ['o', 'oui', 'y', 'yes']:
                        solution_filename = filename.replace('.txt', '_solution.txt')
                        save_grid_to_file(solver_grid, solution_filename)
                else:
                    print("Impossible de résoudre cette grille!")
                    
            except FileNotFoundError:
                print(f"Erreur: Le fichier '{filename}' n'existe pas")
            except ValueError as e:
                print(f"Erreur de format: {e}")
            except Exception as e:
                print(f"Erreur inattendue: {e}")
        
        elif choice == "3":
            print("Au revoir!")
            break
        
        else:
            print("Choix invalide. Veuillez choisir 1, 2 ou 3.")


if __name__ == "__main__":
    main()