
from pydantic import BaseModel, Field, field_validator, model_validator
from typing import List, Optional, Dict, Any
from enum import Enum
import re

class GameStyle(str, Enum):
    """Predefined game styles with modern classifications."""
    FANTASY = "Fantasy"
    SCI_FI = "Sci-Fi"
    CYBERPUNK = "Cyberpunk"
    STEAMPUNK = "Steampunk"
    POST_APOCALYPTIC = "Post-Apocalyptic"
    HISTORICAL = "Historical"
    MODERN = "Modern"
    HORROR = "Horror"

class TechLevel(str, Enum):
    """Technology levels for consistent world-building."""
    STONE_AGE = "Stone Age"
    BRONZE_AGE = "Bronze Age"
    IRON_AGE = "Iron Age"
    MEDIEVAL = "Medieval"
    RENAISSANCE = "Renaissance"
    INDUSTRIAL = "Industrial"
    MODERN = "Modern"
    INFORMATION = "Information Age"
    NEAR_FUTURE = "Near Future"
    FUTURISTIC = "Futuristic"
    INTERSTELLAR = "Interstellar"
    TRANSHUMAN = "Transhuman"

class Metadata(BaseModel):
    """Enhanced metadata with validation and modern fields."""
    name: str = Field(..., min_length=2, max_length=100, description="The unique name of the world.")
    description: str = Field(..., min_length=10, max_length=500, description="A comprehensive summary of the world's essence and atmosphere.")
    style: GameStyle = Field(..., description="The primary genre or style of the world.")
    version: str = Field(default="1.0.0", description="World version for tracking changes.")
    author: Optional[str] = Field(default=None, description="Creator of this world.")
    tags: List[str] = Field(default_factory=list, description="Descriptive tags for the world.")

    @field_validator('name')
    @classmethod
    def validate_name(cls, v):
        if not v.strip():
            raise ValueError("World name cannot be empty or whitespace")
        if not re.match(r'^[a-zA-Z0-9\s\-_\'".]+$', v):
            raise ValueError("World name contains invalid characters")
        return v.strip()

class Cosmology(BaseModel):
    """Enhanced cosmology with modern game design principles."""
    magic_system: str = Field(..., min_length=10, description="Detailed description of how magic works, its source, limitations, and rules.")
    tech_level: TechLevel = Field(..., description="The general level of technology in this world.")
    calendar_system: str = Field(..., min_length=10, description="Complete calendar system including current year, month names, and seasonal patterns.")
    physics_laws: str = Field(..., min_length=10, description="How physics and natural laws work in this world.")
    metaphysics: str = Field(default="Standard physical laws apply", description="Spiritual and metaphysical rules.")

    @model_validator(mode='after')
    def validate_magic_system_compatibility(self):
        if hasattr(self, 'tech_level') and hasattr(self, 'magic_system'):
            if self.tech_level in ['Futuristic', 'Interstellar', 'Transhuman']:
                if 'magic' in self.magic_system.lower() and 'no magic' not in self.magic_system.lower():
                    raise ValueError("High-tech worlds should not have traditional magic systems")
        return self

class Geography(BaseModel):
    """Enhanced geography with modern mapping standards."""
    macro_geography: str = Field(..., min_length=20, description="Detailed overview of continents, oceans, major landforms, and climate zones.")
    key_regions: List[Dict[str, str]] = Field(..., min_length=3, description="Important regions with coordinates, biomes, and strategic significance.")
    climate_zones: List[str] = Field(default_factory=list, description="Major climate zones and their characteristics.")
    natural_resources: List[str] = Field(default_factory=list, description="Key natural resources available in this world.")
    strategic_locations: List[Dict[str, Any]] = Field(default_factory=list, description="Key locations with tactical importance.")

    @field_validator('key_regions')
    @classmethod
    def validate_regions(cls, v):
        required_fields = {'name', 'description'}
        for region in v:
            if not isinstance(region, dict):
                raise ValueError("Each region must be a dictionary")
            if not required_fields.issubset(region.keys()):
                raise ValueError(f"Region missing required fields: {required_fields}")
            if not region.get('name') or not region.get('description'):
                raise ValueError("Region name and description cannot be empty")
        return v

class Society(BaseModel):
    """Enhanced society model with modern social dynamics."""
    races: List[Dict[str, str]] = Field(..., min_length=1, description="Intelligent races with detailed culture, traits, and societal roles.")
    factions: List[Dict[str, str]] = Field(..., min_length=2, description="Major organizations with clear goals, relationships, and influence levels.")
    social_structure: str = Field(..., min_length=15, description="Complete social hierarchy and class system.")
    cultural_traits: List[str] = Field(default_factory=list, description="Dominant cultural values and traditions.")
    languages: List[str] = Field(default_factory=list, description="Major languages and dialects.")
    religions: List[Dict[str, str]] = Field(default_factory=list, description="Religious systems and their influence.")

    @field_validator('races')
    @classmethod
    def validate_races(cls, v):
        required_fields = {'name', 'description'}
        for race in v:
            if not isinstance(race, dict):
                raise ValueError("Each race must be a dictionary")
            if not required_fields.issubset(race.keys()):
                raise ValueError(f"Race missing required fields: {required_fields}")
        return v

    @field_validator('factions')
    @classmethod
    def validate_factions(cls, v):
        for faction in v:
            if not isinstance(faction, dict):
                raise ValueError("Each faction must be a dictionary")
            if 'name' not in faction or 'description' not in faction:
                raise ValueError("Faction must have name and description")
        return v

class History(BaseModel):
    """Enhanced history with narrative structure and timeline."""
    creation_myth: str = Field(..., min_length=20, description="The foundational story of how the world came to be.")
    major_conflicts: str = Field(..., min_length=15, description="The core, ongoing conflict that drives the world's narrative.")
    historical_events: List[str] = Field(..., min_length=3, max_length=10, description="Key historical events with chronological significance.")
    timeline: Dict[str, str] = Field(default_factory=dict, description="Important dates and their significance.")
    prophecies: List[str] = Field(default_factory=list, description="Known prophecies or future predictions.")
    lost_knowledge: List[str] = Field(default_factory=list, description="Ancient secrets or lost technologies/magic.")

class Systems(BaseModel):
    """Modern game systems with balance and progression frameworks."""
    economy: str = Field(..., min_length=20, description="Complete economic system including currency, trade, and wealth distribution.")
    abilities: str = Field(..., min_length=20, description="Comprehensive skill and power system with progression paths.")
    items: str = Field(..., min_length=20, description="Detailed item system with crafting, rarity, and balance guidelines.")
    combat_system: str = Field(..., min_length=15, description="Rules for conflict resolution and combat mechanics.")
    progression_system: str = Field(default="Level-based advancement", description="How characters grow and improve over time.")
    crafting_system: Optional[str] = Field(default=None, description="Rules for creating and modifying items.")

    @field_validator('economy')
    @classmethod
    def validate_economy(cls, v):
        if 'currency' not in v.lower() and 'trade' not in v.lower() and 'gold' not in v.lower():
            raise ValueError("Economy description must include currency or trade information")
        return v

class CharacterAttributes(BaseModel):
    """Comprehensive character attributes with modern game design."""
    health: int = Field(ge=0, le=1000, description="Current health points")
    max_health: int = Field(ge=1, le=1000, description="Maximum health points")
    mana: int = Field(ge=0, le=1000, description="Current magic/energy points")
    max_mana: int = Field(ge=0, le=1000, description="Maximum magic/energy points")
    stamina: int = Field(ge=0, le=100, description="Current stamina/fatigue level")
    max_stamina: int = Field(ge=1, le=100, description="Maximum stamina")

    # Enhanced mana tracking per GEMINI.md requirements
    mana_tier: str = Field(default="normal_person", description="Mana proficiency tier for game balance")
    mana_regen_rate: float = Field(default=1.0, ge=0.1, le=10.0, description="Mana regeneration rate per minute")

    # Core attributes
    strength: int = Field(ge=1, le=20, description="Physical power and damage")
    agility: int = Field(ge=1, le=20, description="Speed, reflexes, and dexterity")
    intelligence: int = Field(ge=1, le=20, description="Mental acuity and magical power")
    wisdom: int = Field(ge=1, le=20, description="Willpower and perception")
    charisma: int = Field(ge=1, le=20, description="Personality and leadership")
    luck: int = Field(ge=1, le=20, description="Fortune and critical hit chance")

    # Derived attributes
    armor_class: int = Field(ge=0, le=50, description="Defense against physical attacks")
    magic_resistance: int = Field(ge=0, le=100, description="Resistance to magical effects")
    movement_speed: int = Field(ge=1, le=50, description="Base movement speed")

class Skill(BaseModel):
    """Individual skill with progression system per GEMINI.md requirements."""
    name: str = Field(..., description="Skill name")
    level: int = Field(ge=0, le=100, description="Current skill level")
    experience: int = Field(ge=0, description="Experience points in this skill")
    max_level: int = Field(ge=1, le=100, description="Maximum possible level")
    description: str = Field(..., description="What this skill allows")

    # Enhanced skill tracking per GEMINI.md requirements
    power_level: str = Field(default="basic", description="Skill power tier (basic/intermediate/advanced/master)")
    mana_cost: int = Field(default=0, ge=0, le=1000, description="Mana cost to use this skill")
    stamina_cost: int = Field(default=0, ge=0, le=100, description="Stamina cost to use this skill")
    learning_difficulty: str = Field(default="moderate", description="Difficulty to learn (easy/moderate/hard/expert)")
    skill_type: str = Field(default="general", description="Skill category (combat/magic/social/crafting)")
    prerequisites: List[str] = Field(default_factory=list, description="Required skills to learn this one")

class InventoryItem(BaseModel):
    """Enhanced inventory item with modern game features."""
    name: str = Field(..., description="Item name")
    description: str = Field(..., description="Item description and properties")
    type: str = Field(..., description="Item type (weapon, armor, consumable, etc.)")
    rarity: str = Field(default="Common", description="Item rarity tier")
    value: int = Field(ge=0, description="Base monetary value")
    weight: float = Field(ge=0, description="Item weight in kg")
    properties: Dict[str, Any] = Field(default_factory=dict, description="Special properties and effects")
    durability: Optional[int] = Field(None, ge=0, le=100, description="Current durability percentage")

class PlayerCharacter(BaseModel):
    """Enhanced player character with modern RPG systems."""
    name: str = Field(..., min_length=2, max_length=50, description="The character's name.")
    race: str = Field(..., description="The character's race, should match one from the Society model.")
    character_class: str = Field(..., description="Character's primary class or profession.")
    level: int = Field(ge=1, le=100, description="Character level")
    experience: int = Field(ge=0, description="Total experience points")
    description: str = Field(..., min_length=10, description="A physical and personality description of the character.")
    backstory: str = Field(..., min_length=20, description="The character's personal history before the game begins.")
    attributes: CharacterAttributes = Field(..., description="Complete character attributes and stats.")
    skills: List[Skill] = Field(default_factory=list, description="Character's learned skills and abilities.")
    inventory: List[InventoryItem] = Field(default_factory=list, description="A list of items the character is carrying.")
    current_location: str = Field(..., description="The current location of the character, referencing a key region or dynamic location.")
    goals: List[str] = Field(default_factory=list, min_length=1, description="The character's current short-term and long-term objectives.")
    reputation: Dict[str, int] = Field(default_factory=dict, description="Reputation with different factions (range -100 to 100)")
    quests: List[Dict[str, Any]] = Field(default_factory=list, description="Active and completed quests")
    status_effects: List[str] = Field(default_factory=list, description="Current status effects (buffs/debuffs)")

    # Enhanced character framework per GEMINI.md requirements
    personality: str = Field(default="", description="Character personality type (e.g., MBTI)")
    short_term_goals: List[str] = Field(default_factory=list, description="Short-term objectives (1-3 months)")
    long_term_goals: List[str] = Field(default_factory=list, description="Long-term life goals (1+ years)")
    relationships: Dict[str, str] = Field(default_factory=dict, description="Relationships with other characters (friend/ally/enemy/rival/mentor)")

class DynamicCharacter(BaseModel):
    """Dynamic NPC character support per GEMINI.md requirements."""
    name: str = Field(..., min_length=2, max_length=100, description="Character name")
    race: str = Field(..., description="Character race")
    character_class: str = Field(..., description="Character class/profession")
    level: int = Field(ge=1, le=100, description="Character level")
    alignment: str = Field(default="neutral", description="Character alignment (ally/enemy/neutral)")

    # Background and personality
    backstory: str = Field(..., min_length=20, description="Character history and background")
    personality: str = Field(default="", description="Character personality type (e.g., MBTI)")
    motivations: List[str] = Field(default_factory=list, description="Character motivations and goals")

    # Relationships and social
    relationships: Dict[str, str] = Field(default_factory=dict, description="Relationships with other characters")
    faction: str = Field(default="", description="Faction or group affiliation")

    # Attributes (simplified for NPCs)
    attributes: Dict[str, int] = Field(default_factory=lambda: {
        "health": 100, "max_health": 100, "strength": 10, "agility": 10,
        "intelligence": 10, "wisdom": 10, "charisma": 10
    }, description="Character attributes")

    # Location and status
    current_location: str = Field(default="", description="Current location in the world")
    status: str = Field(default="active", description="Character status (active/inactive/deceased)")

    # Game integration
    quest_relevance: List[str] = Field(default_factory=list, description="Quests this character is involved in")
    dialogue_options: List[Dict[str, Any]] = Field(default_factory=list, description="Available dialogue choices")

    @field_validator('name')
    @classmethod
    def validate_name(cls, v):
        if not re.match(r"^[a-zA-Z\s\-']+$", v):
            raise ValueError("Character name contains invalid characters")
        return v.strip()

    @model_validator(mode='before')
    @classmethod
    def validate_character(cls, values):
        if isinstance(values, dict):
            if values.get('experience', 0) < 0:
                raise ValueError("Experience cannot be negative")
            if values.get('level', 1) < 1:
                raise ValueError("Level must be at least 1")
        return values

class WorldBible(BaseModel):
    """The complete and comprehensive definition of a game world with modern features."""
    metadata: Metadata
    cosmology: Cosmology
    geography: Geography
    society: Society
    history: History
    systems: Systems

    # The main character of the story
    protagonist: Optional[PlayerCharacter] = Field(default=None, description="The player's character. Can be added after the world is generated.")

    # These fields will be populated during gameplay per GEMINI.md requirements
    dynamic_characters: List[DynamicCharacter] = Field(default_factory=list, description="NPCs that emerge during gameplay with full character models.")
    dynamic_locations: List[Dict[str, Any]] = Field(default_factory=list, description="Locations discovered during gameplay with coordinates.")
    dynamic_events: List[Dict[str, Any]] = Field(default_factory=list, description="Events that unfold during gameplay.")
    active_quests: List[Dict[str, Any]] = Field(default_factory=list, description="Current active quests in the world.")
    world_state: Dict[str, Any] = Field(default_factory=dict, description="Global world state variables for consistency.")

    # Game balance and progression
    difficulty_level: str = Field(default="Normal", description="World difficulty setting")
    game_balance_settings: Dict[str, Any] = Field(default_factory=dict, description="Balance parameters for gameplay systems.")

    # Numerical stability frameworks (per GEMINI.md requirements)
    mana_framework: Dict[str, Any] = Field(default_factory=lambda: {
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
    }, description="Mana measurement framework for consistency")

    economic_framework: Dict[str, Any] = Field(default_factory=lambda: {
        "currency": "Gold Coins",
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
    }, description="Economic framework with currency and pricing system")

    skills_framework: Dict[str, Any] = Field(default_factory=dict, description="Global skills registry tracking power, costs, and difficulty")

    @model_validator(mode='before')
    @classmethod
    def validate_world_consistency(cls, values):
        """Validate overall world consistency."""
        if isinstance(values, dict):
            cosmology = values.get('cosmology')
            society = values.get('society')

            if cosmology and society:
                # Validate race consistency with tech level
                tech_level = cosmology.get('tech_level')
                for race in society.get('races', []):
                    race_name = race.get('name', '').lower()
                    if tech_level in ['Futuristic', 'Interstellar', 'Transhuman']:
                        if any(ancient in race_name for ancient in ['elf', 'dwarf', 'orc']):
                            raise ValueError(f"Race '{race['name']}' is inconsistent with high-tech setting")

        return values

