import csv
import os
import datetime
import requests
from lxml import etree


class Cat(object):
    def __init__(self):
        # 遍历页码
        for i in range(1, 6):
            # 代理
            self.proxies = {
                "http": "http://60.172.85.188:4286",
                "https": "http://60.172.85.188:4286",
            }
            # 路由
            self.url = "https://www.xin.com/suqian/i%s/" % i
            # 伪装
            self.headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36",
                "Cookie": "pif=; RELEASE_KEY=; XIN_anti_uid=0D74369C-F36B-4525-1CFB-55FA37F6DA51; XIN_LOCATION_CITY=%7B%22cityid%22%3A%221520%22%2C%22cityname%22%3A%22%5Cu5bbf%5Cu8fc1%22%2C%22ename%22%3A%22suqian%22%2C%22service%22%3A%221%22%2C%22zhigou%22%3A%221%22%2C%22is_visit%22%3A%221%22%2C%22city_rank%22%3A%22100%22%2C%22is_gold_partner%22%3A%22-1%22%2C%22direct_rent_support%22%3A%221%22%2C%22is_wz_mortgage%22%3A%221%22%7D; uid=CvQmd1/RiMSboQAQE+CPAg==; XIN_UID_CK=58247cf3-b905-72da-1dde-a91b4f99a16b; Hm_lvt_ae57612a280420ca44598b857c8a9712=1607567559; SEO_SOURCE=https://www.xin.com/suqian/i1/; SEO_REF=https://www.xin.com/suqian/i1/; session_xin=tp2kp95b5gs8u50hanv9nicqv1nke76m; acw_tc=9963f82816075695383252503ec14516459ba80b44221cdfd22644a68c; acw_sc__v2=5fd19086e2fd115e0291272affdc50398b6d7820; Hm_lpvt_ae57612a280420ca44598b857c8a9712=1607569544; SERVERID=b13028cd19ef1711d5f40612dd61793a|1607569545|1607567556"
            }
            self.dict01 = dict()
            self.get_requests()

    def get_requests(self):
        # 获取网页
        r = requests.get(url=self.url, headers=self.headers, proxies=self.proxies)
        # 获取网页text数据
        html = etree.HTML(r.text)
        # 获取网页大框架数据
        x0 = html.xpath("//ul/li[@class='con caritem conHeight']")

        # 遍历网页大框架数据
        for item in x0:
            # 使用xpath和字符串操作获取指定数据
            # 标题
            x1 = item.xpath(".//div[@class='pad']/h2/span/text()") if len(
                item.xpath(".//div[@class='pad']/h2/span/text()")) > 0 else None
            str_x101 = str(x1)
            str_x102 = str_x101.replace("['", "")
            str_x103 = str_x102.replace("']", "")
            # 汽车品牌
            self.path_cat = str_x103.split(" ")[0] + '/'
            # 汽车系列
            self.path_cat_set = str_x103.split(" ")[1]

            # 年份
            x2 = item.xpath(".//div[@class='pad']/span/text()")[0] if len(
                item.xpath(".//div[@class='pad']/span/text()")[0]) > 0 else None
            str_x201 = str(x2).strip()
            str_x202 = str_x201.replace("年", "")

            # 价格
            x3 = item.xpath(".//div[@class='pad']/p/em/text()") if len(
                item.xpath(".//div[@class='pad']/p/em/text()")) > 0 else None
            str_x301 = str(x3)
            str_x302 = str_x301.replace("['", "")
            str_x303 = str_x302.replace("']", "")
            str_x304 = str_x303.replace("\\n", "")
            str_x305 = str_x304.replace("万", "").strip()

            # 图片
            x4 = item.xpath("./@data-img") if len(
                item.xpath("./@data-img")) > 0 else None
            str_x401 = str(x4).replace("['", "").strip()
            str_x402 = str_x401.replace("']", "")

            # 爬取日期
            i = datetime.datetime.now()
            date = "%s年%s月%s日" % (i.year, i.month, i.day)

            # 写入字典
            self.dict01["标题"] = str_x103
            self.dict01["年份"] = str_x202
            self.dict01["价格"] = str_x305
            self.dict01["图片"] = str_x402
            self.dict01["爬取日期"] = date
            print(self.dict01)

            # 创建主文件夹路径
            self.file_path = os.getcwd() + './优信二手车/'
            # 如果文件夹不存在
            if not os.path.exists(self.file_path):
                # 创建文件夹
                os.makedirs(self.file_path)
            # 创建主文件夹路径
            self.file_path_cat = os.getcwd() + './优信二手车/' + self.path_cat
            # 如果文件夹不存在
            if not os.path.exists(self.file_path_cat):
                # 创建文件夹
                os.makedirs(self.file_path_cat)
            # 创建主文件夹路径
            self.file_path_cat_images = os.getcwd() + './优信二手车/' + self.path_cat + 'images/'
            # 如果文件夹不存在
            if not os.path.exists(self.file_path_cat_images):
                # 创建文件夹
                os.makedirs(self.file_path_cat_images)
            self.file_csv()
        print("保存成功")

    def file_csv(self):
        # 创建汽车系列csv
        with open(self.file_path_cat + self.path_cat_set + ".csv", "a+") as f:
            self.csv_f = csv.writer(f)
            # 写入汽车数据
            self.csv_f.writerow(self.dict01.values())

        # 下载图片
        with open(self.file_path_cat_images + self.dict01["标题"] + ".jpg", "wb") as f_img:
            # 请求图片数据
            r_img = requests.get(url="http:" + self.dict01["图片"])
            # 开始下载图片
            f_img.write(r_img.content)


cat = Cat()
