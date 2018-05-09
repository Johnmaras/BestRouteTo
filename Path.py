from functools import reduce
from Page import Page


class Path:

    def __init__(self, starting_page: Page):
        self.cost = 0
        self.start = starting_page
        self.path = []
        self.last = None
        self.add(self.start)

    def add(self, page: Page):
        self.path.append(page)
        self.last = page
        self.calc_cost()

    def calc_cost(self):
        self.cost += self.last.weight

    def __str__(self):
        st = "Start = ({start}), End = ({end}), Cost = {cost}"\
            .format(start=self.start, end=self.last, cost=self.cost)

        st += ", Intermediate Nodes = {}".format(self.path[1:-1])
        return st

    def __hash__(self, *args, **kwargs):
        return super().__hash__(*args, **kwargs)

    def __eq__(self, other):
        return self.start == other.start and self.last == other.last

    def __gt__(self, other):
        return self.cost > other.cost

    def __lt__(self, other):
        return self.cost < other.cost

    def __ge__(self, other):
        return self.cost >= other.cost

    def __le__(self, other):
        return self.cost <= other.cost

    def __cmp__(self, other):
        if self > other:
            return 1
        elif self < other:
            return -1
        else:
            return 0

    def copy(self):
        new_path = Path(self.start)
        for p in self.path[1:]:
            new_path.add(p)

        return new_path
