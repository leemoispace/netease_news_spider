#http://www.gregreda.com/2013/04/29/more-web-scraping-with-python/
#the site is already different form that in the blog,so i rewrite one.


#get all of their URLs from the initial list page, and then process each details page. We're also going to write all of the data to a tab-delimited file using Python's CSV package.
from bs4 import BeautifulSoup
from urllib.request import urlopen
import csv

base_url = ("http://www.chicagomag.com/Chicago-Magazine/November-2012/Best-Sandwiches-Chicago/")



with open("data/src-best-sandwiches.tsv", "w") as f:
    fieldnames = ("rank", "sandwich", "restaurant", "description", "price",
                    "address", "phone", "website")
    output = csv.writer(f, delimiter="\t")
    output.writerow(fieldnames)


    soup = BeautifulSoup(urlopen(base_url).read(),"lxml")
    sammies = soup.find_all("div", "sammy")
    #直接在目录获得的信息,rank,restaurant,sanwich_name
    for item in sammies:
        rank=item.find("div","sammyRank").string
        restaurant=((str)(item.find("a"))).split("<br/>")[1].replace("\n","")
        sandwich=item.find("b").string
        output.writerow([rank, sandwich, restaurant])

    #在第二级页面里,description,price,address, phone,website
    sammy_urls = [div.a["href"] for div in sammies]
    for url in sammy_urls:
        url = url.replace("http://www.chicagomag.com", "")  # inconsistent URL
        #print("http://www.chicagomag.com{0}".format(url))
        #str.format():
        page = urlopen("http://www.chicagomag.com{0}".format(url))

        soup = BeautifulSoup(page.read(),"lxml")
        #description=soup.find_all("div","content_post").find("p")[1].string.strip()
        description=soup.find_all("p")[1].string.strip()
        addy = soup.find("p", "addy").text
        price = addy.partition(",")[0].partition(". ")[0].strip()
        address = addy.partition(",")[0].partition(". ")[2].strip()

        #NO12 那家没有电话,电话和网址都有错误
        try:
            addy.index("-")
            phone = addy.partition(",")[2].split(", ")[0]
            if soup.find("p", "addy").em.a:
                website=addy.partition(",")[2].split(", ")[1]
            else:
                website = ""
        except:
            phone=""
        #csv module don't support add a new column
        output.writerow([description, price, address, phone, website])

print("Done writing file")
