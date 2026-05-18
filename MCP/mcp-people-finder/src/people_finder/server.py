from mcp.server.fastmcp import FastMCP
import os
import sys
import asyncio
from dotenv import load_dotenv

# Load environment variables (useful for local testing)
load_dotenv()

# Initialize FastMCP - the name identifies your server to the LLM
# mcp = FastMCP("PeopleFinder", dependencies=["httpx"])
mcp = FastMCP("PeopleFinder")


# Tool 1: Search Employee
@mcp.tool()
async def search_employee(name: str) -> str:
    """Find employee contact info by name."""
    # In production, this would call your HR API or Database
    return f"Found: {name} | Role: Senior Engineer | Email: {name.lower()}@company.com | Status: Active"

# Tool 2: Get Office Info
@mcp.tool()
async def get_office_location(city: str) -> str:
    """Get the address of a specific branch office."""
    offices = {"New York": "123 Wall St", "San Francisco": "456 Market St", "London": "789 Baker St", "Tokyo": "101 Shibuya St"}
    return offices.get(city, "Office not found.")

@mcp.tool()
async def list_all_offices() -> list[str]:
    """List all available company office locations."""
    return ["New York", "San Francisco", "London", "Tokyo"]

def main():
    """
    Entry point that supports multiple environments.
    Usage:
      - Default: 'people-finder' -> starts stdio
      - Cloud: 'MCP_TRANSPORT=sse people-finder' -> starts HTTP server
    """
    # 1. Get transport from Environment Variable (Standard for Cloud Run/Docker)
    # 2. Default to 'stdio' if nothing is set (Standard for Local pip users)
    transport_type = os.getenv("MCP_TRANSPORT", "stdio").lower()
    
    # mcp.run(transport=transport_type)

    if transport_type == "sse" or transport_type == "http":
        # In production cloud environments, we need a port
        port = int(os.getenv("PORT", 8000))
        print(f"Starting MCP Server on HTTP port {port}", file=sys.stderr)
        mcp.run(transport="sse", port=port)
    else:
        # Local mode for Claude Desktop, Cursor, etc.
        mcp.run(transport="stdio")

if __name__ == "__main__":
    main()