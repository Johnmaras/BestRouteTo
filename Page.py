import requests
from bs4 import BeautifulSoup

# NOTE assume urls are valid


class Page:
    def __init__(self, url, base_url):
        self.url = base_url + url
        self.base_url = base_url
        self.links = []
        self.weight = 0
        self.create_page()

    def create_page(self):
        url_text = requests.get(self.url).text
        soup = BeautifulSoup(url_text, "html.parser")
        link_tags = soup.find_all("a")
        for tag in link_tags:
            self.links.append(tag["href"])
        self.cost(soup)

    def cost(self, content):
        # TODO also mind the media the page carries
        media_tags = content.find_all(src=True)

        self.weight = self.links.__len__() + media_tags.__len__()

    def __lt__(self, other_page):
        return self.weight < other_page.weight

    def __gt__(self, other_page):
        return self.weight > other_page.weight

    def __le__(self, other_page):
        return self.weight <= other_page.weight

    def __ge__(self, other_page):
        return self.weight >= other_page.weight

    def __cmp__(self, other_page):
        if self.weight > other_page.weight:
            return 1
        elif self.weight < other_page.weight:
            return -1
        else:
            return 0
