import threading
import time


class Solver:

    def __init__(self, board=None, delay: float = 0.0):
        self.board = board
        self.__delay = delay / 1000
        self.__e = threading.Event()
        self.__kill = False
        self.__e.set()

    @property
    def delay(self) -> float:
        """delay property (getter)"""
        return self.__delay

    @delay.setter
    def delay(self, delay: float):
        self.__delay = delay / 1000

    @property
    def e(self):
        """e property (getter)"""
        return self.__e.is_set()

    @e.setter
    def e(self, set: bool):
        if set:
            self.__e.set()
        else:
            self.__e.clear()

    @property
    def kill(self):
        """stop solve function to join the thread"""
        return self.__kill

    @kill.setter
    def kill(self, kill: bool):
        self.__kill = kill

    def auto_solver(self) -> bool:
        if not self.__kill:
            # get the next unused position from (LTR, TTB)
            pos = self.nextpos(self.board.board)
            # solved -edge
            if not pos:
                return True
            # itertate over all possible numbers(0-9)
            for n in range(1, 10):
                # check if the number valid in sudoku rules
                if not self.exists(self.board.board, n, pos):
                    # pause/resumption
                    self.__e.wait()
                    # change board state
                    self.board.set_sq_value(n, (pos[0], pos[1]))
                    self.board.board[pos[0]][pos[1]] = n
                    # sleep (solution case)
                    time.sleep(self.__delay)
                    # continue in the solution -edge
                    if self.auto_solver():
                        return True
                    if not self.__kill:
                        # pause/resumption
                        self.__e.wait()
                        # backtracking
                        # change board state
                        self.board.set_sq_value(0, (pos[0], pos[1]))
                        self.board.board[pos[0]][pos[1]] = 0
            # sleep (backtracking case)
            time.sleep(self.__delay)
            # invalid solution
            return False

    def solve(self, board: list) -> bool:
        # get the next unused position from (LTR, TTB)
        pos = self.nextpos(board)
        # solved -edge
        if not pos:
            return True
        # itertate over all possible numbers(0-9)
        for n in range(1, 10):
            # check if the number valid in sudoku rules
            if not self.exists(board, n, pos):
                # set value as solution
                board[pos[0]][pos[1]] = n
                # continue in the solution -edge
                if self.solve(board):
                    return True
                # backtracking
                board[pos[0]][pos[1]] = 0
        # invalid solution
        return False

    def nextpos(self, board: list) -> tuple:
        for r in range(9):
            for c in range(9):
                if board[r][c] == 0:
                    return (r, c)
        return ()

    def exists(self, board: list, n: int, rc: tuple) -> tuple:

        for c in range(len(board)):
            # check same row
            if board[rc[0]][c] == n:
                return (rc[0], c)
        # check same rcol
        for r in range(len(board)):
            if board[r][rc[1]] == n:
                return (r, rc[1])
        # check 3*3
        spos = ((rc[0] // 3) * 3, (rc[1] // 3) * 3)
        for r in range(spos[0], spos[0] + 3):
            for c in range(spos[1], spos[1] + 3):
                if board[r][c] == n:
                    return (r, c)
        return ()
