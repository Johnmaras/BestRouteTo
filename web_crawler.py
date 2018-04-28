from bs4 import BeautifulSoup
import requests
from threading import Thread
from Path import Path
from Page import Page
from urllib import parse

base_url = "http://www.aueb.gr"
parsed_base_url = parse.urlparse(base_url)
base_url_netloc = parsed_base_url.netloc

paths = []

visited = set()

# NOTE program output(under consideration): tree of all best routes to final pages(more outputs to be added)
# NOTE                                      dead links, and (probably) all of their routes

# TODO create an xml(or something) file that prettily presents the best route tree

# NOTE The program must decide which route to choose to go with(namely which link to request next from each page)
# NOTE                    ^partially done
# NOTE despite the fact that in the end it will scan every possible route

# TODO create a heuristic(or something) function that determines why a route is preferable over another.
# TODO It will possibly be used the location(internal/external) of the page. More to be added for a better discrimination


def is_valid_link(link):
    if link.startswith("http") or link.startswith("https"):
        parsed_new_link = parse.urlparse(link)
        link_netloc = parsed_new_link.netloc

        if link_netloc == base_url_netloc:
            return True  # it was link
    elif link.startswith("/"):
        return True  # it was base_url + link

    return False


def create_pages(urls):
    pages = []
    for url in urls:
        pages.append(Page(url))
    return pages


def create_path(url, path):

    url_contents = requests.get(url).text

    soup = BeautifulSoup(url_contents, "html.parser")

    a_tags = soup.find_all("a")

    page_links = filter(lambda x: is_valid_link(x), map(lambda x: x["href"], a_tags))

    pages = create_pages(page_links).sort()

    path.add(url)
    for page in pages:
        page_url = page.url
        if not(page_url in visited):
            create_path(page_url, path)
        else:
            paths.append(path)


url_contents = requests.get(base_url).text

soup = BeautifulSoup(url_contents, "html.parser")

a_tags = soup.find_all("a")
page_links = filter(lambda x: is_valid_link(x), map(lambda x: x["href"], a_tags))

pages = create_pages(page_links)

for page in pages:
    path = Path(base_url)
    page_url = page.url
    path.add(page_url)
    Thread(target=create_path, args=(page_url, path)).start()
print("The Empire Strikes Back")
