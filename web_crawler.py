from bs4 import BeautifulSoup
import requests

base_url = "http://www.aueb.gr"

url_contents = requests.get(base_url).text

soup = BeautifulSoup(url_contents, "html.parser")

