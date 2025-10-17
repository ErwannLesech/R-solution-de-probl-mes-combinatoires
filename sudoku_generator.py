#!/usr/bin/env python3
"""
Générateur de grilles de Sudoku
Script dédié uniquement à la création et génération de puzzles de Sudoku
"""

import random
from utils import SudokuGrid, save_grid_to_file, value_to_char


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
            cells_to_remove = self.size * 7
        elif difficulty == "medium":
            cells_to_remove = self.size * 8
        else:  # hard
            cells_to_remove = self.size * 9
        
        # S'assurer de ne pas supprimer trop de cellules
        cells_to_remove = min(cells_to_remove, self.size * self.size - self.size)
        
        # Supprimer aléatoirement des cellules
        positions = [(i, j) for i in range(self.size) for j in range(self.size)]
        random.shuffle(positions)
        
        for i in range(cells_to_remove):
            row, col = positions[i]
            complete_grid.grid[row][col] = 0
        
        return complete_grid


def generate_single_puzzle():
    """Interface interactive pour générer une seule grille"""
    print("=== Générateur de Puzzles Sudoku ===")
    
    try:
        size = int(input("Entrez la dimension de la grille (4, 9, 16, 25, etc.): "))
        if int(size**0.5)**2 != size:
            print("Erreur: La dimension doit être un carré parfait (4, 9, 16, 25, etc.)")
            return
        
        print("Génération de la grille...")
        generator = SudokuGenerator(size)
        
        difficulty = input("Difficulté (easy/medium/hard) [medium]: ").strip().lower()
        if difficulty not in ["easy", "medium", "hard"]:
            difficulty = "medium"
        
        puzzle = generator.create_puzzle(difficulty)
        
        # Affichage de la grille avec lettres pour les valeurs > 9
        print(f"\nGrille Sudoku {size}x{size} générée:")
        puzzle.display()
        
        # Sauvegarder la grille
        filename = f"data/raw/sudoku_{size}x{size}_{difficulty}.txt"
        save_grid_to_file(puzzle, filename)
        
    except ValueError as e:
        print(f"Erreur: {e}")
    except Exception as e:
        print(f"Erreur inattendue: {e}")


def generate_test_grids():
    """Génère des grilles de test de différentes tailles"""
    
    sizes = [4, 9, 16]  # 25 sera très lent
    difficulties = ["easy", "medium", "hard"]
    
    for size in sizes:
        print(f"\nGénération de grilles {size}x{size}...")
        generator = SudokuGenerator(size)
        
        for difficulty in difficulties:
            print(f"  - Difficulté: {difficulty}")
            try:
                puzzle = generator.create_puzzle(difficulty)
                filename = f"data/raw/test_sudoku_{size}x{size}_{difficulty}.txt"
                save_grid_to_file(puzzle, filename)
            except Exception as e:
                print(f"    Erreur: {e}")


def main():
    """Menu principal du générateur"""
    while True:
        print("\n=== Générateur de Grilles Sudoku ===")
        print("1. Générer une grille personnalisée")
        print("2. Générer un lot de grilles de test")
        print("3. Quitter")
        
        choice = input("\nVotre choix (1-3): ").strip()
        
        if choice == "1":
            generate_single_puzzle()
        elif choice == "2":
            generate_test_grids()
            print("\nGrilles de test générées dans le dossier 'data/raw/'")
        elif choice == "3":
            print("Au revoir!")
            break
        else:
            print("Choix invalide. Veuillez choisir 1, 2 ou 3.")


if __name__ == "__main__":
    main()