from bs4 import BeautifulSoup
import time
#www.ted.com/talks
try:
    # For Python 3.0 and later
    from urllib.request import urlopen
except ImportError:
    # Fall back to Python 2's urllib2
    from urllib2 import urlopen
#python3 里面已经是用request了:http://stackoverflow.com/questions/2792650/python3-error-import-error-no-module-name-urllib

#先按照教程https://movie.douban.com/top250?filter=,抓芝加哥reader
#然后抓https://movie.douban.com/top250
BASE_URL="https://www.ted.com"

def make_soup(url):
    html=urlopen(url).read()
    return BeautifulSoup(html,"lxml")#html to lxml

def get_talks(url):
    talks=make_soup(url).find("div","row row-sm-4up row-lg-6up row-skinny")# tag and class
    talk_links= [BASE_URL+h4.a["href"] for h4 in talks.findAll("h4","h9 m5")]#List Comprehensions
    return talk_links

def get_talk_info(talk_url,tag,clas):
    soup=make_soup(talk_url)
    info_string=[info.string for info in soup.findAll(tag,clas)]
    return info_string

# print(get_talks("https://www.ted.com/talks"))
#
#soup=BeautifulSoup(open('Browse TED Talks _ TED.com.html'),"lxml")
soup=BeautifulSoup(open('Alex Kipman_ The dawn of the age of holograms _ TED Talk _ TED.com.html'),"lxml")

#talks=soup.find("div","row row-sm-4up row-lg-6up row-skinny")# tag and class
# print(talks.findAll("h4","h9 m5"))

watch_times=[info.string for info in soup.findAll("span","talk-sharing__value")]

print(watch_times)
