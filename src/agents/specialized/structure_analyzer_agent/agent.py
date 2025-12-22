"""Structure Analyzer Agent"""

import logging
from typing import Dict, Any
from src.models.state import AnalysisState
from src.api.client import APIClient
from src.agents.core.base_agent import BaseAgent
from .prompt import STRUCTURE_ANALYZER_INSTRUCTIONS

logger = logging.getLogger(__name__)


async def structure_analyzer_agent(state: AnalysisState, api_client: APIClient) -> Dict[str, Any]:
    """Evaluates content organization and presentation quality."""
    logger.info("Running structure analyzer node...")
    
    base_agent = BaseAgent(api_client, "structure_analyzer")
    
    try:
        tweet_text = base_agent.extract_tweet_text(state)
        
        prompt = f"""{STRUCTURE_ANALYZER_INSTRUCTIONS}

Tweet Content: {tweet_text[:1200]}
Author: {state.get('tweet_data', {}).get('author_username', 'N/A')}
Tweet ID: {state.get('tweet_id', 'N/A')}
"""
        
        response = await base_agent.call_llm(prompt)
        parsed = base_agent.parse_response(response)
        
        structure_score = parsed.get("agent_score", 5.0)
        logger.success(f"Structure analysis complete | Score: {structure_score:.1f}/10")
        
        return {
            "structure_score": structure_score,
            "structure_reasoning": parsed.get("detailed_reasoning", ""),
            "organization_assessment": parsed.get("organization_assessment", ""),
            "logical_flow": parsed.get("logical_flow", ""),
        }
        
    except Exception as e:
        logger.error(f"Structure analysis failed: {e}")
        return {
            "structure_score": 5.0,
            "structure_reasoning": f"Error: {str(e)}",
            "error": str(e)
        }
