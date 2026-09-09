"""MCP tools exposed by Browser Control."""

from contextlib import asynccontextmanager
from collections.abc import AsyncIterator

from mcp.server.fastmcp import FastMCP
from pydantic import AnyHttpUrl, Field

from .actions import interaction, navigation
from .actions.extraction import get_page_markdown
from .browser.manager import BrowserManager

browser_manager = BrowserManager()


@asynccontextmanager
async def server_lifespan(_: FastMCP) -> AsyncIterator[dict]:
    """Release the browser process when the MCP transport shuts down."""
    try:
        yield {}
    finally:
        await browser_manager.cleanup()


mcp = FastMCP("AdvancedBrowserControl", lifespan=server_lifespan)


@mcp.tool()
async def navigate(url: AnyHttpUrl, timeout_ms: int = Field(default=30_000, ge=1_000, le=120_000)) -> str:
    """Navigate to an HTTP(S) URL and wait until the network is idle."""
    try:
        return await navigation.navigate(await browser_manager.get_page(), str(url), timeout_ms)
    except Exception as exc:
        return f"Navigation failed: {exc}"


@mcp.tool()
async def extract_content() -> str:
    """Extract the current webpage as compact, LLM-readable Markdown."""
    try:
        return await get_page_markdown(await browser_manager.get_page())
    except Exception as exc:
        return f"Content extraction failed: {exc}"


@mcp.tool()
async def click_element(selector: str) -> str:
    """Click the first visible element matching a CSS or Playwright selector."""
    try:
        await interaction.click(await browser_manager.get_page(), selector)
        return f"Clicked: {selector}"
    except Exception as exc:
        return f"Click failed for {selector!r}: {exc}"


@mcp.tool()
async def type_text(selector: str, text: str) -> str:
    """Replace text in the first visible input matching a selector."""
    try:
        await interaction.fill(await browser_manager.get_page(), selector, text)
        return f"Entered text into: {selector}"
    except Exception as exc:
        return f"Text entry failed for {selector!r}: {exc}"


@mcp.tool()
async def hover_element(selector: str) -> str:
    """Hover over the first element matching a selector."""
    try:
        await interaction.hover(await browser_manager.get_page(), selector)
        return f"Hovered: {selector}"
    except Exception as exc:
        return f"Hover failed for {selector!r}: {exc}"


@mcp.tool()
async def drag_element(source_selector: str, target_selector: str) -> str:
    """Drag the first source element onto the first target element."""
    try:
        await interaction.drag_and_drop(await browser_manager.get_page(), source_selector, target_selector)
        return f"Dragged {source_selector} to {target_selector}"
    except Exception as exc:
        return f"Drag-and-drop failed: {exc}"


@mcp.tool()
async def go_back() -> str:
    """Navigate back in the active tab's history."""
    try:
        return await navigation.go_back(await browser_manager.get_page())
    except Exception as exc:
        return f"Back navigation failed: {exc}"


@mcp.tool()
async def go_forward() -> str:
    """Navigate forward in the active tab's history."""
    try:
        return await navigation.go_forward(await browser_manager.get_page())
    except Exception as exc:
        return f"Forward navigation failed: {exc}"


@mcp.tool()
async def execute_javascript(script: str) -> str:
    """Run JavaScript in the current page and return its serializable result."""
    try:
        result = await (await browser_manager.get_page()).evaluate(script)
        return f"Execution successful. Result: {result!r}"
    except Exception as exc:
        return f"JavaScript execution failed: {exc}"
