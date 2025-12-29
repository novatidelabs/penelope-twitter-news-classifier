"""Summary Agent"""

import logging
from typing import Dict, Any
from src.state import AnalysisState
from src.api.client import APIClient
from src.agents.core.base_agent import BaseAgent
from .prompt import SUMMARY_INSTRUCTIONS

logger = logging.getLogger(__name__)


async def summary_agent(state: AnalysisState, api_client: APIClient) -> Dict[str, Any]:
    """Generates titles and abstracts for social media content."""
    logger.info("Running summary agent node...")
    
    base_agent = BaseAgent(api_client, "summary")
    
    try:
        tweet_text = base_agent.extract_tweet_text(state)
        
        metadata = base_agent.get_tweet_metadata(state)
        prompt = f"""{SUMMARY_INSTRUCTIONS}

Tweet Content: {tweet_text[:1200]}
Author: {metadata.get('author_username', 'N/A')}
Tweet ID: {state.get('tweet_id', 'N/A')}
"""
        
        response = await base_agent.call_llm(prompt)
        parsed = base_agent.parse_response(response)
        
        logger.success(f"Summary generation complete | Title: {parsed.get('title', 'N/A')[:50]}...")
        
        return {
            "summary": parsed.get("abstract", ""),
            "title": parsed.get("title", ""),
            "abstract": parsed.get("abstract", ""),
            "key_themes": parsed.get("key_themes", []),
            "content_category": parsed.get("content_category", ""),
        }
        
    except Exception as e:
        logger.error(f"Summary generation failed: {e}")
        return {
            "summary": "",
            "title": "",
            "error": str(e)
        }

