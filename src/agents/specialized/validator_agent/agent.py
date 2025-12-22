"""Validator Agent"""

import logging
import json
from typing import Dict, Any
from src.state import AnalysisState
from src.api.client import APIClient
from src.agents.core.base_agent import BaseAgent
from .prompt import VALIDATOR_INSTRUCTIONS

logger = logging.getLogger(__name__)


async def validator_agent(state: AnalysisState, api_client: APIClient) -> Dict[str, Any]:
    """Performs final validation and quality assurance."""
    logger.info("Running validator node...")
    
    base_agent = BaseAgent(api_client, "validator")
    
    try:
        tweet_text = base_agent.extract_tweet_text(state)
        
        all_agent_responses = json.dumps({
            "summary": state.get("summary", ""),
            "context_score": state.get("context_score", 0),
            "fact_check_score": state.get("fact_check_score", 0),
            "overall_score": state.get("overall_score", 0),
        }, indent=2)
        
        prompt = f"""{VALIDATOR_INSTRUCTIONS}

Tweet Content: {tweet_text[:1200]}
Author: {state.get('tweet_data', {}).get('author_username', 'N/A')}
Tweet ID: {state.get('tweet_id', 'N/A')}

All Agent Responses:
{all_agent_responses}
"""
        
        response = await base_agent.call_llm(prompt)
        parsed = base_agent.parse_response(response)
        
        validation_passed = parsed.get("validation_passed", True)
        logger.success(f"Validation complete | Passed: {validation_passed}")
        
        return {
            "validation_passed": validation_passed,
            "analysis_quality": parsed.get("analysis_quality", ""),
            "identified_issues": parsed.get("identified_issues", []),
            "recommendations": parsed.get("recommendations", []),
        }
        
    except Exception as e:
        logger.error(f"Validation failed: {e}")
        return {
            "validation_passed": False,
            "error": str(e)
        }
