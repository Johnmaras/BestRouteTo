import requests
from bs4 import BeautifulSoup
from urllib import parse


class Page:
    def __init__(self, url: str, base_url: str):
        self.url = "{}/{}".format(base_url.strip('/'), url.strip('/'))
        self.base_url = base_url
        self.links = []
        self.weight = 0

        self.base_url_netloc = parse.urlparse(base_url).netloc
        self.create_page()

    def create_page(self):
        url_text = requests.get(self.url).text
        soup = BeautifulSoup(url_text, "html.parser")
        link_tags = soup.find_all("a")

        self.links = list(filter(lambda x: self.is_valid_link(x), map(lambda x: x["href"], link_tags)))

        self.cost(soup)

    def cost(self, content: BeautifulSoup):
        # TODO also mind the media the page carries
        media_tags = content.find_all(src=True)

        self.weight = self.links.__len__() + media_tags.__len__()

    def is_valid_link(self, link: str):
        if link.startswith("http") or link.startswith("https"):
            parsed_new_link = parse.urlparse(link)
            link_netloc = parsed_new_link.netloc

            if link_netloc == self.base_url_netloc:
                return True  # it was link
        elif link.startswith("/"):
            return True  # it was base_url + link

        return False

    def __hash__(self, *args, **kwargs):
        return super().__hash__(*args, **kwargs)

    def __eq__(self, other):
        return self.url == other.url

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

    def print(self):
        print("\nUrl = {}, Weight = {}".format(self.url, self.weight))

    def __str__(self):
        return self.url
