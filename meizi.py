# -*-coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
from urllib.request import urlretrieve
from time import sleep
import random


def html_text(url1, url2, page, headers):
    url = url1 + str(page) + url2
    html = requests.get(url, headers=headers).content
    soup = BeautifulSoup(html)
    body = soup.find('ol', {'class': 'commentlist'})
    images = body.find_all('li')
    for i in images:
        x = i.find('img').get('src')
        y = i.get('id')
        try:
            urlretrieve('http:' + x, "d:/pycharm/crawler/meizi/%s.jpg" % y)
            print('图片%s已下载' % y)
            sleep(random.random()*3)  # 随机休息0-3秒再爬
        except ValueError:
            pass


def main():
    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)"
                      " Chrome/61.0.3163.100 Safari/537.36"
    }
    url1 = "http://jandan.net/ooxx/page-"
    url2 = "#comments"
    pages = list(range(111, 116))
    num = 1
    for page in pages:
        html_text(url1, url2, page, headers)
        print("第%s已下载" % num)
        num += 1


if __name__ == '__main__':
    main()
