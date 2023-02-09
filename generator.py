from random import randint, shuffle
from solver import Solver

class Generator:
    def __init__(self):
        self.__solver = Solver()
        self.__DIFFICULTY = {
        "easy":         62,
        "medium":       53,
        "hard":         44,
        "very-hard":    35,
        "insane":       26,
        "inhuman":      17,
        }
        self.__listNum = [1,2,3,4,5,6,7,8,9]
    @property
    def grid(self)->list:
         return self.__grid
    def fillGrid(self, grid):
        pos = self.__solver.nextpos(grid)
        shuffle(self.__listNum)
        if not pos:
            return True
        for n in self.__listNum:
             if not self.__solver.exists(grid, n, pos):
                grid[pos[0]][pos[1]] = n
                if self.__solver.solve(grid):
                    return True
                grid[pos[0]][pos[1]] = 0
        return False

    def generate(self, difficulty):
        grid = [[0 for r in range(9)] for c in range(9)]
        self.fillGrid(grid)
        difficulty = self.__DIFFICULTY.get(difficulty)
        for i in range(0, 81 - difficulty):
                col = randint(0,8)
                row = randint(0,8)
                while grid[col][row] == 0:
                        col = randint(0,8)
                        row = randint(0,8)
                grid[col][row] = 0
        return grid