"""Context Evaluator Agent"""

import logging
from typing import Dict, Any
from src.models.state import AnalysisState
from src.api.client import APIClient
from src.agents.core.base_agent import BaseAgent
from .prompt import CONTEXT_EVALUATOR_INSTRUCTIONS

logger = logging.getLogger(__name__)


async def context_evaluator_agent(state: AnalysisState, api_client: APIClient) -> Dict[str, Any]:
    """Evaluates content context and quality."""
    logger.info("Running context evaluation node...")
    
    base_agent = BaseAgent(api_client, "context_evaluator")
    
    try:
        tweet_text = base_agent.extract_tweet_text(state)
        
        prompt = f"""{CONTEXT_EVALUATOR_INSTRUCTIONS}

Tweet Content: {tweet_text[:1200]}
Author: {state.get('tweet_data', {}).get('author_username', 'N/A')}
Tweet ID: {state.get('tweet_id', 'N/A')}
"""
        
        response = await base_agent.call_llm(prompt)
        parsed = base_agent.parse_response(response)
        
        logger.success(f"Context evaluation complete | Quality: {parsed.get('agent_score', 5.0):.1f}/10")
        
        return {
            "context_score": parsed.get("agent_score", 5.0),
            "context_reasoning": parsed.get("detailed_reasoning", ""),
            "context_richness": parsed.get("context_richness", ""),
            "information_completeness": parsed.get("information_completeness", ""),
            "source_credibility": parsed.get("source_credibility", ""),
            "temporal_relevance": parsed.get("temporal_relevance", ""),
        }
        
    except Exception as e:
        logger.error(f"Context evaluation failed: {e}")
        return {
            "context_score": 5.0,
            "context_reasoning": f"Error: {str(e)}",
            "error": str(e)
        }

