import pygame, time, sys
from surface import convertStrToGrid
from board import Board
from left_panel import LeftPanel
from right_panel import RightPanel
from solver import Solver

class GUI:
    def __init__(self, board: list):
        self.__running = True
        self.__screen_size = (850, 600)
        self.__screen = pygame.display.set_mode(self.__screen_size[:2])
        # icon
        self.__board = board
        self.__board_model = Board((400,400), self.__board, self.__screen)
        self.__solver = Solver(self.__board_model, 200)
        self.__left_panel = LeftPanel(self.__solver, (400,400), self.__screen)
        self.__right_panel = RightPanel((400, 400), self.__screen)
        self.__pencil = True
        pygame.display.set_caption("Sudoku")
    def __del__(self):
        pass
    @property
    def running(self):
        return self.__running
    
    @running.setter
    def running(self, value: bool):
        self.__running = value

    def __refresh(self):
        bg = pygame.image.load("bg7.jpg")
        bg = pygame.transform.scale(bg, (850, 600))
        self.__screen.blit(bg, (0, 0))
        self.__board_model.draw()
        self.__left_panel.draw()
        self.__right_panel.draw()
        pygame.display.update()

        for b in self.__left_panel.options.buttons:
            b.reset
    def save(self):
        file = open("save.txt","w")
        board_init = ""
        board = ""
        board_pencil = ""
        selected = (-1,-1)
        if self.__left_panel.gamesystem.won:
            time_save = (self.__left_panel.time.end_time - self.__left_panel.time.init_time) + self.__left_panel.time.continue_time
        else:
            time_save = time.time() - self.__left_panel.time.init_time + self.__left_panel.time.continue_time
        if self.__board_model.selected:
            selected = self.__board_model.selected
        for i in range(9):
            for j in range(9):
                if self.__board_model.squares[i][j].changeable:
                    board_init+= str(0)
                else:
                    board_init += str(self.__board_model.squares[i][j].value)
        for i in range(9):
            for j in range(9):
                if self.__board_model.squares[i][j].pencil == 0:
                    board_pencil+= str(0)
                else:
                    board_pencil += str(self.__board_model.squares[i][j].pencil)
        for i in range(9):
            for j in range(9):
                board += str(self.__board[i][j])
        file.writelines([
                            board_init + "\n",
                            board + "\n",
                            board_pencil + "\n", 
                            str(time_save) + "\n",
                            str(selected[0]) + " " + str(selected[1]) + "\n",
                            str(self.__left_panel.gamesystem.get_wrongs_counter())
                        ])
        file.close()
    def continue_game(self):
        file = open("save.txt", "r")
        data = file.readlines()
        board_init = convertStrToGrid(data[0].split("\n")[0])
        board = convertStrToGrid(data[1].split("\n")[0])
        board_pencil = convertStrToGrid(data[2].split("\n")[0])
        time = data[3].split("\n")[0]
        selected = data[4].split("\n")[0]
        wrongs = data[5]
        file.close()
        if selected[0] == "-1":
            self.__board_model.selected = None
        else:
            self.__board_model.selected = (int(selected.split(" ")[0]), int(selected.split(" ")[1]))
        self.__left_panel.gamesystem.set_wrongs_counter(int(wrongs))
        list_change = []
        list_pencil = []
        for i in range(9):
            for j in range(9):
                if int(board_init[i][j]) - int(board[i][j]) < 0:
                    list_change.append((i, j))
                if int(board_init[i][j]) - int(board_pencil[i][j]) < 0:
                    list_pencil.append((i,j))
        for pos in list_pencil:
            i,j = pos
            self.__board_model.set_pencil_save((i,j),int(board_pencil[i][j]))
        for pos in list_change:
            i,j = pos
            issuccess = self.__board_model.set_value_save((i,j), int(board[i][j]))
            self.set_issuccess(issuccess)
        self.__left_panel.time.continue_time = float(time)

    def loop(self):
        jump_mode = False
        while self.__running:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif e.type == pygame.MOUSEBUTTONDOWN:
                    if not self.__select_by_mouse():
                        self.__buttons_mouse()
                elif e.type == pygame.KEYDOWN:
                    if (
                        not self.__left_panel.gamesystem.lost
                        and not self.__left_panel.gamesystem.won
                    ):
                        self.__set_del_value_by_key(e)
                        self.__select_by_arrows(
                                e, self.__board_model.selected, jump_mode
                            )
                    if e.key == pygame.K_q:
                        return
                    elif e.key == pygame.K_j:
                        jump_mode = not jump_mode
            self.__refresh()    

    def __select_by_mouse(self):
        p = pygame.mouse.get_pos()
        if self.__board_model.get_bg_box().collidepoint(p):
            self.__right_panel.selected = None
            self.__board_model.selected = ((p[1] - 100) // (400 // 9 ), (p[0]-225)//(400//9))
            return True
        if self.__right_panel.get_box_bg().collidepoint(p):
            self.__right_panel.selected = (((p[0]-665)//(400//9),(p[1] - 100) // (400 // 9 )))
            if self.__board_model.selected:
                v = self.__right_panel.squares[self.__right_panel.selected[0]][self.__right_panel.selected[1]].value
                self.__board_model.set_pencil(v)
                if self.__pencil == False:
                    issuccess = self.__board_model.set_value()
                    self.set_issuccess(issuccess)
                return True
        return False
        
    def __buttons_mouse(self):
        p = pygame.mouse.get_pos()
        s = True
        for b in self.__left_panel.options.buttons:
            if b.bg_box.collidepoint(p):
                if b.innertxt == "menu":
                    self.save()
                    s = b.click()
                    self.running = False
                elif b.innertxt == "pencil":
                    self.__pencil = True
                    s = b.click()
                elif b.innertxt == "value":
                    self.__pencil = False
                    s = b.click()
                elif b.innertxt == "selected":
                     # copy board
                    copy = [[] for r in range(9)]
                    for r in range(9):
                        for c in range(9):
                            # append the num
                            copy[r].append(self.__board_model.board[r][c])
                    s = b.click((copy, self.__board_model.selected))
                    break
                elif b.innertxt == "reset":
                    self.__board_model.selected = None
                    self.__board_model.clear_state()
                    # reset won/lost/wrongs_counter
                    self.__left_panel.gamesystem.reset()
                    # # reset time
                    self.__left_panel.time.init_time = time.time()
                    self.__left_panel.time.end_time = None
                    self.__left_panel.time.continue_time = 0
                    # reset hint
                    self.__left_panel.hints.hint = "Everything is well"
                    s = b.click()
                    break
                else:
                    self.__board_model.clear_state()
                    self.__board_model.selected = None
                    s = b.click()
                    break
        # check for unsolvable case
        if not s:
            self.__left_panel.hints.hint = "Unsolvable board"

    def set_issuccess(self, issuccess):
        if issuccess == 's':
                if self.__board_model.isfinished:
                    self.__left_panel.gamesystem.won = True
                    self.__left_panel.time.end_time = time.time()
        elif issuccess == 'w':
                self.__left_panel.gamesystem.wrongs_counter
                self.__left_panel.hints.hint = "Press backspace"
                if self.__left_panel.gamesystem.lost:
                    self.__left_panel.time.end_time = time.time()
        elif issuccess == "c":
                self.__left_panel.hints.hint = "Unsolvable board"
    def __set_del_value_by_key(self, e: pygame.event.Event):
        v = 0
        # delete / backspace key
        if e.key == pygame.K_BACKSPACE or e.key == pygame.K_DELETE:
            # clear selected item
            self.__board_model.clear
            # reset hints
            self.__left_panel.hints.hint = "Everything is well"
        # return / enter key
        elif e.key == pygame.K_RETURN:
            issuccess = self.__board_model.set_value()
            self.set_issuccess(issuccess)
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
            if self.__pencil == False:
                    issuccess = self.__board_model.set_value()
                    self.set_issuccess(issuccess)
    
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


