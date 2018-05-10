from bs4 import BeautifulSoup
import requests
from threading import Thread
from Path import Path
from Page import Page
from MySet import MySet
from urllib import parse

# base_url = "http://www.aueb.gr"
base_url = "http://127.0.0.1:3117"
first_page = "a.html"

# NOTE program output(under consideration): tree of all best routes to final pages(more outputs to be added)
# NOTE                                      dead links, and (probably) all of their routes

# TODO create an xml(or something) file that prettily presents the best route tree

# NOTE The program must decide which route to choose to go with(namely which link to request next from each page)
# NOTE                    ^partially done
# NOTE despite the fact that in the end it will scan every possible route

# TODO create a heuristic(or something) function that determines why a route is preferable over another.
# TODO It will possibly be used the location(internal/external) of the page. More to be added for a better discrimination


def create_pages(urls):
    pages = []
    for url in urls:
        pages.append(Page(url, base_url))
    return pages


collection = MySet()
aPage = Page(first_page, base_url)
path = Path(aPage)

collection.add(path)
collection.set_min()

while collection.has_next():
    path = collection.pop()
    node = path.last

    raw_neighbors = create_pages(node.links)
    neighbors = list(filter(lambda x: not(x in collection.visited), raw_neighbors))
    for n in neighbors:
        new_path = path.copy()
        new_path.add(n)
        collection.add(new_path)
    collection.set_min()

for p in collection.paths:
    print("Best route to\n{ln}\nis\n{path}\n".format(ln=p.last, path=p))
