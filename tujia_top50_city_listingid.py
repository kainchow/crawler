# -*- coding:utf-8 -*-
import requests
import pymysql
import re

con = pymysql.connect(host='MYSQL5005.webweb.com', user='138e1b2_24', password='zhoukai0607', db='test', charset='utf8mb4')
cur = con.cursor()

headers = {'Accept': 'application/json, text/javascript, */*; q=0.01',
 'Accept-Encoding': 'gzip, deflate, br',
 'Accept-Language': 'zh-CN,zh;q=0.9',
 'Connection': 'keep-alive',
 'Cookie': 'tujia.com_PortalContext_UserId=0; tujia.com_PortalContext_RefUrl=https://www.tujia.com/; tujia.com_PortalContext_LongerRefUrl=https://www.tujia.com/; tujia.com_PortalContext_GuestToken=13a87ba9-2a43-45bf-ba1d-124c8ff63ab7; tujia.com_PortalContext_GuestId=-736837281; tujia.com_PortalContext_LandingUrl=http://www.tujia.com/api/pchome/homepage; tujia.com_PortalContext_GuestCount=0; tujia.com_PortalContext_BedCount=0; tujia.com_PortalContext_RoomCount=0; _ga=GA1.2.2053008939.1527688726; _gid=GA1.2.501422731.1527688726; Hm_lvt_405c96e7f6bed44fb846abfe1f65c6f5=1527688726; Hm_lpvt_405c96e7f6bed44fb846abfe1f65c6f5=1527688726; qimo_seosource_797098a0-b29d-11e5-b3b1-49764155fe50=%E7%AB%99%E5%86%85; qimo_seokeywords_797098a0-b29d-11e5-b3b1-49764155fe50=; accessId=797098a0-b29d-11e5-b3b1-49764155fe50; pageViewNum=1; gr_user_id=34316da5-e660-4dd1-87ae-53f790d53db2; gr_cs1_25264967-da34-4ab9-8372-f62c711192ea=user_id%3A0; gr_session_id_1fa38dc3b3e047ffa08b14193945e261=25264967-da34-4ab9-8372-f62c711192ea_true; bad_id797098a0-b29d-11e5-b3b1-49764155fe50=7f17adc1-6411-11e8-89fb-6174749c48c2; nice_id797098a0-b29d-11e5-b3b1-49764155fe50=7f17adc2-6411-11e8-89fb-6174749c48c2; manualclose=1',
 'Host': 'www.tujia.com',
 'Referer': 'https://www.tujia.com/',
 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
 'X-Requested-With': 'XMLHttpRequest'}


url = "https://www.tujia.com/api/pccity/cityinforguonei"
response = requests.post(url, headers=headers)
