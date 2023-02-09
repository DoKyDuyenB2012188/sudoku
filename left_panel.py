
from base import GUIBase
from parallel import Threads
import pygame, time

class LeftPanel(GUIBase):
    def __init__(self, solver, size: tuple, screen: pygame.Surface):
        super().__init__(size, screen)
        self.time = Time(self.size, self.screen)
        self.hints = Hints(self.size, self.screen)
        self.options = Options(solver, self.size, self.screen)
        self.gamesystem = GameSystem(self.size, self.screen)
    def draw(self):
        self.time.draw()
        self.hints.draw()
        self.options.draw()
        self.gamesystem.draw()


class GameSystem(GUIBase):
    def __init__(self, size: tuple, screen: pygame.Surface):
        super().__init__((size[0], size[1] // 9), screen)
        self.__wrongs_counter = 0
        self.__lost = False
        self.__won = False

    def reset(self):
        self.__lost = False
        self.__won = False
        self.__wrongs_counter = 0

    def get_wrongs_counter(self):
        return self.__wrongs_counter
    
    def set_wrongs_counter(self, value: int):
        self.__wrongs_counter = value

    @property
    def wrongs_counter(self):
        if self.__wrongs_counter < 5:
            self.__wrongs_counter += 1
        else:
            self.__lost = True

    @property
    def lost(self) -> bool:
        return self.__lost

    @lost.setter
    def lost(self, value: bool):
        self.__lost = value

    @property
    def won(self) -> bool:
        return self.__won

    @won.setter
    def won(self, value: bool):
        self.__won = value

    def draw(self):
        w = 1
        self._type("Info",(57, 48, 155), (20, 100 + 44*6 -20),20)
        pygame.draw.rect(
            self.screen,
            (225, 225, 225),
            ((20, 100 + 44*6 + 10), (44*4 +10,44)),1
        )
        # draw wrongs
        # check if the player lost or won
        if self.__won:
            self._type(
                "You Won",
                (57, 48, 155),
                (64, 100 + 44*6+15),
                24,
            )
        elif not self.__lost:
            self._type(
                "X  " * self.__wrongs_counter,
                (234, 72, 54),
                (50, self.size[1] * 8 + 28),
                24,
            )
        else:
            self._type(
                "You Lost",
                (57, 48, 155),
                (64, 100 + 44*6+15),
                24,
            )

class Options(GUIBase):
    def __init__(self, solver, size: tuple, screen: pygame.Surface):
        super().__init__(size, screen)
        self.__threads = Threads()
        self.__solver = solver
        self.__run = False
        self.__buttons = [
            Button(*i, (44*2,44), self.screen)
            for i in (
                (self.start, (), (-2, 0.7), "auto", 24, (20,100 + 44*1)),
                (self.solve_all, (), (-2, 0.7), "past", 24, (20+44*2+10,100 + 44*1)),
                (self.kill, (), (-2, 0.7), "stop", 24, (20,100 + 44*2+10)),
                (self.solve_selected, (), (-17, 3), "selected", 20, (20+44*2+10,100 + 44*2+10)),
                (self.reset, (), (-6, 0.7), "reset", 24, (20,100+44*4 + 10)),
                (self.menu, (), (-9, 0.7), "menu", 24, (20+44*2+10,100+44*4 + 10)),
                (self.pencil, (), (-9, 0.7), "pencil", 24, (30+700,100 + 44*1)),
                (self.value, (), (-9, 0.7), "value", 24, (30+700,100 + 44*2 + 10))
            )
        ]
    def menu(self):
        return True
    def pencil(self):
        return True
    def value(self):
        return True
    def start(self):
        """Start auto solver"""
        if not self.__run:
            self.__solver.kill = False
            self.__solver.e = True
            self.__threads.start(self.__solver.auto_solver)
            self.__run = True

    def kill(self):
        """Kill/Stop auto solver"""
        self.__solver.kill = True
        self.__threads.stop()
        self.__run = False
    
    def solve_all(self) -> bool:
        # solve all
        s = self.__solver.solve(self.__solver.board.board)
        self.__solver.board.update_squares()
        return s

    def solve_selected(self, board: list, pos: tuple):
        # solve the board
        solution = self.__solver.solve(board)
        # if it's solvable set selected square value
        if solution and pos:
            self.__solver.board.board[pos[0]][pos[1]] = board[pos[0]][pos[1]]
            self.__solver.board.update_squares()
        return solution
    
    def reset(self) -> bool:
        """Reset board"""
        # iterate over all squares
        for r in range(9):
            for c in range(9):
                # check for changeable squares
                if self.__solver.board.squares[r][c].changeable:
                    # reset it to 0
                    self.__solver.board.board[r][c] = 0
        # clear wrong square
        if self.__solver.board.wrong:
            self.__solver.board.clear
        # update squares
        self.__solver.board.update_squares()
        return True
    
    @property
    def buttons(self)->list:
        return self.__buttons
    def draw(self):
        for b in self.__buttons:
            b.draw()
        self._type(
            f"Solver",
            (57, 48, 155),
            (20,115),
            20,
        )
        self._type(
            f"Option",
            (57, 48, 155),
            (20,115+44*3+10),
            20,
        )

class Time(GUIBase):
    def __init__(self, size: tuple, screen: pygame.Surface):
        super().__init__((size[0], size[1] // 9), screen) # 850 600
        self.__init_time = time.time()
        self.__end_time = None
        self.__continue_time = 0.0

    @property
    def init_time(self):
        """init time property (getter)"""
        return self.__init_time
    
    @init_time.setter
    def init_time(self, value: time.time):
        self.__init_time = value

    @property
    def end_time(self):
        return self.__end_time
    
    @end_time.setter
    def end_time(self, value: time.time):
        self.__end_time = value
    
    @property
    def continue_time(self):
        return self.__continue_time
    
    @continue_time.setter
    def continue_time(self, value: float):
        self.__continue_time = value

    def __time_formatter(self, delta: float) -> str:
        # calculate HHMMSS from franctional secs
        hms = [delta // 60 // 60, delta // 60, delta % 60]
        # convert in to str with required left zero if the number < 10
        for i in range(len(hms)):
            hms[i] = f"0{int(hms[i])}" if hms[i] < 10 else f"{int(hms[i])}"
        return f"{hms[0]}:{hms[1]}:{hms[2]}"
    
    def draw(self):
        if self.__end_time:
            ftime = self.__time_formatter((self.__end_time - self.__init_time) + self.__continue_time)
            self._type(
                f"{ftime}",
                (225, 225, 225),
                (self.size[1]*9 + 100, 60),
                30,
            )
        else:
            ftime = self.__time_formatter((time.time() - self.__init_time) + self.__continue_time)
            self._type(
                f"{ftime}",
                (225, 225, 225),
                (self.size[1]*9 + 100, 60),
                30,
            )

class Hints(GUIBase):
    def __init__(self, size: tuple, screen: pygame.Surface):
        super().__init__((size[0], size[1] // 9), screen)
        self.__hint = "Everything is well"

    @property
    def hint(self) -> str:
        """hint property (getter)"""
        return self.__hint

    @hint.setter
    def hint(self, value: str):
        self.__hint = value

    def draw(self):
        self._type(
            f"{self.__hint}",
            (225, 225, 225),
            (225, 65),
            24,
        )

class Button(GUIBase):
    def __init__(
        self,
        target,
        _args: tuple,
        s: tuple,
        innertxt: str,
        fontsize: int,
        pos: tuple,
        size: tuple,
        screen: pygame.Surface,
    ):
        super().__init__(size, screen)
        self.__pos = pos
        self.__innertxt = innertxt
        self.__fontsize = fontsize
        self.__target = target
        self.__args = _args
        self.__fill = (0, 0, 0)
        self.__color = (96, 87, 193)
        self.__s = s
        self.__bg_box = None
    
    @property
    def bg_box(self):
        return self.__bg_box
    @property
    def innertxt(self):
        """innertxt property (getter)"""
        return self.__innertxt

    @property
    def click_range(self):
        """click range property"""
        return self.__click_range

    @property
    def reset(self):
        """Reset button style"""
        self.__fill = (0, 0, 0)
        self.__w = 1
        self.__color = (96, 87, 193)

    def click(self, args: tuple = ()):
        # change button style
        self.__fill = (30, 50, 20)
        self.__w = 2
        self.__color = (247, 128, 191)
        # call the traget
        if self.__args:
            return self.__target(self.__args)
        elif args:
            return self.__target(*args)
        else:
            return self.__target()

    def draw(self):
        # Draw main frame
        # draw rectangle (frame)
        self.__bg_box = pygame.draw.rect(
            self.screen,
            self.__color,
            (self.__pos, self.size)
        )
        for i in range(2):
            # pygame.draw.line()
            pygame.draw.line(self.screen, (225,225,225), (self.__pos[0], self.__pos[1] + 44*i),(self.__pos[0] + 88, self.__pos[1] + 44*i), 2)
            pygame.draw.line(self.screen, (225,225,225), (self.__pos[0]+ 88*i, self.__pos[1]),(self.__pos[0] + 88*i, self.__pos[1]+ 44), 2)
        # set inner text
        self._type(
            self.__innertxt,
            "#ffffff",
            (
                self.__pos[0] + self.size[0] // 4 + self.__s[0],
                self.__pos[1] + self.size[1] // 8 + self.__s[1],
            ),
            self.__fontsize,
        )
