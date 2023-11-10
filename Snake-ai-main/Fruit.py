import pygame
from pygame.math import Vector2
from Constants import *
import random

random.seed(USER_SEED)


import time

class Fruit:
    def __init__(self):
        self.position = Vector2(0, 0)
        self.reset_seed()

    def generate_fruit(self):

        # SỐ LƯỢNG CỘT LÀ THEO CHIỀU NGANG TƯƠNG ỨNG VỚI X
        x = random.randrange(1, BANNER_POS_X/CELL_SIZE - 1)
        # SỐ LƯỢNG HÀNG LÀ THEO CHIỀU DỌC TƯƠNG ỨNG VỚI Y
        y = random.randrange(1, NO_OF_CELLS_ROW-1)

        self.position = Vector2(x, y)


    def reset_seed(self):
        seed = int(time.time())  # Use current time as seed
        random.seed(seed)
        self.generate_fruit()




