# Browser Control MCP Server

A Playwright-powered [Model Context Protocol](https://modelcontextprotocol.io/) server for controlled browser navigation, interaction, and Markdown content extraction.

## Features

- Reusable Chromium context managed for the MCP server lifetime
- Navigation, history controls, clicking, typing, hovering, and drag-and-drop
- Clean HTML-to-Markdown extraction for efficient LLM context
- Optional `playwright-stealth` integration
- MCP stdio transport for Claude Desktop, Cursor, and MCP Inspector

## Install

Requires Python 3.10+.

```bash
uv sync
uv run playwright install chromium
```

Or with pip:

```bash
pip install -r requirements.txt
playwright install chromium
```

## Run

```bash
uv run main.py
```

The original launcher remains available:

```bash
uv run browser_control.py
```

For MCP Inspector:

```bash
mcp dev main.py
```

## Available tools

`navigate`, `extract_content`, `click_element`, `type_text`, `hover_element`, `drag_element`, `go_back`, `go_forward`, and `execute_javascript`.

Use only with sites and accounts you are authorized to automate. JavaScript evaluation is intentionally powerful; only pass trusted scripts.
