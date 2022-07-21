import os
from urllib.error import HTTPError
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import csv
import random

from requests import request
import requests

FILE_NAME = "datasets.csv"

links_ekantipur = [
]

links_onlinekhabar = [
    "https://www.onlinekhabar.com/2022/05/1132857",
    "https://www.onlinekhabar.com/2022/05/1134197",
    "https://www.onlinekhabar.com/2022/05/1134087",
    "https://www.onlinekhabar.com/2022/05/1134021",
    "https://www.onlinekhabar.com/2022/05/1133972",
    "https://www.onlinekhabar.com/2022/05/1133925",
    "https://www.onlinekhabar.com/2022/05/1133925",
    "https://www.onlinekhabar.com/2022/05/1133677",
    "https://www.onlinekhabar.com/2022/05/1133255",
    "https://www.onlinekhabar.com/2022/05/1133125",
    "https://www.onlinekhabar.com/2022/05/1133125",
    "https://www.onlinekhabar.com/2022/05/1132861",
    "https://www.onlinekhabar.com/2022/05/1132775",
    "https://www.onlinekhabar.com/2022/05/1132657",
    "https://www.onlinekhabar.com/2022/05/1132531",
    "https://www.onlinekhabar.com/2022/05/1132496",
    "https://www.onlinekhabar.com/2022/05/1132480",
    "https://www.onlinekhabar.com/2022/05/1132222",
    "https://www.onlinekhabar.com/2022/05/1131689"
]

def GET_UA():
    uastrings = ["Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36",\
                "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.72 Safari/537.36",\
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10) AppleWebKit/600.1.25 (KHTML, like Gecko) Version/8.0 Safari/600.1.25",\
                "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:33.0) Gecko/20100101 Firefox/33.0",\
                "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36",\
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36",\
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/600.1.17 (KHTML, like Gecko) Version/7.1 Safari/537.85.10",\
                "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko",\
                "Mozilla/5.0 (Windows NT 6.3; WOW64; rv:33.0) Gecko/20100101 Firefox/33.0",\
                "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.104 Safari/537.36"\
                ]
 
    return random.choice(uastrings)

def get_soup(link:str):
    req = Request(link, headers={'User-Agent':GET_UA()})
    req = urlopen(req)
    soup = BeautifulSoup(req.read().decode("utf-8"), "html.parser")

    return soup    

def get_links(path:str):
    if path[-1] != '/':
        path = path + '/'
    files = os.listdir(path)
    files = list(map(lambda x: path + x, files))
    links = []

    for file in files:
        with open(file, 'r') as f:
            link_file = f.readlines()
            for link in link_file:
                if link not in links:
                    links.append(link)
            f.close()

    return links


def scrape_ekantipur():
    links_ekantipur = get_links("data/ekantipur_links/")
    for link in links_ekantipur:
        try:
            req = requests.get(link.strip())
        except HTTPError:
            pass
        soup = BeautifulSoup(req.text, "html.parser")
        body = soup.find("div", attrs={"class": "article-header"})
        title = body.find("h1").text
        # get sub heading of the news as the body 
        contents_list = body.find_all("div", attrs={"class": "sub-headline"})

        # get all the paragraphs
        news_block = soup.find("div", attrs={"class": "current-news-block"})
        if news_block:
            contents_list.extend(soup.find("div", attrs={"class": "current-news-block"}).find_all("p"))
        else:
            continue

        content = "".join([content_tag.text for content_tag in contents_list])
        link = link.strip()
        with open(FILE_NAME, 'a') as f:
            csv_writer = csv.writer(f, delimiter=";", quotechar='|')
            csv_writer.writerow([title, link, content])

            f.close()


def scrape_nagarik():
    raise NotImplementedError

def scrape_annapurna():
    raise NotImplementedError

def scrape_online_khabar():
    for link in links_onlinekhabar:
        soup = get_soup(link)
        title = soup.find("h1", attrs={"class": "entry-title"}).getText()

        contents_div = soup.find("div", attrs = {"class": "ok18-single-post-content-wrap"})
        contents_list = contents_div.find_all("p")

        content = "".join([content_p.text for content_p in contents_list])

        with open(FILE_NAME, 'a') as f:
            csv_writer = csv.writer(f, delimiter=";", quotechar='|')
            csv_writer.writerow([title, link, content])

            f.close()


def setup():
    if not os.path.exists("datasets.csv"):
        with open(FILE_NAME, 'w') as f:
            f.write("id, Title, Link, Text\n")
    
        f.close()


if __name__ == "__main__":
    pass