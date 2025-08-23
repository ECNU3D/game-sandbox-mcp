"""
Test configuration and shared fixtures for the Game World Sandbox MCP tests.
"""
import pytest
import uuid
from typing import Dict, Any, List
from faker import Faker

from world_bible_schema import (
    WorldBible, PlayerCharacter, Metadata, Cosmology, Geography,
    Society, History, Systems, CharacterAttributes, Skill, InventoryItem
)

fake = Faker()

# Test data factories
@pytest.fixture
def sample_metadata() -> Dict[str, Any]:
    """Sample metadata for testing."""
    return {
        "name": fake.name() + " World",
        "description": fake.text(max_nb_chars=200),
        "style": "Fantasy",
        "version": "1.0.0",
        "author": fake.name(),
        "tags": ["test", "fantasy"]
    }

@pytest.fixture
def sample_cosmology() -> Dict[str, Any]:
    """Sample cosmology for testing."""
    return {
        "magic_system": "Elemental magic drawn from nature spirits",
        "tech_level": "Medieval",
        "calendar_system": "Twelve-month lunar calendar",
        "physics_laws": "Standard physics with magical exceptions",
        "metaphysics": "Spiritual energy permeates the world"
    }

@pytest.fixture
def sample_geography() -> Dict[str, Any]:
    """Sample geography for testing."""
    return {
        "macro_geography": "Three main continents with diverse biomes",
        "key_regions": [
            {
                "name": "Starting Village",
                "description": "A humble beginning for adventurers"
            },
            {
                "name": "Ancient Ruins",
                "description": "Remnants of a lost civilization"
            },
            {
                "name": "Capital City",
                "description": "The political and economic heart of the realm"
            }
        ],
        "climate_zones": ["Temperate", "Tropical"],
        "natural_resources": ["Gold", "Silver", "Magic Crystals"],
        "strategic_locations": [
            {
                "name": "Dragon's Peak",
                "importance": "Strategic mountain pass",
                "coordinates": "42.5, -71.2"
            }
        ]
    }

@pytest.fixture
def sample_society() -> Dict[str, Any]:
    """Sample society for testing."""
    return {
        "races": [
            {
                "name": "Humans",
                "description": "Adaptable and ambitious, found everywhere"
            },
            {
                "name": "Elves",
                "description": "Graceful and long-lived, connected to nature"
            }
        ],
        "factions": [
            {
                "name": "Merchants Guild",
                "description": "Controls trade and commerce"
            },
            {
                "name": "Mages Council",
                "description": "Regulates magical practices"
            }
        ],
        "social_structure": "Feudal system with modern elements",
        "cultural_traits": ["Honor-bound", "Magic-respecting"],
        "languages": ["Common", "Elvish", "Dwarvish"],
        "religions": [
            {
                "name": "Nature Pantheon",
                "description": "Worship of nature spirits"
            }
        ]
    }

@pytest.fixture
def sample_history() -> Dict[str, Any]:
    """Sample history for testing."""
    return {
        "creation_myth": "In the beginning, the gods shaped the world from chaos.",
        "major_conflicts": "The Great War between light and darkness.",
        "historical_events": [
            "The Founding of the First Kingdom",
            "The Discovery of Magic",
            "The Dragon Wars"
        ],
        "timeline": {
            "year_0": "World creation",
            "year_1000": "First Kingdom founded",
            "year_1500": "Magic discovery"
        },
        "prophecies": ["The Chosen One will unite the kingdoms"],
        "lost_knowledge": ["Ancient rune magic", "Lost city locations"]
    }

@pytest.fixture
def sample_systems() -> Dict[str, Any]:
    """Sample systems for testing."""
    return {
        "economy": "Mixed barter and gold standard with magical currencies",
        "abilities": "Magic schools (Arcane, Divine, Nature) and martial skills",
        "items": "Weapons, armor, potions, scrolls, and enchanted artifacts",
        "combat_system": "D20-based combat with magic integration",
        "progression_system": "Level-based advancement with experience points",
        "crafting_system": "Skill-based crafting with quality modifiers"
    }

@pytest.fixture
def sample_character_attributes() -> Dict[str, Any]:
    """Sample character attributes for testing."""
    return {
        "health": 120,
        "max_health": 120,
        "mana": 80,
        "max_mana": 80,
        "stamina": 100,
        "max_stamina": 100,
        "strength": 14,
        "agility": 16,
        "intelligence": 12,
        "wisdom": 15,
        "charisma": 13,
        "luck": 10,
        "armor_class": 15,
        "magic_resistance": 10,
        "movement_speed": 12
    }

@pytest.fixture
def sample_skills() -> List[Dict[str, Any]]:
    """Sample skills for testing."""
    return [
        {
            "name": "Archery",
            "level": 15,
            "experience": 1200,
            "max_level": 100,
            "description": "Mastery of bow and arrow combat"
        },
        {
            "name": "Stealth",
            "level": 12,
            "experience": 800,
            "max_level": 100,
            "description": "Ability to move unseen and unheard"
        }
    ]

@pytest.fixture
def sample_inventory() -> List[Dict[str, Any]]:
    """Sample inventory for testing."""
    return [
        {
            "name": "Longbow",
            "description": "A sturdy longbow made of yew",
            "type": "weapon",
            "rarity": "Common",
            "value": 50,
            "weight": 2.0,
            "properties": {"damage": "1d8", "range": "150ft"},
            "durability": 100
        },
        {
            "name": "Health Potion",
            "description": "Restores 50 health points",
            "type": "consumable",
            "rarity": "Common",
            "value": 25,
            "weight": 0.5,
            "properties": {"healing": 50},
            "durability": None
        }
    ]

@pytest.fixture
def sample_player_character(sample_character_attributes, sample_skills, sample_inventory) -> Dict[str, Any]:
    """Complete sample player character for testing."""
    return {
        "name": "Elara Moonshadow",
        "race": "Elf",
        "character_class": "Ranger",
        "level": 1,
        "experience": 0,
        "description": "A graceful elf with silver hair and emerald eyes",
        "backstory": "Born to the ancient Moonshadow tribe, trained from childhood in archery and nature magic",
        "attributes": sample_character_attributes,
        "skills": sample_skills,
        "inventory": sample_inventory,
        "current_location": "Starting Village",
        "goals": ["Find the lost Moonshadow tribe", "Master nature magic"],
        "reputation": {"Elven Council": 10, "Forest Spirits": 25},
        "quests": [
            {
                "name": "The Lost Grove",
                "description": "Find the sacred grove hidden in the forest",
                "status": "active",
                "objectives": ["Find the grove entrance", "Retrieve the Moonstone"]
            }
        ],
        "status_effects": [],
        # GEMINI.md enhancements
        "personality": "INFJ - The Advocate",
        "short_term_goals": ["Find the Moonstone", "Master basic nature magic"],
        "long_term_goals": ["Reunite the Moonshadow tribe", "Become a guardian of the forest"],
        "relationships": {"Elven Council": "trusted", "Forest Spirits": "protected", "Dark Forces": "enemy"}
    }

@pytest.fixture
def sample_world_bible_data(sample_metadata, sample_cosmology, sample_geography,
                          sample_society, sample_history, sample_systems) -> Dict[str, Any]:
    """Complete sample world bible data for testing."""
    return {
        "metadata": sample_metadata,
        "cosmology": sample_cosmology,
        "geography": sample_geography,
        "society": sample_society,
        "history": sample_history,
        "systems": sample_systems
    }

@pytest.fixture
def world_id() -> str:
    """Generate a test world ID."""
    return str(uuid.uuid4())

@pytest.fixture
def mock_context():
    """Mock FastMCP context for testing."""
    class MockContext:
        async def info(self, message: str):
            pass

        async def error(self, message: str):
            pass

        async def warning(self, message: str):
            pass

    return MockContext()
