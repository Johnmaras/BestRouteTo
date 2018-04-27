import requests
from bs4 import BeautifulSoup

# NOTE assume urls are valid


class Page:
    def __init__(self, url):
        self.url = url
        self.links = []

    def create_page(self):
        url_text = requests.get(self.url).text
        soup = BeautifulSoup(url_text, "html.parser")
        link_tags = soup.find_all("a")
        for tag in link_tags:
            self.links.append(tag["href"])

    def cost(self, content):
        # TODO also mind the media the page carries
        media_tags = content.find_all(src=True)

        return self.links.__len__() + media_tags.__len__()

    def __lt__(self, other_page):
        return self.cost() < other_page.cost()

    def __gt__(self, other_page):
        return self.cost() > other_page.cost()

    def __le__(self, other_page):
        return self.cost() <= other_page.cost()

    def __ge__(self, other_page):
        return self.cost() >= other_page.cost()

    def __cmp__(self, other_page):
        if self.cost() > other_page.cost():
            return 1
        elif self.cost() < other_page.cost():
            return -1
        else:
            return 0
