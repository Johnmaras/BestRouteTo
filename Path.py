class Path:

    def __init__(self, starting_page):
        self.start = starting_page
        self.path = [self.start]
        self.last = self.path[-1]

    def add(self, page):
        self.path.append(page)
        self.last = page

    def size(self):
        return self.path.__len__()

    def is_better_than(self, path):
        if (self.start != path.start) or (self.last != path.last):
            return False

        return self.size() > path.size()
