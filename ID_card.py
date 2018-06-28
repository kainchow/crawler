# -*- coding: utf-8 -*-
import pandas as pd
import requests
from bs4 import BeautifulSoup


'''def checkIdcard(idcard):
    done = ['验证通过！']
    Errors = ['身份证号码位数不对！', '身份证号码出生日期超出范围或包含非法字符！', '身份证号码校验错误！',
              '身份证地区非法！']
    area = {"11": "北京", "12": "天津", "13": "河北", "14": "山西", "15": "内蒙古", "21": "辽宁",
            "22": "吉林", "23": "黑龙江", "31": "上海", "32": "江苏", "33": "浙江", "34": "安徽",
            "35": "福建", "36": "江西", "37": "山东", "41": "河南", "42": "湖北","43": "湖南",
            "44": "广东", "45": "广西", "46": "海南", "50": "重庆", "51": "四川", "52": "贵州",
            "53": "云南", "54": "西藏","61": "陕西", "62": "甘肃", "63": "青海", "64": "宁夏",
            "65": "新疆", "71": "台湾", "81": "香港", "82": "澳门", "91": "国外"}
    idcard = str(idcard)
    idcard = idcard.strip()
    idcard_list = list(idcard)

    # 地区校验
    if not area[idcard[0:2]]:
        print(Errors[3])
    # 15位身份证号码检测
    if len(idcard) == 15:
        if (int(idcard[6:8])+1900) % 4 == 0 or ((int(idcard[6:8]) + 1900) % 100 == 0 and
                                                            (int(idcard[6:8]) + 1900) % 4 == 0):
            # 闰年出生
            ereg = re.compile('[1-9][0-9]{5}[0-9]{2}((01|03|05|07|08|10|12)(0[1-9]|[1-2][0-9]|3[0-1])|'
                              '(04|06|09|11)(0[1-9]|[1-2][0-9]|30)|02(0[1-9]|[1-2][0-9]))[0-9]{3}$')
        else:
            # 平年出生
            ereg = re.compile('[1-9][0-9]{5}[0-9]{2}((01|03|05|07|08|10|12)(0[1-9]|[1-2][0-9]|3[0-1])|'
                              '(04|06|09|11)(0[1-9]|[1-2][0-9]|30)|02(0[1-9]|1[0-9]|2[0-8]))[0-9]{3}$')
        if re.match(ereg, idcard):
            print(done)
        else:
            print(Errors[1])

    # 18位身份证号码检测
    elif len(idcard) == 18:
        if int(idcard[6:10]) % 4 == 0 or (int(idcard[6:10]) % 100 == 0 and
                                                              (int(idcard[6:10]) % 4 == 0)):
            # 闰年出生
            ereg = re.compile('[1-9][0-9]{5}(19[0-9]{2}|20[0-9]{2})((01|03|05|07|08|10|12)(0[1-9]|[1-2]'
                              '[0-9]|3[0-1])|(04|06|09|11)(0[1-9]|[1-2][0-9]|30)|02(0[1-9]|[1-2]'
                              '[0-9]))[0-9]{3}[0-9Xx]$')
        else:
            # 平年出生
            ereg = re.compile('[1-9][0-9]{5}(19[0-9]{2}|20[0-9]{2})((01|03|05|07|08|10|12)(0[1-9]|[1-2]'
                              '[0-9]|3[0-1])|(04|06|09|11)(0[1-9]|[1-2][0-9]|30)|02(0[1-9]|2[0-8]))'
                              '[0-9]{3}[0-9Xx]$')
        # 测试出生日期的合法性
        if re.match(ereg, idcard):
            # 计算校验位
            S = (int(idcard_list[0]) + int(idcard_list[10])) * 7 + (int(idcard_list[1]) + int(idcard_list[11])) * 9 + (int(idcard_list[2]) + int(idcard_list[12])) * 10 + (int(idcard_list[3]) + int(idcard_list[13])) * 5 + (int(idcard_list[4]) + int(idcard_list[14])) * 8 + (int(idcard_list[5]) + int(idcard_list[15])) * 4 + (int(idcard_list[6]) + int(idcard_list[16])) * 2 + int(idcard_list[7]) * 1 + int(idcard_list[8]) * 6 + int(idcard_list[9]) * 3
            Y = S % 11
            M = "F"
            JYM = "10X98765432"
            M = JYM[Y]
            if M == idcard_list[17]:
                print(done)
            else:
                print(Errors[2])
        else:
            print(Errors[1])
    else:
        print(Errors[0])'''


def get_message():
    df = pd.read_csv("d:/id_card_generator.csv")
    df.drop('index', axis=1, inplace=True)
    idcards = list(df['id_card'])
    genders = []
    births = []
    adds = []
    for idcard in idcards:
        url = "http://qq.ip138.com/idsearch/index.asp?action=idcard&userid=" + str(idcard) + \
          "&B1=%B2%E9+%D1%AF"
        content = requests.get(url).content
        soup = BeautifulSoup(content)
        mes = soup.find_all('td', {'class': 'tdc2'})
        gender = mes[0].text
        birth = mes[1].text
        add = mes[2].text
        genders.append(gender)
        births.append(birth)
        adds.append(add)
    province = []
    city = []
    area = []
    for add in adds:
        province.append(add.split()[0])
        city.append(add.split()[1])
        area.append(add.split()[2])
    id_df = pd.DataFrame({'name': df['name'], 'gender': genders, 'birth': births, 'province': province,
                          'city': city, 'area': area}, columns=['name', 'gender', 'birth', 'province',
                                                                'city', 'area'])
    id_df.index.name = 'index'
    return id_df


if __name__ == '__main__':
    '''while True:
        cdcard = input(u"请输入你的身份证号：")
        if cdcard == 'exit':
            print(u"程序已结束！")
            break
        else:
            # checkIdcard(cdcard)'''
    id_df = get_message()
    id_df.to_csv("d:/id_df.csv", encoding='utf_8_sig')
