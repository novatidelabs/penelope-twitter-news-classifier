"""
Unified API Client

Single interface for all external API interactions.
Handles OpenAI, Twitter, Reddit, Binance, Coinbase APIs.
"""
import asyncio
import logging
from typing import Dict, Any, Optional, List
from openai import AsyncOpenAI
from ..config import settings


class APIClient:
    """
    Unified API client for all external service interactions.
    
    Provides a single interface for:
    - OpenAI API calls
    - Twitter API calls
    - Reddit API calls
    - Crypto exchange API calls (Binance, Coinbase)
    """
    
    def __init__(self):
        """Initialize API client with configuration"""
        self.logger = logging.getLogger(__name__)
        self.settings = settings
        
        # Initialize OpenAI client
        if self.settings.openai_api_key:
            self.openai_client = AsyncOpenAI(api_key=self.settings.openai_api_key)
        else:
            self.openai_client = None
            self.logger.warning("OpenAI API key not configured")
        
        # Initialize other API clients as needed
        self._reddit_client = None
        self._twitter_client = None
    
    async def call_openai(
        self,
        prompt: str,
        model: Optional[str] = None,
        max_tokens: Optional[int] = None,
        temperature: Optional[float] = None,
        retries: int = 3
    ) -> str:
        """
        Call OpenAI API with retry logic.
        
        Args:
            prompt: The prompt to send to OpenAI
            model: Model to use (defaults to settings.openai_model)
            max_tokens: Max tokens (defaults to settings.openai_max_tokens)
            temperature: Temperature (defaults to settings.openai_temperature)
            retries: Number of retries on failure
            
        Returns:
            Response text from OpenAI
        """
        if not self.openai_client:
            raise ValueError("OpenAI API key not configured")
        
        model = model or self.settings.openai_model
        max_tokens = max_tokens or self.settings.openai_max_tokens
        temperature = temperature or self.settings.openai_temperature
        
        for attempt in range(retries):
            try:
                response = await self.openai_client.chat.completions.create(
                    model=model,
                    messages=[
                        {"role": "system", "content": "You are a specialized AI agent for social media content analysis. Always respond with valid JSON format as specified in the prompt."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=max_tokens,
                    temperature=temperature
                )
                return response.choices[0].message.content
            except Exception as e:
                if attempt == retries - 1:
                    raise
                self.logger.warning(f"OpenAI API call failed (attempt {attempt + 1}/{retries}): {e}")
                await asyncio.sleep(2 ** attempt)  # Exponential backoff
        
        raise Exception("OpenAI API call failed after all retries")
    
    async def fetch_tweet_data(self, tweet_id: str) -> Dict[str, Any]:
        """
        Fetch tweet data from Twitter API.
        
        Args:
            tweet_id: Twitter tweet ID
            
        Returns:
            Tweet data dictionary
        """
        # TODO: Implement Twitter API integration
        # This will use the Twitter API adapter
        raise NotImplementedError("Twitter API integration not yet implemented")
    
    async def get_crypto_price(
        self,
        symbol: str,
        exchange: str = "binance"
    ) -> Dict[str, Any]:
        """
        Get cryptocurrency price data.
        
        Args:
            symbol: Crypto symbol (e.g., 'BTC', 'ETH')
            exchange: Exchange name ('binance' or 'coinbase')
            
        Returns:
            Price data dictionary
        """
        # TODO: Implement crypto exchange API integration
        raise NotImplementedError("Crypto exchange API integration not yet implemented")
    
    async def search_reddit(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Search Reddit for posts matching query.
        
        Args:
            query: Search query
            limit: Maximum number of results
            
        Returns:
            List of Reddit post dictionaries
        """
        # TODO: Implement Reddit API integration
        raise NotImplementedError("Reddit API integration not yet implemented")

