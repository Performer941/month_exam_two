import asyncio
import time
from pyppeteer import launch

width, height = 1366, 768


async def main():
    # headless是在后端显示页面，ages '--disable-infobars'是不显示正在自动化控制，args f'--window-size={width},{height}'设定内窗口宽高
    browser = await launch({"headless": False}, args=['--disable-infobars', f'--window-size={width},{height}'])
    page = await browser.newPage()
    await page.setViewport({'width': width, 'height': height})
    # 加载路由
    await page.goto('https://demo.mycodes.net/daima/suopingjiesuo/')

    x = 676
    y = 236
    await page.mouse.move(x, y)
    await page.mouse.down()
    await page.mouse.move(x + 100, y, {'steps': 20})
    await page.mouse.move(x + 100, y + 100, {'steps': 20})
    await page.mouse.move(x - 100, y, {'steps': 20})
    await page.mouse.move(x, y + 100, {'steps': 20})
    await page.mouse.move(x + 80, y + 200, {'steps': 20})
    await page.mouse.up()

    time.sleep(2)

    await page.mouse.move(x, y)
    await page.mouse.down()
    await page.mouse.move(x + 100, y, {'steps': 20})
    await page.mouse.move(x + 100, y + 100, {'steps': 20})
    await page.mouse.move(x - 100, y, {'steps': 20})
    await page.mouse.move(x, y + 100, {'steps': 20})
    await page.mouse.move(x + 80, y + 200, {'steps': 20})

    await page.mouse.up()
    time.sleep(2)

asyncio.get_event_loop().run_until_complete(main())
