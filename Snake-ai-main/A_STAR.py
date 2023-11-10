from Algorithm import Algorithm


class A_STAR(Algorithm):
    def __init__(self, grid):
        super().__init__(grid)

    def run_algorithm(self, snake):
        # clear everything
        self.frontier = []
        self.explored_set = []
        self.path = []
        self.explored = []

        initialstate, goalstate = self.get_initstate_and_goalstate(snake)

        # open list
        self.frontier.append(initialstate)

        # while we have states in open list
        while len(self.frontier) > 0:
            # get node with lowest h(n) (heuristic)
            lowest_index = 0
            print(len(self.frontier))
            for i in range(len(self.frontier)):
                if self.frontier[i].h < self.frontier[lowest_index].h:
                    lowest_index = i
                    vi_tri = i
                    # print(lowest_index)

            lowest_node = self.frontier.pop(lowest_index)
            # check if its goal state
            if lowest_node.equal(goalstate):
                return self.get_path(lowest_node)

            self.explored_set.append(lowest_node)  # mark visited
            neighbors = self.get_neighbors(lowest_node)  # get neighbors

            # for each neighbor
            for neighbor in neighbors:
                print('tesft')
                # check if path inside snake, outside boundary or already visited
                if self.inside_body(snake, neighbor) or self.outside_boundary(
                        neighbor) or neighbor in self.explored_set or self.inside_obstacles(snake, neighbor):
                    continue  # skip this path

                if neighbor not in self.frontier:
                    neighbor.h = self.manhattan_distance(goalstate, neighbor)
                    self.frontier.append(neighbor)
                    neighbor.parent = lowest_node

        return None
