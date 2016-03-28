from bs4 import BeautifulSoup
import sqlite3
import time
import os
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

#already string
def get_talk_info(talk_url,tag,clas):
    soup=make_soup(talk_url)
    info_string=[info.string for info in soup.findAll(tag,clas)]
    return info_string

# print(get_talks("https://www.ted.com/talks"))
#本地存了各个演讲的网址
#https://www.ted.com/talks?page=2


if os.path.exists("data/TED.db"):
    conn=sqlite3.connect("data/TED.db")
    cur=conn.cursor()
else:
    #建立数据库
    conn=sqlite3.connect("data/TED.db")
    #建立cursor
    cur=conn.cursor()
    cur.execute('''CREATE TABLE TED
    (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        speaker CHAR,
        talk_name CHAR,
        talk_link TEXT,
        watch_times INT,
        place CHAR,
        length CHAR,
        month CHAR,
        brief_description TEXT,
        transcript TEXT,
        similar_topics TEXT
    );''')
    conn.commit()

def list_to_string(list):
    return "".join(list).strip()


count=1
for page in range(19,61):
    url="https://www.ted.com/talks?page="+str(page)
    print(url)
    #talk_links=get_talks(url)#得到该目录页的所有演讲链接
    talks=make_soup(url).find("div","row row-sm-4up row-lg-6up row-skinny")# tag and class
    talk_links= [BASE_URL+h4.a["href"] for h4 in talks.findAll("h4","h9 m5")]#List Comprehensions
    #print(talk_links)
    for talk in talk_links:
        try:
            speaker="".join(get_talk_info(talk,"span","player-hero__speaker__content")).strip("\n")
            talk_name="".join(get_talk_info(talk,"span","player-hero__title__content")).strip("\n")
            watch_times=(int)(get_talk_info(talk,"span","talk-sharing__value")[0].strip("\n").replace(',',''))

            place="".join(make_soup(talk).find("div","player-hero__meta").find("strong").text)
            length="".join(make_soup(talk).find("div","player-hero__meta").find("span").text).strip()
            month="".join(make_soup(talk).find("div","player-hero__meta").findAll("span")[1].text).strip().split('\n')[1]
            brief_description="".join(get_talk_info(talk,"p","talk-description"))
            transcript="".join(get_talk_info(talk+"/transcript?language=en","span","talk-transcript__fragment"))
            similar_topics="".join(get_talk_info(talk,"a","l3 talk-topics__link ga-link"))
            #存储数据到数据库!!
            count+=1
            #print(speaker,talk_name,talk,watch_times,place,length,month,brief_description,transcript,similar_topics)
            cur.execute("INSERT INTO TED VALUES(null,?,?,?,?,?,?,?,?,?,?)",(speaker,talk_name,talk,watch_times,place,length,month,brief_description,transcript,similar_topics))
            conn.commit()
            #cur.execute("INSERT INTO TED VALUES (NULL,'%s','%s','%s','%d','%s','%s','%s','%s','%s','%s');"%(speaker,talk_name,talk,watch_times,place,length,month,brief_description,transcript,similar_topics))
            print(count," ",speaker," ",talk_name)
        except:
            cur.execute("INSERT INTO TED VALUES(null,?,?,?,null,null,null,null,null,null,null)",(speaker,talk_name,talk))
            conn.commit()
            print("Error",count," ",speaker," ",talk_name)
        time.sleep(0.1)
    time.sleep(0.1)
