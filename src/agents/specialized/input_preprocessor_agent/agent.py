"""Input Preprocessor Agent"""

import logging
from typing import Dict, Any
from src.models.state import AnalysisState
from src.api.client import APIClient
from src.agents.core.base_agent import BaseAgent
from .prompt import INPUT_PREPROCESSOR_INSTRUCTIONS

logger = logging.getLogger(__name__)


async def input_preprocessor_agent(state: AnalysisState, api_client: APIClient) -> Dict[str, Any]:
    """Performs data cleansing and normalization."""
    logger.info("Running input preprocessor node...")
    
    base_agent = BaseAgent(api_client, "input_preprocessor")
    
    try:
        tweet_text = base_agent.extract_tweet_text(state)
        
        prompt = f"""{INPUT_PREPROCESSOR_INSTRUCTIONS}

Tweet Content: {tweet_text[:1200]}
Author: {state.get('tweet_data', {}).get('author_username', 'N/A')}
Tweet ID: {state.get('tweet_id', 'N/A')}
"""
        
        response = await base_agent.call_llm(prompt)
        parsed = base_agent.parse_response(response)
        
        logger.success(f"Input preprocessing complete | Quality: {parsed.get('agent_score', 5.0):.1f}/10")
        
        return {
            "normalized_text": parsed.get("normalized_text", tweet_text),
            "preprocessing_applied": parsed.get("preprocessing_applied", []),
            "data_quality_assessment": parsed.get("data_quality_assessment", ""),
        }
        
    except Exception as e:
        logger.error(f"Input preprocessing failed: {e}")
        return {
            "normalized_text": state.get('tweet_text', ''),
            "error": str(e)
        }

