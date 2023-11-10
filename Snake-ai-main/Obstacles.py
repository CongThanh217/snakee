import pygame
from pygame.math import Vector2
from Constants import *
import random

random.seed(USER_SEED)

import time


class Obtacles:
    def __init__(self):
        self.position = []
        self.reset_obstacles()

    def generate_obstacles(self):
        num_of_obstacles = 10

        for i in range(num_of_obstacles):
            # SỐ LƯỢNG CỘT LÀ THEO CHIỀU NGANG TƯƠNG ỨNG VỚI X
            x = random.randrange(1, BANNER_POS_X / CELL_SIZE - 1)
            # SỐ LƯỢNG HÀNG LÀ THEO CHIỀU DỌC TƯƠNG ỨNG VỚI Y
            y = random.randrange(1, NO_OF_CELLS_ROW - 1)
            self.position.append(Vector2(x, y))

    def reset_obstacles(self):
        random.seed()  # Đặt seed mặc định (tự động sử dụng một seed mới)
        self.position = []  # Reset danh sách chướng ngại vật
        self.generate_obstacles()
