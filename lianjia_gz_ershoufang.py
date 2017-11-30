# -*- coding: utf-8 -*-
import re  # 正则大法好
import requests  # 请求http，也可用urllib
from lxml import etree  # 使用xpath方式获取信息, 也可用bs4
import pandas as pd  # 结构化数据，方便导出csv
import datetime  # 看程序多久跑完
# import pymysql  # 链接MySQL

# 定义请求头，不然爬不了链家
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/'
                         '62.0.3202.94 Safari/537.36'}
# 数据库连接
# con = pymysql.connect(db='crawler', user='root', password='123456', charset='utf8')
# cur = con.cursor()


# 定义一个Lianjia类，用来获取链家所有的数据
class Lianjia(object):

    def __init__(self):
        self.url = "https://gz.lianjia.com/ershoufang/"  # 二手房网站
        self.url_bash = "https://gz.lianjia.com"  # 广州链家主网站
        self.headers = headers  # 需要外部的headers

    # 用于获得每个区域的名字和二级链接
    def get_area_url_name(self):
        url = self.url
        html = requests.post(url, headers=self.headers).text  # 使用post方式请求
        selector = etree.HTML(html)  # 解析网页
        areas = selector.xpath('//div[@data-role="ershoufang"]/div/a/text()')  # 区域名称
        urls = selector.xpath('//div[@data-role="ershoufang"]/div/a/@href')  # 不完整的区域链接
        return urls, areas

    # 用于获取每个区域的某一页二手房信息
    def get_area_one_house(self, url_area, page):
        url = self.url_bash + url_area  # 拼接网页，得到完整的区域链接
        url_page = url + 'pg%s' % str(page + 1)  # 某个区域某一页的链接
        html = requests.post(url_page, headers=self.headers).text  # 请求某个区域某一页的链接
        selector = etree.HTML(html)  # 解析

        lianjia_data = dict()
        try:
            li = selector.xpath('//ul[@class="sellListContent"]/li[@class="clear"]')[0]
            lianjia_data['introduction'] = li.xpath('//div[@class="info clear"][1]/div[@class="title"]/a/text()')  # 简介
            lianjia_data['url'] = li.xpath('//div[@class="info clear"][1]/div[@class="title"]/a/@href')  # 每个房子的链接
            lianjia_data['community'] = li.xpath('//div[@class="houseInfo"]/a/text()')  # 小区
            descriptions = li.xpath('//div[@class="houseInfo"]/text()')  # 户型、面积、朝向、装修、有无电梯
            floors = li.xpath('//div[@class="positionInfo"]/text()')  # 楼层、年限
            lianjia_data['street'] = li.xpath('//div[@class="positionInfo"]/a/text()')  # 街道
            freq = li.xpath('//div[@class="followInfo"]/text()')  # 关注人数、带看人次，发布时间
            lianjia_data['price'] = li.xpath('//div[@class="totalPrice"]/span/text()')  # 价格，单位：万
            lianjia_data['unit_price'] = li.xpath('//div[@class="unitPrice"]/span/text()')  # 单价

            # descriptions每个列表包括五类，将其拆分
            lianjia_data['room_type'] = [i.split(' | ')[1] for i in descriptions]  # 户型
            lianjia_data['acreage'] = [i.split(' | ')[2] for i in descriptions]  # 面积
            lianjia_data['toward'] = [i.split(' | ')[3] for i in descriptions]  # 朝向
            lianjia_data['decoration'] = [i.split(' | ')[4] for i in descriptions]  # 装修情况
            # 有无电梯这一项可能什么也没有，会得到索引错误的信息，判断descriptions每一项长度是否为6，不是则使用'-'代替
            lianjia_data['elevator'] = [i.split(' | ')[5] if len(i.split(' | ')) == 6 else '-' for i in descriptions]  # 有无电梯

            # floors每个列表包括两类，将其拆分
            lianjia_data['floor'] = [i.replace('-', '').strip().split(')')[0] + ')' if ')' in i else
                                     i.replace('-', '').strip().split('层')[0] + '层' for i in floors]  # 楼层
            lianjia_data['year'] = [i.replace('-', '').strip().split(')')[1] if ')' in i else
                                    i.replace('-', '').strip().split('层')[1] + '层' for i in floors]  # 年限

            # freq每个列表包括两类，将其拆分
            lianjia_data['follow'] = [i.split(' / ')[0] for i in freq]  # 关注人数
            lianjia_data['visit'] = [i.split(' / ')[1] for i in freq]  # 带看人次
            lianjia_data['release_time'] = [i.split(' / ')[2] for i in freq]  # 发布时间
        except IndexError as e:
            print(e)
        return lianjia_data

    # 用于获取每个区域的所有二手房信息
    def get_area_all_house(self, url_area, area):
        url = self.url_bash + url_area
        html = requests.post(url, headers=self.headers).text  # 请求某个区域某一页的链接
        selector = etree.HTML(html)  # 解析
        max_pages = selector.xpath('//div[@class="page-box fr"]/div/@page-data')[0]  # 此区域最大页面数
        pattern = '{"totalPage":(.*?),"curPage":1}'  # 正则字符串
        max_page = re.findall(pattern, max_pages)[0]  # 使用正则表达式得到最大页码数字，以备后用
        lianjia_area_data = pd.DataFrame()
        for page in range(int(max_page)):
            lianjia_data = self.get_area_one_house(url_area, page)
            df = pd.DataFrame(lianjia_data, columns=['url', 'introduction', 'community', 'room_type', 'acreage',
                                                     'toward', 'decoration', 'elevator', 'floor', 'year', 'street',
                                                     'follow', 'visit', 'release_time', 'price', 'unit_price'])
            lianjia_area_data = lianjia_area_data.append(df)
            print('已爬取%s区第%s页。' % (area, page+1))
        return lianjia_area_data

    def get_all_house(self):
        start_time = datetime.datetime.now()  # 爬取开始的时间
        urls, areas = self.get_area_url_name()
        lianjia_area_datas = pd.DataFrame()
        # 遍历每一个区域
        for i in range(len(urls)):
            lj_data = self.get_area_all_house(urls[i], areas[i])
            lj_data['area'] = areas[i]
            lianjia_area_datas = lianjia_area_datas.append(lj_data)
            print(areas[i] + '区所有数据已爬取！\n')
        end_time = datetime.datetime.now()  # 爬取结束的时间
        run_time = (end_time - start_time).seconds  # 爬取总时间
        print('共计%s条数据。' % len(lianjia_area_datas))
        print('用时%s秒。' % run_time)
        return lianjia_area_datas


if __name__ == '__main__':
    lj = Lianjia()
    lianjia_area_datas = lj.get_all_house()
    columns = ['area', 'street', 'community', 'introduction', 'room_type', 'acreage', 'price', 'unit_price', 'toward',
               'decoration', 'elevator', 'floor', 'year', 'follow', 'visit', 'release_time', 'url']
    lianjia_area_datas = lianjia_area_datas.reindex(columns=columns)  # 将数据列重新排序
    lianjia_area_datas.index = range(len(lianjia_area_datas))  # 将DataFrame的index从0开始排
    lianjia_area_datas.to_csv('d:/lianjia_gz_ershoufang.csv')
