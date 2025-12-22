"""
Unified API Client for all external service interactions
"""

import os
import asyncio
import logging
from typing import Optional, Dict, Any, List
from openai import AsyncOpenAI
from src.config import settings


logger = logging.getLogger(__name__)


class APIClient:
    """
    Unified API client for all external service interactions.
    
    Handles:
    - OpenAI API calls
    - Twitter API calls
    - Reddit API calls
    - Cryptocurrency exchange API calls (Binance, Coinbase)
    
    Designed to be easily replaceable with MCP service calls in the future.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize API client with configuration.
        
        Args:
            config: Optional configuration dictionary. If not provided,
                   uses settings from environment variables.
        """
        self.config = config or {}
        
        # Initialize OpenAI client
        openai_key = self.config.get('openai_api_key') or settings.openai_api_key
        if openai_key:
            self.openai_client = AsyncOpenAI(api_key=openai_key)
        else:
            self.openai_client = None
            logger.warning("OpenAI API key not provided")
        
        # Store other API credentials
        self.twitter_config = {
            'api_key': self.config.get('twitter_api_key') or settings.twitter_api_key,
            'api_secret': self.config.get('twitter_api_secret') or settings.twitter_api_secret,
            'access_token': self.config.get('twitter_access_token') or settings.twitter_access_token,
            'access_token_secret': self.config.get('twitter_access_token_secret') or settings.twitter_access_token_secret,
            'bearer_token': self.config.get('twitter_bearer_token') or settings.twitter_bearer_token,
        }
        
        self.reddit_config = {
            'client_id': self.config.get('reddit_client_id') or settings.reddit_client_id,
            'client_secret': self.config.get('reddit_client_secret') or settings.reddit_client_secret,
            'user_agent': self.config.get('reddit_user_agent') or settings.reddit_user_agent,
        }
        
        self.binance_config = {
            'api_key': self.config.get('binance_api_key') or settings.binance_api_key,
            'api_secret': self.config.get('binance_api_secret') or settings.binance_api_secret,
        }
        
        self.coinbase_config = {
            'api_key': self.config.get('coinbase_api_key') or settings.coinbase_api_key,
            'api_secret': self.config.get('coinbase_api_secret') or settings.coinbase_api_secret,
            'passphrase': self.config.get('coinbase_api_passphrase') or settings.coinbase_api_passphrase,
        }
    
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
            prompt: The prompt to send to the model
            model: Model name (defaults to settings.openai_model)
            max_tokens: Maximum tokens (defaults to settings.openai_max_tokens)
            temperature: Temperature (defaults to settings.openai_temperature)
            retries: Number of retry attempts
            
        Returns:
            Response text from OpenAI
            
        Raises:
            Exception: If API call fails after retries
        """
        if not self.openai_client:
            raise ValueError("OpenAI client not initialized. Check API key.")
        
        model = model or settings.openai_model
        max_tokens = max_tokens or settings.openai_max_tokens
        temperature = temperature or settings.openai_temperature
        
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
                    logger.error(f"OpenAI API call failed after {retries} attempts: {e}")
                    raise
                logger.warning(f"OpenAI API call failed (attempt {attempt + 1}/{retries}): {e}")
                await asyncio.sleep(2 ** attempt)  # Exponential backoff
    
    async def fetch_tweet_data(self, tweet_id: str) -> Optional[Dict[str, Any]]:
        """
        Fetch tweet data from Twitter API.
        
        Args:
            tweet_id: Twitter tweet ID
            
        Returns:
            Tweet data dictionary or None if not available
        """
        # TODO: Implement Twitter API call
        # For now, return None as this will be implemented later
        logger.warning("Twitter API fetch not yet implemented")
        return None
    
    async def get_crypto_price(self, symbol: str, exchange: str = "binance") -> Optional[float]:
        """
        Get cryptocurrency price from exchange API.
        
        Args:
            symbol: Cryptocurrency symbol (e.g., "BTC", "ETH")
            exchange: Exchange name ("binance" or "coinbase")
            
        Returns:
            Current price or None if not available
        """
        # TODO: Implement crypto price fetching
        # For now, return None as this will be implemented later
        logger.warning(f"Crypto price fetch from {exchange} not yet implemented")
        return None
    
    async def search_reddit(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Search Reddit for posts matching query.
        
        Args:
            query: Search query
            limit: Maximum number of results
            
        Returns:
            List of Reddit post dictionaries
        """
        # TODO: Implement Reddit API search
        # For now, return empty list as this will be implemented later
        logger.warning("Reddit API search not yet implemented")
        return []

