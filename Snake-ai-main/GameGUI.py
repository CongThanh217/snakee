import pygame
from pygame import Vector2

from Constants import *
from main_menu import *
from GameController import GameController
from GA import *
import sys


class GameGUI:
    def __init__(self):
        pygame.init()

        # self.WIDTH = self.SIZE
        # self.HEIGHT = self.SIZE
        #
        # self.display = pygame.Surface((self.WIDTH, self.HEIGHT))
        # self.window = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.clock = pygame.time.Clock()
        self.SCREEN_UPDATE = pygame.USEREVENT
        self.paused = False
        self.speed = 110
        self.speed_up = 80

        pygame.time.set_timer(self.SCREEN_UPDATE, self.speed)

        self.controller = GameController()
        self.player_mode = False
        self.running, self.playing = True, False
        self.RIGHTKEY, self.LEFTKEY, self.START, self.BACK = False, False, False, False

        # SỐ LƯỢNG CỘT LÀ COL TƯƠNG ỨNG VỚI ĐỘ RỘNG X THEO CHIỀU NGANG, SỐ LƯỢNG HÀNG LÀ ROW TƯƠNG ỨNG VỚI ĐỘ DÀI Y
        self.SIZE_ROW = CELL_SIZE * NO_OF_CELLS_ROW
        self.SIZE_COL = CELL_SIZE * NO_OF_CELLS_COL
        self.display = pygame.Surface((self.SIZE_COL, self.SIZE_ROW))
        self.window = pygame.display.set_mode((self.SIZE_COL, self.SIZE_ROW))

        self.font_name = 'assets/font.otf'

        self.main_menu = MainMenu(self)
        self.algo_menu = AlgoMenu(self)
        # self.GA = GAMenu(self, self.controller)
        self.curr_menu = self.main_menu

        self.load_model = False
        self.view_path = False
        self.head_up = pygame.image.load('Graphics/head_up.png').convert_alpha()
        self.head_down = pygame.image.load('Graphics/head_down.png').convert_alpha()
        self.head_right = pygame.image.load('Graphics/head_right.png').convert_alpha()
        self.head_left = pygame.image.load('Graphics/head_left.png').convert_alpha()
        self.head_up = pygame.image.load('Graphics/head_up.png').convert_alpha()
        self.tail_up = pygame.image.load('Graphics/tail_up.png').convert_alpha()
        self.tail_down = pygame.image.load('Graphics/tail_down.png').convert_alpha()
        self.tail_right = pygame.image.load('Graphics/tail_right.png').convert_alpha()
        self.tail_left = pygame.image.load('Graphics/tail_left.png').convert_alpha()
        self.body_vertical = pygame.image.load('Graphics/body_vertical.png').convert_alpha()
        self.body_horizontal = pygame.image.load('Graphics/body_horizontal.png').convert_alpha()
        self.body_tr = pygame.image.load('Graphics/body_tr.png').convert_alpha()
        self.body_tl = pygame.image.load('Graphics/body_tl.png').convert_alpha()
        self.body_br = pygame.image.load('Graphics/body_br.png').convert_alpha()
        self.body_bl = pygame.image.load('Graphics/body_bl.png').convert_alpha()

    def checkSTop(self):
        while self.playing:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        self.paused = not self.paused;

    def game_loop(self):
        print('game loop')
        while self.playing:
            if not self.paused:
                # if self.player_mode:
                #     self.controller.player_play()
                    self.event_handler()
                    if self.BACK:
                        self.playing = False
                    if self.controller.algo != None:
                      self.draw_elements()
                    self.window.blit(self.display, (0, 0))
                    pygame.display.update()
                    self.clock.tick(60)
                    self.reset_keys()

    def add_obstacle(self, pos):
        x, y = pos
        x //= CELL_SIZE
        y //= CELL_SIZE
        if 0 <= x < NO_OF_CELLS and BANNER_HEIGHT <= y < NO_OF_CELLS:
            self.controller.grid.grid[x][y].obstacle = True

    def draw_elements(self):
        # draw banner and stats
        self.draw_grass()

        self.draw_all_path()
        self.draw_path()
        self.draw_banner()
        self.draw_game_stats()

        # if self.curr_menu.state != 'GA' or self.controller.model_loaded:
        fruit = self.controller.get_fruit_pos()

        obstacle = self.controller.get_obstacles_pos()

        snake = self.controller.snake

        self.draw_fruit(fruit)
        self.draw_obstacles(obstacle)

        self.draw_snake(snake)
        self.draw_score()
        self.draw_speed()






    def draw_grass(self):
        grass_img = pygame.image.load('assets/ground.png')
        grass_react = grass_img.get_rect(topleft=(0, 0))
        self.display.blit(grass_img, grass_react)

    def draw_game_stats(self):
        if self.curr_menu.state != 'GA':  # path Ai algo
            instruction = 'Space to view Ai path, W to speed up, Q to go back'

        elif self.controller.model_loaded:  # trained model
            instruction = 'W to speed up, Q to go back'

        else:  # training model GA algo
            instruction = 'Space to hide all snakes, W to speed up, Q to go back'
            curr_gen = str(self.controller.curr_gen())
            best_score = str(self.controller.best_GA_score())

            stats_gen = f'Generation: {curr_gen}/{GA.generation}'
            stats_score = f'Best score: {best_score}'
            stats_hidden_node = f'Hidden nodes {Population.hidden_node}'

            # draw stats
            self.draw_text(
                stats_gen, size=20,
                x=3 * CELL_SIZE, y=CELL_SIZE - 10,
            )
            self.draw_text(
                stats_score, size=20,
                x=3 * CELL_SIZE, y=CELL_SIZE + 20,
            )
            self.draw_text(
                stats_hidden_node, size=20,
                x=self.SIZE / 2, y=CELL_SIZE - 30,
                color=SNAKE_COLOR
            )

        # instruction
        self.draw_text(
            instruction, size=20,
            x=self.SIZE_ROW / 2, y=(CELL_SIZE * NO_OF_CELLS_COL) - NO_OF_CELLS_COL,
            color=WHITE
        )

        # current Algo Title
        self.draw_text(
            self.curr_menu.state, size=30,
            x=1360, y=CELL_SIZE * 2.5,
        )

        self.draw_text(
            'AI MODE', size=30,
            x=1360, y=CELL_SIZE,
        )

    def draw_all_snakes_GA(self):
        if not self.view_path:  # have all snakes visible by default

            for snake in self.controller.snakes:  # for each snake in list
                self.draw_snake(snake)

                # fruit of each snake
                self.draw_fruit(snake.get_fruit())

    def draw_all_path(self):
        if self.controller.algo != None and self.view_path:
            for path in self.controller.algo.explored_set:  # for each {x,y} in path
                x = int(path.x * CELL_SIZE + CELL_SIZE / 2)
                y = int(path.y * CELL_SIZE + CELL_SIZE / 2)
                # print(len(self.controller.algo.explored))
                pygame.draw.circle(self.display, ALLPATHCOLOR, (x, y), 5)

    def draw_path(self):
        if self.controller.algo != None and self.view_path:
            for path in self.controller.algo.path:  # for each {x,y} in path
                x = int(path.x * CELL_SIZE + CELL_SIZE / 2)
                y = int(path.y * CELL_SIZE + CELL_SIZE / 2)
                pygame.draw.circle(self.display, PATHCOLOR, (x, y), 5)

    def draw_snake_head(self, snake):
        head_relation = snake.body[1] - snake.body[0]
        if head_relation == Vector2(1, 0):
            self.head = self.head_left
        elif head_relation == Vector2(-1, 0):
            self.head = self.head_right
        elif head_relation == Vector2(0, 1):
            self.head = self.head_up
        elif head_relation == Vector2(0, -1):
            self.head = self.head_down
        head = snake.body[0]  # Get the position of the snake's head
        x = int(head.x * CELL_SIZE)
        y = int(head.y * CELL_SIZE)

        self.display.blit(self.head, (x, y))

    def draw_snake_tail(self, snake):
        tail_relation = snake.body[-2] - snake.body[-1]
        if tail_relation == Vector2(1, 0):
            self.tail = self.tail_left
        elif tail_relation == Vector2(-1, 0):
            self.tail = self.tail_right
        elif tail_relation == Vector2(0, 1):
            self.tail = self.tail_up
        elif tail_relation == Vector2(0, -1):
            self.tail = self.tail_down
        head = snake.body[-1]  # Get the position of the snake's head
        x = int(head.x * CELL_SIZE)
        y = int(head.y * CELL_SIZE)

        self.display.blit(self.tail, (x, y))

    def draw_snake_body(self, body):
        self.draw_rect(body, color=SNAKE_COLOR, border=True)

    def draw_rect(self, element, color, border=False):
        x = int(element.x * CELL_SIZE)
        y = int(element.y * CELL_SIZE)

        body_rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(self.display, color, body_rect)

        if border:
            pygame.draw.rect(self.display, WINDOW_COLOR, body_rect, 3)

    def draw_snake(self, snake):
        global body_image
        self.draw_snake_head(snake)
        self.draw_snake_tail(snake)

        for index, block in enumerate(snake.body):
            x_pos = int(block.x * CELL_SIZE)
            y_pos = int(block.y * CELL_SIZE)
            block_rect = pygame.Rect(x_pos, y_pos, CELL_SIZE, CELL_SIZE)

            if index == 0:
                # Draw the head
                head_relation = snake.body[1] - snake.body[0]
                if head_relation == Vector2(1, 0):
                    head_image = self.head_left
                elif head_relation == Vector2(-1, 0):
                    head_image = self.head_right
                elif head_relation == Vector2(0, 1):
                    head_image = self.head_up
                elif head_relation == Vector2(0, -1):
                    head_image = self.head_down
                self.display.blit(head_image, block_rect)
            elif index == len(snake.body) - 1:
                # Draw the tail
                tail_relation = snake.body[-2] - snake.body[-1]
                if tail_relation == Vector2(1, 0):
                    tail_image = self.tail_left
                elif tail_relation == Vector2(-1, 0):
                    tail_image = self.tail_right
                elif tail_relation == Vector2(0, 1):
                    tail_image = self.tail_up
                elif tail_relation == Vector2(0, -1):
                    tail_image = self.tail_down
                self.display.blit(tail_image, block_rect)
            else:
                # Draw the body segments
                previous_block = snake.body[index + 1] - block
                next_block = snake.body[index - 1] - block
                if previous_block.x == next_block.x:
                    body_image = self.body_vertical
                elif previous_block.y == next_block.y:
                    body_image = self.body_horizontal
                else:
                    if previous_block.x == -1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == -1:
                        body_image = self.body_tl
                    elif previous_block.x == -1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == -1:
                        body_image = self.body_bl
                    elif previous_block.x == 1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == 1:
                        body_image = self.body_tr
                    elif previous_block.x == 1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == 1:
                        body_image = self.body_br
                self.display.blit(body_image, block_rect)

    # draw body

    def draw_fruit(self, fruit):
        x = int(fruit.x * CELL_SIZE)
        y = int(fruit.y * CELL_SIZE)
        apple_image = pygame.image.load('apple.png').convert_alpha()
        apple_image = pygame.transform.scale(apple_image, (CELL_SIZE + 10, CELL_SIZE + 10))
        fruit_rect = apple_image.get_rect()
        fruit_rect.topleft = (x, y)
        self.display.blit(apple_image, fruit_rect)

    def draw_obstacles(self, obstacles):
        for obstacle in obstacles:
            x = int(obstacle.x * CELL_SIZE)
            y = int(obstacle.y * CELL_SIZE)
            obstacle_img = pygame.image.load('assets/obstacles.png').convert_alpha()

            # Define the scale factor
            scale_factor = 3  # Change this to adjust the scale

            # Scale the image
            obstacle_img = pygame.transform.scale(obstacle_img, (CELL_SIZE * scale_factor, CELL_SIZE * scale_factor))

            # Calculate the new position based on the scaled size
            new_x = x - (obstacle_img.get_width() - CELL_SIZE) // 2
            new_y = y - (obstacle_img.get_height() - CELL_SIZE) // 2

            obstacle_rect = obstacle_img.get_rect()
            obstacle_rect.topleft = (new_x, new_y)

            self.display.blit(obstacle_img, obstacle_rect)

    def draw_banner(self):
        #
        banner = pygame.image.load('assets/img_6.png')
        banner_rect = banner.get_rect()
        banner_rect.topleft = (BANNER_POS_X, 0)
        banner_rect.width = BANNER_HEIGHT
        banner_rect.height = NO_OF_CELLS_ROW * CELL_SIZE

        self.display.blit(banner, banner_rect)

    def draw_score(self):
        score_text = 'Score: ' + str(self.controller.get_score())
        score_x = self.SIZE_COL - (CELL_SIZE + 2 * len(score_text) + 180)
        score_y = CELL_SIZE * 4
        button_width = 185  # Adjust button width based on text length

        # Draw the button background (filled rectangle)
        pygame.draw.rect(self.window, (255, 255, 255), (score_x, score_y, button_width, 30))

        # Draw the button with score text
        self.draw_button(score_text, 20, score_x, score_y, button_width, 30, WINDOW_COLOR, BTN_COLOR)

    def draw_speed(self):
        if (self.speed == 110):
            score_text = 'Speed: 1x'
        else:
            score_text = 'Speed: 3x'
        score_x = self.SIZE_COL - (CELL_SIZE + 2 * len(score_text) + 180)
        score_y = CELL_SIZE * 6
        # button_width = len(score_text) * 15 + 50  # Adjust button width based on text length
        button_width = 185;
        # Draw the button background (filled rectangle)
        pygame.draw.rect(self.window, (255, 255, 255), (score_x, score_y, button_width, 30))

        # Draw the button with score text
        self.draw_button(score_text, 20, score_x, score_y, button_width, 30, WINDOW_COLOR, BTN_COLOR)

    def draw_button(self, text, size, x, y, width, height, color=WINDOW_COLOR, button_color=(255, 255, 255)):
        pygame.draw.rect(self.display, (0, 0, 0), (x, y, width, height),
                         3)  # The last argument is the border thickness
        font = pygame.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.center = (x + width // 2, y + height // 2)
        self.display.blit(text_surface, text_rect)

    def game_over(self):
        again = False

        while not again:
            for event in pygame.event.get():
                if self.is_quit(event):
                    again = True
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        again = True
                        break
                    if event.key == pygame.K_s:
                        again = True
                        self.controller.save_model()
                        break

            self.display.fill(MENU_COLOR)

            # training model results
            if self.curr_menu.state == 'GA' and self.controller.model_loaded == False:
                best_score = self.controller.best_GA_score()
                best_gen = self.controller.best_GA_gen()

                high_score = f'Best snake Score: {best_score} in generation {best_gen}'
                save = 'Press S to save best snake'

                self.draw_text(
                    save, size=30,
                    x=self.SIZE / 2, y=self.SIZE / 2 + 3 * CELL_SIZE,
                    color=FRUIT_COLOR
                )
            else:
                # Path ai or trained model results
                high_score = f'High Score: {self.controller.get_score()}'

            to_continue = 'Enter to Continue'

            self.draw_text(
                high_score, size=35,
                x=self.SIZE_ROW / 2, y=self.SIZE_COL / 2,
            )

            self.draw_text(
                to_continue, size=30,
                x=self.SIZE_ROW / 2, y=self.SIZE_COL / 2 + 2 * CELL_SIZE,
                color=WHITE
            )

            self.window.blit(self.display, (0, 0))
            pygame.display.update()
        self.controller.reset()

    def is_quit(self, event):
        # user presses exit icon
        if event.type == pygame.QUIT:
            self.running, self.playing = False, False
            self.curr_menu.run_display = False
            return True
        return False

    def is_paused(self):
        while self.paused:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        self.paused = False

    def event_handler(self):
        for event in pygame.event.get():
            print('bye bye')
            if self.is_quit(event):
                print('Bye :)')
                pygame.quit()
                sys.exit()


            # user event that runs every self.speed milisec
            elif self.playing and event.type == pygame.USEREVENT :
                print('the second')


                self.controller.ai_play(self.curr_menu.state)  # play

                if self.controller.end == True:  # Only path ai and trained model
                    self.playing = False
                    self.game_over()  # show game over stats

            elif event.type == pygame.KEYDOWN:

                if event.key == pygame.K_RETURN:  # on Enter
                    pygame.mixer.init()
                    print('2')
                    # Load sound file
                    sound = pygame.mixer.Sound('assets/click.mp3')  # Replace with your sound file

                    # Play the sound
                    sound.play()
                    self.START = True
                    self.view_path = False

                if event.key == pygame.K_q:  # on q return
                    self.BACK = True
                    self.controller.reset()

                elif event.key == pygame.K_SPACE:  # space view path or hide training snakes
                    self.view_path = not self.view_path

                elif event.key == pygame.K_RIGHT:
                    self.RIGHTKEY = True
                elif event.key == pygame.K_LEFT:
                    self.LEFTKEY = True

                elif event.key == pygame.K_w:  # speed up/down by self.speed_up
                    self.speed_up = -1 * self.speed_up
                    self.speed = self.speed + self.speed_up
                    pygame.time.set_timer(self.SCREEN_UPDATE, self.speed)

                elif event.key == pygame.K_p:  # speed up/down by self.speed_up
                    self.paused = True;
                    self.is_paused()

                    # body_rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
                    # print(body_rect)
                    # pygame.draw.rect(self.display, (0, 0, 0), body_rect)
                    # pygame.display.update()

    # RESET KEY THÀNH FALSE ĐỂ KHÔNG BỊ DỊCH CHUYỂN LIÊN TỤC
    def reset_keys(self):
        self.RIGHTKEY, self.LEFTKEY, self.START, self.BACK = False, False, False, False

    def draw_text(self, text, size, x, y, color=WINDOW_COLOR):
        font = pygame.font.Font(self.font_name, size)
        font.set_bold(True)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        self.display.blit(text_surface, text_rect)
