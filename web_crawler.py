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


# def create_path(url, path):
#     # visited.add(url)
#     url_contents = requests.get(url).text
#
#     soup = BeautifulSoup(url_contents, "html.parser")
#
#     a_tags = soup.find_all("a")
#
#     page_links = list(filter(lambda x: is_valid_link(x), map(lambda x: x["href"], a_tags)))
#
#     pages = create_pages(page_links)
#     pages.sort()
#
#     path.add(url)
#     for page in pages:
#         page_url = page.url
#         if not(page_url in visited):
#             create_path(page_url, path)
#             path.add(page_url)
#             paths.append(path)
#         else:
#             paths.append(path)
#             # visited.add(page.url)


# url_contents = requests.get(first_page).text
# paths = set()
# visited = set()

collection = MySet()
aPage = Page(first_page, base_url)
path = Path(aPage)
collection.add(path)

# soup = BeautifulSoup(url_contents, "html.parser")

# a_tags = soup.find_all("a")
# page_links = list(filter(lambda x: is_valid_link(x), map(lambda x: x["href"], a_tags)))

# neighbors = create_pages(page_links)

# TODO the paths set must delete Path objects that are more costly than others
# TODO path must be the min_cost, not_visited one
while collection.has_next():
    path = collection.pop()
# for path in collection.paths:
    node = path.last
    # visited.add(node)  It is done inside the MySet class

    # DONE get only the not_visited ones
    raw_neighbors = create_pages(node.links)
    neighbors = list(filter(lambda x: not(x in collection.visited), raw_neighbors))
    for n in neighbors:
        new_path = path.copy()
        new_path.add(n)
        collection.add(new_path)
        # Thread(target=create_path, args=(page_url, path)).start()
print("The Empire Strikes Back")
