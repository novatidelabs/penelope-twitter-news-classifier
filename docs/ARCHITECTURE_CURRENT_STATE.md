# Current Architecture State - Before LangGraph Refactor

**Date**: December 16, 2025  
**Branch**: `refactor/langgraph-foundation`  
**Purpose**: Document current system architecture before LangGraph migration

## Project Structure

```
twitter-news-classifier/
├── main.py                          # Main entry point
├── extract_real_tweets.py           # Tweet extraction script
├── requirements.txt                 # Python dependencies
├── Dockerfile                       # Docker configuration
├── .dockerignore                   # Docker ignore patterns
├── .gitignore                      # Git ignore patterns
├── README.md                       # Project documentation
│
├── application/                     # Application layer
│   ├── __init__.py
│   ├── orchestrators/
│   │   └── twitter_analysis_orchestrator.py
│   └── use_cases/
│       ├── __init__.py
│       └── analyze_tweets_use_case.py
│
├── domain/                          # Domain layer (DDD)
│   ├── __init__.py
│   ├── entities/                    # Business entities
│   │   ├── __init__.py
│   │   ├── tweet.py
│   │   └── analysis_result.py
│   └── services/                    # Domain services
│       ├── __init__.py
│       ├── core_analysis/           # Core analysis agents (12)
│       │   ├── __init__.py
│       │   ├── multi_agent_analyzer.py
│       │   ├── multi_agent_analysis_service.py
│       │   └── tweet_extraction_service.py
│       ├── signal_integrity/        # Signal integrity agents (5)
│       │   ├── __init__.py
│       │   ├── sarcasm_sentinel_agent.py
│       │   ├── echo_mapper_agent.py
│       │   ├── latency_guard_agent.py
│       │   ├── slop_filter_agent.py
│       │   └── banned_phrase_skeptic_agent.py
│       ├── orchestration/           # Orchestration services
│       │   ├── __init__.py
│       │   ├── enhanced_multi_agent_analyzer.py
│       │   └── enhanced_score_consolidator.py
│       └── memory/                  # Memory management
│           ├── __init__.py
│           └── memory_namespace_manager.py
│
├── infrastructure/                  # Infrastructure layer
│   ├── __init__.py
│   ├── adapters/                    # External API adapters
│   │   ├── __init__.py
│   │   └── twitter_api_adapter.py
│   ├── repositories/                # Repository implementations
│   │   ├── __init__.py
│   │   └── file_repository.py
│   ├── prompts/                     # AI agent prompts
│   │   ├── __init__.py
│   │   └── agent_prompts.py
│   └── config.py                    # Configuration (dataclass-based)
│
├── presentation/                    # Presentation layer
│   └── cli/                         # CLI interface (empty, future use)
│
├── tests/                           # Test suite
│   └── integration/
│       ├── __init__.py
│       ├── test_optional_apis.py
│       └── verify_real_data_only.py
│
├── docs/                            # Documentation
│   ├── API_REFERENCE.md
│   ├── TECHNICAL_SPECIFICATION.md
│   └── ENV_TEMPLATE.md
│
├── data/                            # Data storage (gitignored)
│   ├── real_extraction/
│   └── sample_extraction/
│
└── results/                         # Analysis results (gitignored)
    └── twitter_analysis_results_*.json
```

## Architecture Layers

### Domain Layer (`domain/`)
**Purpose**: Core business logic and entities

**Key Components**:
- **Entities**: `Tweet`, `AnalysisResult` - Core business objects
- **Services**: 
  - `core_analysis/` - 12-agent analysis system
  - `signal_integrity/` - 5 signal integrity agents
  - `orchestration/` - Enhanced orchestration and score consolidation
  - `memory/` - Memory namespace management

### Application Layer (`application/`)
**Purpose**: Workflow orchestration and use cases

**Key Components**:
- `orchestrators/twitter_analysis_orchestrator.py` - Main workflow manager
- `use_cases/analyze_tweets_use_case.py` - Use case implementations

### Infrastructure Layer (`infrastructure/`)
**Purpose**: External integrations and technical concerns

**Key Components**:
- `adapters/twitter_api_adapter.py` - Twitter API integration
- `repositories/file_repository.py` - File-based data persistence
- `prompts/agent_prompts.py` - Centralized AI agent prompts
- `config.py` - Configuration class (dataclass-based)

### Presentation Layer (`presentation/`)
**Purpose**: Entry points and user interfaces

**Current State**: Minimal implementation, mostly empty placeholders

## Current System Flow

1. **Entry Point**: `main.py` initializes all 17 agents
2. **Signal Integrity Phase**: 5 agents analyze tweet quality
3. **Core Analysis Phase**: 12 agents perform comprehensive analysis
4. **Score Consolidation**: Enhanced consolidator merges results
5. **Output**: JSON results saved to `results/` directory

## Agents Overview

### Signal Integrity Agents (5)
1. **SarcasmSentinelAgent** - Detects sarcasm and irony
2. **EchoMapperAgent** - Cross-platform virality analysis
3. **LatencyGuardAgent** - Market timing analysis
4. **SlopFilterAgent** - Content quality assessment
5. **BannedPhraseSkepticAgent** - Policy compliance

### Core Analysis Agents (12)
1. Summary Agent
2. Input Preprocessor
3. Context Evaluator
4. Fact Checker
5. Depth Analyzer
6. Relevance Analyzer
7. Structure Analyzer
8. Reflective Agent
9. Metadata Ranking Agent
10. Consensus Agent
11. Score Consolidator
12. Validator

## Configuration System

**Current Implementation**: Dataclass-based `Configuration` class
- Location: `infrastructure/config.py`
- Type: `@dataclass(kw_only=True)`
- Access: Global `config` instance
- Features: Type hints, computed properties, backward compatibility

## Key Files

### Entry Points
- `main.py` - Main execution entry point
- `extract_real_tweets.py` - Tweet extraction script

### Core Services
- `domain/services/core_analysis/multi_agent_analyzer.py` - Core 12-agent system
- `domain/services/orchestration/enhanced_score_consolidator.py` - Score consolidation
- `application/orchestrators/twitter_analysis_orchestrator.py` - Workflow orchestration

### Configuration
- `infrastructure/config.py` - Application configuration (dataclass)
- `.env.example` - Environment variable template

## Data Flow

```
Twitter API → Tweet Extraction → Signal Integrity Agents → Core Analysis Agents → Score Consolidation → JSON Output
```

## Notes for LangGraph Migration

1. **Current Structure**: Domain-Driven Design (DDD) with clear layer separation
2. **Agents**: Currently class-based, will be converted to function-based nodes
3. **Orchestration**: Currently manual, will be handled by LangGraph StateGraph
4. **State Management**: Currently scattered, will be centralized in LangGraph state
5. **Configuration**: Already modernized with dataclass, ready for LangGraph

## Cleanup Status

- ✅ `__pycache__/` directories removed
- ✅ Python cache files removed
- ✅ Empty `__init__.py` files removed (from develop)
- ✅ Codebase structure documented
- ✅ Configuration system modernized

## Next Steps for LangGraph Foundation

1. Create `src/` directory structure
2. Define LangGraph state models
3. Create unified API client
4. Organize prompts by domain
5. Set up graph workflow structure

