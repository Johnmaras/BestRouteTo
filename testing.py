import collections


class MyList(collections.Iterable):
    def __init__(self):
        self.l = []

    def __iter__(self):
        return (x for x in self.l)

    def add(self, other):
        for n in other:
            self.l.append(n)

    def __next__(self):
        return max(self.l)


my_list = MyList()
my_list.add([1, 4, 3, 14, 23, 46, 37, 95, 2, 118])

for n in my_list:
    print(n)
