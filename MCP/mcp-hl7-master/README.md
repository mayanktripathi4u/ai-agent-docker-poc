# MCP HL7 Master

**Model Context Protocol (MCP) Server** for AI agents to safely generate, parse, and extract **HL7 v2 healthcare messages**.

This is a **production-grade** MCP server designed for healthcare engineers and AI applications that need to work with HL7 messages. Using simulated patient data, it demonstrates how to build enterprise-grade tools that AI agents can call securely over standard input/output (stdio).

## What is HL7?

**HL7 (Health Level 7)** is an international standard for exchanging healthcare information electronically. Version 2 (v2) uses pipe-delimited text to represent medical data:

```
MSH|^~\&|SendingApp|SendingFacility|ReceivingApp|ReceivingFacility|20240522120000||ADT^A01|MSG123|P|2.5
PID|1||123456^^^MRN||Doe^John||19800101|M
```

**Message Types**: ADT (Admission/Discharge/Transfer), ORM (Order), ORU (Order Result), etc.

**Why it matters**: Healthcare systems use HL7 to exchange patient records, lab results, and billing information securely.

## What is MCP?

Model Context Protocol enables AI agents (like Claude) to call external tools in a standardized, type-safe way. Instead of embedding logic directly, agents can request specific information through well-defined tool interfaces. This server uses `stdio` for communication — a client (like Claude Desktop) starts your Python script as a background process.

## Features

- ✅ **Synthetic HL7 Generation** — Create realistic ADT/ORM messages with fake patient data
- ✅ **Intelligent Parsing** — Convert complex pipe-delimited HL7 into readable JSON
- ✅ **Field Extraction** — Query specific patient fields without manual parsing
- ✅ **Error Handling** — Graceful error responses for malformed messages
- ✅ **Dual Transport** — Works locally (stdio) or as a web service (SSE)

# Prerequisites

- **Python 3.11+** — Required for running the server
- **Node.js** — Required for MCP Inspector testing (optional, for local development)

## Dependencies

Automatically installed with `pip install mcp-hl7-master`:

- `mcp[cli]` — Model Context Protocol SDK
- `fastmcp` — Modern Python MCP framework
- `hl7apy` — HL7 message parsing and generation
- `hl7` — Alternative HL7 parsing library
- `faker` — Generate realistic synthetic patient data
- `python-dotenv` — Environment variable management
  

# Installation
```bash
pip install mcp-hl7-master
```

# Usage

Once installed, run the server:

```bash
hl7-master
```

The server starts in **stdio mode by default**, listening for MCP protocol messages.

## Deployment Options

### Local Usage (stdio)

Best for: Claude Desktop, local development, secure environments.

Add to your Claude Desktop configuration file:

```json
"hl7-master": {
  "command": "hl7-master"
}
```

### Cloud Usage (SSE/HTTP)

Best for: Cloud services, remote agents, scalable deployments.

Start the server with:

```bash
MCP_TRANSPORT=sse PORT=8000 hl7-master
```

Then configure your client to call `http://localhost:8000`.

**Environment Variables:**
- `MCP_TRANSPORT` — `stdio` (default) or `sse`
- `PORT` — Server port (default: 8000)

## Available Tools
## Available Tools

### 1. `generate_hl7_message`

Generate a synthetic HL7 message with fake patient data.

**Parameters:**
- `message_type` (string) — HL7 message type (default: `ADT`)
  - Supported: `ADT`, `ORM`, `ORU` (extensible)
- `trigger_event` (string) — Event trigger code (default: `A01`)
  - ADT events: `A01` (Admit), `A03` (Discharge), `A08` (Update)
  - ORM events: `O01` (Order), `O02` (Cancel)

**Returns:** HL7 v2.5 formatted message string with simulated patient data

**Example:**
```python
await generate_hl7_message(message_type="ADT", trigger_event="A01")
# Returns: MSH|^~\&|...|PID|1||12345^^^MRN||Doe^John||...
```

---

### 2. `parse_hl7_message`

Parse a raw HL7 string into a structured JSON-friendly dictionary.

**Parameters:**
- `raw_message` (string) — HL7 message in pipe-delimited format

**Returns:**
```json
{
  "status": "success",
  "data": {
    "MSH": ["MSH", "^~\\&", "SendingApp", ...],
    "PID": ["PID", "1", "", "12345^^^MRN", ...]
  }
}
```

**Error Response:**
```json
{
  "status": "error",
  "message": "Invalid HL7 format"
}
```

---

### 3. `extract_hl7_details`

Extract specific fields from an HL7 message without manual parsing.

**Parameters:**
- `raw_message` (string) — HL7 message
- `fields` (list[string]) — Field names to extract
  - Valid fields: `patient_name`, `hl7_version`, `facility`, `message_date`

**Returns:**
```json
{
  "patient_name": "Doe^John",
  "hl7_version": "2.5",
  "facility": "HOSPITAL_A",
  "message_date": "20240522120000"
}
```

**Example:**
```python
await extract_hl7_details(
  raw_message="MSH|...",
  fields=["patient_name", "facility"]
)
```

---

## Example Workflow

Here's how Claude might use these tools together:

```
1. Generate: Create a test ADT message
   → generate_hl7_message("ADT", "A01")
   → Returns: MSH|^~\&|...|PID|1||...

2. Parse: Convert it to JSON structure
   → parse_hl7_message(raw_message)
   → Returns: {"MSH": [...], "PID": [...]}

3. Extract: Get specific patient details
   → extract_hl7_details(raw_message, ["patient_name", "facility"])
   → Returns: {"patient_name": "Doe^John", "facility": "HOSPITAL_A"}
```

---

## Testing & Development

### Test locally with MCP Inspector

MCP Inspector provides a web UI to test tools locally:

```bash
npm install -g @modelcontextprotocol/inspector
npx @modelcontextprotocol/inspector hl7-master
```

This launches http://localhost:3000 where you can:
- Call `generate_hl7_message` and see the output
- Paste an HL7 message into `parse_hl7_message`
- Extract specific fields using `extract_hl7_details`

### Test with Python

```python
import asyncio
from hl7_master.server import generate_hl7_message, parse_hl7_message

# Generate and parse
message = await generate_hl7_message()
result = await parse_hl7_message(message)
print(result)
```

---

## Error Handling

The server handles errors gracefully:

| Scenario | Response |
|----------|----------|
| Invalid HL7 format | `{"status": "error", "message": "..."}` |
| Missing field | `{"error": "Field not found"}` |
| Malformed message | Tool returns error dict with message |

Errors don't crash the server — Claude receives them and can retry or ask for clarification.

---

## Troubleshooting

### Issue: "command not found: hl7-master"
**Solution:** Ensure the package is installed: `pip install mcp-hl7-master`

### Issue: Port 8000 already in use
**Solution:** Use a different port: `PORT=8001 MCP_TRANSPORT=sse hl7-master`

### Issue: Extract tool returns empty dict
**Solution:** Check that field names are valid (`patient_name`, `hl7_version`, `facility`, `message_date`)

### Issue: Parse fails on some messages
**Solution:** Ensure the message uses correct HL7 v2 format with pipes and carriage returns

---

## License

MIT License — See LICENSE file for details.


## Need Help?

- **HL7 Documentation**: https://www.hl7.org/
- **MCP Documentation**: https://modelcontextprotocol.io/
- **Claude API**: https://claude.ai/
