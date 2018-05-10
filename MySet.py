class MySet(set):
    def __init__(self):
        self.paths = list()
        self.visited = list()
        self.min = None
        super().__init__()

    def add(self, path):
        found = False
        for p in self.paths:
            if path == p:
                if path < p:
                    self.paths.remove(p)
                    self.paths.append(path)
                    return
                else:
                    found = True
                    break

        if not(found):
            self.paths.append(path)

    def pop(self):
        self.visited.append(self.min.last)
        return self.min

    def set_min(self):
        not_visited_paths = list(filter(lambda x: not(x.last in self.visited), self.paths))
        if not not_visited_paths:
            return
        self.min = min(not_visited_paths)

    def has_next(self):
        last_nodes = set(map(lambda x: x.last, self.paths))
        diff = last_nodes.difference(set(self.visited))
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
