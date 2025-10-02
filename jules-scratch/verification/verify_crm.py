import asyncio
from playwright.async_api import async_playwright, expect

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        # Listen for all console events and print them to the output
        page.on("console", lambda msg: print(f"BROWSER LOG: {msg.type} - {msg.text}"))

        import os
        file_path = os.path.abspath('index.html')
        await page.goto(f'file://{file_path}')

        # Wait for the first owner item to appear, which confirms loading is complete
        first_owner = page.locator(".owner-item").first
        await expect(first_owner).to_be_visible(timeout=20000)

        # Proceed with the rest of the test
        await first_owner.click()
        await expect(page.locator(".property-header")).to_be_visible()

        # Open the Status Breakdown modal
        await page.get_by_role("button", name="📊 Status Breakdown").click()

        # Wait for the chart in the modal to be visible
        status_chart = page.locator("#statusChart")
        await expect(status_chart).to_be_visible()

        # Add a short delay to allow the chart animation to complete
        await page.wait_for_timeout(1000)

        # Take a screenshot of the entire page
        await page.screenshot(path="jules-scratch/verification/verification.png")

        await browser.close()

if __name__ == '__main__':
    asyncio.run(main())