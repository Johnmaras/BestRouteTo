import json

import requests
from bs4 import BeautifulSoup
from urllib import parse
import xml.etree.ElementTree as ET


class Page:
    def __init__(self, page: str, base_url: str):
        self.page = page
        self.url = "{}/{}".format(base_url.strip('/'), page.strip('/'))
        self.base_url = base_url
        self.links = []
        self.weight = 0
        self.dead = False
        self.base_url_netloc = parse.urlparse(base_url).netloc
        self.create_page()

    def create_page(self):
        try:
            url_req = requests.get(self.url)
            ct = url_req.headers.get("content-type")
            if ct.lower().startswith("text"):
                url_text = url_req.text
            else:
                return
        except Exception as e:
            print("{} on page {}".format(e, self.page.strip("/")))

            # Assume that failed requests are dead links
            self.dead = True
            return
        soup = BeautifulSoup(url_text, "html.parser")
        link_tags = soup.find_all("a")

        self.links = list(filter(lambda x: self.is_valid_link(x), map(lambda x: x["href"] if x.has_attr("href") else None, link_tags)))

        self.cost(soup)

    def cost(self, content: BeautifulSoup):
        # TODO also mind the media the page carries
        media_tags = content.find_all(src=True)

        self.weight = self.links.__len__() + media_tags.__len__()

    def is_valid_link(self, link: str):
        if link is None:
            return False
        if link.startswith("http") or link.startswith("https"):
            parsed_new_link = parse.urlparse(link)
            link_netloc = parsed_new_link.netloc

            if link_netloc == self.base_url_netloc:
                return True
        elif link.startswith("/"):
            return True

        return False

    def is_dead(self):
        return self.dead

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
        return self.to_json()
        # return "\nUrl = {}, Weight = {}".format(self.url, self.weight)

    def to_json(self):
        s = {"url": self.url}
        return s

    def to_xml(self):
        page = ET.Element("page")
        page.text = self.url
        return page
