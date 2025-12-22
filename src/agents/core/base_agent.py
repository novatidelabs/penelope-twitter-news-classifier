"""
Base agent functionality
"""

import logging
from typing import Dict, Any, Optional
from src.models.state import AnalysisState
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
        return state.get('tweet_text', '') or state.get('tweet_data', {}).get('text', '')