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
BASE_URL="https://www.ted.com"
def make_soup(url):
    html=urlopen(url).read()
    return BeautifulSoup(html,"lxml")#html to lxml

def get_talks(url):
    talks=make_soup(url).find("div","row row-sm-4up row-lg-6up row-skinny")# tag and class
    talk_links= [BASE_URL+h4.a["href"] for h4 in talks.findAll("h4","h9 m5")]#List Comprehensions
    #there is "posted rated" info on the index page
    return talk_links

def get_talk_info(talk_url,tag,clas):
    soup=make_soup(talk_url)
    info_string=[info.string for info in soup.findAll(tag,clas)]
    return info_string

# print(get_talks("https://www.ted.com/talks"))
#本地存了各个演讲的网址
#https://www.ted.com/talks?page=2
for page in range(1,61):
    url="https://www.ted.com/talks?page="+str(page)
    talk_links=get_talks(url)#得到该目录页的所有演讲链接
    for talk in talk_links:
        speaker=get_talk_info(talk,"span","player-hero__speaker__content")
        talk_name=get_talk_info(talk,"span","player-hero__title__content")
        # watch_times=get_talk_info(talk,"span","talk-sharing__value")
        # time_info=get_talk_info(talk,'span',"player-hero__meta__label")
        # brief_description=get_talk_info(talk,"p","talk-description")
        #transcript: url/transcript?language=en 对beautiful soup的进一步应用.
            #similar topics
        #存储数据到数据库!!
        print(speaker,talk_name)
    time.sleep(1)
