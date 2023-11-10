from collections import deque
from Utility import Node
from Algorithm import Algorithm
import random

class BFS(Algorithm):
    def __init__(self, grid):
        super().__init__(grid)
        self.explored = []
        self.goalstateCheck = [],
        self.check = True
    def run_algorithm(self,snake):
        # start clean
        self.frontier = deque([])
        self.explored_set = []
        self.path = []
        self.frontier_1 = deque([])
        self.explored_set_1 = []
        # self.path1 = []
        # initialstate1, goalstate1 = self.get_initstate1_and_goalstate1(snake)
        # print(goalstate1)
        initialstate, goalstate = self.get_initstate_and_goalstate(snake)
        # open list

        self.frontier.append(initialstate)

        # while we have states in open list
        while len(self.frontier) > 0:
            # shallowest_node là nút hiện tại
            shallowest_node = self.frontier.popleft()  # FIFO queue
            self.explored_set.append(shallowest_node)

            # get neighbors
            neighbors = self.get_neighbors(shallowest_node)

            # for each neighbor
            for neighbor in neighbors:
                # check if path inside snake, outside boundary or already visited
                if self.inside_body(snake, neighbor) or self.outside_boundary(neighbor) or self.inside_obstacles(snake,neighbor):
                    self.explored_set.append(neighbor)
                    continue  # skip this path

                if neighbor not in self.frontier and neighbor not in self.explored_set:
                    neighbor.parent = shallowest_node  # mark parent
                    self.explored_set.append(neighbor)  # mark visited
                    # add to frontier to explore its kids next cycle
                    self.frontier.append(neighbor)

                    # check if goal state
                    if neighbor.equal(goalstate):
                        # return path
                        # print(self.get_path(neighbor))
                        return self.get_path(neighbor)


        initial_state, tail_state = self.get_initstate_and_tailstate(snake)
        # open list
        self.frontier_1.append(initial_state)

        longest_path = None

        # while we have states in open list
        while len(self.frontier_1) > 0:
            # shallowest_node là nút hiện tại
            shallowest_node = self.frontier_1.popleft()  # FIFO queue
            self.explored_set_1.append(shallowest_node)

            # get neighbors
            neighbors = self.get_neighbors(shallowest_node)

            # for each neighbor
            for neighbor in neighbors:

                if self.inside_body_but_tail(snake, neighbor) or self.outside_boundary(neighbor) or self.inside_obstacles(snake,
                                                                                                                 neighbor):
                    self.explored_set_1.append(neighbor)
                    continue

                if neighbor not in self.frontier_1 and neighbor not in self.explored_set_1:
                    neighbor.parent = shallowest_node
                    self.explored_set_1.append(neighbor)

                    self.frontier_1.append(neighbor)


                    if neighbor.equal(tail_state):
                        current_path = self.get_path(neighbor)
                        if longest_path is None or len(current_path) > len(longest_path):
                            longest_path = current_path
        print(longest_path)
        return longest_path

