#!/usr/bin/env python3
"""
Script pour générer des grilles de test de différentes tailles
"""

from sudoku_solver_v1 import SudokuGenerator, save_grid_to_file

def generate_test_grids():
    """Génère des grilles de test de différentes tailles"""
    
    sizes = [4, 9, 16]  # 25 sera très lent avec la force brute
    difficulties = ["easy", "medium", "hard"]
    
    for size in sizes:
        print(f"\nGénération de grilles {size}x{size}...")
        generator = SudokuGenerator(size)
        
        for difficulty in difficulties:
            print(f"  - Difficulté: {difficulty}")
            try:
                puzzle = generator.create_puzzle(difficulty)
                filename = f"data/test_sudoku_{size}x{size}_{difficulty}.txt"
                save_grid_to_file(puzzle, filename)
            except Exception as e:
                print(f"    Erreur: {e}")

if __name__ == "__main__":
    generate_test_grids()
    print("\nGrilles de test générées dans le dossier 'data/'")