import time
from threading import Thread
from MySet import MySet
from Page import Page
from Path import Path
import argparse
import xml.etree.ElementTree as ET

parser = argparse.ArgumentParser(prog="python3 web_crawler.py", description="Export shortest paths of a domain into XML, create XML sitemap, find dead links")
parser.add_argument("-d", "--domain", help="The domain url", type=str, required=True)
parser.add_argument("-f", "--firstpage", help="The home page of the domain. Defaults to /", type=str, default="/")
parser.add_argument("-so", "--sitemapout", help="The path to where the sitemap xml will be saved", type=str, default="sitemap.xml")
parser.add_argument("-po", "--pathsout", help="The path to where the shortest paths xml will be saved", type=str, default="paths.xml")
parser.add_argument("-do", "--deadout", help="The path to where the dead links xml will be saved", type=str, default="dead.xml")
arg = parser.parse_args()

base_url = arg.domain
first_page = arg.firstpage

pages = []
parsed = []
dead = []


def sitemap_out():
    rootEl = ET.Element("urlset")
    for site in collection.visited:
        url_Elem = ET.Element("url")

        loc_Elem = ET.Element("loc")
        loc_Elem.text = site.url

        url_Elem.append(loc_Elem)

        rootEl.append(url_Elem)
    xmltree = ET.ElementTree(element=rootEl)
    xmltree.write(arg.sitemapout)


def paths_out():
    rootElem = ET.Element("paths")
    for path in collection.paths:
        rootElem.append(path.to_xml())

    xmltree = ET.ElementTree(element=rootElem)
    xmltree.write(arg.pathsout)


def dead_out():
    rootElem = ET.Element("dead")
    for page in dead:
        rootElem.append(page.to_xml())

    xmltree = ET.ElementTree(element=rootElem)
    xmltree.write(arg.deadout)


def command(url, baseurl):
    page = Page(url, baseurl)
    if not(page.is_dead()):
        pages.append(page)
    else:
        dead.append(page)


def create_pages(urls: list):
    global collection
    global pages
    pages = []
    threads = []
    for url in urls:
        if collection.is_visited(url) or (url in parsed):
            continue
        else:
            parsed.append(url)
            t = Thread(target=command, args=(url, base_url))
            threads.append(t)
            t.start()
    for t in threads:
        if t.is_alive():
            t.join()

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

paths_out()
sitemap_out()
dead_out()

print("It took {} seconds to crawl the domain".format(end - start))
