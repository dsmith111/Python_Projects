import matplotlib.pyplot as plt
import copy


class DFS():

    def __init__(self, graph, starting_loc=None):
        self.map = graph
        self.starting_loc = starting_loc
        self.current_loc = starting_loc
        self.found_target = False
        self.target_loc = None
        self.shape = (len(graph), len(graph[0]))
        self.fig = None
        self.ax = None

    def start_map(self):
        self.fig = plt.figure()
        self.ax = self.fig.gca()
        self.fig.show()

    def show_map(self):
        plt.imshow(self.map)
        self.fig.canvas.draw()
        plt.pause(0.00000001)

    def search_children(self, loc=None):
        r, c = loc or self.starting_loc
        self.current_loc = (r, c)
        self.map[r][c] = 3
        self.show_map()
        r_dif = -1
        c_dif = -1

        while (not self.found_target and r_dif < 2):

            while(c_dif < 2):

                if (abs(c_dif) + abs(r_dif) == 2):
                    c_dif += 1
                    continue

                new_r = abs(r + r_dif)
                new_c = abs(c + c_dif)

                if (new_r < self.shape[0] and new_c < self.shape[1]):

                    if (self.map[new_r][new_c] == 2):
                        self.found_target = True
                        self.target_loc = (new_r, new_c)
                        break

                    if (self.map[new_r][new_c] == 0):
                        self.search_children((new_r, new_c))

                c_dif += 1
            r_dif += 1
            c_dif = -1


class BFS():

    def __init__(self, graph, starting_loc=None):
        self.map = graph
        self.starting_loc = starting_loc
        self.current_loc = starting_loc
        self.found_target = False
        self.target_loc = None
        self.shape = (len(graph), len(graph[0]))
        self.search_queue = []
        self.fig = None
        self.ax = None

    def start_map(self):
        self.fig = plt.figure()
        self.ax = self.fig.gca()
        self.fig.show()

    def show_map(self):
        plt.imshow(self.map)
        self.fig.canvas.draw()
        plt.pause(0.00000001)

    def push_queue(self, item):
        self.search_queue.append(item)

    def pull_queue(self):
        return self.search_queue.pop(0)

    def search_children(self, loc=None):
        r, c = loc or self.starting_loc
        self.current_loc = (r, c)
        self.map[r][c] = 3
        self.show_map()
        r_dif = -1
        c_dif = -1

        while (not self.found_target and r_dif < 2):

            while(c_dif < 2):

                if (abs(c_dif) + abs(r_dif) == 2):
                    c_dif += 1
                    continue

                new_r = abs(r + r_dif)
                new_c = abs(c + c_dif)

                if (new_r < self.shape[0] and new_c < self.shape[1]):

                    if (self.map[new_r][new_c] == 2):
                        self.found_target = True
                        self.target_loc = (new_r, new_c)
                        break

                    if (self.map[new_r][new_c] == 0 and (new_r, new_c) not in self.search_queue):
                        self.push_queue((new_r, new_c))

                c_dif += 1
            r_dif += 1
            c_dif = -1

        next_child = self.pull_queue()
        if (next_child != None):
            self.search_children(next_child)


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
