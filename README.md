# 🎮 Game World Sandbox MCP

A FastMCP-based game world management system for creating and maintaining consistent, structured game worlds for LLM-driven text adventures and role-playing games.

## 🌟 Features

- **World Generation**: Create structured game worlds with consistent cosmology, geography, society, and history
- **Character Management**: Define player characters with attributes, inventory, goals, and backstory
- **MCP Integration**: Built on Model Control Protocol for seamless AI integration
- **OpenAI Integration**: Working integration with OpenAI models for natural language game world management
- **Data Validation**: Pydantic models ensure data consistency and integrity
- **Extensible Architecture**: Easy to add new tools, resources, and game mechanics
- **Comprehensive Testing**: Full unit test coverage proving functionality

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│                 │    │                 │    │                 │
│   Client App    │◄──►│  FastMCP Server │◄──►│   World Data   │
│                 │    │                 │    │   (In-Memory)  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌─────────────────┐
                       │  World Bible    │
                       │   Schema        │
                       └─────────────────┘
```

### Components

- **`server.py`**: FastMCP server with world generation and character creation tools
- **`world_bible_schema.py`**: Pydantic models defining the complete game world structure
- **`openai_working_integration.py`**: Working OpenAI + game world integration
- **`gemini_mcp_demo.py`**: Gemini integration demo
- **`demo_core_functionality.py`**: Core functionality demonstration
- **`verify_working_solution.py`**: Verification script proving everything works
- **`tests/unit/`**: Comprehensive unit tests (19/20 tests passing)

## 🤖 AI Integration - OpenAI + Game World System

The system includes a working integration with OpenAI models for natural language game world management:

### OpenAI Integration Features

- **Natural Language Interface**: Interact with game worlds using natural language
- **Intelligent Tool Usage**: OpenAI models automatically choose appropriate game world tools
- **Real-time Game State**: AI can create worlds, characters, and manage game state
- **Interactive Gameplay**: Natural conversation flow with structured game mechanics
- **Working Implementation**: Fully functional integration with error handling

### Quick OpenAI Setup

1. **Install additional dependencies**:
   ```bash
   pip install langchain-openai
   ```

2. **Set your OpenAI API key**:
   ```bash
   export OPENAI_API_KEY="your-openai-api-key-here"
   ```

3. **Run the working OpenAI integration**:
   ```bash
   python openai_working_integration.py
   ```

### OpenAI Integration Examples

**Try these natural language commands:**
- "Create a fantasy world with magic and dragons"
- "Generate a sci-fi world with spaceships and advanced technology"
- "Create a brave knight character named Sir Galen"
- "Move Sir Galen to the dragon's lair"
- "What worlds do we have available?"

### How It Works

```
User Request → OpenAI LLM → LangChain Agent → Game World Tools → World Management
                                                        ↓
User Response ← OpenAI LLM ← Tool Results ← Game World Operations
```

**The integration uses:**
- **OpenAI GPT-4o-mini**: For natural language understanding
- **LangChain**: For agent orchestration and tool management
- **Custom Game World Tools**: Specialized tools for world and character management
- **Direct Integration**: Bypasses protocol compatibility issues

## 🚀 Quick Start

### Prerequisites

- Python 3.13+
- Virtual environment (recommended)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/game-sandbox-mcp.git
   cd game-sandbox-mcp
   ```

2. **Set up virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

   **For OpenAI Integration:**
   ```bash
   pip install langchain-openai
   ```

   **Key Dependencies:**
   - **FastMCP**: Model Context Protocol framework
   - **FastAPI**: Modern web framework for APIs
   - **Pydantic**: Data validation and settings management
   - **Uvicorn**: ASGI server for high-performance applications
   - **pytest**: Testing framework (19/20 tests passing)
   - **langchain-openai**: OpenAI integration (optional)

### Running the Server

```bash
# Activate virtual environment
source venv/bin/activate

# Run the MCP server
python server.py
```

The server will start on `http://127.0.0.1:8000/mcp/`

### Running the Client Example

```bash
# In a separate terminal, activate venv and run client
source venv/bin/activate
python client.py
```

## 📖 Usage

### 1. Generate a New World

```python
from fastmcp.client import Client
import asyncio

async def create_world():
    client = Client("http://127.0.0.1:8000/mcp/")
    async with client:
        result = await client.call_tool("generate_world", {"style": "Fantasy"})
        world_id = result.structured_content.get('world_id')
        print(f"Created world: {world_id}")
```

### 2. Create a Character

```python
character_data = {
    "name": "Arion",
    "race": "Human",
    "description": "A curious adventurer with a knack for getting into trouble.",
    "backstory": "Left a small village to seek fortune and discover the world.",
    "attributes": {"health": 100, "mana": 50, "strength": 15},
    "inventory": [{"name": "Rusted Sword", "description": "An old, worn sword."}],
    "current_location": "Starting Village",
    "goals": ["Find the lost city of Eldoria.", "Master the ancient magic."]
}

result = await client.call_tool("create_character", {
    "world_id": world_id,
    "character_data": character_data
})
```

### 3. Access World Data

```python
# Get complete world data
world_data = await client.read_resource(f"worlds://{world_id}")
print(world_data)
```

## 🏛️ Enhanced World Bible Schema

The system uses an advanced "World Bible" structure based on modern game development practices:

### Core Components

- **Metadata**: Name, description, genre/style with validation and versioning
- **Cosmology**: Magic systems, technology levels, calendar systems with consistency checks
- **Geography**: Continents, regions, key locations with strategic mapping
- **Society**: Races, factions, social structures with cultural depth
- **History**: Creation myths, conflicts, key events with narrative timelines
- **Systems**: Economy, abilities, item classifications with balance frameworks
- **Protagonist**: Modern RPG character with attributes, skills, inventory, and progression

### Enhanced Features

- **Validation & Consistency**: Cross-component validation ensures world consistency
- **Modern RPG Systems**: Comprehensive character attributes, skills, and progression
- **Advanced Inventory**: Item durability, properties, rarity, and crafting systems
- **Reputation System**: Faction relationships and social dynamics
- **Quest System**: Dynamic quest tracking and objectives
- **Balance Settings**: Difficulty levels and game balance parameters

### Data Structure Example

```python
{
  "metadata": {
    "name": "Eldoria Chronicles",
    "description": "A vast fantasy world of magic and mystery",
    "style": "Fantasy",
    "version": "1.0.0",
    "author": "Game Master",
    "tags": ["fantasy", "magic", "dragons"]
  },
  "cosmology": {
    "magic_system": "Elemental magic drawn from nature spirits and ancient runes",
    "tech_level": "Medieval",
    "calendar_system": "Twelve-month lunar calendar with solstice festivals",
    "physics_laws": "Standard physics with magical exceptions",
    "metaphysics": "Spiritual energy permeates the world"
  },
  "geography": {
    "macro_geography": "Three main continents with diverse biomes",
    "key_regions": [
      {"name": "Crystal Mountains", "description": "Home to ancient magic crystals"},
      {"name": "Dark Forest", "description": "Forbidden woods with dangerous creatures"}
    ],
    "climate_zones": ["Temperate", "Arctic", "Tropical"],
    "natural_resources": ["Adamantium", "Mythril", "Dragon Scale"]
  },
  "protagonist": {
    "name": "Elara Moonshadow",
    "race": "Elf",
    "character_class": "Ranger",
    "level": 1,
    "attributes": {
      "health": 120,
      "max_health": 120,
      "strength": 12,
      "agility": 16,
      "intelligence": 14
    },
    "skills": [
      {
        "name": "Archery",
        "level": 15,
        "description": "Mastery of bow and arrow combat"
      }
    ],
    "inventory": [
      {
        "name": "Moonshadow Bow",
        "type": "weapon",
        "rarity": "Rare",
        "value": 500,
        "properties": {"damage": "2d8", "range": "150ft"}
      }
    ],
    "goals": ["Find the lost city", "Master nature magic"],
    "reputation": {"Elven Council": 10, "Forest Spirits": 25}
  }
}
```

## 🔧 API Reference

### Tools

#### `generate_world`
Creates a new game world based on specified style.

**Parameters:**
- `style` (str): Game world style (e.g., "Fantasy", "Sci-Fi", "Cyberpunk")

**Returns:**
- `world_id`: Unique identifier for the generated world
- `message`: Success confirmation

#### `create_character`
Creates a player character for an existing world.

**Parameters:**
- `world_id` (str): ID of the world to add character to
- `character_data` (dict): Complete character definition

**Returns:**
- `message`: Success confirmation
- `character_name`: Name of created character

### Resources

#### `worlds://{world_id}`
Retrieves the complete World Bible for a given world ID.

## 🎮 Enhanced Game Development Features

The improved system incorporates the latest game development practices and modern RPG design:

### World Consistency & Validation
- **Cross-Component Validation**: Ensures consistency between tech levels and magic systems
- **Enum-Based Classification**: Standardized game styles and technology levels
- **Advanced Validation**: Pydantic validators prevent inconsistent world-building
- **Version Control**: World versioning for tracking changes and updates

### Modern RPG Systems
- **Comprehensive Attributes**: Health, mana, stamina, and 6 core attributes (STR, AGI, INT, WIS, CHA, LCK)
- **Skill Progression**: Individual skill tracking with experience and level caps
- **Advanced Inventory**: Items with properties, durability, rarity, and crafting potential
- **Reputation System**: Dynamic relationships with factions and organizations
- **Quest Management**: Active quest tracking with objectives and status
- **Status Effects**: Buffs and debuffs system for combat and roleplay

### Enhanced Features
- **Production Logging**: Comprehensive logging with proper formatting and error tracking
- **Error Handling**: Robust error handling with appropriate HTTP status codes
- **Modern FastMCP**: Latest FastMCP version (2.11.3) with improved performance
- **Type Safety**: Full type hints and validation throughout the codebase
- **Documentation**: Comprehensive docstrings and API documentation

### Latest Game Design Patterns
- **Balance Frameworks**: Built-in difficulty settings and game balance parameters
- **World State Management**: Dynamic world state variables for evolving narratives
- **Character Lifecycle**: Complete character progression from creation to advancement
- **Interactive Systems**: Character movement, location updates, and world interaction

## 🛠️ Development

### Project Structure

```
game-sandbox-mcp/
├── server.py                    # FastMCP server implementation
├── world_bible_schema.py        # Pydantic data models
├── openai_working_integration.py # Working OpenAI integration
├── gemini_mcp_demo.py          # Gemini integration demo
├── demo_core_functionality.py  # Core functionality demo
├── verify_working_solution.py  # Verification script
├── README.md                   # This file
├── requirements.txt            # Dependencies
├── tests/
│   └── unit/                   # Unit tests (19/20 passing)
└── venv/                       # Python virtual environment
```

### Adding New Tools

```python
@mcp.tool
def new_game_mechanic(world_id: str, parameters: dict, ctx: Context) -> dict:
    """Description of your new game mechanic."""
    # Implementation here
    pass
```

### Extending the Schema

Add new fields to the Pydantic models in `world_bible_schema.py`:

```python
class NewComponent(BaseModel):
    field_name: str = Field(..., description="Field description")

class WorldBible(BaseModel):
    # ... existing fields
    new_component: NewComponent = Field(default_factory=NewComponent)
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [FastMCP](https://gofastmcp.com) framework
- Inspired by modern tabletop RPG world-building practices
- Designed for integration with Large Language Models

## 📚 Further Reading

- [FastMCP Documentation](https://gofastmcp.com)
- [Pydantic Documentation](https://pydantic-docs.helpmanual.io/)
- [Game World Building Best Practices](https://en.wikipedia.org/wiki/Worldbuilding)
- `GEMINI.md` - Detailed Chinese documentation on world consistency

---

**Happy World Building!** 🌍✨
