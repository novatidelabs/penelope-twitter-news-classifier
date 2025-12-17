"""
🔧 CONFIGURATION MODULE
======================
Application configuration constants and settings.
Separates constants from sensitive environment variables.

Uses a dataclass-based Configuration class for better type safety and maintainability.
"""

from dataclasses import dataclass


@dataclass(kw_only=True)
class Configuration:
    """
    Configuration class for Twitter News Classifier application settings.
    
    All configuration constants are centralized here, providing type hints
    and better maintainability compared to module-level constants.
    """
    
    # Application Constants
    app_name: str = "TwitterNewsClassifier"
    version: str = "2.0"
    
    @property
    def user_agent(self) -> str:
        """Generate user agent string from app name and version"""
        return f"{self.app_name}/{self.version}"
    
    # Reddit Configuration
    @property
    def reddit_user_agent(self) -> str:
        """Reddit user agent (same as main user agent)"""
        return self.user_agent
    
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
    
    # OpenAI Configuration
    openai_model: str = "gpt-4"
    openai_max_tokens: int = 2000
    openai_temperature: float = 0.3
    
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


# Create global configuration instance
config = Configuration()

# Backward compatibility: Export constants as module-level attributes
# This allows existing code to continue working while migrating to the class-based approach
APP_NAME = config.app_name
APP_VERSION = config.version
USER_AGENT = config.user_agent
REDDIT_USER_AGENT = config.reddit_user_agent

DEFAULT_ANALYSIS_TIMEOUT = config.default_analysis_timeout
MAX_TWEETS_PER_BATCH = config.max_tweets_per_batch
SCORE_SCALE_MIN = config.score_scale_min
SCORE_SCALE_MAX = config.score_scale_max

DEFAULT_MAX_TWEETS = config.default_max_tweets
DEFAULT_HOURS_BACK = config.default_hours_back
DEFAULT_BATCH_SIZE = config.default_batch_size
DEFAULT_MAX_RETRIES = config.default_max_retries
DEFAULT_RETRY_DELAY = config.default_retry_delay

OPENAI_MODEL = config.openai_model
OPENAI_MAX_TOKENS = config.openai_max_tokens
OPENAI_TEMPERATURE = config.openai_temperature

SARCASM_PROTECTION_MAX_BOOST = config.sarcasm_protection_max_boost
SARCASM_PROTECTION_THRESHOLD = config.sarcasm_protection_threshold
ECHO_VELOCITY_MAX_BOOST = config.echo_velocity_max_boost
ECHO_VELOCITY_THRESHOLD = config.echo_velocity_threshold
ECHO_VELOCITY_SCALING = config.echo_velocity_scaling
SLOP_PENALTY_MAX = config.slop_penalty_max
SLOP_PENALTY_THRESHOLD = config.slop_penalty_threshold
SLOP_PENALTY_SCALING = config.slop_penalty_scaling
TONE_PENALTY_MAX = config.tone_penalty_max
TONE_PENALTY_THRESHOLD = config.tone_penalty_threshold
TONE_PENALTY_SCALING = config.tone_penalty_scaling

DEFAULT_RESULTS_DIR = config.default_results_dir
DEFAULT_DATA_DIR = config.default_data_dir

LOG_FORMAT = config.log_format
LOG_LEVEL = config.log_level

OPENAI_RATE_LIMIT = config.openai_rate_limit
REDDIT_RATE_LIMIT = config.reddit_rate_limit
BINANCE_RATE_LIMIT = config.binance_rate_limit
COINBASE_RATE_LIMIT = config.coinbase_rate_limit

HIGH_CONFIDENCE_THRESHOLD = config.high_confidence_threshold
MEDIUM_CONFIDENCE_THRESHOLD = config.medium_confidence_threshold
LOW_CONFIDENCE_THRESHOLD = config.low_confidence_threshold

BANNED_PHRASES_CHECK_ENABLED = config.banned_phrases_check_enabled
ECHO_MAPPING_CHECK_ENABLED = config.echo_mapping_check_enabled
LATENCY_GUARD_ENABLED = config.latency_guard_enabled
SARCASM_DETECTION_ENABLED = config.sarcasm_detection_enabled
SLOP_FILTER_ENABLED = config.slop_filter_enabled
