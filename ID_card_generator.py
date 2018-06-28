# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import re
import pymysql
import pandas as pd
import random

url_id = "http://www.welefen.com/lab/identify?province={0}&city={1}&area={2}&year={3}&month={4}&" \
      "day={5}&sex={6}"
url_name = "http://www.shengliyoutian.com/multiple/2127.html"
con = pymysql.connect(db='crawler', user='root', password='097514', charset='utf8')
sql = "select * from administrative_divisions;"
df = pd.read_sql(sql, con)
df = df.iloc[:, 1:4]
years = list(range(1949, 2000))
mons = list(range(1, 13))
days = list(range(1, 32))
sexs = ['男', '女']


# 从数据库中提取省市区县信息，与日期、性别组成搜索项，得到多组ID
def set_id(num):
    id_cards = []
    for i in range(num):
        num1 = random.randint(0, len(df))  # 随机抽取省市区
        num2 = random.randint(0, 1)  # 随机抽取性别
        x = df.iloc[num1, :]  # df中的其中一条信息
        pro, ct, area = x[0], x[1], x[2]  # 省、市、区/县
        sex = sexs[num2]  # 性别
        year = random.randint(years[0], years[-1])  # 年份
        mon = random.randint(mons[0], mons[-1])  # 月份
        day = random.randint(days[0], days[-1])  # 天
        date_a = str(year * 10000 + mon * 100 + day)  # 年月日
        # 闰年匹配项
        if int(date_a[0:4]) % 4 == 0 or (int(date_a[0:4]) % 100 == 0 and (int(date_a[0:4]) % 4 == 0)):
            pattern = re.compile('19[0-9]{2}((01|03|05|07|08|10|12)(0[1-9]|[1-2][0-9]|3[0-1])|'
                                 '(04|06|09|11)(0[1-9]|[1-2][0-9]|30)|02(0[1-9]|[1-2][0-9]))$')
        # 平年匹配项
        else:
            pattern = re.compile('19[0-9]{2}((01|03|05|07|08|10|12)(0[1-9]|[1-2][0-9]|3[0-1])|'
                                 '(04|06|09|11)(0[1-9]|[1-2][0-9]|30)|02(0[1-9]|2[0-8]))$')
        if re.match(pattern, date_a):
            id_card = list([pro, ct, area, year, mon, day, sex])
        else:
            id_card = list([pro, ct, area, year, mon, day-3, sex])
        id_cards.append(id_card)
    return id_cards


# 根据多组ID，从网页中生成多组身份证号
def get_id(url):
    content = requests.get(url).content
    soup = BeautifulSoup(content)
    text = soup.find('body').find_all('p')[0].text  # 从生成的身份证号中取第一个（随便哪个都行）
    return text


# 全国500强姓名
def get_name(url):
    content = requests.get(url).content
    soup = BeautifulSoup(content)
    text = soup.find('table', {'cellspacing': '0'}).find_all('tr')
    names = []
    for i in text:
        name = i.find_all('td')[1].text
        names.append(name)
    names.pop(0)
    return names


# 跑起来
if __name__ == '__main__':
    num = 30  # 想得到ID的数量
    id_cc = set_id(num)
    names = get_name(url_name)
    id_cards = []
    for id_card in id_cc:
        url1 = url_id.format(id_card[0], id_card[1], id_card[2], id_card[3], id_card[4], id_card[5],
                          id_card[6])
        # 数据库中某些区域的划分与这个网站不太一样，加try避免出错
        try:
            id_c = get_id(url1)
            id_cards.append(id_c)
        except IndexError:
            pass
    len_id = len(id_cards)
    len_name = len(names)
    name_id = []
    for i in range(len_id):
        x = random.randint(0, len_name-1)
        name = names[x]
        name_id.append(name)
    df = pd.DataFrame({'name': name_id, 'id_card': id_cards}, columns=['name', 'id_card'])
    df.index.name = 'index'
    df.to_csv('d:/id_card_generator.csv', encoding='utf_8_sig')
