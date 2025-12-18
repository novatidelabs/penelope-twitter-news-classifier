"""
Analysis State Model for LangGraph Workflow

Defines the state structure that flows through the LangGraph workflow.
Uses TypedDict for flexibility with optional fields.
"""
from typing import TypedDict, Optional, Dict, Any, List


class AnalysisState(TypedDict, total=False):
    """
    State structure for the analysis workflow.
    
    Uses TypedDict with total=False to make all fields optional,
    allowing incremental state updates as the workflow progresses.
    """
    
    # Input fields
    tweet_id: str
    tweet_text: str
    tweet_data: Dict[str, Any]
    
    # Signal Integrity Results
    sarcasm_score: float
    sarcasm_detected: bool
    sarcasm_reasoning: str
    
    echo_detected: bool
    echo_velocity: float
    reddit_threads: int
    
    latency_valid: bool
    content_repriced: bool
    time_delta_seconds: int
    
    quality_pass: bool
    quality_score: float
    quality_reasoning: str
    
    banned_phrases: List[str]
    banned_phrase_penalty: float
    
    # Core Analysis Results
    summary: str
    context_score: float
    fact_check_results: Dict[str, Any]
    depth_score: float
    relevance_score: float
    structure_score: float
    reflection_score: float
    metadata_score: float
    consensus_score: float
    
    # Final Output
    overall_score: float
    recommendation: str
    formatted_output: Dict[str, Any]
    
    # Metadata
    agent_responses: Dict[str, Any]
    execution_metadata: Dict[str, Any]

