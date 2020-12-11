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
    await page.goto('https://flight.qunar.com/')

    await page.evaluateOnNewDocument('() =>')


