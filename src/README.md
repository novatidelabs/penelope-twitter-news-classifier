# LangGraph Foundation Structure

This directory contains the new LangGraph-based architecture foundation.

## Directory Structure

```
src/
├── config/              # Configuration with Pydantic Settings
├── models/             # State models (TypedDict & Pydantic)
├── api/                # Unified API client
├── agents/             # Agent functions (to be populated)
│   ├── signal_integrity/
│   ├── core_analysis/
│   └── prompts/        # Domain-grouped prompts
├── graph/              # LangGraph workflow (to be populated)
└── tools/              # Utility functions
```

## Key Components

### Configuration (`config/`)
- `Settings` class using Pydantic Settings
- Loads from `.env` file
- Type-safe configuration access

### Models (`models/`)
- `AnalysisState`: TypedDict for LangGraph state
- `TweetData`: Pydantic model for tweet structure

### API Client (`api/`)
- Unified interface for all external APIs
- OpenAI, Twitter, Reddit, Crypto exchanges
- Built-in rate limiting and retry logic

### Prompts (`agents/prompts/`)
- Domain-grouped prompt templates
- Signal integrity prompts implemented
- Core analysis prompts (to be added)

## Usage Example

```python
from src.config import get_settings
from src.models import AnalysisState, TweetData
from src.api import APIClient

# Get settings
settings = get_settings()

# Create API client
api_client = APIClient(settings)

# Use in LangGraph agents
# (to be implemented in Milestone 2-4)
```

## Next Steps

- Milestone 2: Convert signal integrity agents to functions
- Milestone 3: Convert core analysis agents to functions
- Milestone 4: Build LangGraph StateGraph workflow

