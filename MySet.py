class MySet(set):
    def __init__(self):
        self.paths = list()
        self.visited = list()
        self.min = None
        super().__init__()

    def add(self, path):
        self.paths.append(path)

        if self.min is None:
            self.min = path
            return

        if not(path.last in self.visited):
            if path.cost < self.min.cost:
                self.min = path

    def pop(self):
        self.visited.append(self.min.last)
        return self.min

    def sort(self):
        not_visited_paths = list(filter(lambda x: not(x.last in self.visited), self.paths))
        self.min = min(not_visited_paths, key=(lambda x, y: x.cost < y.cost))

    def has_next(self):

    # TODO iterating through MySet needs improvement