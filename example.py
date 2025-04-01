import asyncio
from pydantic_ai import Agent
from pydantic_ai.mcp import MCPServerStdio
from dotenv import load_dotenv
load_dotenv()

server = MCPServerStdio(
    command="C:\\Users\\Alonso\\.cargo\\bin\\uv.exe",
    args=[
        "--directory",
        "C:\\Users\\Alonso\\Dropbox\\personal\\repos\\whatsapp-mcp\\whatsapp-mcp-server",
        "run",
        "main.py"
    ]
)
agent = Agent('openai:gpt-4o', mcp_servers=[server])


async def main():
    async with agent.run_mcp_servers():
        result = await agent.run('Can you summarize my last 10 whatsapp messages with my boss (Loreto Bravo)?')
    print(result.data)
    #> There are 9,208 days between January 1, 2000, and March 18, 2025.

if __name__ == "__main__":
    asyncio.run(main())