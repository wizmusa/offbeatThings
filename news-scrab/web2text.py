import requests
from bs4 import BeautifulSoup
import re

#webpage = requests.get("https://m.mt.co.kr/renew/view.html/view.html?no=2018101021264914891&MVRN")
webpage = requests.get("https://www.fnnews.com/news/201809061709398412")
#soup = BeautifulSoup(webpage.content, "html.parser")
soup = BeautifulSoup(webpage.text, "html.parser")
soup = re.search('<body.*/body>', soup, re.I|re.S)

print(soup)


# for d in soup.div.children:
    # print(d)