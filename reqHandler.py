import asyncio
from playwright.async_api import async_playwright, Browser, BrowserContext, Page
from playwright_stealth import Stealth
import time

class StealthBrowserManager:
    def __init__(self):
        self.playwright = None
        self.browser = None
        self.context = None
        
        # 1. Initialize stealth parameters once. 
        # This compiles the internal JavaScript payload into memory.
        self.stealth = Stealth(
            navigator_languages_override=("fr-FR", "fr"),
            init_scripts_only=True
        )

    async def start(self) -> BrowserContext:
        """Launches the browser and binds the stealth payload to the context."""
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(headless=False)
        self.context = await self.browser.new_context()
        
        # 2. Inject the compiled payload into the context. 
        # Every new page generated from this context automatically inherits the stealth logic.
        await self.stealth.apply_stealth_async(self.context)
        return self.context

    async def get_page(self, url: str) -> Page:
        """Spawns a clean page with stealth pre-applied and navigates to the URL."""
        if not self.context:
            raise RuntimeError("Browser context is not initialized. Run start() first.")

        # 3. Create a page. It automatically receives the init scripts from the context.
        page = await self.context.new_page()
        await page.goto(url)
        return page

    async def close(self):
        """Clean shutdown of all streams and browser instances."""
        if self.context:
            await self.context.close()
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()


'''
async def start_page():
    a = StealthBrowserManager()
    await a.start()
    print("get site?")
    page = await a.get_page("https://www.jw.org/en/")
    print(page)

    await a.close()

asyncio.run(start_page())
'''
