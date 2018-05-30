import json
from functools import reduce
from Page import Page
import xml.etree.ElementTree as ET


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

    def copy(self):
        new_path = Path(self.start)
        for p in self.path[1:]:
            new_path.add(p)

        return new_path

    def print(self):
        print()
        print("Cost = {}".format(self.cost))
        print("Start = {}".format(self.start))
        print("End = {}".format(self.last))
        print("Path[")
        for p in self.path:
            print(p)
        print("]")

    def __str__(self):
        # st = ""
        # for p in self.path:
        #     st += str(p) + "\n"
        # return st
        return self.to_json()

    def to_json(self):
        s = {"start": self.start.to_json(),
             "end": self.last.to_json(),
             "cost": self.cost,
             "path": list(map(lambda x: x.to_json(), self.path))}
        return s

    def to_xml(self):
        pathElem = ET.Element("path")

        startElem = ET.Element("start")
        startElem.append(self.start.to_xml())

        endElem = ET.Element("end")
        endElem.append(self.last.to_xml())

        costElem = ET.Element("cost")
        costElem.text = str(self.cost)

        routeElem = ET.Element("route")
        for page in self.path:
            routeElem.append(page.to_xml())

        pathElem.append(startElem)
        pathElem.append(endElem)
        pathElem.append(costElem)
        pathElem.append(routeElem)

        return pathElem

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
