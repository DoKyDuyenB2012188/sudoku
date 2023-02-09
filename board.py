import pygame
from base import GUIBase
from solver import Solver
from square import Squares


class Board(GUIBase):
    def __init__(self, size: tuple, board: list, screen: pygame.Surface):
        super().__init__((size[1], size[1], size[0] - size[1]), screen)
        self.__solver = Solver(self)
        self.__board = board
        self.__squares = [
            [
                Squares(
                    self.__board[c][r],
                    (r, c),
                    (self.size[0], self.size[2]),
                    self.screen,
                    True if self.__board[c][r] == 0 else False,
                )
                for r in range(9)
            ]
            for c in range(9)
        ]
        self.__bg_box = None
        self.__selected = None
        self.__wrong = None
        self.__units_list = None
        self.__same_num_list = None

    @property
    def wrong(self):
        return self.__wrong

    @property
    def squares(self) -> list:
        return self.__squares

    def update_squares(self):
        for r in range(9):
            for c in range(9):
                self.__squares[r][c].value = self.__board[r][c]
                self.__squares[r][c].pencil = 0

    def update__unit_list(self):
        if self.__selected:
            self.__units_list = []
            i, j = self.__selected
            for it in range(9):
                if (i, it) != self.__selected:
                    self.__units_list.append((i, it))
                if (it, j) != self.__selected:
                    self.__units_list.append((it, j))
            it = i//3
            jt = j//3
            for x in range(it * 3, it * 3 + 3):
                for y in range(jt * 3, jt * 3 + 3):
                    if (x, y) != self.__selected:
                        self.__units_list.append((x, y))

    def update__same_num_list(self):
        if self.__selected:
            i, j = self.__selected
            if self.__board[i][j] != 0:
                self.__same_num_list = []
                for r in range(9):
                    for c in range(9):
                        if self.__board[r][c] == self.__board[i][j] and (r, c) != (i, j):
                            self.__same_num_list.append((r, c))
            else:
                self.__same_num_list = None

    @property
    def board(self) -> list:
        return self.__board

    @board.setter
    def board(self, board: list):
        self.__board = board
        self.__squares = [
            [
                Square(
                    self.__board[c][r],
                    (r, c),
                    (self.size[0], self.size[2]),
                    self.screen,
                    True if self.__board[c][r] == 0 else False,
                )
                for r in range(9)
            ]
            for c in range(9)
        ]

    @property
    def selected(self) -> tuple:
        return self.__selected

    def clear_state(self):
        if self.__units_list:
            for p in self.__units_list:
                r, c = p
                self.__squares[r][c].unit_selected = False
            self.__units_list = None
        if self.__same_num_list:
            for p in self.__same_num_list:
                r, c = p
                self.__squares[r][c].is_same_num = False
            self.__same_num_list = None

    @selected.setter
    def selected(self, pos: tuple):
        if not self.__wrong:
            # clear previous selection
            if self.__selected != None:
                self.__squares[self.__selected[0]
                               ][self.__selected[1]].selected = False
            if pos:
                # select new square
                self.__selected = pos
                self.__squares[self.__selected[0]
                               ][self.__selected[1]].selected = True
                self.clear_state()
                self.update__unit_list()
                self.update__same_num_list()
            else:
                # set selected to None if pos out of board
                self.__selected = None

    @property
    def get_pencil(self) -> int:
        r, c = self.__selected
        return self.__squares[r][c].pencil

    def set_pencil(self, value: int):
        r, c = self.__selected
        if self.__squares[r][c].value == 0:
            self.__squares[r][c].pencil = value

    def set_pencil_save(self, pos: tuple, value: int):
        r, c = pos
        if self.__squares[r][c].value == 0:
            self.__squares[r][c].pencil = value
    @property
    def get_value(self) -> int:
        r, c = self.__selected
        return self.__squares[r][c].value

    def set_value(self) -> str:
        r, c = self.__selected
        if self.get_value == 0:
            pencil = self.get_pencil
            if pencil != 0:
                w = self.__solver.exists(self.__board, pencil, (r, c))
                if w:
                    self.__squares[r][c].wrong = True
                    self.__squares[w[0]][w[1]].wrong = True
                    self.__squares[r][c].value = pencil
                    self.__board[r][c] = pencil
                    self.__wrong = w
                    return "w"
                else:
                    self.__squares[r][c].value = pencil
                    self.__board[r][c] = pencil
                    copy = [[] for r in range(9)]
                    for r in range(9):
                        for c in range(9):
                            copy[r].append(self.__board[r][c])
                    if not self.__solver.solve(copy):
                        return "c"
                    return "s"

    def set_value_save(self, pos: tuple, value: int) -> str:
        r, c = pos
        if value != 0:
            w = self.__solver.exists(self.__board, value, (r, c))
            if w:
                self.__squares[r][c].wrong = True
                self.__squares[w[0]][w[1]].wrong = True
                self.__squares[r][c].value = value
                self.__board[r][c] = value
                self.__wrong = w
                return "w"
            else:
                self.__squares[r][c].value = value
                self.__board[r][c] = value
                copy = [[] for r in range(9)]
                for r in range(9):
                    for c in range(9):
                        copy[r].append(self.__board[r][c])
                if not self.__solver.solve(copy):
                    return "c"
                return "s"

    @property
    def clear(self):
        """clear selected square value"""
        # get selected square
        r, c = self.__selected
        # clear square value and pencil
        self.__squares[r][c].value = 0
        self.__squares[r][c].pencil = 0
        self.__board[r][c] = 0
        self.clear_state()
        # change wrong state
        if self.__wrong:
            self.__squares[r][c].wrong = False
            self.__squares[self.__wrong[0]][self.__wrong[1]].wrong = False
            self.__wrong = None

    @property
    def isfinished(self):
        return not self.__solver.nextpos(self.board)

    def set_sq_value(self, value: int, pos: tuple):
        self.__squares[pos[0]][pos[1]].value = value

    def get_bg_box(self):
        return self.__bg_box

    def draw(self):
        """Draw the board on the screen"""
        # Draw squares
        self.__bg_box = pygame.draw.rect(
            self.screen, (255, 225, 225), pygame.Rect(225, 100, 396, 396))
        # iterate over all rows
        for r in range(9):
            # iterate over all columns
            for c in range(9):
                # draw square value
                if self.__units_list and (c, r) in self.__units_list:
                    self.__squares[c][r].unit_selected = True
                if self.__same_num_list and (c, r) in self.__same_num_list:
                    self.__squares[c][r].is_same_num = True
                self.__squares[c][r].draw()
        # Draw grid
        # set space between squares
        space = self.size[0] // 9
        # drow 10 lines HvV
        for r in range(10):
            # set line weight (bold at the end of 3*3 area)
            w = 4 if r % 3 == 0 else 1
            # draw horizontal line (screen, (color), (start_pos), (end_pos), width)
            pygame.draw.line(
                self.screen,
                (0, 0, 0),
                (225, (r * space)+100),
                (space*9 + 225, (r * space) + 100),
                w,
            )
            # draw vertical line (screen, (color), (start_pos), (end_pos), width)
            pygame.draw.line(
                self.screen,
                (0, 0, 0),
                ((r * space) + 225, 100),
                ((r * space) + 225, space*9 + 100),
                w,
            )
