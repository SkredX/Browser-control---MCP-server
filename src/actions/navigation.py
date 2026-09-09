"""Navigation actions."""

from playwright.async_api import Page


async def navigate(page: Page, url: str, timeout_ms: int = 30_000) -> str:
    response = await page.goto(url, wait_until="networkidle", timeout=timeout_ms)
    status = response.status if response else "unknown"
    return f"Navigated to {page.url} (status: {status})"


async def go_back(page: Page) -> str:
    await page.go_back(wait_until="domcontentloaded")
    return f"Navigated back to {page.url}"


async def go_forward(page: Page) -> str:
    await page.go_forward(wait_until="domcontentloaded")
    return f"Navigated forward to {page.url}"
