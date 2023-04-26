import pygame, sys
from board import Board
from right_panel import RightPanel
from menu import Button
class Custom:
    def __init__(self) -> None:
        self.__running = True
        self.__screen_size = (850, 600)
        self.__screen = pygame.display.set_mode(self.__screen_size[:2])
        self.__board = [[0 for r in range(9)] for c in range(9)]
        self.__board_model = Board((400,400), self.__board, self.__screen)
        self.__right_panel = RightPanel((400, 400), self.__screen)
        self.__play = Button(screen=self.__screen, pos=(100, 200),
                                 text_input="Play", font=pygame.font.Font("./Rubik-Bold.ttf", 28), base_color="#ffffff", hovering_color="#f780bf", size=(100, 40))
        self.__menu = Button(screen=self.__screen, pos=(100, 300),
                                 text_input="Menu", font=pygame.font.Font("./Rubik-Bold.ttf", 28), base_color="#ffffff", hovering_color="#f780bf", size=(100, 40))
        self.state = ""
        pygame.display.set_caption("Sudoku")
    def __del__(self):
        pass
    @property
    def running(self):
        return self.__running
    
    @running.setter
    def running(self, value: bool):
        self.__running = value
    @property
    def board(self):
        return self.__board
    def __refresh(self):
        pos = pygame.mouse.get_pos()
        bg = pygame.image.load("bg7.jpg")
        bg = pygame.transform.scale(bg, (850, 600))
        self.__screen.blit(bg, (0, 0))
        self.__board_model.draw()
        self.__right_panel.draw()
        pygame.draw.rect(self.__screen, (225, 225, 225), ((
            100-(100//2), 200-(40//2 -1)), (100, 40)),1,20)
        pygame.draw.rect(self.__screen, (225, 225, 225), ((
            100-(100//2), 300-(40//2 -1)), (100, 40)),1,20)
        for button in [self.__play, self.__menu]:
            button.changeColor(pos)
            button.update()
        pygame.display.update()
    
    def loop(self):
        jump_mode = False
        while self.__running:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif e.type == pygame.MOUSEBUTTONDOWN:
                    self.__select_by_mouse()
                    self.playing()
                elif e.type == pygame.KEYDOWN:
                    self.__set_del_value_by_key(e)
                    self.__select_by_arrows(
                                e, self.__board_model.selected, jump_mode
                            )
                    if e.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()
                    elif e.key == pygame.K_j:
                        jump_mode = not jump_mode
            self.__refresh()

    def __select_by_mouse(self):
        p = pygame.mouse.get_pos()
        if self.__board_model.get_bg_box().collidepoint(p):
            self.__right_panel.selected = None
            self.__board_model.selected = ((p[1] - 100) // (400 // 9 ), (p[0]-225)//(400//9))
        if self.__right_panel.get_box_bg().collidepoint(p):
            self.__right_panel.selected = (((p[0]-665)//(400//9),(p[1] - 100) // (400 // 9 )))
            if self.__board_model.selected:
                v = self.__right_panel.squares[self.__right_panel.selected[0]][self.__right_panel.selected[1]].value
                self.__board_model.set_pencil(v)
                self.__board_model.set_value()

    def playing(self):
        p = pygame.mouse.get_pos()
        if self.__play.checkForInput(p):
            self.state = "play"
            self.__running = False
        if self.__menu.checkForInput(p):
            self.state = "menu"
            self.__running = False
    def __set_del_value_by_key(self, e: pygame.event.Event):
        v = 0
        # delete / backspace key
        if e.key == pygame.K_BACKSPACE or e.key == pygame.K_DELETE:
            # clear selected item
            self.__board_model.clear
        # pencil 1-9
        elif e.key == pygame.K_1:
            v = 1
        elif e.key == pygame.K_2:
            v = 2
        elif e.key == pygame.K_3:
            v = 3
        elif e.key == pygame.K_4:
            v = 4
        elif e.key == pygame.K_5:
            v = 5
        elif e.key == pygame.K_6:
            v = 6
        elif e.key == pygame.K_7:
            v = 7
        elif e.key == pygame.K_8:
            v = 8
        elif e.key == pygame.K_9:
            v = 9
        if 0 < v < 10:
            self.__board_model.set_pencil(v)
            self.__board_model.set_value()
    
    def __select_by_arrows(self, e: pygame.event.Event, pos: tuple, jump_mode: bool):
        # set row, column change value
        r, c = 0, 0
        if e.key == pygame.K_UP or e.key == pygame.K_w:
            r = -1
        elif e.key == pygame.K_DOWN or e.key == pygame.K_s:
            r = 1
        elif e.key == pygame.K_RIGHT or e.key == pygame.K_d:
            c = 1
        elif e.key == pygame.K_LEFT or e.key == pygame.K_a:
            c = -1
        # check if there's selected square
        if pos:
            if jump_mode:
                # find next empty position in the same direction
                while -1 < pos[0] + r < 9 and -1 < pos[1] + c < 9 and r + c != 0:
                    pos = (pos[0] + r, pos[1] + c)
                    if self.__board_model.board[pos[0]][pos[1]] == 0:
                        break
                # move only if the next position is empty
                if self.__board_model.board[pos[0]][pos[1]] == 0:
                    self.__board_model.selected = pos
            else:
                # move to the next position
                pos = (pos[0] + r, pos[1] + c)
                if -1 < pos[0] < 9 and -1 < pos[1] < 9:
                    self.__board_model.selected = pos
    