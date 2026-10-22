"""Render artboards to PNG: python _shot.py DirectionZ DirectionAA ..."""
import asyncio, sys
from pathlib import Path
from playwright.async_api import async_playwright
D = Path(__file__).parent
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        page = await (await b.new_context(viewport={"width":1440,"height":900})).new_page()
        for n in sys.argv[1:]:
            await page.goto((D/f"{n}.dc.html").as_uri(), wait_until="load")
            await page.wait_for_timeout(4500)
            h = await page.evaluate("document.querySelector('x-dc > div').getBoundingClientRect().height")
            w = await page.evaluate("document.documentElement.scrollWidth")
            await page.screenshot(path=str(D/f"{n}.png"), full_page=True)
            print(n, "height", round(h), "scrollWidth", w)
        await b.close()
asyncio.run(main())
