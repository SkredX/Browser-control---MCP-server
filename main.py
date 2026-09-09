"""Stdio entry point for Browser Control MCP."""

from src.server import mcp


def main() -> None:
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
