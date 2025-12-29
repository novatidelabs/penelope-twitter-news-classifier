"""Metadata Ranker Agent"""

import logging
from typing import Dict, Any
from src.state import AnalysisState
from src.api.client import APIClient
from src.agents.core.base_agent import BaseAgent
from .prompt import METADATA_RANKER_INSTRUCTIONS

logger = logging.getLogger(__name__)


async def metadata_ranker_agent(state: AnalysisState, api_client: APIClient) -> Dict[str, Any]:
    """Assesses user credibility and authority."""
    logger.info("Running metadata ranker node...")
    
    base_agent = BaseAgent(api_client, "metadata_ranker")
    
    try:
        tweet_text = base_agent.extract_tweet_text(state)
        
        prompt = f"""{METADATA_RANKER_INSTRUCTIONS}

Tweet Content: {tweet_text[:1200]}
Author: {state.get('tweet_data', {}).get('author_username', 'N/A')}
Tweet ID: {state.get('tweet_id', 'N/A')}
"""
        
        response = await base_agent.call_llm(prompt)
        parsed = base_agent.parse_response(response)
        
        metadata_score = parsed.get("agent_score", 5.0)
        logger.success(f"Metadata ranking complete | Score: {metadata_score:.1f}/10")
        
        return {
            "metadata_score": metadata_score,
            "metadata_reasoning": parsed.get("detailed_reasoning", ""),
            "verification_status": parsed.get("verification_status", ""),
            "expertise_indicators": parsed.get("expertise_indicators", ""),
        }
        
    except Exception as e:
        logger.error(f"Metadata ranking failed: {e}")
        return {
            "metadata_score": 5.0,
            "metadata_reasoning": f"Error: {str(e)}",
            "error": str(e)
        }
