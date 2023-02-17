import pygame
import sys
from menu import Button

class Guide:
    def __init__(self) -> None:
        self.running = True
        self.__screen_size = (850, 600)
        self.__screen = pygame.display.set_mode(self.__screen_size[:2])
        pygame.display.set_caption("Sudoku")
    def __del__(self):
        pass
    def loop(self):
        while self.running:
            # set background
            bg = pygame.image.load("bg7.jpg")
            bg = pygame.transform.scale(bg, (850, 600))
            self.__screen.blit(bg, (0, 0))
            # create object button
            MENU_BUTTON = Button(screen=self.__screen, pos=(425, 600-50),
                                     text_input="Menu", font=pygame.font.Font(r"C:\Users\Admin\Desktop\my_Sudoku\Rubik-Bold.ttf", 28), base_color="#ffffff", hovering_color="#f780bf", size=(100, 40))
            #set title game
            font = pygame.font.Font(r"C:\Users\Admin\Desktop\my_Sudoku\Rubik-Medium.ttf", 17)
            font_title = pygame.font.Font(r"C:\Users\Admin\Desktop\my_Sudoku\Rubik-Bold.ttf", 24)
            font_intro_title = pygame.font.Font(r"C:\Users\Admin\Desktop\my_Sudoku\Rubik-Bold.ttf", 17)
            font_intro = pygame.font.Font(r"C:\Users\Admin\Desktop\my_Sudoku\Rubik-Medium.ttf", 17)
            #How to Play Sudoku
            line_title_1 = font_title.render("How to Play Sudoku", True, "#ffffff")
            line1 = font.render("In Sudoku, you must complete the grid so each row, column and 3-by-3 box (in bold borders)", True, "#ffffff")
            line1_1 = font.render("contains every digit 1 through 9.", True, "#ffffff")
            line2 = font.render("No row, column, or 3×3 box can feature the same number twice.",True, "#ffffff")
            line3 = font.render("That means each row, column, and 3×3 square in a Sudoku puzzle must contain ONLY one 1,",True, "#ffffff")
            line3_1 = font.render("one 2, one 3, one 4, one 5, one 6, one 7, one 8, and one 9.",True, "#ffffff")
            line_title_2 = font_title.render("Introduce", True, "#ffffff")
            intro1 = font_intro_title.render("Developer:",True, "#ffffff")
            intro1_1 = font_intro.render("Do Ky Duyen",True, "#ffffff")
            #version
            intro2 = font_intro_title.render("Version:",True, "#ffffff")
            intro2_2 = font_intro.render("1.0 (demo)",True, "#ffffff")
            #release
            intro3 = font_intro_title.render("Release:",True, "#ffffff")
            intro3_3 = font_intro.render("17/2/2023",True, "#ffffff")
            #engine
            intro4 = font_intro_title.render("Engine:",True, "#ffffff")
            intro4_4 = font_intro.render("Python, pygame",True, "#ffffff")
            self.__screen.blit(line_title_1,(44, 180 - 30))
            self.__screen.blit(line1,(44, 220 - 30))
            self.__screen.blit(line1_1,(44, 240 - 30))
            self.__screen.blit(line2,(44, 260 - 30))
            self.__screen.blit(line3,(44, 280 - 30))
            self.__screen.blit(line3_1,(44, 300 - 30))
            self.__screen.blit(line_title_2,(44, 330 - 30))
            #developer
            self.__screen.blit(intro1,(44, 370 - 30))
            self.__screen.blit(intro1_1,(140, 370 - 30))
            #version
            self.__screen.blit(intro2,(44, 390 - 30))
            self.__screen.blit(intro2_2,(120, 390 - 30))
            #release
            self.__screen.blit(intro3,(44, 410 - 30))
            self.__screen.blit(intro3_3,(120, 410 - 30))
            #Engine
            self.__screen.blit(intro4,(44, 430 - 30))
            self.__screen.blit(intro4_4,(115, 430 - 30))
            # draw button
            MENU_MOUSE_POS = pygame.mouse.get_pos()
            for button in [MENU_BUTTON]:
                button.changeColor(MENU_MOUSE_POS)
                button.update()
            # check vent
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if MENU_BUTTON.checkForInput(MENU_MOUSE_POS):
                        self.running = False
            pygame.display.update()

