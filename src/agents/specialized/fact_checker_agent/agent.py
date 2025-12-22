"""Fact Checker Agent"""

import logging
from typing import Dict, Any
from src.models.state import AnalysisState
from src.api.client import APIClient
from src.agents.core.base_agent import BaseAgent
from .prompt import FACT_CHECKER_INSTRUCTIONS

logger = logging.getLogger(__name__)


async def fact_checker_agent(state: AnalysisState, api_client: APIClient) -> Dict[str, Any]:
    """Performs accuracy verification and factual assessment."""
    logger.info("Running fact checker node...")
    
    base_agent = BaseAgent(api_client, "fact_checker")
    
    try:
        tweet_text = base_agent.extract_tweet_text(state)
        
        prompt = f"""{FACT_CHECKER_INSTRUCTIONS}

Tweet Content: {tweet_text[:1200]}
Author: {state.get('tweet_data', {}).get('author_username', 'N/A')}
Tweet ID: {state.get('tweet_id', 'N/A')}
"""
        
        response = await base_agent.call_llm(prompt)
        parsed = base_agent.parse_response(response)
        
        fact_check_score = parsed.get("agent_score", 5.0)
        logger.success(f"Fact checking complete | Score: {fact_check_score:.1f}/10")
        
        return {
            "fact_check_score": fact_check_score,
            "fact_check_results": {
                "factual_claims": parsed.get("factual_claims", []),
                "verification_status": parsed.get("verification_status", ""),
                "accuracy_assessment": parsed.get("accuracy_assessment", ""),
                "source_credibility": parsed.get("credibility_indicators", []),
            }
        }
        
    except Exception as e:
        logger.error(f"Fact checking failed: {e}")
        return {
            "fact_check_score": 5.0,
            "fact_check_results": {},
            "error": str(e)
        }

