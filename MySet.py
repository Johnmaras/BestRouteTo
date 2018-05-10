class MySet(set):
    def __init__(self):
        self.paths = list()
        self.visited = list()
        self.min = None
        super().__init__()

    def add(self, path):
        found = False
        # for each of the paths we have so far discovered(visited or not)
        for p in self.paths:
            # if the path's starting and ending nodes coincide with p's ones
            if path == p:
                # if path is cheapest than p -> add it
                if path < p:
                    self.paths.remove(p)
                    self.paths.append(path)
                    return
                else:
                    found = True
                    break

        # if path's and p's starting and ending nodes do not coincide with p's -> add it
        if not(found):
            self.paths.append(path)

    def pop(self):
        # the last node of the path we are about to pop is now considered visited
        self.visited.append(self.min.last)

        # return the next unvisited cheapest path
        return self.min

    def set_min(self):
        # get the unvisited paths
        not_visited_paths = list(filter(lambda x: not(x.last in self.visited), self.paths))
        if not not_visited_paths:
            return

        # find the cheapest of them
        self.min = min(not_visited_paths)

    def has_next(self):
        # get the last nodes of all paths in our path list
        last_nodes = set(map(lambda x: x.last, self.paths))

        # check if the last_nodes set is a subset of the visited set
        diff = last_nodes.difference(set(self.visited))

        # if it is then there are no more unvisited paths
        return not(diff.__len__() == 0)

    def print(self):
        print()
        print("Min = {}".format(self.min))
        print("Paths{")
        for p in self.paths:
            print(p)
        print("}")

        print("Visited{")
        for p in self.visited:
            print(p)
        print("}")
