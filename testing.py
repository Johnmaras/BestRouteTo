import requests
from bs4 import BeautifulSoup

url = "http://www.youtube.gr"
content = requests.get(url).text

soup = BeautifulSoup(content, "html.parser")
tags = soup.find_all(src=True)
for tag in tags:
    print(tag)
print("end")
