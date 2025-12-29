"""Relevance Analyzer Agent"""

import logging
from typing import Dict, Any
from src.state import AnalysisState
from src.api.client import APIClient
from src.agents.core.base_agent import BaseAgent
from .prompt import RELEVANCE_ANALYZER_INSTRUCTIONS

logger = logging.getLogger(__name__)


async def relevance_analyzer_agent(state: AnalysisState, api_client: APIClient) -> Dict[str, Any]:
    """Evaluates real-world importance and impact."""
    logger.info("Running relevance analyzer node...")
    
    base_agent = BaseAgent(api_client, "relevance_analyzer")
    
    try:
        tweet_text = base_agent.extract_tweet_text(state)
        
        prompt = f"""{RELEVANCE_ANALYZER_INSTRUCTIONS}

Tweet Content: {tweet_text[:1200]}
Author: {state.get('tweet_data', {}).get('author_username', 'N/A')}
Tweet ID: {state.get('tweet_id', 'N/A')}
"""
        
        response = await base_agent.call_llm(prompt)
        parsed = base_agent.parse_response(response)
        
        relevance_score = parsed.get("agent_score", 5.0)
        logger.success(f"Relevance analysis complete | Score: {relevance_score:.1f}/10")
        
        return {
            "relevance_score": relevance_score,
            "relevance_reasoning": parsed.get("detailed_reasoning", ""),
            "current_relevance": parsed.get("current_relevance", ""),
            "impact_assessment": parsed.get("impact_assessment", ""),
        }
        
    except Exception as e:
        logger.error(f"Relevance analysis failed: {e}")
        return {
            "relevance_score": 5.0,
            "relevance_reasoning": f"Error: {str(e)}",
            "error": str(e)
        }
