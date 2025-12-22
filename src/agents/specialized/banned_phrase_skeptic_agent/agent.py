"""Banned Phrase Skeptic Agent"""

import logging
from typing import Dict, Any
from src.state import AnalysisState
from src.api.client import APIClient
from src.agents.core.base_agent import BaseAgent
from .prompt import BANNED_PHRASE_SKEPTIC_INSTRUCTIONS

logger = logging.getLogger(__name__)


async def banned_phrase_skeptic_agent(state: AnalysisState, api_client: APIClient) -> Dict[str, Any]:
    """Detects banned words and applies tone penalties."""
    logger.info("Running banned phrase skeptic node...")
    
    base_agent = BaseAgent(api_client, "banned_phrase_skeptic")
    
    try:
        tweet_text = base_agent.extract_tweet_text(state)
        banned_phrases = "Standard banned phrase taxonomy: moon, lambo, trash, etc."
        
        prompt = f"""{BANNED_PHRASE_SKEPTIC_INSTRUCTIONS}

Tweet Content: {tweet_text[:1200]}
Author: {state.get('tweet_data', {}).get('author_username', 'N/A')}
Tweet ID: {state.get('tweet_id', 'N/A')}

Banned Phrase Taxonomy: {banned_phrases}
"""
        
        response = await base_agent.call_llm(prompt)
        parsed = base_agent.parse_response(response)
        
        banned_terms = parsed.get("banned_terms", [])
        tone_penalty = parsed.get("tone_penalty", 0.0)
        logger.success(f"Banned phrase check complete | Terms found: {len(banned_terms)} | Penalty: {tone_penalty:.2f}")
        
        return {
            "banned_phrases": banned_terms,
            "tone_penalty": tone_penalty,
            "violation_categories": parsed.get("violation_categories", []),
        }
        
    except Exception as e:
        logger.error(f"Banned phrase check failed: {e}")
        return {
            "banned_phrases": [],
            "tone_penalty": 0.0,
            "error": str(e)
        }
