import matplotlib.pyplot as plt
import copy


class DFS():

    directions = [(0, 1), (-1, 0), (0, -1), (1, 0)]
    map_items = {
        "obstacle": 1,
        "treasure": 5,
        "history": 2,
        "best_path": 20
    }
    count = 0
    skips = 1

    def __init__(self, graph, starting_loc=None):
        self.map = graph
        self.current_loc = starting_loc
        self.history = {str(starting_loc): (None, 0)}
        self.best_path = []
        self.found_target = False
        self.target_loc = None
        self.shape = (len(graph), len(graph[0]))
        self.search_stack = [(*starting_loc, 0)]
        self.fig = None
        self.ax = None
        self.im = None

    def start_map(self):
        self.fig, self.ax = plt.subplots()
        self.im = self.ax.imshow(self.map)
        self.fig.show()

    def show_map(self):
        self.im.set_data(self.map)
        self.fig.canvas.draw()

    def push_stack(self, item):
        self.search_stack.append(item)

    def pull_stack(self):
        if(len(self.search_stack)):
            return self.search_stack.pop()

    def back_track(self):

        if (self.history[str(self.current_loc)][0] != None):
            self.map[self.current_loc[0]][self.current_loc[1]
                                          ] = self.map_items["best_path"]
            self.current_loc = self.history[str(self.current_loc)][0]
            self.best_path.insert(0, self.current_loc)
            self.show_map()
            self.back_track()
        else:
            self.search_stack.clear()

    def search_children(self):

        while(len(self.search_stack)):
            self.count += 1
            r, c, current_step = self.pull_stack()
            self.current_loc = (r, c)

            if (self.map[r][c] == self.map_items["treasure"]):
                self.found_target = True
                self.target_loc = ((r, c), current_step)
                self.back_track()
                break

            self.map[r][c] = self.map_items["history"]
            if(self.count % self.skips == 0):
                self.show_map()

            for direction in self.directions:
                new_r, new_c = [abs(sum(pair))
                                for pair in zip(self.current_loc, direction)]

                if (new_r < self.shape[0] and new_c < self.shape[1]):

                    if (self.map[new_r][new_c] not in [self.map_items["history"], self.map_items["obstacle"]] and (new_r, new_c) not in self.search_stack):
                        self.push_stack((new_r, new_c, current_step + 1))
                        string_hist = str((new_r, new_c))

                        if (self.history.get(string_hist, False)):
                            if (self.history[string_hist][1] > current_step):
                                self.history[string_hist] = (
                                    (r, c), current_step)
                        else:
                            self.history[string_hist] = ((r, c), current_step)


class BFS():

    directions = [(0, 1), (-1, 0), (0, -1), (1, 0)]
    map_items = {
        "obstacle": 1,
        "treasure": 5,
        "history": 2,
        "best_path": 20
    }
    count = 0
    skips = 400

    def __init__(self, graph, starting_loc=None):
        self.map = graph
        self.current_loc = starting_loc
        self.history = {str(starting_loc): (None, 0)}
        self.best_path = []
        self.found_target = False
        self.target_loc = None
        self.shape = (len(graph), len(graph[0]))
        self.search_queue = [(*starting_loc, 0)]
        self.fig = None
        self.ax = None
        self.im = None

    def start_map(self):
        self.fig, self.ax = plt.subplots()
        self.im = self.ax.imshow(self.map)
        self.fig.show()

    def show_map(self):
        self.im.set_data(self.map)
        self.fig.canvas.draw()

    def push_queue(self, item):
        self.search_queue.append(item)

    def pull_queue(self):
        if(len(self.search_queue)):
            return self.search_queue.pop(0)

    def back_track(self):

        if (self.history[str(self.current_loc)][0] != None):
            self.map[self.current_loc[0]][self.current_loc[1]
                                          ] = self.map_items["best_path"]
            self.current_loc = self.history[str(self.current_loc)][0]
            self.best_path.insert(0, self.current_loc)
            self.show_map()
            self.back_track()
        else:
            self.search_queue.clear()

    def search_children(self):

        while(len(self.search_queue)):
            self.count += 1
            r, c, current_step = self.pull_queue()
            self.current_loc = (r, c)

            if (self.map[r][c] == self.map_items["treasure"]):
                self.found_target = True
                self.target_loc = ((r, c), current_step)
                self.back_track()
                break

            self.map[r][c] = self.map_items["history"]
            if(self.count % self.skips == 0):
                self.show_map()

            for direction in self.directions:
                new_r, new_c = [abs(sum(pair))
                                for pair in zip(self.current_loc, direction)]

                if (new_r < self.shape[0] and new_c < self.shape[1]):

                    if (self.map[new_r][new_c] not in [self.map_items["history"], self.map_items["obstacle"]] and (new_r, new_c) not in self.search_queue):
                        self.push_queue((new_r, new_c, current_step + 1))
                        string_hist = str((new_r, new_c))

                        if (self.history.get(string_hist, False)):
                            if (self.history[string_hist][1] > current_step):
                                self.history[string_hist] = (
                                    (r, c), current_step)
                        else:
                            self.history[string_hist] = ((r, c), current_step)


def prep_graph():
    # Prepare Graph

    def split_chars(string):
        return [eval(char) for char in string]

    with open("maze.txt", "r") as maze_file:
        graph_strings = maze_file.read().split("\n")
        maze_file.close()

    return [split_chars(row) for row in graph_strings]


if __name__ == "__main__":
    choice = input("bfs or dfs\n")
    graph_list = prep_graph()

    if (choice.lower() == "bfs"):
        searcher = BFS(copy.deepcopy(graph_list), (0, 0))

    elif (choice.lower() == "dfs"):
        searcher = DFS(copy.deepcopy(graph_list), (0, 0))

    searcher.start_map()
    searcher.search_children()
    print("Current location: ", searcher.current_loc)
    print("Found target: ", searcher.found_target)
    print("Target location: ", searcher.target_loc)
    print("Best Path: \n{}".format(searcher.best_path))
    input("Press Enter to Continue.")
