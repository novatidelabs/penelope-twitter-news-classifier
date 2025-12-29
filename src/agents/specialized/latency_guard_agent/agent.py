"""Latency Guard Agent"""

import logging
from typing import Dict, Any
from src.state import AnalysisState
from src.api.client import APIClient
from src.agents.core.base_agent import BaseAgent
from .prompt import LATENCY_GUARD_INSTRUCTIONS

logger = logging.getLogger(__name__)


async def latency_guard_agent(state: AnalysisState, api_client: APIClient) -> Dict[str, Any]:
    """Detects temporal misalignment and stale news."""
    logger.info("Running latency guard node...")
    
    base_agent = BaseAgent(api_client, "latency_guard")
    
    try:
        tweet_text = base_agent.extract_tweet_text(state)
        market_data = "No market data available yet"
        
        prompt = f"""{LATENCY_GUARD_INSTRUCTIONS}

Tweet Content: {tweet_text[:1200]}
Author: {state.get('tweet_data', {}).get('author_username', 'N/A')}
Tweet ID: {state.get('tweet_id', 'N/A')}

Market Data: {market_data}
"""
        
        response = await base_agent.call_llm(prompt)
        parsed = base_agent.parse_response(response)
        
        repriced = parsed.get("repriced", False)
        logger.success(f"Latency guard complete | Repriced: {repriced}")
        
        return {
            "latency_valid": not repriced,
            "content_repriced": repriced,
            "time_delta_seconds": parsed.get("delta_seconds", 0),
            "price_change_pct": parsed.get("price_change_pct", 0.0),
        }
        
    except Exception as e:
        logger.error(f"Latency guard failed: {e}")
        return {
            "latency_valid": True,
            "content_repriced": False,
            "error": str(e)
        }
