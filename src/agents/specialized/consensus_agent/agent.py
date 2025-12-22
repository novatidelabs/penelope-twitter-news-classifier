"""Consensus Agent"""

import logging
from typing import Dict, Any
from src.models.state import AnalysisState
from src.api.client import APIClient
from src.agents.core.base_agent import BaseAgent
from .prompt import CONSENSUS_AGENT_INSTRUCTIONS

logger = logging.getLogger(__name__)


async def consensus_agent(state: AnalysisState, api_client: APIClient) -> Dict[str, Any]:
    """Evaluates agreement and consensus levels."""
    logger.info("Running consensus agent node...")
    
    base_agent = BaseAgent(api_client, "consensus")
    
    try:
        tweet_text = base_agent.extract_tweet_text(state)
        
        prompt = f"""{CONSENSUS_AGENT_INSTRUCTIONS}

Tweet Content: {tweet_text[:1200]}
Author: {state.get('tweet_data', {}).get('author_username', 'N/A')}
Tweet ID: {state.get('tweet_id', 'N/A')}
"""
        
        response = await base_agent.call_llm(prompt)
        parsed = base_agent.parse_response(response)
        
        consensus_score = parsed.get("agent_score", 5.0)
        logger.success(f"Consensus analysis complete | Score: {consensus_score:.1f}/10")
        
        return {
            "consensus_score": consensus_score,
            "consensus_reasoning": parsed.get("detailed_reasoning", ""),
            "consensus_evaluation": parsed.get("consensus_evaluation", ""),
            "community_agreement": parsed.get("community_agreement", ""),
        }
        
    except Exception as e:
        logger.error(f"Consensus analysis failed: {e}")
        return {
            "consensus_score": 5.0,
            "consensus_reasoning": f"Error: {str(e)}",
            "error": str(e)
        }
