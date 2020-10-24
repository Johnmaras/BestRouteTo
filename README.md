# BestRouteTo
Find the best route to the inner links of a website, find dead links and create the sitemap.xml

Implements the Dijkstra algorithm for finding the shortest paths. 
Not professionally made, but provides three utilities that can be easily extended.
All results are saved on separate xml files.

It is also provided an http server for testing purposes and a script that creates randomly interlinked html pages.

# Depedencies
It requires the following libraries:<br>
<li> bs4
<li> dominate<br>

# Running
Runs on python 3.x<r>

From terminal:<br>
python3 web_crawler.py --domain http://www.example.com --firstpage thefirstpage.html<br>
-d/--domain is required<br>
-f/--firstpage defaults to /<br>
-so/--sitemapout defaults to sitemap.xml<br>
-po/--pathsout defaults to paths.xml<br>
-do/--deadout defaults to dead.xml<br>
