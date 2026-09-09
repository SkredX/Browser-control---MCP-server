"""Optional Playwright stealth integration."""

from playwright.async_api import Page


async def apply_stealth(page: Page) -> None:
    """Apply playwright-stealth when installed; remain usable without it."""
    try:
        from playwright_stealth import Stealth
    except ImportError:
        try:
            from playwright_stealth import stealth_async
        except ImportError:
            return
        await stealth_async(page)
    else:
        await Stealth().apply_stealth_async(page)
