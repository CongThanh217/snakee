from pygame.math import Vector2
from Fruit import Fruit
from Obstacles import Obtacles
from NN import NeuralNework
import pickle
from Constants import CELL_SIZE


class Snake_main:
    def __init__(self, hidden=8):
        self.Obstacles = Obtacles()
        self.body = [Vector2(5, 8), Vector2(4, 8), Vector2(3, 8)]
        self.fruit = Fruit()
        self.Obstacles = Obtacles()
        self.score = 0
        self.fitness = 0
        self.life_time = 0
        self.steps = 0
        self.hidden = hidden

    def reset(self):
        self.body = [Vector2(5, 8), Vector2(4, 8), Vector2(3, 8)]
        self.fruit.reset_seed()

        self.score = 0
        self.fitness = 0
        self.steps = 0

    def get_x(self):
        return self.body[0].x

    def get_y(self):
        return self.body[0].y

    def get_tail_x(self):
        return self.body[-1].x

    def get_tail_y(self):
        return self.body[-1].y

    def get_tail(self):
        return self.body[-1]

    def get_fruit(self):
        while True:
            check = True
            for pos in self.Obstacles.position:
                a = int(pos.x)
                b = int(pos.y)
                # Trường hợp 1
                if self.fruit.position.x == a and self.fruit.position.y == b:
                    check = False
                    break

                # Trường hợp 2
                if self.fruit.position.x == a + 1 and self.fruit.position.y == b:
                    check = False
                    break

                # Trường hợp 3
                if self.fruit.position.x == a - 1 and self.fruit.position.y == b:
                    check = False
                    break

                # Trường hợp 4
                if self.fruit.position.x == a and self.fruit.position.y == b - 1:
                    check = False
                    break

                # Trường hợp 5
                if self.fruit.position.x == a + 1 and self.fruit.position.y == b - 1:
                    check = False
                    break

                # Trường hợp 6
                if self.fruit.position.x == a - 1 and self.fruit.position.y == b - 1:
                    check = False
                    break

                # Trường hợp 7
                if self.fruit.position.x == a - 1 and self.fruit.position.y == b + 1:
                    check = False
                    break

                # Trường hợp 8
                if self.fruit.position.x == a and self.fruit.position.y == b + 1:
                    check = False
                    break

                # Trường hợp 9
                if self.fruit.position.x == a + 1 and self.fruit.position.y == b + 1:
                    check = False
                    break

            if check:
                break
            else:
                self.fruit.reset_seed()
        return self.fruit.position

    def get_obstacles(self):
        while True:
            check = True
            for i in self.Obstacles.position:
                if i == self.fruit.position:
                    check = False
                for body in self.body[1:]:
                    if i == body:
                        check = False
            if check:
                break
            else:
                self.Obstacles.reset_obstacles()
        return self.Obstacles.position

    def ate_fruit(self):
        if self.fruit.position == self.body[0]:
            self.score += 1
            self.life_time -= 40
            return True
        return False

    def ate_obstacles(self, body):
        for pos in self.Obstacles.position:
            a = pos.x
            b = pos.y
            a = int(a)
            b = int(b)

            obstacle_points = [(a, b), (a + 1, b), (a - 1, b), (a, b - 1),
                               (a + 1, b - 1), (a - 1, b - 1),
                               (a - 1, b + 1), (a, b + 1), (a + 1, b + 1)]

            if body in obstacle_points:
                print('die' + str(self.body[0]))

                return True

        return False

    def create_fruit(self):
        self.fruit.generate_fruit()

    def move_ai(self, x, y):
        self.life_time += 1
        self.steps += 1
        for i in range(len(self.body) - 1, 0, -1):
            self.body[i].x = self.body[i - 1].x
            self.body[i].y = self.body[i - 1].y

        self.body[0].x = x
        self.body[0].y = y

    def add_body_ai(self):
        last_index = len(self.body) - 1
        tail = self.body[-1]
        before_last = self.body[-2]

        if tail.x == before_last.x:
            if tail.y < before_last.y:
                self.body.append(Vector2(tail.x, tail.y - 1))
            else:
                self.body.append(Vector2(tail.x, tail.y + 1))
        elif tail.y == before_last.y:
            if tail.x < before_last.x:
                self.body.append(Vector2(tail.x - 1, tail.y))
            else:
                self.body.append(Vector2(tail.x + 1, tail.y))

    def ate_body(self):
        for body in self.body[1:]:
            if self.body[0] == body:
                return True
        return False
