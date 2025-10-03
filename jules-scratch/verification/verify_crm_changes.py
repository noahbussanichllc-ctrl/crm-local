import asyncio
from playwright.async_api import async_playwright
import os

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        # Get the absolute path to the index.html file
        file_path = os.path.abspath('index.html')

        # Go to the local HTML file
        await page.goto(f'file://{file_path}')

        # Wait for the main layout elements to be visible
        # We expect the owners list and the new follow-up list to be present
        await page.wait_for_selector('#ownersList', timeout=5000)
        await page.wait_for_selector('#followUpList', timeout=5000)

        # Give a brief moment for any initial rendering to settle
        await page.wait_for_timeout(1000)

        # Take a screenshot of the initial layout
        await page.screenshot(path="jules-scratch/verification/verification.png")

        await browser.close()

if __name__ == '__main__':
    asyncio.run(main())