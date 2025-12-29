"""Score Consolidator Agent"""

import logging
import json
from typing import Dict, Any
from src.state import AnalysisState
from src.api.client import APIClient
from src.agents.core.base_agent import BaseAgent
from .prompt import SCORE_CONSOLIDATOR_INSTRUCTIONS

logger = logging.getLogger(__name__)


async def score_consolidator_agent(state: AnalysisState, api_client: APIClient) -> Dict[str, Any]:
    """Aggregates all scores and provides final classification."""
    logger.info("Running score consolidator node...")
    
    base_agent = BaseAgent(api_client, "score_consolidator")
    
    try:
        tweet_text = base_agent.extract_tweet_text(state)
        
        all_agent_responses = json.dumps({
            "summary": state.get("summary", ""),
            "context_score": state.get("context_score", 0),
            "fact_check_score": state.get("fact_check_score", 0),
            "depth_score": state.get("depth_score", 0),
            "relevance_score": state.get("relevance_score", 0),
            "structure_score": state.get("structure_score", 0),
            "reflection_score": state.get("reflection_score", 0),
            "metadata_score": state.get("metadata_score", 0),
            "consensus_score": state.get("consensus_score", 0),
        }, indent=2)
        
        prompt = f"""{SCORE_CONSOLIDATOR_INSTRUCTIONS}

Tweet Content: {tweet_text[:1200]}
Author: {state.get('tweet_data', {}).get('author_username', 'N/A')}
Tweet ID: {state.get('tweet_id', 'N/A')}

All Agent Responses:
{all_agent_responses}
"""
        
        response = await base_agent.call_llm(prompt)
        parsed = base_agent.parse_response(response)
        
        overall_score = parsed.get("agent_score", 5.0)
        logger.success(f"Score consolidation complete | Overall Score: {overall_score:.1f}/10")
        
        return {
            "overall_score": overall_score,
            "score_aggregation": parsed.get("score_aggregation", ""),
            "classification_category": parsed.get("classification_category", ""),
            "weighted_average": parsed.get("weighted_average", ""),
        }
        
    except Exception as e:
        logger.error(f"Score consolidation failed: {e}")
        return {
            "overall_score": 5.0,
            "error": str(e)
        }
