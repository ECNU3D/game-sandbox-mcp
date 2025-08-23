"""
Proper Gemini 2.5 Flash + MCP Server Integration

This demonstrates the CORRECT way to integrate MCP with Gemini:
- Uses actual MCP server (not mock tools)
- Gemini has access to real MCP tools and decides when to use them
- Proper MCP client implementation using mcp-use library

Based on Model Context Protocol (MCP) concepts where AI models
have access to external tools and decide when to use them.
"""

import asyncio
import json
import sys
from typing import Dict, List, Any, Optional

# Import mcp-use for proper MCP client functionality
from mcp_use import MCPClient

# Import Gemini for AI integration
from google import genai
from google.genai import types


class GeminiGameMaster:
    """AI Game Master that uses Gemini 2.5 Flash with proper MCP tool integration."""

    def __init__(self):
        """Initialize the Game Master with Gemini client and MCP tools."""
        self.gemini_client = genai.Client()

        # Configure MCP server connection to connect to existing server
        config = {
            "mcpServers": {
                "game_world": {
                    "url": "http://localhost:8000/mcp"
                }
            }
        }
        self.mcp_client = MCPClient.from_dict(config)
        self.game_history = []

    def create_mcp_function_declarations(self) -> List[types.Tool]:
        """Create function declarations for MCP tools that Gemini can call."""

        return [
            types.Tool(
                function_declarations=[
                    types.FunctionDeclaration(
                        name="generate_world",
                        description="Generate a new game world with the specified style (Fantasy, Sci-Fi, Cyberpunk, etc.)",
                        parameters={
                            "type": "OBJECT",
                            "properties": {
                                "style": {
                                    "type": "STRING",
                                    "description": "The genre/style of the world"
                                }
                            },
                            "required": ["style"]
                        }
                    ),
                    types.FunctionDeclaration(
                        name="create_character",
                        description="Create a new character in a specific world",
                        parameters={
                            "type": "OBJECT",
                            "properties": {
                                "world_id": {
                                    "type": "STRING",
                                    "description": "The ID of the world to create the character in"
                                },
                                "character_data": {
                                    "type": "OBJECT",
                                    "description": "Character information",
                                    "properties": {
                                        "name": {"type": "STRING", "description": "Character name"},
                                        "race": {"type": "STRING", "description": "Character race"},
                                        "character_class": {"type": "STRING", "description": "Character class"},
                                        "description": {"type": "STRING", "description": "Character description"},
                                        "level": {"type": "INTEGER", "description": "Character level"}
                                    }
                                }
                            },
                            "required": ["world_id", "character_data"]
                        }
                    ),
                    types.FunctionDeclaration(
                        name="update_character_location",
                        description="Move a character to a new location",
                        parameters={
                            "type": "OBJECT",
                            "properties": {
                                "world_id": {
                                    "type": "STRING",
                                    "description": "The ID of the world"
                                },
                                "character_name": {
                                    "type": "STRING",
                                    "description": "The name of the character to move"
                                },
                                "new_location": {
                                    "type": "STRING",
                                    "description": "The new location for the character"
                                }
                            },
                            "required": ["world_id", "character_name", "new_location"]
                        }
                    ),
                    types.FunctionDeclaration(
                        name="list_worlds",
                        description="List all available game worlds",
                        parameters={
                            "type": "OBJECT",
                            "properties": {},
                            "required": []
                        }
                    )
                ]
            )
        ]

    async def execute_mcp_tool(self, function_name: str, args: Dict[str, Any]) -> Dict[str, Any]:
        """Execute an MCP tool function based on Gemini's function call."""
        try:
            # Create session and call the tool
            session = await self.mcp_client.create_session("game_world")
            result = await session.call_tool(function_name, args)
            await self.mcp_client.close_session("game_world")
            return result
        except Exception as e:
            print(f"⚠️ MCP Server error: {e}")
            return {"error": f"Failed to execute {function_name}: {str(e)}"}

    async def process_game_request(self, user_request: str) -> str:
        """Process a user request using Gemini with MCP tools available."""

        system_prompt = """
        You are an intelligent Game Master for an open-world adventure game.
        You have access to MCP (Model Context Protocol) tools to manage game worlds and characters.

        Available tools:
        - generate_world: Create a new game world with a specific style
        - create_character: Create a new character in a world
        - update_character_location: Move a character to a new location
        - list_worlds: List all available worlds

        When the user wants to:
        - Create a world: Use the generate_world tool
        - Create a character: Use the create_character tool
        - Move or explore: Use the update_character_location tool
        - Check status: Use the list_worlds tool

        Provide immersive, engaging responses as a Game Master. Only use the MCP tools when necessary
        to manage the game state. For general conversation or descriptions, respond naturally without
        calling tools.

        If you call a tool, explain what happened in an engaging way to the player.
        """

        print(f"\n🎮 User request: {user_request}")

        try:
            response = self.gemini_client.models.generate_content(
                model='gemini-2.0-flash-exp',
                contents=[
                    system_prompt,
                    f"\nUser request: {user_request}"
                ],
                config=types.GenerateContentConfig(
                    tools=self.create_mcp_function_declarations(),
                    automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=True)
                )
            )

            # Check if Gemini wants to call any tools
            if response.function_calls:
                print(f"🔧 Gemini requested {len(response.function_calls)} tool calls")

                # Execute the tool calls
                tool_results = []
                for function_call in response.function_calls:
                    print(f"📞 Executing: {function_call.name}({function_call.args})")
                    result = await self.execute_mcp_tool(function_call.name, dict(function_call.args))
                    tool_results.append(result)

                # Provide the tool results back to Gemini for a final response
                function_responses = []
                for i, (function_call, result) in enumerate(zip(response.function_calls, tool_results)):
                    function_responses.append(types.Part.from_function_response(
                        name=function_call.name,
                        response={"result": result}
                    ))

                # Get final response from Gemini with tool results
                final_response = self.gemini_client.models.generate_content(
                    model='gemini-2.0-flash-exp',
                    contents=[
                        system_prompt,
                        f"\nUser request: {user_request}",
                        response.candidates[0].content,
                        types.Content(role="tool", parts=function_responses)
                    ]
                )

                final_text = final_response.text
            else:
                # No tool calls, use the direct response
                final_text = response.text

            # Add to game history
            self.game_history.append({
                "user_request": user_request,
                "gm_response": final_text,
                "tool_calls": len(response.function_calls) if response.function_calls else 0
            })

            return final_text

        except Exception as e:
            print(f"❌ Error processing request: {e}")
            return f"I encountered an error while processing your request: {str(e)}"


async def demo_proper_mcp_integration():
    """Demonstrate proper MCP integration where Gemini decides when to use tools."""

    print("🎮 **Proper Gemini + MCP Integration Demo**")
    print("=" * 60)
    print("This demo shows Gemini using MCP tools intelligently:")
    print("- Gemini decides when to call MCP tools")
    print("- Tools are executed and results fed back to Gemini")
    print("- Natural conversation with structured game management")
    print("=" * 60)

    gm = GeminiGameMaster()

    # Demo scenarios that will trigger different MCP tool calls
    scenarios = [
        "Create a fantasy world with magic and dragons",
        "Create a brave knight named Sir Galen in that world",
        "Move Sir Galen to the dragon's lair",
        "What worlds do we have available?",
        "Create a sci-fi world with spaceships",
        "Tell me about our current adventures"
    ]

    for scenario in scenarios:
        print(f"\n🎯 **Scenario: {scenario}**")
        print("-" * 50)

        response = await gm.process_game_request(scenario)
        print(f"🤖 Game Master: {response}")
        print()

        # Small delay between requests
        await asyncio.sleep(1)

    print("=" * 60)
    print("🎉 **Demo Complete!**")
    print(f"Total interactions: {len(gm.game_history)}")
    print(f"Tool calls made: {sum(h['tool_calls'] for h in gm.game_history)}")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(demo_proper_mcp_integration())
