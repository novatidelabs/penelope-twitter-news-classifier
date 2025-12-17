"""
Analysis State Model
===================
TypedDict-based state model for LangGraph StateGraph.
"""

from typing import TypedDict, Optional, List, Dict, Any
from datetime import datetime


class AnalysisState(TypedDict, total=False):
    """
    LangGraph state model for tweet analysis workflow.
    
    Uses TypedDict with total=False to allow optional fields.
    This matches LangGraph's state management pattern.
    """
    
    # Input fields
    tweet_data: Dict[str, Any]  # TweetData as dict
    tweet_id: str
    
    # Signal Integrity Results
    sarcasm_score: float
    sarcasm_detected: bool
    sarcasm_reasoning: str
    
    echo_detected: bool
    echo_velocity: float
    reddit_threads: int
    farcaster_refs: int
    discord_refs: int
    
    latency_valid: bool
    content_repriced: bool
    time_delta_seconds: Optional[int]
    price_change_percentage: Optional[float]
    asset_symbol: Optional[str]
    
    quality_pass: bool
    quality_score: float
    quality_reasoning: str
    
    banned_phrases_detected: List[str]
    tone_penalty: float
    risk_assessment: str
    
    # Core Analysis Results
    summary: Optional[str]
    summary_title: Optional[str]
    
    context_score: float
    context_reasoning: str
    
    fact_check_score: float
    fact_check_results: Dict[str, Any]
    fact_check_reasoning: str
    
    depth_score: float
    depth_reasoning: str
    
    relevance_score: float
    relevance_reasoning: str
    
    structure_score: float
    structure_reasoning: str
    
    reflection_score: float
    reflection_reasoning: str
    
    metadata_score: float
    metadata_reasoning: str
    
    consensus_score: float
    consensus_reasoning: str
    
    # Final Output
    overall_score: float
    recommendation: str  # "Approve", "Review", "Reject"
    formatted_output: Dict[str, Any]
    
    # Metadata
    analysis_timestamp: datetime
    processing_time: float
    agents_executed: List[str]
    errors: List[str]

