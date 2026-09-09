"""Content extraction helpers designed for compact LLM input."""

import html2text
from bs4 import BeautifulSoup
from playwright.async_api import Page


async def get_page_markdown(page: Page) -> str:
    """Return meaningful page content as Markdown, without presentation noise."""
    soup = BeautifulSoup(await page.content(), "html.parser")
    for element in soup(["script", "style", "noscript", "svg", "img", "template"]):
        element.decompose()
    converter = html2text.HTML2Text()
    converter.ignore_links = False
    converter.ignore_images = True
    converter.body_width = 0
    return converter.handle(str(soup)).strip()
