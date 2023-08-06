import asyncio

import bottle

# import pyppeteer


# async def main():
#     browser = await pyppeteer.launch(headless=False)
#     page = await browser.newPage()
#     await page.goto('http://example.com')
#     await page.setViewport({'width': 100, 'height': 100})
#     await page.screenshot({'path': 'example.png'})
#     await browser.close()

# asyncio.get_event_loop().run_until_complete(main())

from playwright.sync_api import sync_playwright


app = bottle.Bottle()

app.run()

pw = sync_playwright().start()
BROWSER = pw.chromium.launch(headless=False)