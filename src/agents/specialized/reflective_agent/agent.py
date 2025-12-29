"""Reflective Agent"""

import logging
from typing import Dict, Any
from src.state import AnalysisState
from src.api.client import APIClient
from src.agents.core.base_agent import BaseAgent
from .prompt import REFLECTIVE_AGENT_INSTRUCTIONS

logger = logging.getLogger(__name__)


async def reflective_agent(state: AnalysisState, api_client: APIClient) -> Dict[str, Any]:
    """Performs meta-analysis and critical evaluation."""
    logger.info("Running reflective agent node...")
    
    base_agent = BaseAgent(api_client, "reflective")
    
    try:
        tweet_text = base_agent.extract_tweet_text(state)
        
        prompt = f"""{REFLECTIVE_AGENT_INSTRUCTIONS}

Tweet Content: {tweet_text[:1200]}
Author: {state.get('tweet_data', {}).get('author_username', 'N/A')}
Tweet ID: {state.get('tweet_id', 'N/A')}
"""
        
        response = await base_agent.call_llm(prompt)
        parsed = base_agent.parse_response(response)
        
        reflection_score = parsed.get("agent_score", 5.0)
        logger.success(f"Reflective analysis complete | Score: {reflection_score:.1f}/10")
        
        return {
            "reflection_score": reflection_score,
            "reflection_reasoning": parsed.get("detailed_reasoning", ""),
            "critical_evaluation": parsed.get("critical_evaluation", ""),
            "bias_identification": parsed.get("bias_identification", ""),
        }
        
    except Exception as e:
        logger.error(f"Reflective analysis failed: {e}")
        return {
            "reflection_score": 5.0,
            "reflection_reasoning": f"Error: {str(e)}",
            "error": str(e)
        }
