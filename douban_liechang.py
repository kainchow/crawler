# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import pandas as pd
from time import sleep
import random

# start=规律0,20,40,60...表示第1,2,3,4...页
url = "https://movie.douban.com/subject/26322642/comments?start=%s&limit=20&sort=new_score&status=P&percent_type="
headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/"
                         "63.0.3239.84 Safari/537.36"}


class Douban(object):
    def __init__(self):
        self.url = url
        self.headers = headers

    def get_message(self):
        url_page = self.url % str(0)
        content = requests.get(url_page, headers=self.headers).content
        soup = BeautifulSoup(content)
        comment_number = soup.find('div', {'class': 'grid-16-8 clearfix'}).find('li', {'class': 'is-active'})\
            .find('span').get_text()
        number = int(comment_number.replace('看过(', '').replace(')', '')) // 20 + 1
        pages = [x * 20 for x in range(number)]
        return pages

    def get_one_page_comment(self, page):
        url_page = self.url % str(page)
        content = requests.get(url_page, headers=self.headers).content
        soup = BeautifulSoup(content)
        text = soup.find('div', {'class': 'grid-16-8 clearfix'}).find('div', {'class': 'mod-bd'})
        texts = text.find_all('div', {'class': 'comment-item'})
        stars, comments = [], []
        for i in texts:
            star = i.find('span', {'class': 'comment-info'}).find_all('span')[1].get('class')[0].replace('allstar', '')
            comment = i.find('div', {'class': 'comment'}).find('p').get_text().strip()
            try:
                stars.append(int(star))
                comments.append(comment)
            except:
                pass
        return stars, comments

    def get_all_comment(self):
        pages = self.get_message()
        stars, comments = [], []
        sleep_random = random.random() * 5
        for page in pages:
            try:
                star, comment = self.get_one_page_comment(page)
                stars += star
                print('第%s页已爬取。' % int((page / 20 + 1)))
                comments += comment
                sleep(sleep_random)
            except:
                print('第%s页爬取失败！' % int((page / 20 + 1)))
        print('所有页面爬取完毕！')
        return stars, comments


if __name__ == '__main__':
    douban = Douban()
    stars, comments = douban.get_all_comment()
    douban_dict = dict()
    douban_dict['star'] = stars
    douban_dict['comment'] = comments
    df = pd.DataFrame(douban_dict)
    df.to_csv('d:/douban_liechang.csv')
    print('已导出csv。')
