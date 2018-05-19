import json
import os

import pickle
from bs4 import BeautifulSoup
import requests
from threading import Thread
import threading
from Path import Path
from Page import Page
from MySet import MySet
import time
import dicttoxml

# base_url = "http://www.aueb.gr"
base_url = "http://127.0.0.1:3117"
first_page = "a.html"
# first_page = "/"

# TODO find and print dead links

# TODO create an xml(or something) file that prettily presents the best route tree

# TODO improve the heuristic

pages = []
parsed = []

xml_f = open("paths.xml", "bw+")


def command(url, baseurl):
    pages.append(Page(url, baseurl))


def create_pages(urls: list):
    global collection
    global pages
    # start = time.time()
    pages = []
    threads = []
    # i = 1
    for url in urls:
        if collection.is_visited(url) or (url in parsed):
            continue
        else:
            parsed.append(url)
            # t_name = "thread" + str(i)
            t = Thread(target=command, args=(url, base_url))
            threads.append(t)
            t.start()
            # print(url)
    for t in threads:
        if t.is_alive():
            t.join()
    # end = time.time()
    # print(end - start)

    return pages


start = time.time()
# create a custom composite data structure that implements some of the algorithm logic
# and keeps track of each needed data structure
collection = MySet()

# create the first page/node
aPage = Page(first_page, base_url)

# create a path starting from the first page
path = Path(aPage)

# add to the data structure which will update its contents
collection.add(path)

# find the next min path that will be chosen
collection.set_min()

# while there are still unvisited paths
while collection.has_next():

    # get the next unvisited cheapest path
    path = collection.pop()

    # get its last node
    node = path.last

    # get its neighbors
    raw_neighbors = create_pages(node.links)
    # get its unvisited neighbors
    neighbors = list(filter(lambda x: not(x in collection.visited), raw_neighbors))

    # for each neighbor
    for n in neighbors:
        # copy the base path so we can create a new path for each neighbor
        new_path = path.copy()

        # create a path for the neighbor
        new_path.add(n)

        # let the collection decide whether to add it or not
        collection.add(new_path)

    # find the next min path
    collection.set_min()

end = time.time()
# f_out = open("crawlResults", 'w+')
# f_out.write(str(collection))

data = dicttoxml.dicttoxml(json.loads(collection.to_json()))

xml_f.write(data)
# print(data)

# print(collection.to_json())

print(end - start)
