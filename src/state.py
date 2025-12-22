"""
Analysis State Model for LangGraph
"""

from typing import TypedDict, Optional, Dict, Any, List
from typing_extensions import NotRequired


class TweetInput(TypedDict):
    """
    Input schema for LangGraph - only these 3 fields should be provided as input.
    """
    tweet_id: str
    tweet_text: str
    tweet_metadata: Dict[str, Any]


class AnalysisState(TypedDict, total=False):
    """
    LangGraph state definition for tweet analysis workflow.
    
    Uses TypedDict with total=False to allow optional fields.
    This is compatible with LangGraph's state management.
    """
    
    # Input fields (only these 3 should be provided initially)
    tweet_id: NotRequired[str]
    tweet_text: NotRequired[str]
    tweet_metadata: NotRequired[Dict[str, Any]]
    
    # Legacy field name (for backward compatibility, maps to tweet_metadata)
    tweet_data: NotRequired[Dict[str, Any]]
    
    # Signal Integrity Results
    sarcasm_score: NotRequired[float]
    sarcasm_detected: NotRequired[bool]
    sarcasm_reasoning: NotRequired[str]
    
    echo_detected: NotRequired[bool]
    echo_velocity: NotRequired[float]
    reddit_threads: NotRequired[int]
    
    latency_valid: NotRequired[bool]
    content_repriced: NotRequired[bool]
    time_delta_seconds: NotRequired[float]
    
    quality_pass: NotRequired[bool]
    quality_score: NotRequired[float]
    quality_reasoning: NotRequired[str]
    
    banned_phrases: NotRequired[List[str]]
    tone_penalty: NotRequired[float]
    
    # Core Analysis Results
    summary: NotRequired[str]
    title: NotRequired[str]
    abstract: NotRequired[str]
    
    context_score: NotRequired[float]
    context_reasoning: NotRequired[str]
    
    fact_check_results: NotRequired[Dict[str, Any]]
    fact_check_score: NotRequired[float]
    
    depth_score: NotRequired[float]
    depth_reasoning: NotRequired[str]
    
    relevance_score: NotRequired[float]
    relevance_reasoning: NotRequired[str]
    
    structure_score: NotRequired[float]
    structure_reasoning: NotRequired[str]
    
    reflection_score: NotRequired[float]
    reflection_reasoning: NotRequired[str]
    
    metadata_score: NotRequired[float]
    metadata_reasoning: NotRequired[str]
    
    consensus_score: NotRequired[float]
    consensus_reasoning: NotRequired[str]
    
    # Final Output
    overall_score: NotRequired[float]
    recommendation: NotRequired[str]
    formatted_output: NotRequired[Dict[str, Any]]
    
    # Error handling
    error: NotRequired[str]
    error_message: NotRequired[str]

