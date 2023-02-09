from base import GUIBase
from square import Squares
import pygame


class RightPanel(GUIBase):
    def __init__(self, size: tuple, screen: pygame.Surface):
        super().__init__(size, screen)
        self.__selected = None
        self.__bg_box = None
        self.__squares = [
            [
                Squares(
                    r + 1,
                    (10, r),
                    (self.size[0], self.size[1]),
                    self.screen,
                    False,
                )
                for r in range(9)
            ]
        ]

    @property
    def squares(self) -> list:
        return self.__squares
    
    @property
    def selected(self) -> tuple:
        return self.__selected

    @selected.setter
    def selected(self, pos: tuple):
        if self.__selected != None:
                self.__squares[self.__selected[0]][self.__selected[1]].selected = False
        if pos:
            # select new square
            self.__selected = pos
            self.__squares[self.__selected[0]
                           ][self.__selected[1]].selected = True
        else:
            # set selected to None if pos out of board
            self.__selected = None

    def get_box_bg(self):
        return self.__bg_box
    
    def draw(self):
        self.__bg_box = pygame.draw.rect(self.screen, (255,225,225), pygame.Rect(665, 100, 400//9, 44*9))
        for i in range(9):
            self.__squares[0][i].draw()

        space = self.size[0] // 9
        for r in range(10):
            # draw col
            if r == 0 or r == 1:
                pygame.draw.line(
                    self.screen,
                    (0, 0, 0),
                    (665 + space*r, 100),
                    (665 + space*r, space*9 + 100),
                    2,
                )
                # draw row
            pygame.draw.line(
                self.screen,
                (0, 0, 0),
                (665, space*r + 100),
                (665 + space, space*r + 100),
                2,
            )
