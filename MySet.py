class MySet(set):
    def __init__(self):
        self.paths = list()
        self.visited = list()
        self.min = None
        super().__init__()

    def add(self, path):
        flag = False
        for p in self.paths:
            if path == p:
                if path < p:
                    self.paths.remove(p)
                    self.paths.append(path)
                    flag = True
                    break
                else:
                    flag = True
                    break

        if not(flag):
            self.paths.append(path)

        if self.min is None:
            self.min = path
            return

        if self.min.last in self.visited:
            self.min = path
        else:
            if not(path.last in self.visited):
                if path.cost < self.min.cost:
                    self.min = path

    def pop(self):
        self.visited.append(self.min.last)
        return self.min

    # def sort(self):
    #     not_visited_paths = list(filter(lambda x: not(x.last in self.visited), self.paths))
    #     self.min = min(not_visited_paths, key=(lambda x, y: x.cost < y.cost))

    def has_next(self):
        last_nodes = set(map(lambda x: x.last, self.paths))
        diff = last_nodes.difference(set(self.visited))
        return not(diff.__len__() == 0)
