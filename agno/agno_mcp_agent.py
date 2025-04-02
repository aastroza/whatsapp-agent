# Code from here: https://github.com/lharries/whatsapp-mcp/issues/17

import asyncio
from textwrap import dedent
import logging
from dotenv import load_dotenv
import os
load_dotenv()

from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools.mcp import MCPTools
from mcp import StdioServerParameters, ClientSession
from mcp.client.stdio import stdio_client

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("agno_mcp_agent")

async def run_agent() -> None:
    """Run the WhatsApp agent in continuous chat mode."""
    # MCP parameters for the WhatsApp MCP server
    server_params = StdioServerParameters(
        command="C:\\Users\\Alonso\\.cargo\\bin\\uv.exe",# your path to uv.exe
        args=[
            "--directory",
            "C:\\Users\\Alonso\\Dropbox\\personal\\repos\\whatsapp-mcp\\whatsapp-mcp-server",# your path to whatsapp-mcp-server
            "run",
            "main.py"
        ]
    )

    try:
        # Create a client session to connect to the MCP server
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                # Initialize the MCP toolkit explicitly
                mcp_tools = MCPTools(session=session)
                await mcp_tools.initialize()
                
                logger.info("MCP tools initialized successfully")
                
                agent = Agent(
                    model=OpenAIChat(id="gpt-4o", api_key=os.getenv('OPENAI_API_KEY')),
                    tools=[mcp_tools],
                    instructions=dedent("""\
                        You are an advanced WhatsApp bridge assistant with cognitive capabilities. Combine real-time information 
                        with messaging operations through the MCP server.

                        Core WhatsApp Operations:
                        - Manage messages (individual/group) with proper context and timestamps
                        - Monitor connection status and handle authentication flows
                        - Process media messages with appropriate security measures
                        - Implement error recovery strategies for WhatsApp API issues

                        Cognitive Enhancements:
                        - Use thinking tools for multi-step problem solving before acting
                        - Perform Google searches to verify information before responding
                        - Cross-reference tech news from HackerNews for relevant updates
                        - Combine message context with external data for comprehensive responses

                        Available WhatsApp MCP Tools:
                        1. search_contacts(query): Search contacts by name or phone number
                        2. list_messages(date_range, sender_phone_number, chat_jid, query, limit, page, include_context, context_before, context_after): 
                        Get messages matching criteria with optional context
                        3. list_chats(query, limit, page, include_last_message, sort_by): 
                        Get chats matching criteria
                        4. get_chat(chat_jid, include_last_message): 
                        Get chat metadata by JID
                        5. get_direct_chat_by_contact(sender_phone_number): 
                        Get chat metadata by sender phone number
                        6. get_contact_chats(jid, limit, page): 
                        Get all chats involving a specific contact
                        7. get_last_interaction(jid): 
                        Get most recent message involving a contact
                        8. get_message_context(message_id, before, after): 
                        Get context around a specific message
                        9. send_message(recipient, message): 
                        Send a message to a person or group

                        Guidelines:
                        - Always use the available MCP tools for any WhatsApp-related task
                        - If a task requires multiple steps, use the thinking tools for guidance
                    """),
                    markdown=True,
                    show_tool_calls=True,
                    debug_mode=True,
                )

                # Continuous chat loop
                while True:
                    message = input("\nYou: ")
                    if message.lower() in ('exit', 'quit', 'q'):
                        break
                    
                    await agent.aprint_response(message, stream=False)
                    
    except Exception as e:
        logger.error(f"Error running WhatsApp agent: {e}")
        raise

if __name__ == "__main__":
    print("WhatsApp MCP Agent - Type 'exit' to quit")
    asyncio.run(run_agent())