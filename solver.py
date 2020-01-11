import itertools, random
from timeit import default_timer as timer

TEST_DATA = [
    "3?5?7????",
    "4?1?2?6?8",
    "???1??3??",
    "?5???9?16",
    "1??8?6??4",
    "64?2???8?",
    "??4??1???",
    "8?7?6?4?1",
    "????3?7?9"
    ]

###################################################################################################
# Puzzle object and helpers
###################################################################################################

class Puzzle:
    # clues - A list of 9 alpha-numeric character strings. Numbers
    #         indicate what clues are provided for the puzzle.
    #         "?" indicate the blank spaces needed to be filled.
    def __init__(self, clues, has_gui=False):
        self.clue_count = 0
        self.load_data(clues)
        self.clues = clues
        self.current_solver = CrossHatchSolver(self.clues)
        if has_gui:
            from kui import SolverApp
            self.gui = SolverApp()
            self.gui.puzzle = self
            self.gui.run()
        
        
    def clockit(self, function):
        start = timer()
        f_ret = function
        end = timer()
        return (end - start, f_ret)
        
    def load_data(self, data):
        self.grid = {}
        for i, row in enumerate(data):
            self.grid[i] = {}
            for j, character in enumerate(row):
                self.grid[i][j] = character

    def dump_data(self):
        data_list = []
        if not self.grid:
            assert("There is no data loaded to dump")
        for i, row in enumerate(self.grid):
            staging_string = ""
            for j, character in enumerate(self.grid):
                staging_string += self.grid[i][j]
            data_list.append(staging_string)
        return data_list

    def check_data(self, data):
        group3 = lambda x: zip(*(iter(x),) * 3)
        check = lambda x: True if sorted(list(x)) == [str(n+1) for n in range(9)] else False
        nonets = []
        cols = ["" for x in range(9)] # LOL
        for trio in group3(data):
            blocks = ["","",""]  
            for row in trio:
                for i, r in enumerate(group3(row)):
                    blocks[i] += "".join(r)
                for i, c in enumerate(row):
                    cols[i] += c
                nonets.append(row)
            nonets += blocks
        nonets += cols
        for nonet in nonets:
            if not check(nonet):
                return False
        return True
    
    def print_grid(self):
        visual = []    
        x_border = " --- " * 4
        visual.append(x_border)
        for line in self.grid:
            visual.append("| " + " ".join([self.grid[line][c] for c in self.grid[line]]) + " |")
        visual.append(x_border)
        for line in visual:
            print(line)                
    
    def set_solver(self, solver):
        self.current_solver = solver(self.clues)
        
    def solve(self):
        if not self.current_solver:
            assert("solver not set")
        results = self.timeit(self.solver.solve())
        prints(results)

###################################################################################################
# SOLVERS
###################################################################################################

class CrossHatchSolver:
    def __init__(self, clues):
        self.clues = clues
        self.load_data()
        self.dump_data()

    def solve(self):
        
        # Logic
        
        pass

    def load_data(self):
        self.grid = {}
        for i, row in enumerate(self.clues):
            self.grid[i] = {}
            for j, character in enumerate(row):
                self.grid[i][j] = character

    def dump_data(self):
        data_list = []
        if not self.grid:
            assert("There is no data loaded to dump")
        for i, row in enumerate(self.grid):
            staging_string = ""
            for j, character in enumerate(self.grid):
                staging_string += self.grid[i][j].replace("?", "X")
            data_list.append(staging_string)
        return data_list
    
    
###################################################################################################
# Running
###################################################################################################

        
if __name__ == '__main__':
    p = Puzzle(TEST_DATA, has_gui=True)
