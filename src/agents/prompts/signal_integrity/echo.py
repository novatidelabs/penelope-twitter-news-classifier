"""
Echo Mapper Prompt
==================
Prompt template for echo mapping agent.
"""


def get_echo_mapper_prompt(tweet_text: str) -> str:
    """
    Generate prompt for echo mapping.
    
    Args:
        tweet_text: Tweet text to analyze
        
    Returns:
        Formatted prompt string
    """
    return f"""Analyze the following tweet for cross-platform virality and echo patterns.

Tweet: {tweet_text}

Determine:
1. Cross-platform discussion indicators
2. Echo velocity (how fast content spreads)
3. Virality signals

Respond with JSON format:
{{
    "echo_detected": <boolean>,
    "echo_velocity": <float 0.0-1.0>,
    "reddit_threads": <int>,
    "farcaster_refs": <int>,
    "discord_refs": <int>
}}
"""

