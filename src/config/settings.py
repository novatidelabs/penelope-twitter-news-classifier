"""
Configuration Settings using Pydantic Settings
"""

from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional


class Settings(BaseSettings):
    """
    Application configuration settings loaded from environment variables.
    
    Uses Pydantic Settings for type-safe configuration management.
    """
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )
    
    # Application Settings
    app_name: str = "TwitterNewsClassifier"
    app_version: str = "2.0"
    
    # OpenAI Configuration
    openai_api_key: Optional[str] = None
    openai_model: str = "gpt-4"
    openai_max_tokens: int = 2000
    openai_temperature: float = 0.3
    
    # Twitter API Configuration (Optional)
    twitter_api_key: Optional[str] = None
    twitter_api_secret: Optional[str] = None
    twitter_access_token: Optional[str] = None
    twitter_access_token_secret: Optional[str] = None
    twitter_bearer_token: Optional[str] = None
    
    # Reddit API Configuration (Optional)
    reddit_client_id: Optional[str] = None
    reddit_client_secret: Optional[str] = None
    reddit_user_agent: str = "TwitterNewsClassifier/2.0"
    
    # Cryptocurrency Exchange APIs (Optional)
    binance_api_key: Optional[str] = None
    binance_api_secret: Optional[str] = None
    coinbase_api_key: Optional[str] = None
    coinbase_api_secret: Optional[str] = None
    coinbase_api_passphrase: Optional[str] = None
    
    # Analysis Configuration
    default_analysis_timeout: int = 60  # seconds
    max_tweets_per_batch: int = 10
    score_scale_min: int = 0
    score_scale_max: int = 10
    
    # Workflow Configuration
    default_max_tweets: int = 30
    default_hours_back: int = 24
    default_batch_size: int = 5
    default_max_retries: int = 3
    default_retry_delay: int = 30
    
    # Score Consolidation Configuration
    sarcasm_protection_max_boost: float = 2.0
    sarcasm_protection_threshold: float = 0.5
    echo_velocity_max_boost: float = 1.5
    echo_velocity_threshold: float = 0.5
    echo_velocity_scaling: float = 2.0
    slop_penalty_max: float = 2.5
    slop_penalty_threshold: float = 0.7
    slop_penalty_scaling: float = 3.0
    tone_penalty_max: float = 2.0
    tone_penalty_threshold: float = 0.3
    tone_penalty_scaling: float = 2.5
    
    # File Paths
    default_results_dir: str = "results"
    default_data_dir: str = "data"
    
    # Logging Configuration
    log_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    log_level: str = "INFO"
    
    # API Rate Limits (requests per minute)
    openai_rate_limit: int = 60
    reddit_rate_limit: int = 60
    binance_rate_limit: int = 1200
    coinbase_rate_limit: int = 10
    
    # Analysis Thresholds
    high_confidence_threshold: float = 8.0
    medium_confidence_threshold: float = 5.0
    low_confidence_threshold: float = 2.0
    
    # Signal Integrity Configuration
    banned_phrases_check_enabled: bool = True
    echo_mapping_check_enabled: bool = True
    latency_guard_enabled: bool = True
    sarcasm_detection_enabled: bool = True
    slop_filter_enabled: bool = True
    
    @property
    def user_agent(self) -> str:
        """Generate user agent string from app name and version"""
        return f"{self.app_name}/{self.app_version}"


# Global settings instance
settings = Settings()

