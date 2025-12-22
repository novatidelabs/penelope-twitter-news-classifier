"""Depth Analyzer Agent"""

import logging
from typing import Dict, Any
from src.models.state import AnalysisState
from src.api.client import APIClient
from src.agents.core.base_agent import BaseAgent
from .prompt import DEPTH_ANALYZER_INSTRUCTIONS

logger = logging.getLogger(__name__)


async def depth_analyzer_agent(state: AnalysisState, api_client: APIClient) -> Dict[str, Any]:
    """Evaluates content complexity and analytical depth."""
    logger.info("Running depth analyzer node...")
    
    base_agent = BaseAgent(api_client, "depth_analyzer")
    
    try:
        tweet_text = base_agent.extract_tweet_text(state)
        
        prompt = f"""{DEPTH_ANALYZER_INSTRUCTIONS}

Tweet Content: {tweet_text[:1200]}
Author: {state.get('tweet_data', {}).get('author_username', 'N/A')}
Tweet ID: {state.get('tweet_id', 'N/A')}
"""
        
        response = await base_agent.call_llm(prompt)
        parsed = base_agent.parse_response(response)
        
        depth_score = parsed.get("agent_score", 5.0)
        logger.success(f"Depth analysis complete | Score: {depth_score:.1f}/10")
        
        return {
            "depth_score": depth_score,
            "depth_reasoning": parsed.get("detailed_reasoning", ""),
            "complexity_assessment": parsed.get("complexity_assessment", ""),
            "analytical_depth": parsed.get("analytical_depth", ""),
        }
        
    except Exception as e:
        logger.error(f"Depth analysis failed: {e}")
        return {
            "depth_score": 5.0,
            "depth_reasoning": f"Error: {str(e)}",
            "error": str(e)
        }
