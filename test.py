from solver import Puzzle as p
from solver import TEST_DATA, TEST_SOLVED_DATA
from algos import CrossHatchSolver as chs

puzzle = p(TEST_DATA)
puzzle.set_solver(chs)
print(f"current_solver: {puzzle.current_solver}")
puzzle.solve()
