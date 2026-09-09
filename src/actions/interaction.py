"""Safe, locator-based page interactions."""

from playwright.async_api import Page


async def click(page: Page, selector: str, timeout_ms: int = 5_000) -> None:
    locator = page.locator(selector).first
    await locator.wait_for(state="visible", timeout=timeout_ms)
    await locator.click(timeout=timeout_ms)


async def fill(page: Page, selector: str, text: str, timeout_ms: int = 5_000) -> None:
    locator = page.locator(selector).first
    await locator.wait_for(state="visible", timeout=timeout_ms)
    await locator.fill(text, timeout=timeout_ms)


async def hover(page: Page, selector: str, timeout_ms: int = 5_000) -> None:
    await page.locator(selector).first.hover(timeout=timeout_ms)


async def drag_and_drop(page: Page, source: str, target: str, timeout_ms: int = 5_000) -> None:
    await page.locator(source).first.drag_to(page.locator(target).first, timeout=timeout_ms)
