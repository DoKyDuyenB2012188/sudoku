from base import GUIBase
import pygame


class Squares(GUIBase):
    def __init__(
            self,
            value: int,
            pos: tuple,
            widthpos: tuple,
            screen: pygame.Surface,
            changeable: bool
    ):
        super().__init__(0, screen)
        self.__value = value
        self.__pos = pos
        self.__widthpos = widthpos
        self.__pencil = 0
        self.__selected = False
        self.__changeable = changeable
        self.__wrong = False
        self.__unit_selected = False
        self.__is_same_num = False

    @property
    def changeable(self):
        return self.__changeable

    @property
    def selected(self):
        return self.__selected

    @selected.setter
    def selected(self, v: bool):
        self.__selected = v

    @property
    def value(self) -> int:
        return self.__value

    @value.setter
    def value(self, value: int):
        if self.__changeable:
            self.__value = value

    @property
    def pencil(self) -> int:
        return self.__pencil

    @pencil.setter
    def pencil(self, value: int):
        if self.__changeable:
            self.__pencil = value

    @property
    def wrong(self):
        return self.__wrong

    @wrong.setter
    def wrong(self, w: bool):
        self.__wrong = w
    @property
    def unit_selected(self):
        return self.__unit_selected

    @unit_selected.setter
    def unit_selected(self, w: bool):
        self.__unit_selected = w
    
    @property
    def is_same_num(self):
        return self.__is_same_num

    @is_same_num.setter
    def is_same_num(self, w: bool):
        self.__is_same_num = w

    def draw(self):
        space = self.__widthpos[0] // 9
        r, c = (self.__pos[0] * space) + 225, (self.__pos[1] * space) + 100
         # main selected
        if not self.__changeable:
            sqzise = self.__widthpos[0] // 9
            pygame.draw.rect(self.screen, (187, 222, 251), ((r, c), (sqzise, sqzise)))
        else:
            sqzise = self.__widthpos[0] // 9
            pygame.draw.rect(self.screen, (225, 225, 225), ((r, c), (sqzise, sqzise)))
        if self.__selected:
            pygame.draw.rect(self.screen, (197, 124, 234), ((r, c), (space, space)))
            # unit selected
        if self.__unit_selected:
            pygame.draw.rect(self.screen, (204, 196, 242), ((r, c), (space, space)))
        if self.__is_same_num:
            pygame.draw.rect(self.screen, (186, 76, 201), ((r, c), (space, space)))
        if self.__value != 0:
            font = pygame.font.Font("./Roboto-Bold.ttf", 30)
            rgb = (0, 0, 0) if not self.__wrong else (234, 72, 54)
            v = font.render(str(self.__value), 1, rgb)
            self.screen.blit(
                v,
                (
                    int(r + ((space / 2) - (v.get_width() / 2))),
                    int(c + ((space / 2) - (v.get_height() / 2)))
                )
            )
        elif self.__pencil != 0:
            font = pygame.font.Font("./Roboto-Bold.ttf", 20)
            v = font.render(str(self.__pencil), 1, (0, 0, 0))
            self.screen.blit(
                v,
                (
                    int(r + ((space / 2) - (v.get_width() / 2)) - 8),
                    int(c + ((space / 2) - (v.get_height() / 2)) - 8),
                ),
            )


