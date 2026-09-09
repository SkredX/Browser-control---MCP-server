"""Playwright lifecycle management for a single MCP server process."""

from __future__ import annotations

import asyncio

from playwright.async_api import Browser, BrowserContext, Page, Playwright, async_playwright

from .stealth import apply_stealth
from ..utils.logger import get_logger

logger = get_logger(__name__)


class BrowserManager:
    """Owns the Playwright process, browser context, and active page."""

    def __init__(self) -> None:
        self._playwright: Playwright | None = None
        self.browser: Browser | None = None
        self.context: BrowserContext | None = None
        self.page: Page | None = None
        self._lock = asyncio.Lock()

    async def initialize(self, headless: bool = True) -> Page:
        """Start Chromium once and return the active page."""
        async with self._lock:
            if self.page and not self.page.is_closed():
                return self.page
            self._playwright = await async_playwright().start()
            self.browser = await self._playwright.chromium.launch(
                headless=headless,
                args=["--disable-blink-features=AutomationControlled"],
            )
            self.context = await self.browser.new_context(
                viewport={"width": 1280, "height": 800},
                user_agent=("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                            "AppleWebKit/537.36 (KHTML, like Gecko) "
                            "Chrome/120.0.0.0 Safari/537.36"),
            )
            self.page = await self.context.new_page()
            await apply_stealth(self.page)
            logger.info("Browser session initialized")
            return self.page

    async def get_page(self) -> Page:
        return await self.initialize()

    async def cleanup(self) -> None:
        """Close all owned resources, allowing idempotent shutdown."""
        async with self._lock:
            if self.context:
                await self.context.close()
            if self.browser:
                await self.browser.close()
            if self._playwright:
                await self._playwright.stop()
            self._playwright = self.browser = self.context = self.page = None
            logger.info("Browser session cleaned up")
