# -*- coding: utf-8 -*-
import requests
from lxml import etree
import random
from time import sleep
import pymysql

# 经测试，以下都是可用的代理（仅测试了大众点评网）
user_agent = ['User-Agent:Mozilla/5.0(Macintosh;U;IntelMacOSX10_6_8;en-us)AppleWebKit/534.50(KHTML,likeGecko)Version/5.1Safari/534.50',
			  'User-Agent:Mozilla/5.0(Windows;U;WindowsNT6.1;en-us)AppleWebKit/534.50(KHTML,likeGecko)Version/5.1Safari/534.50',
			  'User-Agent:Mozilla/5.0(Macintosh;IntelMacOSX10.6;rv:2.0.1)Gecko/20100101Firefox/4.0.1',
			  'User-Agent:Opera/9.80(Macintosh;IntelMacOSX10.6.8;U;en)Presto/2.8.131Version/11.11',
			  'User-Agent:Mozilla/5.0(Macintosh;IntelMacOSX10_7_0)AppleWebKit/535.11(KHTML,likeGecko)Chrome/17.0.963.56Safari/535.11',
			  'User-Agent:Mozilla/4.0(compatible;MSIE7.0;WindowsNT5.1;Trident/4.0;SE2.XMetaSr1.0;SE2.XMetaSr1.0;.NETCLR2.0.50727;SE2.XMetaSr1.0)',
			  'User-Agent:Mozilla/5.0(iPhone;U;CPUiPhoneOS4_3_3likeMacOSX;en-us)AppleWebKit/533.17.9(KHTML,likeGecko)Version/5.0.2Mobile/8J2Safari/6533.18.5',
			  'User-Agent:Mozilla/5.0(iPod;U;CPUiPhoneOS4_3_3likeMacOSX;en-us)AppleWebKit/533.17.9(KHTML,likeGecko)Version/5.0.2Mobile/8J2Safari/6533.18.5',
			  'User-Agent:Mozilla/5.0(iPad;U;CPUOS4_3_3likeMacOSX;en-us)AppleWebKit/533.17.9(KHTML,likeGecko)Version/5.0.2Mobile/8J2Safari/6533.18.5',
			  'User-Agent:Mozilla/5.0(Linux;U;Android2.3.7;en-us;NexusOneBuild/FRF91)AppleWebKit/533.1(KHTML,likeGecko)Version/4.0MobileSafari/533.1',
			  'User-Agent:MQQBrowser/26Mozilla/5.0(Linux;U;Android2.3.7;zh-cn;MB200Build/GRJ22;CyanogenMod-7)AppleWebKit/533.1(KHTML,likeGecko)Version/4.0MobileSafari/533.1',
			  'User-Agent:Mozilla/5.0(Linux;U;Android3.0;en-us;XoomBuild/HRI39)AppleWebKit/534.13(KHTML,likeGecko)Version/4.0Safari/534.13',
			  'User-Agent:Mozilla/5.0(BlackBerry;U;BlackBerry9800;en)AppleWebKit/534.1+(KHTML,likeGecko)Version/6.0.0.337MobileSafari/534.1+',
			  'User-Agent:Mozilla/5.0(hp-tablet;Linux;hpwOS/3.0.0;U;en-US)AppleWebKit/534.6(KHTML,likeGecko)wOSBrowser/233.70Safari/534.6TouchPad/1.0',
			  'User-Agent:Mozilla/5.0(SymbianOS/9.4;Series60/5.0NokiaN97-1/20.0.019;Profile/MIDP-2.1Configuration/CLDC-1.1)AppleWebKit/525(KHTML,likeGecko)BrowserNG/7.1.18124',
			  'User-Agent:Mozilla/5.0(compatible;MSIE9.0;WindowsPhoneOS7.5;Trident/5.0;IEMobile/9.0;HTC;Titan)',
			  'User-Agent:UCWEB7.0.2.37/28/999',
			  'User-Agent:NOKIA5700/UCWEB7.0.2.37/28/999',
			  'User-Agent:Openwave/UCWEB7.0.2.37/28/999']
user_agent2 = ['Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 OPR/26.0.1656.60',
			   'Opera/8.0 (Windows NT 5.1; U; en)',
			   'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36',
			   'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36',
			   'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
			   'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 SE 2.X MetaSr 1.0',
			   'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Maxthon/4.4.3.4000 Chrome/30.0.1599.101 Safari/537.36',
			   'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 UBrowser/4.0.3214.0 Safari/537.36',
			   'Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5',
			   'Mozilla/5.0 (iPod; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5',
			   'Mozilla/5.0 (iPad; U; CPU OS 4_2_1 like Mac OS X; zh-cn) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5',
			   'Mozilla/5.0 (iPad; U; CPU OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5',
			   'Mozilla/5.0 (Linux; U; Android 2.2.1; zh-cn; HTC_Wildfire_A3333 Build/FRG83D) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1',
			   'Mozilla/5.0 (Linux; U; Android 2.3.7; en-us; Nexus One Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1',
			   'MQQBrowser/26 Mozilla/5.0 (Linux; U; Android 2.3.7; zh-cn; MB200 Build/GRJ22; CyanogenMod-7) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1',
			   'Opera/9.80 (Android 2.3.4; Linux; Opera Mobi/build-1107180945; U; en-GB) Presto/2.8.149 Version/11.10',
			   'Mozilla/5.0 (Linux; U; Android 3.0; en-us; Xoom Build/HRI39) AppleWebKit/534.13 (KHTML, like Gecko) Version/4.0 Safari/534.13',
			   'Mozilla/5.0 (BlackBerry; U; BlackBerry 9800; en) AppleWebKit/534.1+ (KHTML, like Gecko) Version/6.0.0.337 Mobile Safari/534.1+',
			   'Mozilla/5.0 (hp-tablet; Linux; hpwOS/3.0.0; U; en-US) AppleWebKit/534.6 (KHTML, like Gecko) wOSBrowser/233.70 Safari/534.6 TouchPad/1.0',
			   'Mozilla/5.0 (SymbianOS/9.4; Series60/5.0 NokiaN97-1/20.0.019; Profile/MIDP-2.1 Configuration/CLDC-1.1) AppleWebKit/525 (KHTML, like Gecko) BrowserNG/7.1.18124',
			   'Mozilla/5.0 (compatible; MSIE 9.0; Windows Phone OS 7.5; Trident/5.0; IEMobile/9.0; HTC; Titan)',
			   'UCWEB7.0.2.37/28/999',
			   'NOKIA5700/ UCWEB7.0.2.37/28/999',
			   'Openwave/ UCWEB7.0.2.37/28/999']


area_url_main = "http://www.dianping.com/guangzhou/ch10/r24"
proxies = {'http': 'http://61.160.190.147:8090'}

con = pymysql.connect(user='root', password='123456', db='crawler', charset='utf8')
cur = con.cursor()
sql_create = '''
				create table dianping2(
				`name` varchar(255) not null,
				`phone` varchar(255) not null);
'''
try:
	cur.execute(sql_create)
except:
	pass
sql_insert = '''
				insert into dianping2(`name`, `phone`) values (%s, %s)
'''

# 每个行政区的链接
def get_area_urls():
	text = requests.get(area_url_main, headers={'User-Agent': random.choice(user_agent)}).text
	response = etree.HTML(text)
	area_urls = response.xpath('//*[@id="region-nav"]/a/@href')
	print('区域链接爬取完毕！')
	print(area_urls[0] + '\n')
	return area_urls

# 行政区下每个商圈的链接
def get_buss_dist_url():
	urls = get_area_urls()
	buss_dist_urls = []
	for url in urls:
		text = requests.get(url, headers={'User-Agent': random.choice(user_agent)}).text
		response = etree.HTML(text)
		area_urls = response.xpath('//*[@id="region-nav-sub"]/a/@href')
		area_urls.pop(0)
		buss_dist_urls.extend(area_urls)
	print('商圈链接爬取完毕！')
	print(buss_dist_urls[0] + '\n')
	return buss_dist_urls

# 商圈下所有商家的链接
def get_urls(url, page):
	urls = []
	for i in range(1, page+1):
		text = requests.get(url+'p%s'%str(i), headers={'User-Agent': random.choice(user_agent)}).text
		response = etree.HTML(text)
		one_page_urls = response.xpath('//*[@id="shop-all-list"]/ul/li/div[2]/div[1]/a[1]/@href')
		urls.extend(one_page_urls)
		sleep(random.random() * 4)
		print('第%s页链接爬取完毕！' % str(i))
	return urls

# 商家的店名和手机号
def get_shop_phone(all_urls):
	i = 1
	for url in all_urls:
		try:
			text = requests.get(url, headers={'User-Agent': random.choice(user_agent)}).text
			response = etree.HTML(text)
		except:
			print('代理错误！')
		else:
			try:
				name = response.xpath('//*[@id="basic-info"]/h1/text()')[0].strip()
			except IndexError:
				name = ''
			try:
				phones = response.xpath('//*[@id="basic-info"]/p/span/text()')
				phone = [x for x in phones if len(x) == 11][0]
			except:
				phone = ''
			cur.execute(sql_insert, (name, phone))
			con.commit()
			sleep(random.random() * 3)
			print('第%s条数据已爬取！' % str(i))
			i += 1

# 获取商圈的最大页码
def get_max_page(url):
	text = requests.get(url, headers={'User-Agent': random.choice(user_agent)}).text
	response = etree.HTML(text)
	pages = response.xpath('/html/body/div[2]/div[3]/div[1]/div[2]/a/text()')
	max_page = pages[-2]
	return max_page

if __name__ == '__main__':
	buss_dist_urls = get_buss_dist_url()  # 所有商圈链接
	print('所有商圈数量：%s' % str(len(buss_dist_urls)) + '\n')
	for url in buss_dist_urls:
		max_page = int(get_max_page(url))
		urlx = get_urls(url, max_page)
		get_shop_phone(urlx)
		print('此商圈爬取完毕，休息一会!\n')
		sleep(random.random() * 20)
	# with open('d:/urls.txt', 'w', encoding='utf8') as f:
	# 	f.write(str(urlx))
	# df = pd.DataFrame({'shop': all_shops, 'phone': all_phones})
	# df.to_csv('d:/dianping.csv', index=False)
	print('所有数据均已导入库！')
