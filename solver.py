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
        self.clues = clues
        self.data = clues
        self.has_gui = has_gui
        self.solvers = {"TestSolver": TestSolver}
        #self.current_solver = CrossHatchSolver(self.clues)
        self.current_solver = TestSolver(self.clues)
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
    
    def print_data(self):
        visual = []    
        x_border = " --- " * 4
        visual.append(x_border)
        for line in self.data:
            visual.append("| " + line + " |")
        visual.append(x_border)
        for line in visual:
            print(line)                
    
    def set_solver(self, solver):
        self.current_solver = solver(self.clues)
        
    def solve(self):
        if not self.current_solver:
            assert("solver not set")
        time, results = self.clockit(self.current_solver.solve())
        test = self.check_data(results)
        if self.has_gui:
            self.gui.pg.update_pg(results)
            self.gui.menu_col.status_label.text = "SUCCESS!" if test else "FAIL!!!"
            self.gui.menu_col.info_label.update_time(time)
        
        print(time, results)

###################################################################################################
# SOLVERS
###################################################################################################

class TestSolver: 
    def __init__(self, clues):
        pass

    def solve(self):
        return [
                "827154396",
                "965327148",
                "341689752",
                "593468271",
                "472513689",
                "618972435",
                "786235914",
                "154796823",
                "239841567"
                ]
        
        

class CrossHatchSolver:
    pass    
    
###################################################################################################
# Running
###################################################################################################

        
if __name__ == '__main__':
    p = Puzzle(TEST_DATA, has_gui=True)
