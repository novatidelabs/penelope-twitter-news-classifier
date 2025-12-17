"""
Latency Validator Prompt
========================
Prompt template for latency validation agent.
"""


def get_latency_validator_prompt(tweet_text: str, created_at: str) -> str:
    """
    Generate prompt for latency validation.
    
    Args:
        tweet_text: Tweet text to analyze
        created_at: Tweet creation timestamp
        
    Returns:
        Formatted prompt string
    """
    return f"""Analyze the following tweet for latency and timing issues.

Tweet: {tweet_text}
Created At: {created_at}

Determine if:
1. Content references events that occurred before the tweet
2. Price movements preceded the tweet
3. News is stale or repriced

Respond with JSON format:
{{
    "latency_valid": <boolean>,
    "content_repriced": <boolean>,
    "time_delta_seconds": <int or null>,
    "price_change_percentage": <float or null>,
    "asset_symbol": "<symbol or null>"
}}
"""

