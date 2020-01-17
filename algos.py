


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
    
class CrossHatchSolver:
    def __init__(self, clues):
        self.clues = clues
        self.load_data()
        self.known_in_cols = ["" for x in range(9)]  # Is there not a better way?
        self.known_in_blocks = ["" for x in range(9)]
        self.unknown_count = 81

    def solve(self):
        self._update_knowns()
        self.print_pretty()
        last_count = self.unknown_count
        while self.unknown_count > 0:
            self._update_grid()
            self._update_knowns()
            if self.unknown_count == last_count:
                break
            last_count = self.unknown_count
            print(f"Unknown_count: {str(self.unknown_count)}")
            break
        self.print_pretty()
    
    def print_pretty(self):
        group3 = lambda x: zip(*(iter(x),) * 3)
        blank_count = 0
        print("#"*79)
        for row_3 in group3(self.grid):
            for row in row_3:
                print(f"{row}: {[self.grid[row][c]['value'] for c in self.grid[row]]}")
                blank_count += len([x for x in self.grid[row] if self.grid[row][x]["value"] == "?"])
            print("-"*45)
        print("#"*79)
        print(f"Missing: {blank_count}  Filled:  {81 - blank_count}")

    def load_data(self):
        maths = lambda r, c: (c // 3) + (r // 3) * 3
        self.grid = {}
        for r, row in enumerate(self.clues):
            self.grid[r] = {}
            for c, character in enumerate(row):
                #self.grid[r][c] = (character, maths(r, c)) 
                self.grid[r][c] = {"value": character, 
                                   "block": maths(r, c), 
                                   "potentials": []
                                   } 

    def _update_grid(self):
        diff = lambda l1, l2: (list(set(l1) - set(l2))) 
        count = 0
        for row in self.grid:
            g = self.grid[row]
            
            known_in_row = "".join([g[col]["value"] for col in g if g[col]["value"] != "?"])
            #print(f"Known in row: {known_in_row}")
            for col in self.grid[row]:
                #character == self.grid[r][c]['value']
                #print(f"Found '?'at {r}, {c}")
                
                knowns_dups = [self.known_in_cols[col] + \
                              known_in_row + \
                              self.known_in_blocks[self.grid[row][col]["block"]]]
                knowns = []
                [knowns.append(x) for x in "".join(knowns_dups) if x not in knowns]
                knowns = "".join(knowns)
                print(f"Cell: ({row}, {col}) knowns: {knowns}")
                #knowns = list(set(knowns))
                #print(f"Cleaned knowns: {knowns}")
                d = diff("".join((str(x+1) for x in range(9))), knowns)
                print(f"(Difference of knowns and what's needed: {d}")
                if len(d) == 1:
                    self.grid[row][col]['value'] = d[0]
                    print(f"Changed {row}, {col} to {self.grid[row][col]['value']}")
                    
    def _update_knowns(self):
        self.unknown_count = 0
        for row in self.grid:
            for col in self.grid[row]:
                if self.grid[row][col]["value"] != "?":
                    cell = self.grid[row][col]
                    if cell["value"] not in self.known_in_cols[col]:
                        self.known_in_cols[col] += cell["value"]
                    if cell["value"] not in self.known_in_blocks[cell["block"]]:
                        self.known_in_blocks[cell["block"]] += cell["value"]
                else:
                    self.unknown_count += 1
        
    
    def dump_data(self):
        data_list = []
        for i, row in enumerate(self.grid):
            staging_string = ""
            for j, character in enumerate(self.grid):
                staging_string += self.grid[i][j]
            data_list.append(staging_string)
        return data_list
    
    

    
if __name__ == "__main__":
    foob = CrossHatchSolver(TEST_DATA)
    foob.solve()
