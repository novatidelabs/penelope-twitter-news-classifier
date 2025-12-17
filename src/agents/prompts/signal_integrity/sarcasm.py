"""
Sarcasm Detector Prompt
=======================
Prompt template for sarcasm detection agent.
"""


def get_sarcasm_detector_prompt(tweet_text: str, author_username: str) -> str:
    """
    Generate prompt for sarcasm detection.
    
    Args:
        tweet_text: Tweet text to analyze
        author_username: Author username
        
    Returns:
        Formatted prompt string
    """
    return f"""Analyze the following tweet for sarcasm, irony, or tone inversion.

Tweet: {tweet_text}
Author: @{author_username}

Determine if this tweet contains:
1. Sarcasm or irony
2. Tone inversion (saying the opposite of what is meant)
3. Satirical content

Respond with JSON format:
{{
    "sarcasm_score": <float 0.0-1.0>,
    "sarcasm_detected": <boolean>,
    "sarcasm_reasoning": "<explanation>"
}}
"""

