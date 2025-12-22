"""Sarcasm Sentinel Agent"""

import logging
from typing import Dict, Any
from src.models.state import AnalysisState
from src.api.client import APIClient
from src.agents.core.base_agent import BaseAgent
from .prompt import SARCASTIC_SENTINEL_INSTRUCTIONS

logger = logging.getLogger(__name__)


async def sarcasm_sentinel_agent(state: AnalysisState, api_client: APIClient) -> Dict[str, Any]:
    """Detects sarcasm, irony, and tone-inverted phrasing."""
    logger.info("Running sarcasm detection node...")
    
    base_agent = BaseAgent(api_client, "sarcasm_sentinel")
    
    try:
        tweet_text = base_agent.extract_tweet_text(state)
        
        prompt = f"""{SARCASTIC_SENTINEL_INSTRUCTIONS}

Tweet Content: {tweet_text[:1200]}
Author: {state.get('tweet_data', {}).get('author_username', 'N/A')}
Tweet ID: {state.get('tweet_id', 'N/A')}
"""
        
        response = await base_agent.call_llm(prompt)
        parsed = base_agent.parse_response(response)
        
        is_sarcastic = parsed.get("is_sarcastic", False)
        p_sarcasm = parsed.get("p_sarcasm", 0.0)
        logger.success(f"Sarcasm detection complete | Sarcastic: {is_sarcastic} | Probability: {p_sarcasm:.2f}")
        
        return {
            "sarcasm_score": p_sarcasm,
            "sarcasm_detected": is_sarcastic,
            "sarcasm_reasoning": parsed.get("reason", ""),
            "confidence_level": parsed.get("confidence_level", "medium"),
        }
        
    except Exception as e:
        logger.error(f"Sarcasm detection failed: {e}")
        return {
            "sarcasm_score": 0.0,
            "sarcasm_detected": False,
            "error": str(e)
        }
