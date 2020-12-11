import asyncio
import time
from pyppeteer import launch


async def main():
    # 窗口像素
    width, height = 1366, 768
    # headless是在后端显示页面，ages '--disable-infobars'是不显示正在自动化控制，args f'--window-size={width},{height}'设定内窗口宽高
    browser = await launch({"headless": False}, args=['--disable-infobars', f'--window-size={width},{height}'])
    # 创建窗口
    page = await browser.newPage()
    # 设置窗口大小
    await page.setViewport({'width': width, 'height': height})
    # 加载路由
    await page.goto('https://demo.mycodes.net/daima/suopingjiesuo/')

    # 第一次移动
    x = 676
    y = 236
    # 定位鼠标位置到圆上
    await page.mouse.move(x, y)
    # 点击
    await page.mouse.down()
    # 开始移动（x轴调整，y轴调整，步长）
    await page.mouse.move(x + 100, y, {'steps': 20})
    await page.mouse.move(x + 100, y + 100, {'steps': 20})
    await page.mouse.move(x - 100, y, {'steps': 20})
    await page.mouse.move(x, y + 100, {'steps': 20})
    await page.mouse.move(x + 80, y + 200, {'steps': 20})
    # 松开鼠标
    await page.mouse.up()
    # 等待
    time.sleep(2)

    # 第二次移动
    # 定位鼠标位置到圆上
    await page.mouse.move(x, y)
    # 点击
    await page.mouse.down()
    # 开始移动（x轴调整，y轴调整，步长）
    await page.mouse.move(x + 100, y, {'steps': 20})
    await page.mouse.move(x + 100, y + 100, {'steps': 20})
    await page.mouse.move(x - 100, y, {'steps': 20})
    await page.mouse.move(x, y + 100, {'steps': 20})
    await page.mouse.move(x + 80, y + 200, {'steps': 20})
    # 松开鼠标
    await page.mouse.up()
    # 等待
    time.sleep(2)

# 结束，关闭
asyncio.get_event_loop().run_until_complete(main())
