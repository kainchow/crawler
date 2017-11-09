# -*-coding: utf-8 -*-
# create time : 2017/10/15
# author : kaichow


import requests
from bs4 import BeautifulSoup
import pandas as pd
from sqlalchemy import create_engine
import re


headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive'
}
xingzhengqu = ['tianhe', 'yuexiu', 'liwan', 'haizhu', 'panyu', 'baiyun', 'huangpugz', 'zengcheng', 'huadou', 'nansha']
xingzhengqu_cn = ['天河', '越秀', '荔湾', '海珠', '番禺', '白云', '黄埔', '增城', '花都', '南沙']


def get_url(url, page):
    html = requests.get(url + '/pg%s' % str(page), headers=headers).text
    table = BeautifulSoup(html, 'lxml').find('div', {'class': 'con-box'}).find_all('li', {'data-el': 'zufang'})
    table_2 = BeautifulSoup(html, 'lxml')
    pattern = re.compile('"totalPage":(.*?),".*?')
    last_page = re.findall(pattern, str(table_2))
    pattern_mianji = re.compile("(.*?)平米.*?")
    pattern_updatetime = re.compile("(.*?)\s更新")
    pattern_quyu = re.compile("(.*?)租房")
    result = []
    for li in table:
        item = dict()
        item[u'网站'] = li.find('a').get('href')
        item[u'房屋描述'] = li.find('img').get('alt')
        item[u'小区'] = li.find('div', {'class': 'where'}).find('a').get_text().replace('\xa0', '')
        item[u'房型'] = li.find('div', {'class': 'where'}).find_all('span')[1].get_text().replace('\xa0', '')
        item[u'面积'] = re.findall(pattern_mianji, li.find('div', {'class': 'where'}).find_all('span')[3].get_text())[0]
        item[u'朝向'] = li.find('div', {'class': 'where'}).find_all('span')[4].get_text()
        item[u'地区'] = re.findall(pattern_quyu, li.find('div', {'class': 'other'}).find('a').get_text())[0]
        item[u'楼层'] = li.find('div', {'class': 'con'}).get_text().split('/')[1]
        item[u'年限'] = li.find('div', {'class': 'con'}).get_text().split('/')[2]
        item[u'价格'] = li.find('div', {'class': 'price'}).find('span', {'class': 'num'}).get_text()
        item[u'更新时间'] = re.findall(pattern_updatetime, li.find('div', {'class': 'price-pre'}).get_text())[0]
        item[u'看房人数'] = li.find('div', {'class': 'square'}).find('span', {'class': 'num'}).get_text()
        result.append(item)
    return result, last_page


def get_quyu_data(area, x):
    url = "https://gz.lianjia.com/zufang/%s" % area
    page = 1
    last_page = get_url(url, page)[1]
    df = pd.DataFrame()
    while True:
        try:
            result = get_url(url, page)[0]
        except:
            print("failed")
            break
        df = df.append(pd.DataFrame(result))
        page += 1
        if page > int(''.join(last_page)):
            break
    df['区域'] = '%s' % x
    return df


def main():
    column = ['房屋描述', '区域', '地区', '小区', '房型', '面积', '楼层', '朝向', '价格', '年限', '更新时间', '看房人数', '网站']
    engine = create_engine('mysql+mysqlconnector://root:097514@127.0.0.1/mysql?charset=utf8')
    frame = pd.DataFrame()
    for i in range(len(xingzhengqu)):
        quyu = get_quyu_data(xingzhengqu[i], xingzhengqu_cn[i])
        frame = frame.append(quyu)
    frame = frame.reindex(columns=column)
    frame.index = range(len(frame))
    frame.to_sql('lianjia_zufang', engine, if_exists='replace')


if __name__ == '__main__':
    main()
