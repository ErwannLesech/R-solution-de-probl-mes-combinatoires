#!/usr/bin/env python3
"""
Solveur de Sudoku
Permet de charger et résoudre des grilles de Sudoku avec différents algorithmes.
"""

import sys
import time
from utils import SudokuGrid, load_grid_from_file, save_grid_to_file, get_solution_filename, find_file_in_raw
from solvers.sudoku_solver_backtracking import SudokuSolver as BacktrackingSolver
from solvers.sudoku_solver_bruteforce import SudokuSolver as BruteforceSolver
from solvers.sudoku_solver_backtracking_human_reflexion import SudokuSolver as HumanReflexionSolver


def get_solver_choice():
    """Demande à l'utilisateur de choisir un algorithme de résolution"""
    print("\nChoisissez un algorithme de résolution:")
    print("1. Backtracking (recommandé)")
    print("2. Brute Force")
    print("3. Human Reflexion Backtracking")
    
    while True:
        choice = input("\nVotre choix (1-2): ").strip()
        if choice == "1":
            return BacktrackingSolver, "backtracking"
        elif choice == "2":
            return BruteforceSolver, "brute force"
        elif choice == "3":
            return HumanReflexionSolver, "human reflexion backtracking"
        else:
            print("Choix invalide. Veuillez choisir 1, 2 ou 3.")


def solve_grid(grid, solver_class, algorithm_name):
    """
    Résout une grille avec l'algorithme choisi
    
    Args:
        grid: La grille à résoudre
        solver_class: La classe du solver à utiliser
        algorithm_name: Le nom de l'algorithme (pour l'affichage)
        
    Returns:
        True si la grille est résolue, False sinon
    """
    solver_grid = grid.copy()
    
    print(f"\nRésolution en cours (algorithme de {algorithm_name})...")
    solver = solver_class(solver_grid.grid)
    
    if solver.solve():
        print("Grille résolue avec succès!")
        solver_grid.display()
        return solver_grid
    else:
        print("Impossible de résoudre cette grille!")
        return None


def main():
    """Fonction principale avec menu interactif pour la résolution"""
    print("=== Solveur de Sudoku ===")
    
    while True:
        print("\nOptions disponibles:")
        print("1. Résoudre une grille depuis un fichier")
        print("2. Quitter")
        
        choice = input("\nVotre choix (1-2): ").strip()
        
        if choice == "1":
            # Résolution d'une grille depuis un fichier
            filename = input("Entrez le nom du fichier à résoudre: ").strip()
            
            # Chercher le fichier dans data/raw/ si nécessaire
            filename = find_file_in_raw(filename)
            
            try:
                print("Chargement de la grille...")
                grid = load_grid_from_file(filename)
                
                print("Grille originale:")
                grid.display()
                
                # Choisir l'algorithme de résolution
                solver_class, algorithm_name = get_solver_choice()
                
                # Résoudre la grille
                solved_grid = solve_grid(grid, solver_class, algorithm_name)
                
                if solved_grid:
                    # Proposer de sauvegarder la solution
                    save_solution = input("\nVoulez-vous sauvegarder la solution? (o/n): ").strip().lower()
                    if save_solution in ['o', 'oui', 'y', 'yes']:
                        solution_filename = get_solution_filename(filename)
                        save_grid_to_file(solved_grid, solution_filename)
                    
            except FileNotFoundError:
                print(f"Erreur: Le fichier '{filename}' n'existe pas")
            except ValueError as e:
                print(f"Erreur de format: {e}")
            except Exception as e:
                print(f"Erreur inattendue: {e}")
        
        elif choice == "2":
            print("Au revoir!")
            break
        
        else:
            print("Choix invalide. Veuillez choisir 1 ou 2.")


if __name__ == "__main__":
    # Vérifier si un fichier est passé en argument
    if len(sys.argv) > 1:
        # Mode ligne de commande
        filename = sys.argv[1]
        
        # Optionnel: spécifier l'algorithme en deuxième argument (1 = backtracking, 2 = bruteforce)
        solver_class = BacktrackingSolver
        algorithm_name = "backtracking"
        
        if len(sys.argv) > 2:
            if sys.argv[2] == "1":
                solver_class = BruteforceSolver
                algorithm_name = "brute force"
            elif sys.argv[2] == "2":
                solver_class = BacktrackingSolver
                algorithm_name = "backtracking"
            elif sys.argv[2] == "3":
                solver_class = HumanReflexionSolver
                algorithm_name = "human reflexion backtracking"
        
        # Chercher le fichier dans data/raw/ si nécessaire
        filename = find_file_in_raw(filename)
        
        print(f"=== Solveur de Sudoku - Mode ligne de commande ===")
        
        try:
            print(f"Chargement de la grille depuis {filename}...")
            grid = load_grid_from_file(filename)
            
            print("Grille originale:")
            grid.display()
            
            begin_time = time.time()
            
            # Résoudre la grille
            solved_grid = solve_grid(grid, solver_class, algorithm_name)
            
            end_time = time.time()
            elapsed_time = end_time - begin_time
            print(f"Temps de résolution : {elapsed_time:.2f} secondes")
            
            if solved_grid:
                # Sauvegarde automatique en mode ligne de commande
                solution_filename = get_solution_filename(filename)
                save_grid_to_file(solved_grid, solution_filename)
                
        except FileNotFoundError:
            print(f"Erreur: Le fichier '{filename}' n'existe pas")
        except ValueError as e:
            print(f"Erreur de format: {e}")
        except Exception as e:
            print(f"Erreur inattendue: {e}")
    else:
        # Mode interactif
        main()