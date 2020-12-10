import re

import requests
from lxml import etree
from PIL import Image
import pytesseract
from pymongo import MongoClient
client = MongoClient("127.0.0.1", 27017)
collection = client["ziru"]["ziru"]

url = "http://cd.ziroom.com/z/"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36",
    "Cookie": "CURRENT_CITY_CODE=510100; _csrf=6Ym3AQhXHwQHQ_kIIZgyWF5RLg3k6Mda; sajssdk_2015_cross_new_user=1; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%221764b8fcb7a171-02f0f1f4c38ab2-c791e37-1327104-1764b8fcb7b1af%22%2C%22%24device_id%22%3A%221764b8fcb7a171-02f0f1f4c38ab2-c791e37-1327104-1764b8fcb7b1af%22%2C%22props%22%3A%7B%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%7D; Hm_lvt_4f083817a81bcb8eed537963fc1bbf10=1607585484; gr_user_id=33127cca-2d84-4ec8-a652-a659390997a3; CURRENT_CITY_NAME=%E6%88%90%E9%83%BD; gr_session_id_8da2730aaedd7628=f7c06ef2-e4d4-4944-a12a-114058ca197b; gr_session_id_8da2730aaedd7628_f7c06ef2-e4d4-4944-a12a-114058ca197b=true; visitHistory=%5B%22807759920%22%5D; PHPSESSID=qt72p71jrm3edsphdv3d7kerv6; Hm_lpvt_4f083817a81bcb8eed537963fc1bbf10=1607587933"
}

r = requests.get(url=url, headers=headers)
list02 = []
html = etree.HTML(r.text)
num_location = {"-0px": 0, "-21.4px": 1, "-42.8px": 2, "-64.2px": 3, "-85.6px": 4, "-107px": 5,
                     "-128.4px": 6, "-149.8px ": 7, "-171.2px": 8, "-192.6px": 9}
x0 = html.xpath("//div[@class='item']/div[@class='info-box']")

for item in x0[0:31]:
    dict01 = dict()
    # 标题1
    if len(item.xpath("./h5/a/text()")):
        x1 = item.xpath("./h5/a/text()")
        str_x101 = str(x1).replace("['", "")
        str_x102 = str_x101.replace("']", "")
        str_x103 = str_x102.split("·")[1]
        str_x104 = str_x103.split("-")
        str_x105 = str_x104[0]
        dict01["标题1"] = str_x105
        # print(str_x105)

        # 标题2
        x2 = str_x104[1]
        dict01["标题2"] = x2
        # print(x2)

    # 楼层
    if len(item.xpath("./div[@class='desc']/div[1]/text()")):
        x3 = item.xpath("./div[@class='desc']/div[1]/text()")
        str_x301 = str(x3).replace("['", "")
        str_x302 = str_x301.replace("']", "")
        str_x303 = str_x302.split(" ")[2]
        dict01["楼层"] = str_x303
        # print(str_x303)

    # 附近
    if len(item.xpath(".//div[@class='location']/text()")):
        x4 = item.xpath(".//div[@class='location']/text()")
        str_x401 = str(x4).replace("['", "")
        str_x402 = str_x401.replace("']", "")
        str_x403 = str_x402.replace("\\n\\t", "")
        str_x404 = str_x403.replace("\\t", "")
        str_x405 = str_x404.strip()
        dict01["附近"] = str_x405
        # print(str_x405)

    # 价格
    k = re.search(r'background-image: url\((.*)\)', r.text)
    m = "http:" + k.group(1)

    r_img = requests.get(url=m)
    with open("123.png", "wb") as f_img:
        f_img.write(r_img.content)
    image = Image.open('123.png')
    text = pytesseract.image_to_string(Image.open("123.png"), lang="eng",
                                config="--psm 6 --oem 3 -c tessedit_char_whitelist=1234567890").strip()
    # print(text)
    # z = re.search(r"\);background-position: (.*);", r.text)
    # print(z)

    list01 = []
    for i in text:
        list01.append(i)
    try:
        x5_1 = item.xpath(".//div[@class='price ']/span[2]/@style")
        # print(x5)
        str_x501 = str(x5_1).replace("['", "")
        str_x502 = str_x501.replace("']", "")
        str_x503_1 = str_x502.split(" ")[2]
        # print(str_x503_1)
        x5_2 = item.xpath(".//div[@class='price ']/span[3]/@style")
        # print(x5)
        str_x501 = str(x5_2).replace("['", "")
        str_x502 = str_x501.replace("']", "")
        str_x503_2 = str_x502.split(" ")[2]
        # print(str_x503_2)
        x5_3 = item.xpath(".//div[@class='price ']/span[4]/@style")
        # print(x5)
        str_x501 = str(x5_3).replace("['", "")
        str_x502 = str_x501.replace("']", "")
        str_x503_3 = str_x502.split(" ")[2]
        # print(str_x503_3)
        x5_4 = item.xpath(".//div[@class='price ']/span[5]/@style")
        # print(x5)
        str_x501 = str(x5_4).replace("['", "")
        str_x502 = str_x501.replace("']", "")
        str_x503_4 = str_x502.split(" ")[2]
        # print(str_x503_4)
    except Exception:
        continue
    try:
        price_1 = list01[num_location.get(str_x503_1)]

        price_2 = list01[num_location.get(str_x503_2)]
        price_3 = list01[num_location.get(str_x503_3)]
        price_4 = list01[num_location.get(str_x503_4)]

        mm = price_1+price_2+price_3+price_4
        dict01["价格"] = mm
    except Exception:
        continue

    # print(dict01)
    list02.append(dict01)

collection.insert(list02)




