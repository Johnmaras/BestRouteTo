import dominate.tags as tags
import random
import os


pages_dir = "test_pages"

try:
    os.mkdir(pages_dir)
except:
    pass

n = 20

pages = []
for i in range(1, n + 1):
    pages.append("page{}.html".format(i))

for j in range(1, n):
    page = tags.html()

    page_title = tags.title("Page " + str(j))
    page_head = tags.head(page_title)

    page_body = tags.body()
    for k in range(1, random.randint(1, n)):
        image = tags.img(src=("image_source" + str(k)))
        page_body.add(image)

    ul_links = tags.ul()
    for r in range(1, random.randint(1, n)):
        li_link = tags.li()
        page_to_link = pages[random.randint(0, n - 1)]
        link = li_link.add(tags.a("This is a link to {}".format(page_to_link), href=page_to_link))
        ul_links.add(li_link)
    page_body.add(ul_links)

    page.add(page_head)
    page.add(page_body)

    out_file = open(pages_dir + os.sep + pages[j - 1], 'w+')
    out_file.write(str(page))

# print(page)
