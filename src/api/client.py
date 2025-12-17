"""
Unified API Client
==================
Single interface for all external API interactions.

Supports:
- OpenAI API calls with retry logic
- Twitter API integration
- Reddit API integration
- Crypto exchange APIs (Binance, Coinbase)
"""

import asyncio
import logging
from typing import Optional, Dict, Any, List
from datetime import datetime, timedelta
from openai import AsyncOpenAI
from tweepy import Client as TwitterClient
import praw  # Reddit API
import requests  # For crypto APIs

from ..config import Settings, get_settings


logger = logging.getLogger(__name__)


class APIClient:
    """
    Unified API client for all external service interactions.
    
    Provides a single interface for:
    - OpenAI LLM calls
    - Twitter data fetching
    - Reddit API access
    - Crypto price data
    """
    
    def __init__(self, settings: Optional[Settings] = None):
        """
        Initialize API client with settings.
        
        Args:
            settings: Settings instance (uses get_settings() if None)
        """
        self.settings = settings or get_settings()
        self.logger = logger
        
        # Initialize OpenAI client
        self.openai_client: Optional[AsyncOpenAI] = None
        if self.settings.openai_api_key:
            self.openai_client = AsyncOpenAI(api_key=self.settings.openai_api_key)
        
        # Initialize Twitter client
        self.twitter_client: Optional[TwitterClient] = None
        if all([
            self.settings.twitter_bearer_token,
            self.settings.twitter_api_key,
            self.settings.twitter_api_secret
        ]):
            self.twitter_client = TwitterClient(
                bearer_token=self.settings.twitter_bearer_token,
                consumer_key=self.settings.twitter_api_key,
                consumer_secret=self.settings.twitter_api_secret,
                access_token=self.settings.twitter_access_token,
                access_token_secret=self.settings.twitter_access_token_secret,
                wait_on_rate_limit=True
            )
        
        # Initialize Reddit client
        self.reddit_client: Optional[praw.Reddit] = None
        if self.settings.reddit_client_id and self.settings.reddit_client_secret:
            self.reddit_client = praw.Reddit(
                client_id=self.settings.reddit_client_id,
                client_secret=self.settings.reddit_client_secret,
                user_agent=self.settings.reddit_user_agent
            )
        
        # Rate limiting tracking
        self._rate_limits: Dict[str, List[datetime]] = {}
    
    async def call_openai(
        self,
        prompt: str,
        model: Optional[str] = None,
        max_tokens: Optional[int] = None,
        temperature: Optional[float] = None,
        max_retries: int = 3,
        retry_delay: int = 1
    ) -> str:
        """
        Call OpenAI API with retry logic.
        
        Args:
            prompt: Prompt text
            model: Model name (defaults to settings)
            max_tokens: Max tokens (defaults to settings)
            temperature: Temperature (defaults to settings)
            max_retries: Maximum retry attempts
            retry_delay: Delay between retries (seconds)
            
        Returns:
            Response text from OpenAI
            
        Raises:
            Exception: If all retries fail
        """
        if not self.openai_client:
            raise ValueError("OpenAI API key not configured")
        
        model = model or self.settings.openai_model
        max_tokens = max_tokens or self.settings.openai_max_tokens
        temperature = temperature or self.settings.openai_temperature
        
        for attempt in range(max_retries):
            try:
                self._check_rate_limit("openai")
                
                response = await self.openai_client.chat.completions.create(
                    model=model,
                    messages=[
                        {
                            "role": "system",
                            "content": "You are a specialized AI agent for social media content analysis. Always respond with valid JSON format as specified in the prompt."
                        },
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=max_tokens,
                    temperature=temperature
                )
                
                self._record_rate_limit("openai")
                return response.choices[0].message.content
                
            except Exception as e:
                self.logger.warning(f"OpenAI API call failed (attempt {attempt + 1}/{max_retries}): {e}")
                if attempt < max_retries - 1:
                    await asyncio.sleep(retry_delay * (attempt + 1))
                else:
                    raise
    
    async def fetch_tweet(self, tweet_id: str) -> Optional[Dict[str, Any]]:
        """
        Fetch tweet data from Twitter API.
        
        Args:
            tweet_id: Twitter tweet ID
            
        Returns:
            Tweet data dictionary or None if not available
        """
        if not self.twitter_client:
            self.logger.warning("Twitter API not configured")
            return None
        
        try:
            self._check_rate_limit("twitter")
            tweet = self.twitter_client.get_tweet(
                id=tweet_id,
                tweet_fields=["created_at", "public_metrics", "author_id"],
                expansions=["author_id"],
                user_fields=["username", "description", "verified", "public_metrics"]
            )
            self._record_rate_limit("twitter")
            
            if tweet.data:
                return {
                    "tweet_id": tweet.data.id,
                    "text": tweet.data.text,
                    "created_at": tweet.data.created_at,
                    "author_id": tweet.data.author_id,
                    "public_metrics": tweet.data.public_metrics
                }
        except Exception as e:
            self.logger.error(f"Error fetching tweet {tweet_id}: {e}")
        
        return None
    
    async def search_reddit(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Search Reddit for posts matching query.
        
        Args:
            query: Search query
            limit: Maximum results
            
        Returns:
            List of Reddit post dictionaries
        """
        if not self.reddit_client:
            self.logger.warning("Reddit API not configured")
            return []
        
        try:
            self._check_rate_limit("reddit")
            results = []
            for submission in self.reddit_client.subreddit("all").search(query, limit=limit):
                results.append({
                    "title": submission.title,
                    "url": submission.url,
                    "score": submission.score,
                    "subreddit": str(submission.subreddit),
                    "created_utc": submission.created_utc
                })
            self._record_rate_limit("reddit")
            return results
        except Exception as e:
            self.logger.error(f"Error searching Reddit: {e}")
            return []
    
    async def get_crypto_price(
        self,
        symbol: str,
        exchange: str = "binance"
    ) -> Optional[Dict[str, Any]]:
        """
        Get cryptocurrency price data.
        
        Args:
            symbol: Crypto symbol (e.g., "BTC", "ETH")
            exchange: Exchange name ("binance" or "coinbase")
            
        Returns:
            Price data dictionary or None
        """
        try:
            if exchange.lower() == "binance":
                return await self._get_binance_price(symbol)
            elif exchange.lower() == "coinbase":
                return await self._get_coinbase_price(symbol)
        except Exception as e:
            self.logger.error(f"Error fetching {symbol} price from {exchange}: {e}")
        
        return None
    
    async def _get_binance_price(self, symbol: str) -> Optional[Dict[str, Any]]:
        """Get price from Binance API"""
        try:
            self._check_rate_limit("binance")
            url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}USDT"
            response = requests.get(url, timeout=5)
            self._record_rate_limit("binance")
            
            if response.status_code == 200:
                data = response.json()
                return {
                    "symbol": symbol,
                    "price": float(data["price"]),
                    "exchange": "binance",
                    "timestamp": datetime.now().isoformat()
                }
        except Exception as e:
            self.logger.error(f"Binance API error: {e}")
        
        return None
    
    async def _get_coinbase_price(self, symbol: str) -> Optional[Dict[str, Any]]:
        """Get price from Coinbase API"""
        try:
            self._check_rate_limit("coinbase")
            url = f"https://api.coinbase.com/v2/exchange-rates?currency={symbol}"
            response = requests.get(url, timeout=5)
            self._record_rate_limit("coinbase")
            
            if response.status_code == 200:
                data = response.json()
                if "data" in data and "rates" in data["data"]:
                    usd_rate = data["data"]["rates"].get("USD")
                    if usd_rate:
                        return {
                            "symbol": symbol,
                            "price": float(usd_rate),
                            "exchange": "coinbase",
                            "timestamp": datetime.now().isoformat()
                        }
        except Exception as e:
            self.logger.error(f"Coinbase API error: {e}")
        
        return None
    
    def _check_rate_limit(self, service: str):
        """Check if rate limit allows request"""
        if service not in self._rate_limits:
            self._rate_limits[service] = []
        
        # Get rate limit from settings
        limits = {
            "openai": self.settings.openai_rate_limit,
            "twitter": 300,  # Twitter has complex rate limits
            "reddit": self.settings.reddit_rate_limit,
            "binance": self.settings.binance_rate_limit,
            "coinbase": self.settings.coinbase_rate_limit
        }
        
        limit = limits.get(service, 60)
        now = datetime.now()
        minute_ago = now - timedelta(minutes=1)
        
        # Remove old entries
        self._rate_limits[service] = [
            ts for ts in self._rate_limits[service]
            if ts > minute_ago
        ]
        
        # Check if limit exceeded
        if len(self._rate_limits[service]) >= limit:
            wait_time = 60 - (now - self._rate_limits[service][0]).seconds
            raise Exception(f"Rate limit exceeded for {service}. Wait {wait_time} seconds.")
    
    def _record_rate_limit(self, service: str):
        """Record API call for rate limiting"""
        if service not in self._rate_limits:
            self._rate_limits[service] = []
        self._rate_limits[service].append(datetime.now())

