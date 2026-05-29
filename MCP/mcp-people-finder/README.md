# MCP People Finder

**Model Context Protocol (MCP) Server** for AI agents to safely discover and query employee information.

This is a **demo/educational project** using simulated data to illustrate how MCP servers work. It demonstrates how to build enterprise-grade tools that AI agents can call securely over standard input/output (stdio).

## What is MCP?

Model Context Protocol enables AI agents (like Claude) to call external tools in a standardized, type-safe way. Instead of embedding logic directly, agents can request specific information through well-defined tool interfaces. This server uses `stdio` for communication — a client (like Claude Desktop) starts your Python script as a background process.

## Features

- **Employee Search** — Query employee details (role, email, status)
- **Office Location Lookup** — Find office addresses by city
- **Global Office Directory** — List all office locations
- **Production-Ready Structure** — Demonstrates enterprise MCP patterns
- **Easy Testing** — Built-in MCP Inspector integration

## Prerequisites

- **Python 3.11+** — Required for running the server
- **Node.js** — Required for MCP Inspector testing (optional, for development only)

## Installation
```bash
pip install mcp-people-finder
```

## Usage
Once installed, you can run the server directly:
```sh
people-finder
```

## Expected Output
```sh
$ people-finder
MCP People Finder Server running on stdio...
```

## Available Tools

| Tool | Input | Output |
|------|-------|--------|
| `search_employee` | Employee name | Role, email, employment status |
| `get_office_location` | City/location | Office address, phone |
| `list_all_offices` | (none) | List of all global office locations |

# Testing & Development

## Use MCP Inspector for local testing
For testing use the **MCP Inspector** (`npx @modelcontextprotocol/inspector`) to test this MCP server locally.

Run this command on your machine (it requires Node.js):
```sh
npx @modelcontextprotocol/inspector people-finder
```

- This will launch a web browser window.
- You will see your `get_employee_info` tool listed.
- You can click "Run", type "Alice" in the box, and see the result.
- Why this matters: This is how you "smoke test" your production server to ensure the logic works before letting an expensive AI Agent touch it.

## Use with Claude Desktop

To integrate this MCP server with Claude Desktop:

1. Ensure the package is installed: `pip install mcp-people-finder`
2. Configure Claude Desktop config file to point to `people-finder` command
3. Restart Claude Desktop to load the server
4. Claude will now have access to all three tools

## Error Handling

If a tool call fails, the server returns a graceful error response:

```json
{
  "error": "Employee 'XYZ' not found in database"
}
```

This allows Claude to handle errors intelligently (retry, ask for clarification, etc.) rather than crashing.

## Configuration

The server reads from environment variables (optional):

- `MCP_LOGLEVEL` — Set to `DEBUG` for verbose output (default: `INFO`)
- `EMPLOYEE_DB` — Path to custom employee database (currently uses hardcoded demo data)


## Need Help?

- **MCP Documentation**: https://modelcontextprotocol.io/
- **Claude API**: https://claude.ai/
- **Report Issues**: Create a GitHub issue with detailed error messages
