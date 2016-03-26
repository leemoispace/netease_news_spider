#http://www.gregreda.com/2013/03/03/web-scraping-101-with-python/

from bs4 import BeautifulSoup

try:
    # For Python 3.0 and later
    from urllib.request import urlopen
except ImportError:
    # Fall back to Python 2's urllib2
    from urllib2 import urlopen

#python3 里面已经是用request了:http://stackoverflow.com/questions/2792650/python3-error-import-error-no-module-name-urllib

#先按照教程https://movie.douban.com/top250?filter=,抓芝加哥reader
#然后抓https://movie.douban.com/top250
BASE_URL="https://www.chicagoreader.com"

def make_soup(url):
    html=urlopen(url).read()
    return BeautifulSoup(html,"lxml")

def get_category_links(section_url):
    html=urlopen(section_url).read()
    soup=BeautifulSoup(html,"lxml")#html to lxml
    boccat=soup.find("dl","boccat")# tag and class
    category_links= [BASE_URL+dd.a["href"] for dd in boccat.findAll("dd")]#List Comprehensions
    return category_links



def get_category_winner(category_url):
    html=urlopen(category_url).read()
    soup=BeautifulSoup(html,"lxml")
    winner=[h2.string for h2 in soup.findAll("h2","boc2")]
    return{ #dictionary
        "category":categroy,
        "category_url":category_url,
        "winner":winner,
        "runners_up":runners_up}


cate_links=get_category_links("http://www.chicagoreader.com/chicago/best-of-chicago-2011-food-drink/BestOf?oid=4106228")

for item in cate_links:
    winner=get_category_winner(item)
    data.append(winner)
    sleep(1)

print(data)
