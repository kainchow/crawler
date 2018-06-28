import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "http://www.xzqy.net"


# 获取省份链接与省份名称
def get_province(url):
    content = requests.get(url).content
    soup = BeautifulSoup(content)
    text = soup.find('div', {'class': 'navi'})
    url_pro = text.find_all('a')
    urls = []
    pros = []
    for i in url_pro:
        try:
            x = i.get('href')
            y = i.text
            urls.append(x)
            pros.append(y)
        except AttributeError:
            pass
    return urls[2:len(urls)], pros[2:len(pros)]


# 获取单个省份的省市区县数据，转换为DataFrame格式
def get_city_area(extr_url, pros):
    content = requests.get(url + extr_url).content
    soup = BeautifulSoup(content)
    text = soup.find('table').find_all('tr')
    all_province = []
    all_city = []
    all_area = []
    for ct in text:
        try:
            city = ct.find('td', {'class': 'parent'}).text
            areas = ct.find_all('td')[1]
            citys = []
            provinces = []
            for area in areas:
                all_area.append(area.text)
                citys.append(city)
                provinces.append(pros)
            for i in citys:
                all_city.append(i)
            for j in provinces:
                all_province.append(j)
        except AttributeError:
            pass
    df = pd.DataFrame({'province': all_province, 'city': all_city, 'area': all_area},
                      columns=['province', 'city', 'area'])
    return df


# 组合所有省份数据
def main():
    urls, pros = get_province(url)
    df = pd.DataFrame()
    for i in range(len(urls)):
        df1 = get_city_area(urls[i], pros[i])
        df = df.append(df1)
        df.index = range(len(df))
    df.to_csv('d:/df.csv')


# 跑起来
if __name__ == '__main__':
    main()
