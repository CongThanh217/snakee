from pygame import Vector2

from Snake import Snake
from Constants import NO_OF_CELLS_COL, NO_OF_CELLS_ROW, BANNER_HEIGHT, CELL_SIZE
from Utility import Grid
from DFS import DFS
from BFS import BFS
from A_STAR import A_STAR
# from Greedy import Greedy
from GA import *
import pygame

class GameController:


    def __init__(self):
        self.snake = None
        self.snakes = []
        self.score = 0
        self.end = False
        self.grid = Grid().grid
        self.algo = None
        self.model_loaded = False
        self.player = None
        self.is_set_play = True

    def reset(self):
        self.end = False
        if self.snake:
            self.snake.reset()
            self.snake = None

        self.algo = None
        self.snakes = []
        self.model_loaded = False

    def best_GA_score(self):
        return self.algo.best_score

    def best_GA_gen(self):
        return self.algo.best_gen

    def curr_gen(self):
        return self.algo.generation

    def save_model(self):
        best_snake = self.algo.best_snake
        network = best_snake.network
        best_snake.save_model(network, 'saved_model')

    def load_model(self):
        self.snake = Snake()
        self.snake.load_model('saved_model')
        self.model_loaded = True

    def get_score(self):
        if self.snake:
            return self.snake.score
        else:
            return 0

    def ate_fruit(self):
        if self.snake.ate_fruit():
            sound = pygame.mixer.Sound('assets/eating.mp3')  # Replace with your sound file

            # Play the sound
            sound.play()

            # Delay to allow sound to play (optional)
            self.randomFruit = random.randint(0,1)
            self.snake.add_body_ai()
            self.change_fruit_location()


    def change_fruit_location(self):
        while True:
            self.snake.create_fruit()
            fruit_pos = self.snake.get_fruit()
            inside_body = False
            for body in self.snake.body:
                if fruit_pos == body:
                    inside_body = True
            # Kiem tra fruit co random trung voi obstacle khong
            check = True
            for obstacle in self.snake.get_obstacles():
                x = obstacle.x
                y = obstacle.y
                x = int(x)
                y = int(y)
                obstacle_points = [ (x, y - 1),  # Điểm trên cạnh trên
                                    (x + 1, y),  # Điểm trên cạnh phải
                                    (x, y + 1),  # Điểm trên cạnh dưới
                                    (x - 1, y),  # Điểm trên cạnh trái
                                    (x + 1, y - 1),  # Điểm giữa trên
                                    (x + 1, y + 1),  # Điểm giữa phải
                                    (x - 1, y + 1),  # Điểm giữa dưới
                                    (x - 1, y - 1),  # Điểm giữa trái
                                    (x, y) ] # Điểm giữa]
                if(fruit_pos in obstacle_points):
                    check = False
            if check and not inside_body:
                break

    def ate_fruit_GA(self, snake):
        if snake.ate_fruit():
            snake.add_body_ai()
            self.change_fruit_location_GA(snake)

    def change_fruit_location_GA(self, snake):
        while True:
            snake.create_fruit()
            position = snake.get_fruit()
            inside_body = False
            for body in snake.body:
                if position == body:
                    inside_body = True

            if inside_body == False:
                break

    def died(self):
        current_x = self.snake.body[0].x
        current_y = self.snake.body[0].y

        if not 0 <= current_x < NO_OF_CELLS_COL-10:
            self.end = True
        elif not 0 <= current_y < NO_OF_CELLS_ROW:
            self.end = True
        elif self.snake.ate_body():
            self.end = True
        elif self.snake.ate_obstacles(self.snake.body[0]):
            self.end = True

    def get_fruit_pos(self):
        return self.snake.get_fruit()

    def get_obstacles_pos(self):
        return self.snake.get_obstacles()

    def set_player(self, player_type):

        if player_type == 'PLAYER':
            self.player = BFS(self.grid)
            self.snake = Snake()

        elif player_type == 'BOT':
            self.player = DFS(self.grid)
            self.snake = Snake()

        elif player_type == 'BATTLE':
            self.player = A_STAR(self.grid)
            self.snake = Snake()


    def set_algorithm(self, algo_type):
        if self.algo != None:
            return

        if algo_type == 'BFS':
            self.algo = BFS(self.grid)
            self.snake = Snake()

        elif algo_type == 'DFS':
            self.algo = DFS(self.grid)
            self.snake = Snake()

        elif algo_type == 'ASTAR':
            self.algo = A_STAR(self.grid)
            self.snake = Snake()

        elif algo_type == 'GA':
            self.algo = GA(self.grid)


    def player_play(self):
        if(self.is_set_play):
            self.snake = Snake()
            self.is_set_play = False
        else:
            return
    def ai_play(self, algorithm):
        self.set_algorithm(algorithm)

        if self.algo == None:
            return

        if isinstance(self.algo, GA):
            self.update_GA_ai()
        else:
            pos = self.algo.run_algorithm(self.snake)
            self.update_path_finding_algo(pos)


    def keep_moving(self):
        x = self.snake.body[0].x
        y = self.snake.body[0].y
        print(x,y)
        if self.snake.body[1].x == x:
            if self.snake.body[1].y < y:
                # keep going down
                y = y + 1
            else:
                # keep going up
                y = y - 1
        elif self.snake.body[1].y == y:
            if self.snake.body[1].x < x:
                # keep going right
                x = x + 1
            else:
                # keep going left
                x = x - 1
        return x, y

    def update_GA_ai(self):
        if not self.snake and not self.model_loaded:
            if self.algo.done():
                if self.algo.next_generation():
                    self.snakes = self.algo.population.snakes
                else:
                    self.end = True

            for snake in self.snakes:
                x, y = self.algo.run_algorithm(snake)

                snake.move_ai(x, y)
                self.algo.died(snake)
                self.ate_fruit_GA(snake)
        else:
            x, y = self.algo.run_algorithm(self.snake)
            self.snake.move_ai(x, y)
            self.died()
            self.ate_fruit()

    def vector_to_node(self, vector):
        x, y = int(vector.x), int(vector.y)
        return self.grid[x][y]
    def any_possible_move(self):
        head_pos_x = self.snake.get_x()
        head_pos_y = self.snake.get_y()
        print(head_pos_x,head_pos_y)
        if(not head_pos_x+1 == NO_OF_CELLS_COL):
            right = self.vector_to_node(Vector2(head_pos_x + 1, head_pos_y))
            if (not self.algo.inside_body(self.snake, right) and not self.algo.outside_boundary(
                    right) and not self.algo.inside_obstacles(self.snake, right)):
                print('right')
                return head_pos_x + 1, head_pos_y
        if (not head_pos_y + 1 == NO_OF_CELLS_ROW):
            up = self.vector_to_node(Vector2(head_pos_x, head_pos_y + 1))
            if (not self.algo.inside_body(self.snake, up) and not self.algo.outside_boundary(
                    up) and not self.algo.inside_obstacles(self.snake, up)):
                print('DOWN')
                return head_pos_x, head_pos_y + 1
        if (not head_pos_y - 1 == 0):
            down = self.vector_to_node(Vector2(head_pos_x, head_pos_y - 1))
            if (not self.algo.inside_body(self.snake, down) and not self.algo.outside_boundary(
                    down) and not self.algo.inside_obstacles(self.snake, down)):
                print('UP')
                return head_pos_x, head_pos_y - 1
        if (not head_pos_x - 1 == 0):
            left = self.vector_to_node(Vector2(head_pos_x - 1, head_pos_y))
            if (not self.algo.inside_body(self.snake, left) and not self.algo.outside_boundary(
                    left) and not self.algo.inside_obstacles(self.snake, left)):
                print('left')
                return head_pos_x - 1, head_pos_y



        x = self.snake.body[0].x
        y = self.snake.body[0].y

        if self.snake.body[1].x == x:
            if self.snake.body[1].y < y:
                # keep going down
                y = y + 1
            else:
                # keep going up
                y = y - 1
        elif self.snake.body[1].y == y:
            if self.snake.body[1].x < x:
                # keep going right
                x = x + 1
            else:
                # keep going left
                x = x - 1
        return x, y
    def update_path_finding_algo(self, pos):
        if pos == None:
            x, y = self.any_possible_move()
            print(f"test {x} {y}")
        else:
            x = pos.x
            y = pos.y
        self.snake.move_ai(x, y)
        self.died()
        self.ate_fruit()
