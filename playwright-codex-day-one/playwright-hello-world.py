import asyncio
from datetime import datetime
from pathlib import Path

from playwright.async_api import async_playwright, TimeoutError

TARGET_URL = "https://chatgpt.com/"
OUTPUT_DIR = Path("screens")

COMPOSER_SELECTORS = [
    "textarea[data-testid='conversation-composer']",
    "textarea[placeholder*='message']",
    "textarea[placeholder*='Message']",
    "[contenteditable='true'][data-testid='conversation-composer']",
]


async def run() -> None:
    """Launch ChatGPT Plus and click the new conversation input."""
    stamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=False)
        page = await browser.new_page()
        await page.goto(TARGET_URL, wait_until="domcontentloaded")

        composer = None
        for selector in COMPOSER_SELECTORS:
            try:
                await page.wait_for_selector(selector, timeout=15000)
                candidate = page.locator(selector).first
                await candidate.scroll_into_view_if_needed()
                await candidate.wait_for(state="visible", timeout=2000)
                composer = candidate
                break
            except TimeoutError:
                continue

        if composer is None:
            raise RuntimeError(
                "Could not locate the ChatGPT new conversation box. Ensure you are signed in and update COMPOSER_SELECTORS if needed."
            )

        await composer.click()
        await page.wait_for_timeout(2000)

        screenshot_path = OUTPUT_DIR / f"chatgpt_new_conversation_{stamp}.png"
        await page.screenshot(path=screenshot_path, full_page=True)
        await browser.close()


if __name__ == "__main__":
    asyncio.run(run())
