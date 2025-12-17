"""
Phrase Detector Prompt
======================
Prompt template for banned phrase detection agent.
"""


def get_phrase_detector_prompt(tweet_text: str, author_username: str) -> str:
    """
    Generate prompt for banned phrase detection.
    
    Args:
        tweet_text: Tweet text to analyze
        author_username: Author username
        
    Returns:
        Formatted prompt string
    """
    return f"""Analyze the following tweet for prohibited words and phrases.

Tweet: {tweet_text}
Author: @{author_username}

Detect:
1. Banned terms or phrases
2. Policy violations
3. Tone penalties

Respond with JSON format:
{{
    "banned_phrases_detected": ["<phrase1>", "<phrase2>"],
    "tone_penalty": <float 0.0-1.0>,
    "risk_assessment": "<low|medium|high>"
}}
"""

