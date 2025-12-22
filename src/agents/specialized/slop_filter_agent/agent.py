"""Slop Filter Agent"""

import logging
from typing import Dict, Any
from src.models.state import AnalysisState
from src.api.client import APIClient
from src.agents.core.base_agent import BaseAgent
from .prompt import SLOP_FILTER_INSTRUCTIONS

logger = logging.getLogger(__name__)


async def slop_filter_agent(state: AnalysisState, api_client: APIClient) -> Dict[str, Any]:
    """Detects low-effort and AI-generated content."""
    logger.info("Running slop filter node...")
    
    base_agent = BaseAgent(api_client, "slop_filter")
    
    try:
        tweet_text = base_agent.extract_tweet_text(state)
        
        prompt = f"""{SLOP_FILTER_INSTRUCTIONS}

Tweet Content: {tweet_text[:1200]}
Author: {state.get('tweet_data', {}).get('author_username', 'N/A')}
Tweet ID: {state.get('tweet_id', 'N/A')}
"""
        
        response = await base_agent.call_llm(prompt)
        parsed = base_agent.parse_response(response)
        
        is_sloppy = parsed.get("is_sloppy", False)
        quality_pass = not is_sloppy
        logger.success(f"Slop filter complete | Quality Pass: {quality_pass} | Sloppy: {is_sloppy}")
        
        return {
            "quality_pass": quality_pass,
            "quality_score": 1.0 - parsed.get("slop_score", 0.0),
            "quality_reasoning": parsed.get("reasoning", ""),
            "is_sloppy": is_sloppy,
        }
        
    except Exception as e:
        logger.error(f"Slop filter failed: {e}")
        return {
            "quality_pass": True,
            "quality_score": 5.0,
            "is_sloppy": False,
            "error": str(e)
        }
