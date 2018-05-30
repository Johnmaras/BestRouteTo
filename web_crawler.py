import json
import time
from threading import Thread
import MyDictToXML
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
parser.add_argument("-css", "--style", help="Provide custom css file for formatting the xml files", type=str)
arg = parser.parse_args()

base_url = arg.domain
first_page = arg.firstpage

# TODO find and print dead links

# TODO create an xml(or something) file that prettily presents the best route tree

# TODO improve the heuristic

pages = []
parsed = []


def sitemap_out():
    # TODO add more info
    rootEl = ET.Element("urlset")
    for site in collection.visited:
        url_Elem = ET.Element("url")

        loc_Elem = ET.Element("loc")
        loc_Elem.text = site.url

        url_Elem.append(loc_Elem)

        rootEl.append(url_Elem)
    xmltree = ET.ElementTree(element=rootEl)
    xmltree.write("sitemap.xml")


def paths_out():
    xml_f = open(arg.pathsout, "bw+")
    addons = []
    if arg.style:
        style_line = "<?xml-stylesheet type=\"text/css\" href=\"{cssfile}\"?>".format(cssfile=arg.style)
        addons = [style_line]

    data = MyDictToXML.dicttoxml(json.loads(collection.to_json()), root=False, additions=addons)

    xml_f.write(data)


def command(url, baseurl):
    pages.append(Page(url, baseurl))


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

print(end - start)
