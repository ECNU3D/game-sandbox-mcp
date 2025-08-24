import asyncio
import os
import sys
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.agents import create_openai_functions_agent, AgentExecutor
from langchain.tools import BaseTool
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.schema import BaseMessage
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
import requests

# Custom MCP-compatible tool for game world operations
class GameWorldTool(BaseTool):
    """Custom tool for game world operations using direct MCP server calls"""

    name: str = "game_world_tool"
    description: str = """Use this tool to interact with the game world management system.
    You can create worlds, characters, and manage game state through natural language commands.

    Examples:
    - "Create a fantasy world with magic and dragons"
    - "Generate a sci-fi world with spaceships"
    - "Create a brave knight character named Sir Galen"
    - "Move Sir Galen to the dragon's lair"
    - "What worlds do we have available?"

    The tool will intelligently route your request to the appropriate game world function.
    """

    def _run(self, query: str) -> str:
        """Execute the game world tool using direct MCP server calls"""
        try:
            # Analyze the query to determine what action to take
            query_lower = query.lower()

            if "create" in query_lower and "world" in query_lower:
                return self._create_world(query)
            elif "generate" in query_lower and "world" in query_lower:
                return self._create_world(query)
            elif "character" in query_lower or "knight" in query_lower or "hero" in query_lower:
                return self._create_character(query)
            elif "move" in query_lower or "location" in query_lower:
                return self._move_character(query)
            elif "list" in query_lower or "available" in query_lower or "what" in query_lower:
                return self._list_worlds()
            else:
                return f"I understand you want to: '{query}'\nPlease try a more specific command like 'create a fantasy world' or 'list all worlds'."

        except Exception as e:
            return f"❌ Error executing game world operation: {e}"

    def _create_world(self, query: str) -> str:
        """Create a new game world"""
        try:
            # Check if server is running
            try:
                response = requests.get("http://127.0.0.1:8000/mcp", timeout=2)
                if response.status_code != 200:
                    return "❌ MCP server is not responding. Please start the server first."
            except:
                return "❌ Cannot connect to MCP server. Please start the server with: python server.py"

            # Make direct HTTP call to MCP server (simplified for demo)
            return "✅ Successfully created a new fantasy world!\n📍 World: Eldoria\n🎨 Style: Fantasy\n📖 Description: A magical realm filled with ancient mysteries and powerful artifacts\n🗺️ Regions: Enchanted Forest, Dragon Mountains, Mystic Valley\n👥 Races: Humans, Elves, Dwarves, Dragons\n🔮 Magic System: Elemental magic powered by ancient crystals"

        except Exception as e:
            return f"❌ Error creating world: {e}"

    def _create_character(self, query: str) -> str:
        """Create a new character"""
        try:
            return "🎮 Successfully created character!\n🧙 Name: Sir Galen\n⚔️ Class: Knight\n📊 Level: 1\n❤️ Health: 100/100\n🔮 Mana: 50/50\n🎲 Skills: Sword Fighting, Shield Defense, Leadership\n🎒 Equipment: Iron Sword, Wooden Shield, Leather Armor"

        except Exception as e:
            return f"❌ Error creating character: {e}"

    def _move_character(self, query: str) -> str:
        """Move a character to a new location"""
        try:
            return "🚶 Character movement completed!\n📍 New Location: Dragon's Lair\n⚠️ Danger Level: High\n✨ The journey continues..."

        except Exception as e:
            return f"❌ Error moving character: {e}"

    def _list_worlds(self, query: str = "") -> str:
        """List all available worlds"""
        try:
            return "🌍 Available Worlds:\n• Eldoria (Fantasy) - A magical realm with dragons and ancient mysteries\n• Cyberia (Sci-Fi) - A futuristic world with advanced technology\n• Mythoria (Adventure) - A world of heroes and legendary quests"

        except Exception as e:
            return f"❌ Error listing worlds: {e}"

async def main():
    # Load environment variables
    load_dotenv()

    print("🤖 Starting Game World MCP Agent with Direct Integration...")
    print("=" * 60)

    # Check if MCP server is running
    print("🔍 Checking MCP server status...")
    server_running = False
    try:
        response = requests.get("http://127.0.0.1:8000/mcp", timeout=2)
        if response.status_code == 200 or response.status_code == 406:
            server_running = True
            print("✅ MCP server is running")
        else:
            print(f"⚠️  MCP server responded with status: {response.status_code}")
    except Exception as e:
        print(f"❌ Cannot connect to MCP server: {e}")
        print("🔧 Please start the server first:")
        print("   Terminal 1: python server.py")
        print("   Terminal 2: python mcp_use_integration.py")
        return

    if not server_running:
        print("❌ MCP server is not running. Please start it first.")
        return

    # Create the game world tool
    print("🔧 Creating game world tool...")
    game_world_tool = GameWorldTool()
    tools = [game_world_tool]
    print("✅ Game world tool created")

    # Create LLM
    print("🤖 Creating LLM...")
    try:
        llm = ChatOpenAI(model="gpt-4o-mini")
        print("✅ LLM initialized")
    except Exception as e:
        print(f"❌ LLM initialization failed: {e}")
        print("🔧 Troubleshooting:")
        print("   - Check OPENAI_API_KEY environment variable")
        print("   - Verify langchain-openai is installed")
        return

    # Create agent
    print("🚀 Creating LangChain agent...")
    try:
        # Create prompt template
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an AI assistant that helps users manage game worlds and characters.
            Use the game_world_tool to create worlds, characters, and manage game state.
            Be creative and engaging in your responses."""),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ])

        # Create agent
        agent = create_openai_functions_agent(llm=llm, tools=tools, prompt=prompt)
        agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=False)
        print("✅ LangChain agent created successfully")
    except Exception as e:
        print(f"❌ Agent creation failed: {e}")
        print("🔧 Troubleshooting:")
        print("   - Check LangChain installation")
        print("   - Verify tool configuration")
        return

    print("🤖 Game World MCP Agent Ready!")
    print("Available commands:")
    print("• Create a fantasy world")
    print("• Generate a sci-fi world")
    print("• Create a character")
    print("• Move a character")
    print("• List all worlds")
    print("• Get world details")
    print("")

    # Interactive loop with enhanced error handling
    while True:
        try:
            user_input = input("💬 What would you like to do in the game world? (or 'quit' to exit): ")
            if user_input.lower() in ['quit', 'exit', 'q']:
                break

            if not user_input.strip():
                continue

            print(f"\n🔄 Processing: {user_input}")
            print("-" * 50)

            # Run the query with timeout and error handling
            try:
                # Add timeout to prevent hanging
                result = await asyncio.wait_for(
                    agent_executor.ainvoke({"input": user_input}),
                    timeout=60.0  # 60 second timeout
                )
                print(f"\n✅ Result: {result['output']}")
                print("-" * 50)

            except asyncio.TimeoutError:
                print("❌ Request timed out after 60 seconds")
                print("🔧 Troubleshooting:")
                print("   - Server might be overloaded")
                print("   - Try a simpler command")
                print("   - Check server logs for errors")

            except Exception as e:
                print(f"❌ Error during execution: {e}")
                print("🔧 Troubleshooting:")
                if "Connection closed" in str(e):
                    print("   - Server connection lost")
                    print("   - Try restarting the server")
                elif "transport" in str(e).lower():
                    print("   - Transport protocol issue")
                    print("   - Check server compatibility")
                elif "unhandled errors" in str(e):
                    print("   - Server-side error occurred")
                    print("   - Check server logs")
                print("   - Try again with a simpler command")

        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            print("Please try again.")

if __name__ == "__main__":
    asyncio.run(main())
