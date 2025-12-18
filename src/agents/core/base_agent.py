"""
Base Agent Class

Base class for all LangGraph agents.
Provides common functionality and interface.
"""
from abc import ABC, abstractmethod
from typing import Dict, Any
from ...models.state import AnalysisState
from ...api.client import APIClient


class BaseAgent(ABC):
    """
    Base class for all LangGraph agents.
    
    All agents should inherit from this class and implement
    the analyze method that takes state and returns state updates.
    """
    
    def __init__(self, api_client: APIClient):
        """
        Initialize base agent.
        
        Args:
            api_client: Unified API client instance
        """
        self.api_client = api_client
        self.agent_name = self.__class__.__name__
    
    @abstractmethod
    async def analyze(
        self,
        state: AnalysisState,
        api_client: APIClient
    ) -> Dict[str, Any]:
        """
        Analyze the current state and return state updates.
        
        This is the main method that each agent must implement.
        It should extract relevant data from state, perform analysis,
        and return a dictionary with state updates.
        
        Args:
            state: Current analysis state
            api_client: API client for external calls
            
        Returns:
            Dictionary with state updates (keys match AnalysisState fields)
        """
        pass
    
    def extract_tweet_text(self, state: AnalysisState) -> str:
        """Extract tweet text from state"""
        return state.get('tweet_text', '') or state.get('tweet_data', {}).get('text', '')
    
    def get_agent_name(self) -> str:
        """Get agent name"""
        return self.agent_name

