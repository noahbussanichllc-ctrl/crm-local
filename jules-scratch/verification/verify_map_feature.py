import asyncio
from playwright.async_api import async_playwright, expect
import os

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        # Get the absolute path to the index.html file
        file_path = os.path.abspath('index.html')

        # Go to the local HTML file
        await page.goto(f'file://{file_path}')

        # Click the "Map" button
        await page.get_by_role("button", name="🗺️ Map").click()

        # Wait for the map view to be visible
        map_view = page.locator("#mapView")
        await expect(map_view).to_be_visible()

        # Wait for the map to initialize (give it a second for tiles to load)
        await page.wait_for_timeout(2000)

        # Take a screenshot
        screenshot_path = "jules-scratch/verification/verification.png"
        await page.screenshot(path=screenshot_path)
        print(f"Screenshot saved to {screenshot_path}")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())