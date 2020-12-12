import asyncio

from lxml import etree
from pyppeteer import launch

width, height = 1366, 768


class Hangban(object):
    async def main(self):
        browser = await launch(headless=False, args=['--disable-infobars', f'--window-size={width},{height}'])
        page = await browser.newPage()
        await page.setViewport({'width': width, 'height': height})
        await page.goto('https://flight.qunar.com/')
        # 一些网站主要通过 window.navigator.webdriver 来对 webdriver 进行检测，所以我们只需要使用 JavaScript 将它设置为 false 即可
        await page.evaluateOnNewDocument('() =>{ Object.defineProperties(navigator,'
                                         '{ webdriver:{ get: () => false } }) }')
        await asyncio.sleep(2)
        await page.type('#dfsForm > div.crl_sp_city > div:nth-child(2) > div > input', input('输入出发地：'))
        await asyncio.sleep(1)
        await page.type('#dfsForm > div.crl_sp_city > div:nth-child(3) > div > input', input('输入目的地：'))
        await asyncio.sleep(1)
        await page.evaluate('document.querySelector("#fromDate").value=""')
        await page.type('#fromDate', input('请输入出发时间（xxxx-xx-xx）：'))
        await asyncio.sleep(2)
        # 点击搜索
        await page.click('#dfsForm > div.crl_sp_action > button')
        while True:
            await asyncio.sleep(3)
            content = await page.content()
            html = etree.HTML(content)
            # 执行数据处理函数
            self.gei_hangban(html)
            if await page.xpath("//div[@class='content']/div/div/div[@class='container']/a[@data-reactid='.1.3.4.0.3']"):
                # 点击下一页
                click_handle = await page.xpath("//div[@class='content']/div/div/div[@class='container']/a[@data-reactid='.1.3.4.0.3']")
                await click_handle[0].click()
            else:
                print("获取完毕")
                break

    def gei_hangban(self, html):
        x0 = html.xpath('//div[@class="b-airfly"]')
        for item in x0:
            dict01 = dict()
            # 公司
            x1 = item.xpath('.//div[@class="air"]//span/text()') if len(item.xpath('.//div[@class="air"]//span/text()')) > 0 else None
            str_x101 = str(x1).replace("['", "")
            str_x102 = str_x101.replace("']", "")
            dict01['公司'] = str_x102
            # 航班号
            x2 = item.xpath('.//div[@class="num"]/span[1]/text()') if len(item.xpath('.//div[@class="num"]/span[1]/text()')) > 0 else None
            str_x201 = str(x2).replace("['", "")
            str_x202 = str_x201.replace("']", "")
            dict01['航班号'] = str_x202
            # 机型
            x3 = item.xpath('.//div[@class="num"]/span[2]/text()') if len(item.xpath('.//div[@class="num"]/span[2]/text()')) > 0 else None
            str_x301 = str(x3).replace("['", "")
            str_x302 = str_x301.replace("']", "")
            dict01['机型'] = str_x302
            # 出发时间
            x4 = item.xpath('.//div[@class="sep-lf"]/h2/text()') if len(item.xpath('.//div[@class="sep-lf"]/h2/text()')) > 0 else None
            str_x401 = str(x4).replace("['", "")
            str_x402 = str_x401.replace("']", "")
            dict01['出发时间'] = str_x402
            # 出发机场
            x5 = item.xpath('.//div[@class="sep-lf"]/p/span[1]/text()') if len(item.xpath('.//div[@class="sep-lf"]/p/span[1]/text()')) > 0 else None
            str_x501 = str(x5).replace("['", "")
            str_x502 = str_x501.replace("']", "")
            dict01['出发机场'] = str_x502
            # 用时
            x6 = item.xpath('.//div[@class="sep-ct"]/div[1]/text()') if len(item.xpath('.//div[@class="sep-ct"]/div[1]/text()')) > 0 else None
            str_x601 = str(x6).replace("['", "")
            str_x602 = str_x601.replace("']", "")
            dict01['用时'] = str_x602
            # 到达时间
            x7 = item.xpath('.//div[@class="sep-rt"]/h2/text()') if len(item.xpath('.//div[@class="sep-rt"]/h2/text()')) > 0 else None
            str_x701 = str(x7).replace("['", "")
            str_x702 = str_x701.replace("']", "")
            dict01['到达时间'] = str_x702
            # 到达机场
            x8 = item.xpath('.//div[@class="sep-rt"]/p/span[1]/text()') if len(item.xpath('.//div[@class="sep-rt"]/p/span[1]/text()')) > 0 else None
            str_x801 = str(x8).replace("['", "")
            str_x802 = str_x801.replace("']", "")
            dict01['到达机场'] = str_x802
            # 票价
            # x9 = temp.xpath('.//div[@class="air"]//span/text()')

            print(dict01)



    def run(self):
        asyncio.get_event_loop().run_until_complete(self.main())


if __name__ == '__main__':
    comment = Hangban()
    comment.run()
