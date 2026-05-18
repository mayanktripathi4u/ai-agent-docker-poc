# MCP HL7 Master

A production-grade Model Context Protocol (MCP) server for Healthcare engineers. It provides AI agents with the ability to generate, parse, and query HL7 v2 messages.

## Features
- **Synthetic Generation**: Create fake ADT/ORM messages using `Faker`.
- **Intelligent Parsing**: Convert complex HL7 pipes into readable JSON.
- **Deep Extraction**: Query specific fields like `patient_name` without manual indexing.

## Installation
```bash
pip install mcp-hl7-master
```

## Local Usage (stdio)
Add this to your Claude Desktop or Cursor configuration:
```json
"hl7-master": {
  "command": "hl7-master"
}
```

## Cloud Usage (SSE)
Set the environment variable MCP_TRANSPORT=sse to run as a web service.


