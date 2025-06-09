# browser_control.py
from mcp.server.fastmcp import FastMCP
import webbrowser

# Create an MCP server for browser control
mcp = FastMCP("Browser Control")

@mcp.tool()
def open_in_chrome(url: str) -> str:
    """Open a URL in Chrome browser"""
    try:
        # Try to open in Chrome specifically
        chrome_path = 'C:/Program Files/Google/Chrome/Application/chrome.exe %s'  # Windows path
        webbrowser.get(chrome_path).open(url)
        return f"Successfully opened {url} in Chrome"
    except Exception as e:
        # Fall back to default browser if Chrome isn't found
        webbrowser.open(url)
        return f"Opened {url} in default browser (Chrome not found)"

# For direct execution
if __name__ == "__main__":
    mcp.run()