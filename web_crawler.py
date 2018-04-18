from bs4 import BeautifulSoup
import requests
from threading import Thread
from Path import Path
from urllib import parse

base_url = "http://www.aueb.gr"
initial = True

paths = []

visited = set()

# NOTE program output(under consideration): tree of all best routes to final pages(more outputs to be added)

# TODO create an xml(or something) file that prettily presents the best route tree

# NOTE The program must decide which route to choose to go with(namely which link to request next from each page)
# NOTE despite the fact that in the end it will scan every possible route

# TODO create a heuristic(or something) function that determines why a route is preferable over another.
# TODO It will possibly be used the location(internal/external) of the page. More to be added for a better discrimination


def create_path(url, path):

    url_contents = requests.get(url).text

    soup = BeautifulSoup(url_contents, "html.parser")

    tags = soup.find_all("a")

    path.add(url)
    for a_tag in tags:
        link = a_tag["href"]
        if not visited.__contains__(link):
            create_path(link, path)
        else:
            paths.append(path)


url_contents = requests.get(base_url).text

soup = BeautifulSoup(url_contents, "html.parser")

tags = soup.find_all("a")
links = []

parsed_base_url = parse.urlparse(base_url)
base_url_netloc = parsed_base_url.netloc

for tag in tags:
    link = tag["href"]
    if link.startswith("http") or link.startswith("https"):
        parsed_new_link = parse.urlparse(link)
        link_netloc = parsed_new_link.netloc

        if link_netloc.__eq__(base_url_netloc):
            links.append(link)
    elif link.startswith("/"):
        links.append(base_url + link)


for link in links:
    path = Path(base_url)
    path.add(link)
    Thread(create_path, args=(link, path))
