
import uuid
import json
import logging
from typing import Dict, Optional
from contextlib import asynccontextmanager
from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from fastmcp import FastMCP, Context
from world_bible_schema import WorldBible, PlayerCharacter

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 2. In-memory storage for generated worlds (for now)
# In a real application, you would use a database.
WORLD_STORAGE: Dict[str, WorldBible] = {}

@asynccontextmanager
async def lifespan(app):
    """Manage the lifespan of the FastMCP application."""
    logger.info("Starting Game World Manager MCP Server")
    logger.info(f"World storage initialized with {len(WORLD_STORAGE)} existing worlds")
    yield
    logger.info("Shutting down Game World Manager MCP Server")
    WORLD_STORAGE.clear()

# 1. Initialize FastMCP Server with modern patterns
mcp = FastMCP(
    name="GameWorldManager",
    instructions="""
    This server manages the lifecycle of game worlds for LLM-driven text adventures.
    Use the 'generate_world' tool to create a new world with structured data.
    Access world data via the 'worlds://{world_id}' resource.
    Create and manage player characters with full attribute systems.
    """,
    lifespan=lifespan
)

# 3. World Generation Tool
@mcp.tool
def generate_world(style: str, ctx: Context) -> dict:
    """
    Generates a new game world based on a specified style (e.g., 'Fantasy', 'Sci-Fi', 'Cyberpunk').

    This function creates a structured game world with consistent cosmology, geography,
    society, and systems. The world follows modern game development best practices
    for consistency and replayability.

    Args:
        style: The genre/style of the world (Fantasy, Sci-Fi, Cyberpunk, etc.)
        ctx: FastMCP context for logging and session management

    Returns:
        dict: Contains world_id and success message

    Raises:
        HTTPException: If world generation fails
    """
    try:
        # Validate input
        if not style or not isinstance(style, str):
            raise ValueError("Style must be a non-empty string")

        world_id = str(uuid.uuid4())
        logger.info(f"Starting world generation for style: {style}")

        # Create world based on style with enhanced templates
        world_templates = {
            "Fantasy": {
                "magic_system": "Elemental magic drawn from nature spirits and ancient runes",
                "tech_level": "Medieval",
                "calendar_system": "Twelve-month lunar calendar with solstice festivals",
                "physics_laws": "Standard physics with magical exceptions and divine interventions",
                "metaphysics": "Magic flows through ley lines and is powered by belief and ritual",
                "economy": "Mixed barter and gold standard with magical currencies",
                "abilities": "Magic schools (Arcane, Divine, Nature) and martial skills",
                "items": "Weapons, armor, potions, scrolls, and enchanted artifacts",
                "combat_system": "D20-based combat with tactical positioning and magical effects"
            },
            "Sci-Fi": {
                "magic_system": "No magic - advanced technology and AI",
                "tech_level": "Interstellar",
                "calendar_system": "Galactic Standard Time with planet-specific adjustments",
                "physics_laws": "Advanced physics including quantum mechanics and relativity",
                "metaphysics": "Scientific understanding of the universe with emerging AI consciousness",
                "economy": "Digital credits with blockchain-based transactions and interstellar trade networks",
                "currency": "Universal Credits and Quantum Coins",
                "abilities": "Cybernetic enhancements, hacking skills, and starship operation",
                "items": "Energy weapons, medical nanites, holo-devices, and AI companions",
                "combat_system": "Tech-based combat with hacking, energy weapons, and tactical systems"
            },
            "Cyberpunk": {
                "magic_system": "Hacking and digital sorcery",
                "tech_level": "Near Future",
                "calendar_system": "Neo-Tokyo Standard Time with corporate calendar overlays",
                "physics_laws": "Modern physics with cybernetic enhancements and digital interfaces",
                "metaphysics": "Transhumanist philosophy merging human consciousness with digital networks",
                "economy": "Cryptocurrency with corporate scrip and black market exchanges",
                "currency": "Crypto-Tokens and Corporate Scrip",
                "abilities": "Hacking, cybernetics integration, and street combat",
                "items": "Smart weapons, neural implants, designer drugs, and ICE breakers",
                "combat_system": "High-tech combat with cybernetic enhancements and digital warfare"
            }
        }

        template = world_templates.get(style, world_templates["Fantasy"])
        logger.info(f"Using template for {style}: {list(template.keys())}")

        # Generate structured world data
        world_data = {
            "metadata": {
                "name": f"{style} Realm",
                "description": f"A detailed {style.lower()} world with rich lore and consistent systems.",
                "style": style
            },
            "cosmology": {
                "magic_system": template["magic_system"],
                "tech_level": template["tech_level"],
                "calendar_system": template["calendar_system"],
                "physics_laws": template["physics_laws"],
                "metaphysics": template["metaphysics"]
            },
            "geography": {
                "macro_geography": f"Three main continents with diverse biomes and strategic locations",
                "key_regions": [
                    {"name": "Starting Village", "description": "A humble beginning for adventurers"},
                    {"name": "Ancient Ruins", "description": "Remnants of a lost civilization"},
                    {"name": "Capital City", "description": "The political and economic heart of the realm"}
                ]
            },
            "society": {
                "races": [
                    {"name": "Humans", "description": "Adaptable and ambitious, found everywhere"},
                    {"name": "Elves", "description": "Graceful and long-lived, connected to nature"} if style == "Fantasy" else {"name": "Androids", "description": "Artificial beings with growing sentience"},
                    {"name": "Dwarves", "description": "Sturdy craftsmen and warriors"} if style == "Fantasy" else {"name": "Cyborgs", "description": "Enhanced humans with cybernetic upgrades"}
                ],
                "factions": [
                    {"name": "Merchants Guild", "description": "Controls trade and commerce"},
                    {"name": "Mages Council", "description": "Regulates magical practices"} if "magic" in template["magic_system"].lower() else {"name": "Tech Consortium", "description": "Advances technological progress"},
                    {"name": "Adventurers League", "description": "Supports exploration and discovery"}
                ],
                "social_structure": "Feudal system with modern elements and social mobility"
            },
            "history": {
                "creation_myth": f"The {style.lower()} realm was shaped by ancient forces and heroic deeds.",
                "major_conflicts": f"The Great {style} War that shaped the current political landscape.",
                "historical_events": [
                    "The Founding of the First Kingdom",
                    "The Discovery of Ancient Technology" if "tech" in template["tech_level"].lower() else "The Discovery of Ancient Magic",
                    "The Last Great Migration"
                ]
            },
            "systems": {
                "economy": template["economy"],
                "abilities": template["abilities"],
                "items": template["items"],
                "combat_system": template["combat_system"],
                "progression_system": "Level-based advancement with skill trees",
                "crafting_system": "Recipe-based crafting with skill requirements"
            },
            # Add the numerical stability frameworks from GEMINI.md
            "mana_framework": {
                "normal_person": {"min": 0, "max": 50},
                "skilled": {"min": 50, "max": 200},
                "expert": {"min": 200, "max": 500},
                "master": {"min": 500, "max": 1000},
                "spell_costs": {
                    "minor": {"min": 5, "max": 20},
                    "moderate": {"min": 20, "max": 100},
                    "major": {"min": 100, "max": 500},
                    "legendary": {"min": 500, "max": 1000}
                }
            },
            "economic_framework": {
                "currency": template.get("currency", "Gold Coins"),
                "base_prices": {
                    "food": {"bread": 5, "meal": 25, "feast": 100},
                    "clothing": {"basic": 50, "fine": 200, "noble": 1000},
                    "equipment": {"basic_weapon": 100, "fine_weapon": 500, "masterwork": 2000},
                    "potions": {"healing": 50, "mana": 75, "buff": 150},
                    "housing": {"room": 50, "house": 5000, "estate": 50000}
                },
                "price_multipliers": {
                    "common": 1.0,
                    "uncommon": 2.5,
                    "rare": 10.0,
                    "epic": 50.0,
                    "legendary": 250.0
                }
            },
            "skills_framework": {}
        }

        # Validate and create world
        world = WorldBible.parse_obj(world_data)
        WORLD_STORAGE[world_id] = world

        ctx.info(f"Successfully created and stored {style} world {world_id}")
        logger.info(f"Generated world with ID: {world_id} for style: {style}")

        return {
            "world_id": world_id,
            "message": f"World generated successfully with {style} theme",
            "world_name": world.metadata.name,
            "style": style
        }

    except ValueError as e:
        ctx.error(f"Invalid input: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        ctx.error(f"Failed to generate world: {e}")
        logger.error(f"World generation failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to generate world")

# 4. World Data Resource
@mcp.resource("worlds://{world_id}")
def get_world_data(world_id: str, ctx: Context) -> dict:
    """
    Retrieves the complete World Bible data for a given world_id.

    This resource provides access to all world information including metadata,
    cosmology, geography, society, history, systems, and any associated characters.

    Args:
        world_id: Unique identifier of the world
        ctx: FastMCP context for logging

    Returns:
        dict: Complete world data structure

    Raises:
        HTTPException: If world is not found
    """
    try:
        if not world_id or not isinstance(world_id, str):
            raise ValueError("World ID must be a non-empty string")

        if world_id not in WORLD_STORAGE:
            ctx.error(f"World ID not found: {world_id}")
            raise HTTPException(status_code=404, detail=f"World with ID '{world_id}' not found.")

        world = WORLD_STORAGE[world_id]
        ctx.info(f"Retrieved world data for {world_id}")
        logger.info(f"World data accessed: {world_id}")

        return world.dict()

    except ValueError as e:
        ctx.error(f"Invalid world ID: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        ctx.error(f"Failed to retrieve world data: {e}")
        logger.error(f"World data retrieval failed for {world_id}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")

# 5. Character Creation Tool
@mcp.tool
def create_character(world_id: str, character_data: dict, ctx: Context) -> dict:
    """
    Creates and assigns a player character to an existing game world.

    This tool validates character data against the PlayerCharacter schema and
    ensures only one protagonist exists per world. The character becomes the
    central figure for gameplay and story progression.

    Args:
        world_id: ID of the world to add the character to
        character_data: Complete character definition including name, race,
                       backstory, attributes, inventory, etc.
        ctx: FastMCP context for logging

    Returns:
        dict: Success message and character details

    Raises:
        HTTPException: For validation errors or conflicts
    """
    try:
        # Input validation
        if not world_id or not isinstance(world_id, str):
            raise ValueError("World ID must be a non-empty string")
        if not character_data or not isinstance(character_data, dict):
            raise ValueError("Character data must be a non-empty dictionary")

        # World validation
        if world_id not in WORLD_STORAGE:
            ctx.error(f"World ID not found: {world_id}")
            raise HTTPException(status_code=404, detail=f"World with ID '{world_id}' not found.")

        world = WORLD_STORAGE[world_id]

        # Check if character already exists
        if world.protagonist:
            ctx.error(f"Character already exists for world {world_id}")
            raise HTTPException(
                status_code=409,
                detail="Character already exists for this world. Each world can have only one protagonist."
            )

        # Validate and create character
        new_character = PlayerCharacter.parse_obj(character_data)
        world.protagonist = new_character

        ctx.info(f"Successfully created character '{new_character.name}' for world {world_id}")
        logger.info(f"Character created: {new_character.name} in world {world_id}")

        return {
            "message": "Character created successfully.",
            "character_name": new_character.name,
            "character_race": new_character.race,
            "world_id": world_id,
            "location": new_character.current_location
        }

    except ValueError as e:
        ctx.error(f"Invalid input: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        ctx.error(f"Failed to create character: {e}")
        logger.error(f"Character creation failed for world {world_id}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to create character")

# 6. Additional Tools for Enhanced Gameplay
@mcp.tool
def update_character_location(world_id: str, character_name: str, new_location: str, ctx: Context) -> dict:
    """
    Updates a character's current location in the game world.

    This enables dynamic movement and exploration within the world,
    supporting the narrative progression of the game.

    Args:
        world_id: ID of the world containing the character
        character_name: Name of the character to move
        new_location: New location for the character
        ctx: FastMCP context for logging

    Returns:
        dict: Success message with location update details
    """
    try:
        if world_id not in WORLD_STORAGE:
            raise HTTPException(status_code=404, detail="World not found.")

        world = WORLD_STORAGE[world_id]
        if not world.protagonist or world.protagonist.name != character_name:
            raise HTTPException(status_code=404, detail="Character not found in this world.")

        old_location = world.protagonist.current_location
        world.protagonist.current_location = new_location

        ctx.info(f"Moved {character_name} from {old_location} to {new_location}")
        logger.info(f"Character location updated: {character_name} -> {new_location}")

        return {
            "message": f"Successfully moved {character_name}",
            "old_location": old_location,
            "new_location": new_location
        }

    except Exception as e:
        ctx.error(f"Failed to update character location: {e}")
        raise HTTPException(status_code=500, detail="Failed to update location")

@mcp.tool
def list_worlds(ctx: Context) -> dict:
    """
    Lists all generated worlds with their basic information.

    This tool provides an overview of all available game worlds,
    useful for managing multiple game sessions.

    Args:
        ctx: FastMCP context for logging

    Returns:
        dict: List of all worlds with metadata
    """
    try:
        worlds_info = []
        for world_id, world in WORLD_STORAGE.items():
            worlds_info.append({
                "world_id": world_id,
                "name": world.metadata.name,
                "style": world.metadata.style,
                "description": world.metadata.description,
                "has_character": world.protagonist is not None,
                "character_name": world.protagonist.name if world.protagonist else None
            })

        ctx.info(f"Listed {len(worlds_info)} worlds")
        return {
            "worlds": worlds_info,
            "total_count": len(worlds_info)
        }

    except Exception as e:
        ctx.error(f"Failed to list worlds: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve world list")

# 6. Runnable block
if __name__ == "__main__":
    import logging

    # Enable debug logging
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger("mcp")
    logger.setLevel(logging.DEBUG)

    print("Starting FastMCP server on port 8000 with debug logging...")

    # Try different configurations
    try:
        # Try different transport configurations
        print("Trying HTTP transport...")
        mcp.run(transport="http", port=8000, host="127.0.0.1")
    except Exception as e:
        logger.error(f"HTTP transport failed: {e}")
        print(f"❌ HTTP transport failed: {e}")

        try:
            print("Trying SSE transport...")
            mcp.run(transport="sse", port=8000, host="127.0.0.1")
        except Exception as e2:
            logger.error(f"SSE transport failed: {e2}")
            print(f"❌ SSE transport failed: {e2}")

            try:
                print("Trying default transport...")
                mcp.run(port=8000)
            except Exception as e3:
                logger.error(f"Default transport failed: {e3}")
                print(f"❌ All transports failed: {e3}")
                raise

