"""
Base agent functionality
"""

import logging
from typing import Dict, Any, Optional
from src.state import AnalysisState
from src.api.client import APIClient
from src.utils.parsers import parse_json_response


class BaseAgent:
    """Base agent class with common utilities."""
    
    def __init__(self, api_client: APIClient, agent_name: str):
        self.api_client = api_client
        self.agent_name = agent_name
        self.logger = logging.getLogger(f"{__name__}.{agent_name}")
    
    async def call_llm(
        self,
        prompt: str,
        model: Optional[str] = None,
        max_tokens: Optional[int] = None,
        temperature: Optional[float] = None
    ) -> str:
        """Call LLM through API client."""
        return await self.api_client.call_openai(
            prompt=prompt,
            model=model,
            max_tokens=max_tokens,
            temperature=temperature
        )
    
    def parse_response(self, response_text: str) -> Dict[str, Any]:
        """Parse LLM response to JSON."""
        return parse_json_response(response_text, self.agent_name)
    
    def extract_tweet_text(self, state: AnalysisState) -> str:
        """Extract tweet text from state."""
        # Try tweet_text first, then check metadata
        tweet_text = state.get('tweet_text', '')
        if tweet_text:
            return tweet_text
        
        # Check tweet_metadata or tweet_data (backward compatibility)
        metadata = state.get('tweet_metadata') or state.get('tweet_data', {})
        return metadata.get('text', '') if isinstance(metadata, dict) else ''
    
    def get_tweet_metadata(self, state: AnalysisState) -> Dict[str, Any]:
        """Get tweet metadata from state (supports both tweet_metadata and tweet_data)."""
        return state.get('tweet_metadata') or state.get('tweet_data', {})