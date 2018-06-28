# -*-coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup


headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) \
Chrome/61.0.3163.100 Safari/537.36'}


def get_joke(url, page):
    html = requests.get(url + str(page), headers=headers).content
    soup = BeautifulSoup(html, 'lxml').find('div', {'id': 'content-left'}).find_all('div', {'class': 'content'})
    jokes = []
    for joke in soup:
        jk = joke.get_text().replace("\n", "")
        jokes.append(jk)
    return jokes


def main():
    url = "https://www.qiushibaike.com/8hr/page/"
    page = 1
    all_jokes = []
    while page <= 13:
        jokes_page = get_joke(url, page)
        for joke in jokes_page:
            all_jokes.append(joke)
        page += 1
    f = open("d:/joke.txt", "a", encoding='gb2312')
    for i in all_jokes:
        f.write('\n' + i + '\n')
    f.close()


if __name__ == '__main__':
    main()
