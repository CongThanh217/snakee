import pygame
from Constants import *
from GA import *
import sys


class Menu:
    def __init__(self, game):
        self.game = game
        self.mid_size = (NO_OF_CELLS_ROW*CELL_SIZE)/2
        self.run_display = True
        #tạo vị trí của cursor
        self.cursor_rect = pygame.Rect(0, 0, 0, 0)
        #offset là vị trí biên
        self.offset = -50
        self.title_size = 50
        self.option_size = 28
        self.backGround_img = pygame.image.load('assets/background.png')

    def draw_cursor(self):
        self.game.draw_text(
            '*', size=20,
            x=self.cursor_rect.x, y=self.cursor_rect.y,
            color=(0, 91, 65)
        )
    def draw_button(self):
        pygame.draw.rect(self.game.display, (0, 0, 0),
                         (self.cursor_rect.x - 25, self.cursor_rect.y - 40, 150, 80))
        pygame.draw.rect(self.game.display, (0, 0, 0), (self.cursor_rect.x - 25, self.cursor_rect.y - 40, 150, 80), 4)

    def blit_menu(self):
        self.game.window.blit(self.game.display, (0, 0))
        pygame.display.update()
        self.game.reset_keys()


class MainMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = 'PLAYER'

        self.cursorBFS = MENU_COLOR
        self.cursorDFS = WHITE
        self.cursorASTAR = WHITE
        self.cursorGA = WHITE

        self.BFSx, self.BFSy = self.mid_size + 70, self.mid_size + 200
        self.DFSx, self.DFSy = self.mid_size + 400, self.mid_size + 200
        self.ASTARx, self.ASTARy = self.mid_size + 700, self.mid_size + 200
        # self.GAx, self.GAy = self.mid_size, self.mid_size + 100

        self.cursor_rect.midtop = (self.BFSx + self.offset, self.BFSy)

    # pygame.mixer.init()
    #
    # # Load sound file
    # sound = pygame.mixer.Sound('assets/background.mp3')  # Replace with your sound file
    #
    # # Play the sound
    # sound.play()

    def change_cursor_color(self):
        self.clear_cursor_color()
        if self.state == 'PLAYER':
            self.cursorBFS = MENU_COLOR
        elif self.state == 'BOT':
            self.cursorDFS = MENU_COLOR
        elif self.state == 'BATTLE':
            self.cursorASTAR = MENU_COLOR
        # elif self.state == 'GA':
        #     self.cursorGA = MENU_COLOR

    def clear_cursor_color(self):
        self.cursorBFS = WHITE
        self.cursorDFS = WHITE
        self.cursorASTAR = WHITE
        # self.cursorGA = WHITE

    def display_menu(self):
        print('1')
        self.run_display = True
        while self.run_display:
            self.backGround_img = pygame.transform.scale(self.backGround_img, (NO_OF_CELLS_COL * CELL_SIZE, NO_OF_CELLS_ROW * CELL_SIZE))

            backGround_img_rect = self.backGround_img.get_rect(topleft=(0,0))
            self.game.display.blit(self.backGround_img, backGround_img_rect)
            self.game.event_handler()
            self.check_input()
            self.draw_button()
            self.game.draw_text(
                'PLAYER', size=self.option_size,
                x=self.BFSx, y=self.BFSy,
                color=self.cursorBFS
            )
            self.game.draw_text(
                'BOT', size=self.option_size,
                x=self.DFSx, y=self.DFSy,
                color=self.cursorDFS
            )

            self.game.draw_text(
                'BATTLE', size=self.option_size,
                x=self.ASTARx, y=self.ASTARy,
                color=self.cursorASTAR
            )
            # self.draw_cursor()
            self.change_cursor_color()
            self.blit_menu()

    def check_input(self):
        self.move_cursor()

        if self.game.START:
            if self.state == 'BOT':
                self.game.curr_menu = self.game.algo_menu
            elif self.state == 'PLAYER':
                print('3')
                self.game.player_mode = True
                self.game.playing = True
            self.run_display = False


    def move_cursor(self):
        if self.game.RIGHTKEY:
            pygame.mixer.init()

            # Load sound file
            sound = pygame.mixer.Sound('assets/selectSound.mp3')  # Replace with your sound file

            # Play the sound
            sound.play()
            if self.state == 'PLAYER':
                self.cursor_rect.midtop = (
                    self.DFSx + self.offset, self.ASTARy)
                self.state = 'BOT'

            elif self.state == 'BOT':
                self.cursor_rect.midtop = (
                    self.ASTARx + self.offset, self.ASTARy)
                self.state = 'BATTLE'

            elif self.state == 'BATTLE':
                self.cursor_rect.midtop = (
                    self.BFSx + self.offset, self.BFSy)
                self.state = 'PLAYER'

            # elif self.state == 'GA':
            #     self.cursor_rect.midtop = (
            #         self.BFSx + self.offset, self.BFSy)
            #     self.state = 'BFS'

        if self.game.LEFTKEY:
            pygame.mixer.init()

            # Load sound file
            sound = pygame.mixer.Sound('assets/selectSound.mp3')  # Replace with your sound file

            # Play the sound
            sound.play()
            if self.state == 'PLAYER':
                self.cursor_rect.midtop = (
                    self.ASTARx + self.offset, self.ASTARy)
                self.state = 'BATTLE'

            elif self.state == 'BOT':
                self.cursor_rect.midtop = (
                    self.BFSx + self.offset, self.BFSy)
                self.state = 'PLAYER'

            elif self.state == 'BATTLE':
                self.cursor_rect.midtop = (
                    self.DFSx + self.offset, self.DFSy)
                self.state = 'BOT'

            # elif self.state == 'GA':
            #     self.cursor_rect.midtop = (
            #         self.ASTARx + self.offset, self.ASTARy)
            #     self.state = 'ASTAR'
    def move_options(self):
        if self.game.RIGHTKEY:
            pygame.mixer.init()

            # Load sound file
            sound = pygame.mixer.Sound('assets/selectSound.mp3')  # Replace with your sound file

            # Play the sound
            sound.play()
            if self.state == 'PLAYER':
                self.cursor_rect.midtop = (
                    self.DFSx + self.offset, self.ASTARy)
                self.state = 'BOT'

            elif self.state == 'BOT':
                self.cursor_rect.midtop = (
                    self.ASTARx + self.offset, self.ASTARy)
                self.state = 'BATTLE'

            elif self.state == 'BATTLE':
                self.cursor_rect.midtop = (
                    self.BFSx + self.offset, self.BFSy)
                self.state = 'PLAYER'



        if self.game.LEFTKEY:
            pygame.mixer.init()

            # Load sound file
            sound = pygame.mixer.Sound('assets/selectSound.mp3')  # Replace with your sound file

            # Play the sound
            sound.play()
            if self.state == 'BFS':
                self.cursor_rect.midtop = (
                    self.ASTARx + self.offset, self.ASTARy)
                self.state = 'ASTAR'

            elif self.state == 'DFS':
                self.cursor_rect.midtop = (
                    self.BFSx + self.offset, self.BFSy)
                self.state = 'BFS'

            elif self.state == 'ASTAR':
                self.cursor_rect.midtop = (
                    self.DFSx + self.offset, self.DFSy)
                self.state = 'DFS'

            # elif self.state == 'GA':
            #     self.cursor_rect.midtop = (
            #         self.ASTARx + self.offset, self.ASTARy)
            #     self.state = 'ASTAR'
class AlgoMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = 'BFS'

        self.cursorBFS = MENU_COLOR
        self.cursorDFS = WHITE
        self.cursorASTAR = WHITE
        self.cursorGA = WHITE

        self.BFSx, self.BFSy = self.mid_size + 70, self.mid_size + 200
        self.DFSx, self.DFSy = self.mid_size + 400, self.mid_size + 200
        self.ASTARx, self.ASTARy = self.mid_size + 700, self.mid_size + 200
        # self.GAx, self.GAy = self.mid_size, self.mid_size + 100

        self.cursor_rect.midtop = (self.BFSx + self.offset, self.BFSy)

    # pygame.mixer.init()
    #
    # # Load sound file
    # sound = pygame.mixer.Sound('assets/background.mp3')  # Replace with your sound file
    #
    # # Play the sound
    # sound.play()

    def change_cursor_color(self):
        self.clear_cursor_color()
        if self.state == 'BFS':
            self.cursorBFS = MENU_COLOR
        elif self.state == 'DFS':
            self.cursorDFS = MENU_COLOR
        elif self.state == 'ASTAR':
            self.cursorASTAR = MENU_COLOR
        # elif self.state == 'GA':
        #     self.cursorGA = MENU_COLOR

    def clear_cursor_color(self):
        self.cursorBFS = WHITE
        self.cursorDFS = WHITE
        self.cursorASTAR = WHITE
        # self.cursorGA = WHITE

    def display_menu(self):

        self.run_display = True
        while self.run_display:
            self.backGround_img = pygame.transform.scale(self.backGround_img, (NO_OF_CELLS_COL * CELL_SIZE, NO_OF_CELLS_ROW * CELL_SIZE))
            backGround_img_rect = self.backGround_img.get_rect(topleft=(0,0))
            self.game.display.blit(self.backGround_img, backGround_img_rect)
            self.game.event_handler()
            self.check_input()
            self.draw_button()
            self.game.draw_text(
                'BFS', size=self.option_size,
                x=self.BFSx, y=self.BFSy,
                color=self.cursorBFS
            )
            self.game.draw_text(
                'BFS', size=self.option_size,
                x=self.DFSx, y=self.DFSy,
                color=self.cursorDFS
            )

            self.game.draw_text(
                'ASTAR', size=self.option_size,
                x=self.ASTARx, y=self.ASTARy,
                color=self.cursorASTAR
            )
            # self.draw_cursor()
            self.change_cursor_color()
            self.blit_menu()

    def check_input(self):
        self.move_cursor()

        if self.game.START:
            if self.state == 'GA':  # go to genetic algorith options
                self.game.curr_menu = self.game.main_menu
            else:
                self.game.playing = True
            self.run_display = False


    def move_cursor(self):
        if self.game.RIGHTKEY:
            pygame.mixer.init()

            # Load sound file
            sound = pygame.mixer.Sound('assets/selectSound.mp3')  # Replace with your sound file

            # Play the sound
            sound.play()
            if self.state == 'BFS':
                self.cursor_rect.midtop = (
                    self.DFSx + self.offset, self.ASTARy)
                self.state = 'DFS'

            elif self.state == 'DFS':
                self.cursor_rect.midtop = (
                    self.ASTARx + self.offset, self.ASTARy)
                self.state = 'ASTAR'

            elif self.state == 'ASTAR':
                self.cursor_rect.midtop = (
                    self.BFSx + self.offset, self.BFSy)
                self.state = 'BFS'

            # elif self.state == 'GA':
            #     self.cursor_rect.midtop = (
            #         self.BFSx + self.offset, self.BFSy)
            #     self.state = 'BFS'

        if self.game.LEFTKEY:
            pygame.mixer.init()

            # Load sound file
            sound = pygame.mixer.Sound('assets/selectSound.mp3')  # Replace with your sound file

            # Play the sound
            sound.play()
            if self.state == 'BFS':
                self.cursor_rect.midtop = (
                    self.ASTARx + self.offset, self.ASTARy)
                self.state = 'ASTAR'

            elif self.state == 'DFS':
                self.cursor_rect.midtop = (
                    self.BFSx + self.offset, self.BFSy)
                self.state = 'BFS'

            elif self.state == 'ASTAR':
                self.cursor_rect.midtop = (
                    self.DFSx + self.offset, self.DFSy)
                self.state = 'DFS'

            # elif self.state == 'GA':
            #     self.cursor_rect.midtop = (
            #         self.ASTARx + self.offset, self.ASTARy)
            #     self.state = 'ASTAR'
    def move_options(self):
        if self.game.RIGHTKEY:
            pygame.mixer.init()

            # Load sound file
            sound = pygame.mixer.Sound('assets/selectSound.mp3')  # Replace with your sound file

            # Play the sound
            sound.play()
            if self.state == 'PLAYER':
                self.cursor_rect.midtop = (
                    self.DFSx + self.offset, self.ASTARy)
                self.state = 'BOT'

            elif self.state == 'BOT':
                self.cursor_rect.midtop = (
                    self.ASTARx + self.offset, self.ASTARy)
                self.state = 'BATTLE'

            elif self.state == 'BATTLE':
                self.cursor_rect.midtop = (
                    self.BFSx + self.offset, self.BFSy)
                self.state = 'PLAYER'



        if self.game.LEFTKEY:
            pygame.mixer.init()

            # Load sound file
            sound = pygame.mixer.Sound('assets/selectSound.mp3')  # Replace with your sound file

            # Play the sound
            sound.play()
            if self.state == 'BFS':
                self.cursor_rect.midtop = (
                    self.ASTARx + self.offset, self.ASTARy)
                self.state = 'ASTAR'

            elif self.state == 'DFS':
                self.cursor_rect.midtop = (
                    self.BFSx + self.offset, self.BFSy)
                self.state = 'BFS'

            elif self.state == 'ASTAR':
                self.cursor_rect.midtop = (
                    self.DFSx + self.offset, self.DFSy)
                self.state = 'DFS'

            # elif self.state == 'GA':
            #     self.cursor_rect.midtop = (
            #         self.ASTARx + self.offset, self.ASTARy)
            #     self.state = 'ASTAR'
class button():
    def __init__(self, x, y, text, game):
        self.x = x
        self.y = y
        self.text = text
        self.game = game
        self.font = pygame.font.Font("assets/font.otf", 30)
        self.clicked = False

    def draw_button(self):
        action = False

        # get mouse position
        pos = pygame.mouse.get_pos()

        # create pygame Rect object for the button
        button_rect = pygame.Rect(self.x, self.y, BTN_WIDTH, BTN_HEIGHT)

        # check mouseover and clicked conditions
        if button_rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                self.clicked = True
                pygame.draw.rect(self.game.display, BTN_CLICKED, button_rect)
            elif pygame.mouse.get_pressed()[0] == 0 and self.clicked == True:
                self.clicked = False
                action = True
            else:
                pygame.draw.rect(self.game.display, BTN_HOVER, button_rect)
        else:
            pygame.draw.rect(self.game.display, BTN_COLOR, button_rect)


        text_img = self.font.render(self.text, True, WHITE)
        text_len = text_img.get_width()
        self.game.display.blit(text_img, (self.x + int(BTN_WIDTH / 2) -
                                          int(text_len / 2), self.y + 25))

        return action


class TextBox:
    def __init__(self, x, y, game):
        self.font = pygame.font.Font("assets/font.otf", 20)
        self.input_rect = pygame.Rect(x, y, TXT_WIDTH, TXT_HEIGHT)
        self.input = ''
        self.game = game
        self.active = False

    def draw_input(self):
        # get mouse position
        pos = pygame.mouse.get_pos()

        if self.input_rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                self.active = True

        elif pygame.mouse.get_pressed()[0] == 1:
            self.active = False

        if self.active:
            color = TXT_ACTIVE
        else:
            color = TXT_PASSIVE

        pygame.draw.rect(self.game.display, color, self.input_rect, 2)
        text_surface = self.font.render(self.input, False, WHITE)
        self.game.display.blit(
            text_surface, (self.input_rect.x + 15, self.input_rect.y + 1))


# class GAMenu(Menu):
#     def __init__(self, game, controller):
#         Menu.__init__(self, game)
#
#         self.controller = controller
#         self.train_model = button(
#             game.SIZE/2 - 4*(CELL_SIZE + NO_OF_CELLS), game.SIZE/2 + 3.5*(CELL_SIZE + NO_OF_CELLS), 'Train Model', game)
#         self.load_model = button(
#             game.SIZE/2 + (CELL_SIZE), game.SIZE/2 + 3.5*(CELL_SIZE + NO_OF_CELLS), 'Load Model', game)
#
#         self.no_population = TextBox(
#             self.game.SIZE/2 + 50, self.game.SIZE/2 - 60, game)
#         self.no_generation = TextBox(
#             self.game.SIZE/2 + 50, self.game.SIZE/2 - 10, game)
#         self.no_hidden_nodes = TextBox(
#             self.game.SIZE/2 + 50, self.game.SIZE/2 + 40, game)
#         self.mutation_rate = TextBox(
#             self.game.SIZE/2 + 50, self.game.SIZE/2 + 90, game)
#         self.init_input()
#
#     def init_input(self):
#         self.no_population.input = '300'
#         self.no_generation.input = '30'
#         self.no_hidden_nodes.input = '8'
#         self.mutation_rate.input = '12'
#
    def display_menu(self):

        self.run_display = True
        while self.run_display:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game.running, self.game.playing = False, False
                    self.game.curr_menu.run_display = False
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        self.game.BACK = True

                    if self.no_population.active:
                        if event.key == pygame.K_BACKSPACE:
                            self.no_population.input = self.no_population.input[:-1]
                        else:
                            if event.unicode.isdigit() and len(self.no_population.input) < 3:
                                self.no_population.input += event.unicode

                    if self.no_generation.active:
                        if event.key == pygame.K_BACKSPACE:
                            self.no_generation.input = self.no_generation.input[:-1]
                        else:
                            if event.unicode.isdigit() and len(self.no_generation.input) < 3:
                                self.no_generation.input += event.unicode

                    if self.no_hidden_nodes.active:
                        if event.key == pygame.K_BACKSPACE:
                            self.no_hidden_nodes.input = self.no_hidden_nodes.input[:-1]
                        else:
                            if event.unicode.isdigit() and len(self.no_hidden_nodes.input) < 2:
                                self.no_hidden_nodes.input += event.unicode

                    if self.mutation_rate.active:
                        if event.key == pygame.K_BACKSPACE:
                            self.mutation_rate.input = self.mutation_rate.input[:-1]
                        else:
                            if event.unicode.isdigit() and len(self.mutation_rate.input) < 3:
                                self.mutation_rate.input += event.unicode

            self.check_input()
            self.game.display.fill(WINDOW_COLOR)

            self.game.draw_text(
                'GA Options', self.title_size,
                self.game.SIZE/2, self.game.SIZE /
                2 - 4*(CELL_SIZE + NO_OF_CELLS),
                color=TITLE_COLOR
            )
            self.game.draw_text(
                'Settings to train model:', 25,
                self.game.SIZE/2,
                self.game.SIZE/2 - 2*(CELL_SIZE + NO_OF_CELLS),
                color=MENU_COLOR
            )
            self.game.draw_text(
                "No. of populations     : ", 20,
                self.game.SIZE/2 - 2*CELL_SIZE,
                self.game.SIZE/2 - 50,
                color=BANNER_COLOR
            )

            self.game.draw_text(
                "No. of generations     : ", 20,
                self.game.SIZE/2 - 2*CELL_SIZE,
                self.game.SIZE/2,
                color=BANNER_COLOR
            )

            self.game.draw_text(
                "No. of hidden nodes   : ", 20,
                self.game.SIZE/2 - 2*CELL_SIZE,
                self.game.SIZE/2 + 50,
                color=BANNER_COLOR
            )

            self.game.draw_text(
                "Mutation rate %:          : ", 20,
                self.game.SIZE/2 - 2*CELL_SIZE,
                self.game.SIZE/2 + 100,
                color=BANNER_COLOR
            )

            self.no_population.draw_input()
            self.no_generation.draw_input()
            self.no_hidden_nodes.draw_input()

            self.mutation_rate.draw_input()

            if self.load_model.draw_button():
                self.load_GA()
            if self.train_model.draw_button():
                self.train_GA()

            self.game.draw_text(
                "Q to return to main menu", 20,
                self.game.SIZE/2, self.game.SIZE/2 + 6*(NO_OF_CELLS+CELL_SIZE),
                color=WHITE
            )

            self.blit_menu()
        self.reset()

    def reset(self):
        self.no_population.active = False
        self.no_generation.active = False
        self.no_hidden_nodes.active = False
        self.mutation_rate.active = False

    def check_input(self):
        if self.game.BACK:
            self.game.curr_menu = self.game.main_menu
            self.run_display = False

    def load_GA(self):
        self.game.curr_menu = self.game.main_menu
        self.run_display = False
        self.game.curr_menu.state = 'GA'
        self.game.playing = True
        self.game.load_model = True

    def train_GA(self):
        self.game.curr_menu = self.game.main_menu
        self.run_display = False
        self.game.curr_menu.state = 'GA'
        self.game.playing = True

        if len(self.no_population.input) > 0:
            Population.population = int(self.no_population.input)

        if len(self.no_hidden_nodes.input) > 0:
            Population.hidden_node = int(self.no_hidden_nodes.input)

        if len(self.no_generation.input) > 0:
            GA.generation = int(self.no_generation.input)

        if len(self.mutation_rate.input) > 0:
            GA.mutation_rate = int(self.mutation_rate.input)/100
