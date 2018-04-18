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


def isValidPage(link):
    if link.startswith("http") or link.startswith("https"):
        parsed_new_link = parse.urlparse(link)
        link_netloc = parsed_new_link.netloc

        if link_netloc.__eq__(base_url_netloc):
            return link
    elif link.startswith("/"):
        return base_url + link

    return None


def create_path(url, path):

    url_contents = requests.get(url).text

    soup = BeautifulSoup(url_contents, "html.parser")

    tags = soup.find_all("a")

    path.add(url)
    for a_tag in tags:
        link = a_tag["href"]
        valid_link = isValidPage(link)
        if not(valid_link is None):
            if not visited.__contains__(valid_link):
                create_path(valid_link, path)
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
    valid_link = isValidPage(link)
    if not(valid_link is None):
        links.append(valid_link)


for link in links:
    path = Path(base_url)
    path.add(link)
    Thread(target=create_path, args=(link, path)).start()
print("The Empire Strikes Back")
