import csv
import os

import requests
from lxml import etree
import time

# 分类路由
url_dict = {
    # 城市建设
    "城市建设": "http://27.223.1.57:10000/PythonApplication/webbasesite/dataInfoList.aspx?lkocok_pageNo=%s&oneClassGuid=171030103404278262",
    # 城市管理
    "城市管理": "http://27.223.1.57:10000/PythonApplication/webbasesite/dataInfoList.aspx?lkocok_pageNo=%s&oneClassGuid=171030103404322242",
    # 公共事业
    "公共事业": "http://27.223.1.57:10000/PythonApplication/webbasesite/dataInfoList.aspx?lkocok_pageNo=%s&oneClassGuid=171030103404382666",
    # 公安管理
    "公安管理": "http://27.223.1.57:10000/PythonApplication/webbasesite/dataInfoList.aspx?lkocok_pageNo=%s&oneClassGuid=171030103404436851",
    # 交通运输
    "交通运输": "http://27.223.1.57:10000/PythonApplication/webbasesite/dataInfoList.aspx?lkocok_pageNo=%s&oneClassGuid=171030103404510243",
    # 工商管理
    "工商管理": "http://27.223.1.57:10000/PythonApplication/webbasesite/dataInfoList.aspx?lkocok_pageNo=%s&oneClassGuid=171030103404582156",
    # 人事管理
    "人事管理": "http://27.223.1.57:10000/PythonApplication/webbasesite/dataInfoList.aspx?lkocok_pageNo=%s&oneClassGuid=171030103404628407",
    # 劳动保障
    "劳动保障": "http://27.223.1.57:10000/PythonApplication/webbasesite/dataInfoList.aspx?lkocok_pageNo=%s&oneClassGuid=171030103404697373",
    # 国土房产
    "国土房产": "http://27.223.1.57:10000/PythonApplication/webbasesite/dataInfoList.aspx?lkocok_pageNo=%s&oneClassGuid=171030103404763407",
    # 公共教育
    "公共教育": "http://27.223.1.57:10000/PythonApplication/webbasesite/dataInfoList.aspx?lkocok_pageNo=%s&oneClassGuid=171030103404851431",
    # 医疗卫生
    "医疗卫生": "http://27.223.1.57:10000/PythonApplication/webbasesite/dataInfoList.aspx?lkocok_pageNo=%s&oneClassGuid=171030103404897858",
    # 环境保护
    "环境保护": "http://27.223.1.57:10000/PythonApplication/webbasesite/dataInfoList.aspx?lkocok_pageNo=%s&oneClassGuid=171030103404941153",
    # 民政事务
    "民政事务": "http://27.223.1.57:10000/PythonApplication/webbasesite/dataInfoList.aspx?lkocok_pageNo=%s&oneClassGuid=171030103404986805",
    # 文化出版
    "文化出版": "http://27.223.1.57:10000/PythonApplication/webbasesite/dataInfoList.aspx?lkocok_pageNo=%s&oneClassGuid=171030103405072771",
    # 税务管理
    "税务管理": "http://27.223.1.57:10000/PythonApplication/webbasesite/dataInfoList.aspx?lkocok_pageNo=%s&oneClassGuid=171030103405121431",
    # 农村事务
    "农村事务": "http://27.223.1.57:10000/PythonApplication/webbasesite/dataInfoList.aspx?lkocok_pageNo=%s&oneClassGuid=171030103405170688",
    # 海洋渔业
    "海洋渔业": "http://27.223.1.57:10000/PythonApplication/webbasesite/dataInfoList.aspx?lkocok_pageNo=%s&oneClassGuid=171030103405276446",
    # 林业水利
    "林业水利": "http://27.223.1.57:10000/PythonApplication/webbasesite/dataInfoList.aspx?lkocok_pageNo=%s&oneClassGuid=171030103405315500"

}
# 遍历路由字典中的key and valve
for url_k, url_v in url_dict.items():
    # 遍历页数
    for i in range(1, 6):
        url = url_v % i
        # 伪装
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36",
            "Cookie": "ASP.NET_SessionId=v2rzyofgdek34z04wbq4esk2"
        }
        # 获取网页
        r = requests.get(url=url, headers=headers)
        # 获取网页的text数据
        html = etree.HTML(r.text)
        # 指定数据
        x0 = html.xpath("//tr/td/table/tbody/tr")
        # 设置一个装数据的字典
        dict01 = dict()
        # 创建文件夹路径
        file_path = os.getcwd() + './青岛问政/'
        # 如果文件夹不存在
        if not os.path.exists(file_path):
            # 创建文件夹
            os.makedirs(file_path)
        # 创建csv文件
        with open(file_path + url_k + ".csv", "a+", encoding="utf-8", newline="") as f:
            # headers
            fieldnames = ["序号", "诉求", "诉求时间", "回复时间"]
            # 创建headers
            f_csv = csv.DictWriter(f, fieldnames=fieldnames)
            # 写入
            f_csv.writeheader()
            # 遍历获取到的是指定数据
            for item in x0[1:]:
                # 开始使用xpath获取
                # 序号  (多出一个)
                x1 = item.xpath("./td[@width='50']/text()")
                str_x101 = str(x1).replace("['", "")
                str_x102 = str_x101.replace("']", "")

                # 诉求
                x2 = item.xpath("./td[2]/@title")
                str_x201 = str(x2).replace("['", "")
                str_x202 = str_x201.replace("']", "")
                str_x203 = str_x202.replace("\\n", "")
                str_x204 = str_x203.replace("\\r", "")
                str_x205 = str_x204.replace("\\t", "")
                str_x206 = str_x205.replace("\\\\", "")
                str_x207 = str_x206.replace("\\xa0", "")

                # 诉求时间
                x3 = item.xpath("./td[3]/text()")
                str_x301 = str(x3).replace("['", "")
                str_x302 = str_x301.replace("']", "")

                # 回复时间
                x4 = item.xpath("./td[4]/text()")
                str_x401 = str(x4).replace("['", "")
                str_x402 = str_x401.replace("']", "")

                # print(str_x102, str_x202,str_x302,str_x402)
                # 将获取到的数据放入字典
                dict01['序号'] = str_x102
                dict01['诉求'] = str_x207
                dict01['诉求时间'] = str_x302
                dict01['回复时间'] = str_x402
                print(dict01)
                # 将字典写入csv文件中
                f_csv.writerow(dict01)
    # time.sleep(3)
