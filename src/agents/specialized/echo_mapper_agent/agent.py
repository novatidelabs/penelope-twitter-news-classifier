"""Echo Mapper Agent"""

import logging
from typing import Dict, Any
from src.models.state import AnalysisState
from src.api.client import APIClient
from src.agents.core.base_agent import BaseAgent
from .prompt import ECHO_MAPPER_INSTRUCTIONS

logger = logging.getLogger(__name__)


async def echo_mapper_agent(state: AnalysisState, api_client: APIClient) -> Dict[str, Any]:
    """Tracks cross-platform virality and echo metrics."""
    logger.info("Running echo mapper node...")
    
    base_agent = BaseAgent(api_client, "echo_mapper")
    
    try:
        tweet_text = base_agent.extract_tweet_text(state)
        cross_platform_data = "No cross-platform data available yet"
        
        prompt = f"""{ECHO_MAPPER_INSTRUCTIONS}

Tweet Content: {tweet_text[:1200]}
Author: {state.get('tweet_data', {}).get('author_username', 'N/A')}
Tweet ID: {state.get('tweet_id', 'N/A')}

Cross-Platform Data: {cross_platform_data}
"""
        
        response = await base_agent.call_llm(prompt)
        parsed = base_agent.parse_response(response)
        
        echo_velocity = parsed.get("echo_velocity", 0.0)
        logger.success(f"Echo mapping complete | Velocity: {echo_velocity:.2f}")
        
        return {
            "echo_detected": echo_velocity > 0.5,
            "echo_velocity": echo_velocity,
            "reddit_threads": parsed.get("reddit_threads", 0),
            "farcaster_refs": parsed.get("farcaster_refs", 0),
        }
        
    except Exception as e:
        logger.error(f"Echo mapping failed: {e}")
        return {
            "echo_detected": False,
            "echo_velocity": 0.0,
            "error": str(e)
        }
