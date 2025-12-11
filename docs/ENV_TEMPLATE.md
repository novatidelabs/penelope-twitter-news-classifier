# Environment Variables Template

Copy this content to your `.env` file and fill in your actual API keys:

```bash
# =============================================================================
# TWITTER NEWS CLASSIFIER - SENSITIVE ENVIRONMENT VARIABLES
# =============================================================================

# OpenAI API (Required)
OPENAI_API_KEY=your_openai_api_key_here

# Twitter API (Required for tweet extraction)
TWITTER_API_KEY=your_twitter_api_key_here
TWITTER_API_SECRET=your_twitter_api_secret_here
TWITTER_ACCESS_TOKEN=your_twitter_access_token_here
TWITTER_ACCESS_TOKEN_SECRET=your_twitter_access_token_secret_here
TWITTER_BEARER_TOKEN=your_twitter_bearer_token_here

# Reddit API (Optional - for enhanced analysis)
REDDIT_CLIENT_ID=your_reddit_client_id_here
REDDIT_CLIENT_SECRET=your_reddit_client_secret_here

# Binance API (Optional - for crypto price data)
BINANCE_API_KEY=your_binance_api_key_here
BINANCE_API_SECRET=your_binance_api_secret_here

# Coinbase API (Optional - for crypto price data)
COINBASE_API_KEY=your_coinbase_api_key_here
COINBASE_API_SECRET=your_coinbase_api_secret_here
COINBASE_API_PASSPHRASE=your_coinbase_passphrase_here
```

## Configuration Constants

All configuration constants are now defined in `infrastructure/config.py`:

- Application settings (name, version, user agent)
- Analysis parameters (timeouts, batch sizes, score ranges)
- Workflow configuration (max tweets, retry settings)
- OpenAI model settings
- Score consolidation thresholds
- Rate limits for different APIs
- Signal integrity parameters

This separation ensures that:
- ✅ Sensitive data stays in `.env` (not committed to git)
- ✅ Configuration constants are in code (version controlled)
- ✅ Easy to modify settings without touching environment
- ✅ Better security and maintainability
