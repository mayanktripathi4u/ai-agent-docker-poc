"""
Writing the "Agent Code" (The AI Way)

In a production-grade system, your Agent doesn't just "import" your library; it launches it. 
Here is the Python code for a "Client" (the Agent) that connects to your library.
"""

import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def run_agent():
    # 1. Point the Agent to your library's entry point
    server_params = StdioServerParameters(
        command="people-finder", # This is the command from your pyproject.toml
        args=[],
        env=None
    )

    # 2. Start the connection
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize the session
            await session.initialize()

            # 3. DISCOVERY: The Agent asks "What can you do?"
            tools = await session.list_tools()
            print(f"Agent sees these tools: {[t.name for t in tools.tools]}")

            # 4. EXECUTION: The Agent decides to use a tool
            # (In a real app, an LLM would choose 'get_employee_info')
            result = await session.call_tool(
                "get_employee_info", 
                arguments={"name": "Alice Smith"}
            )

            # 5. RESPONSE: The Agent gets the data
            for content in result.content:
                print(f"Agent received: {content.text}")

if __name__ == "__main__":
    asyncio.run(run_agent())