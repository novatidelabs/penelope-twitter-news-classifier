"""
Quality Filter Prompt
=====================
Prompt template for quality filtering agent.
"""


def get_quality_filter_prompt(tweet_text: str, author_username: str) -> str:
    """
    Generate prompt for quality filtering.
    
    Args:
        tweet_text: Tweet text to analyze
        author_username: Author username
        
    Returns:
        Formatted prompt string
    """
    return f"""Analyze the following tweet for content quality and authenticity.

Tweet: {tweet_text}
Author: @{author_username}

Determine:
1. Content quality (high-effort vs low-effort)
2. Authenticity indicators
3. Bot-like patterns
4. Generic or templated content

Respond with JSON format:
{{
    "quality_pass": <boolean>,
    "quality_score": <float 0.0-1.0>,
    "quality_reasoning": "<explanation>"
}}
"""

