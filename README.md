# Browser-control---MCP-server
## Usage directive:
The Model Context Protocol allows applications to provide context for LLMs in a standardized way, separating the concerns of providing context from the actual LLM interaction. This Python SDK implements the full MCP specification, making it easy to:

- Build MCP clients that can connect to any MCP server
- Create MCP servers that expose resources, prompts and tools
- Use standard transports like stdio, SSE, and Streamable HTTP
- Handle all MCP protocol messages and lifecycle events

Run the following code in your Python IDE (after basic installations like installing [uv](https://docs.astral.sh/uv/) and Claude Desktop :
```python
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
```

Run the following command in your terminal, opened in the working directory:
```bash
uv run mcp install {name of the file}
```
For example, if your file name is saved as browser_control.py, use :
```bash
uv run mcp install browser_control.py
```

Alternatively, you can test it with the MCP Inspector:
```bash
mcp dev browser_control.py
```

Open your Claude Desktop application and once the MCP server is connected, type the following:
```bash
open_in_chrome("https://medium.com/@vidyarthy.shuvam")
```
