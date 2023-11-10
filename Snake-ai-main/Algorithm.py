from abc import ABC, abstractmethod
from Constants import NO_OF_CELLS_ROW, NO_OF_CELLS_COL, BANNER_HEIGHT
from Utility import Node
import math


class Algorithm(ABC):

    def __init__(self, grid):
        self.grid = grid
        self.frontier = []
        self.explored_set = []
        self.path = []


    def get_initstate_and_goalstate(self, snake):
        return Node(snake.get_x(), snake.get_y()), Node(snake.get_fruit().x, snake.get_fruit().y)

    def get_initstate_and_tailstate(self, snake):
        return Node(snake.get_x(), snake.get_y()), Node(snake.get_tail_x(), snake.get_tail_y())

    def inside_body_but_tail(self, snake, node):
        for body in snake.body:
            if body.x == node.x and body.y == node.y:
                if body.x == snake.body[-1].x and body.y == snake.body[-1].y:
                    return False
                return True

    def manhattan_distance(self, nodeA, nodeB):
        distance_1 = abs(nodeA.x - nodeB.x)
        distance_2 = abs(nodeA.y - nodeB.y)
        return distance_1 + distance_2

    def euclidean_distance(self, nodeA, nodeB):
        distance_1 = nodeA.x - nodeB.x
        distance_2 = nodeA.y - nodeB.y
        return math.sqrt(distance_1**2 + distance_2**2)

    @abstractmethod
    def run_algorithm(self, snake):
        pass

    def get_path(self, node):
        if node.parent == None:
            return node

        while node.parent.parent != None:
            self.path.append(node)
            node = node.parent
        return node

    def inside_body(self, snake, node):
        for body in snake.body:
            if body.x == node.x and body.y == node.y:
                return True
        return False

    def inside_obstacles(self, snake, node):
        for pos in snake.Obstacles.position:

            a = int(pos.x)
            b = int(pos.y)

            # Trường hợp 1
            if node.x == a and node.y == b:
                return True

            # Trường hợp 2
            if node.x == a + 1 and node.y == b:
                return True

            # Trường hợp 3
            if node.x == a - 1 and node.y == b:
                return True

            # Trường hợp 4
            if node.x == a and node.y == b - 1:
                return True

            # Trường hợp 5
            if node.x == a + 1 and node.y == b - 1:
                return True

            # Trường hợp 6
            if node.x == a - 1 and node.y == b - 1:
                return True

            # Trường hợp 7
            if node.x == a - 1 and node.y == b + 1:
                return True

            # Trường hợp 8
            if node.x == a and node.y == b + 1:
                return True

            # Trường hợp 9
            if node.x == a + 1 and node.y == b + 1:
                return True


            # Nếu không thuộc bất kỳ trường hợp nào
        return False

    def outside_boundary(self, node):
        if not 0 <= node.x < (NO_OF_CELLS_COL-10):
            return True
        elif not 0 <= node.y < NO_OF_CELLS_ROW:
            return True
        return False



    def get_neighbors(self, node):
        i = int(node.x)
        j = int(node.y)

        neighbors = []
        # left [i-1, j]
        if i > 0:
            neighbors.append(self.grid[i-1][j])
        # right [i+1, j]
        if i < NO_OF_CELLS_COL - 1:
            neighbors.append(self.grid[i+1][j])
        # top [i, j-1]
        if j > 0:
            neighbors.append(self.grid[i][j-1])

        # bottom [i, j+1]
        if j < NO_OF_CELLS_ROW - 1:
            neighbors.append(self.grid[i][j+1])

        return neighbors
