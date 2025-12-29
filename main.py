#!/usr/bin/env python3
"""
Multi-agent Twitter news classification system using LangGraph workflows.
"""

import asyncio
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List

from dotenv import load_dotenv
from loguru import logger

from src.graph import graph
from src.state import AnalysisState

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


def create_initial_state(
    tweet_id: str,
    tweet_text: str,
    tweet_metadata: Dict[str, Any],
    session_id: str = None
) -> AnalysisState:
    """
    Create initial state for LangGraph workflow.
    
    Only these 3 fields should be provided as input:
    - tweet_id: ID of the tweet
    - tweet_text: Text content of the tweet
    - tweet_metadata: Metadata dictionary (author, timestamps, engagement metrics, etc.)
    """
    if not session_id:
        session_id = f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    return AnalysisState(
        tweet_id=tweet_id,
        tweet_text=tweet_text,
        tweet_metadata=tweet_metadata,
        # Keep tweet_data for backward compatibility
        tweet_data=tweet_metadata,
    )


async def load_tweets_data() -> List[Dict[str, Any]]:
    """Load tweets from the most recent extraction."""
    try:
        data_dir = Path("data")
        extraction_files = []
        
        if data_dir.exists():
            for item in data_dir.rglob("extracted_tweets.json"):
                if item.is_file() and item.stat().st_size > 0:
                    extraction_files.append(item)
        
        if not extraction_files:
            logger.warning("No extracted tweets found, using sample data")
            return get_sample_tweets()
        
        latest_file = max(extraction_files, key=lambda x: x.stat().st_mtime)
        logger.info(f"Reading: {latest_file}")
        
        with open(latest_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        if isinstance(data, list):
            return data[:25]
        elif isinstance(data, dict) and 'tweets' in data:
            return data['tweets'][:25]
        else:
            logger.warning("Unexpected tweet data format, using sample data")
            return get_sample_tweets()
            
    except Exception as e:
        logger.warning(f"Error loading tweets: {str(e)}, using sample data")
        return get_sample_tweets()


def get_sample_tweets() -> List[Dict[str, Any]]:
    """Generate sample tweets for testing."""
    return [
        {
            "tweet_id": "1953769308057682392",
            "text": "🚀 Bitcoin breaking new resistance levels! #BTC #Crypto",
            "created_at": "2025-01-08T10:44:36",
            "author_username": "CryptoTrader_Pro",
            "author_id": "1766033656089370624",
            "like_count": 142,
            "retweet_count": 28,
            "reply_count": 15,
            "quote_count": 7,
            "user_metadata": {
                "username": "CryptoTrader_Pro",
                "display_name": "Crypto Trader Pro",
                "description": "Professional crypto trader. Technical analysis and market insights.",
                "verified": False,
                "followers_count": 15420,
                "following_count": 892,
                "tweet_count": 3241,
                "profile_image_url": "https://example.com/profile.jpg"
            },
            "media_attachments": None,
            "external_links": [],
            "thread_context": {
                "is_thread": False,
                "conversation_id": None,
                "in_reply_to_user_id": None,
                "thread_position": None
            }
        }
    ]


async def main():
    """Process tweets with LangGraph workflow."""
    logger.info("Starting Twitter News Classifier...")
    
    output_dir = Path("results")
    output_dir.mkdir(exist_ok=True)
    
    logger.info("Loading tweets...")
    tweets = await load_tweets_data()
    tweets = tweets[:5]  # Process first 5 tweets
    
    logger.info(f"Processing {len(tweets)} tweets")
    
    session_id = f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    batch_results = []
    batch_start = datetime.now()
    
    for idx, tweet_data in enumerate(tweets, 1):
        tweet_text = tweet_data.get('text', '')
        tweet_id = tweet_data.get('tweet_id', f'unknown_{idx}')
        
        logger.info(f"Tweet {idx}/{len(tweets)}: {tweet_text[:50]}...")
        
        try:
            initial_state = create_initial_state(
                tweet_id=tweet_id,
                tweet_text=tweet_text,
                tweet_metadata=tweet_data,
                session_id=f"{session_id}_tweet_{idx}"
            )
            
            result = await graph.ainvoke(initial_state)
            
            overall_score = result.get("overall_score", 0.0)
            recommendation = result.get("recommendation", "Review")
            summary = result.get("summary", "")
            title = result.get("title", "")
            
            # Signal Integrity Results
            sarcasm_detected = result.get("sarcasm_detected", False)
            sarcasm_score = result.get("sarcasm_score", 0.0)
            echo_detected = result.get("echo_detected", False)
            echo_velocity = result.get("echo_velocity", 0.0)
            quality_pass = result.get("quality_pass", True)
            quality_score = result.get("quality_score", 0.0)
            
            # Core Analysis Results
            context_score = result.get("context_score", 0.0)
            fact_check_score = result.get("fact_check_score", 0.0)
            depth_score = result.get("depth_score", 0.0)
            relevance_score = result.get("relevance_score", 0.0)
            structure_score = result.get("structure_score", 0.0)
            reflection_score = result.get("reflection_score", 0.0)
            metadata_score = result.get("metadata_score", 0.0)
            consensus_score = result.get("consensus_score", 0.0)
            
            batch_results.append({
                "tweet_id": tweet_id,
                "tweet_text": tweet_text[:200],  # Truncate for readability
                "author_username": tweet_data.get("author_username", "unknown"),
                "overall_score": overall_score,
                "recommendation": recommendation,
                "summary": summary[:200] if summary else "",
                "title": title[:100] if title else "",
                "signal_integrity": {
                    "sarcasm_detected": sarcasm_detected,
                    "sarcasm_score": sarcasm_score,
                    "echo_detected": echo_detected,
                    "echo_velocity": echo_velocity,
                    "quality_pass": quality_pass,
                    "quality_score": quality_score,
                },
                "core_analysis_scores": {
                    "context_score": context_score,
                    "fact_check_score": fact_check_score,
                    "depth_score": depth_score,
                    "relevance_score": relevance_score,
                    "structure_score": structure_score,
                    "reflection_score": reflection_score,
                    "metadata_score": metadata_score,
                    "consensus_score": consensus_score,
                },
                "processing_complete": result.get("processing_complete", True),
                "error": result.get("error"),
            })
            
            logger.success(
                f"Tweet {idx} complete | "
                f"Score: {overall_score:.1f}/10 | "
                f"Recommendation: {recommendation} | "
                f"Quality: {'PASS' if quality_pass else 'FAIL'}"
            )
            
        except Exception as e:
            logger.error(f"Tweet {idx} failed: {e}")
            batch_results.append({
                "tweet_id": tweet_id,
                "tweet_text": tweet_text[:200],
                "author_username": tweet_data.get("author_username", "unknown"),
                "overall_score": 0.0,
                "recommendation": "ERROR",
                "processing_complete": False,
                "error": str(e),
            })
    
    batch_end = datetime.now()
    
    results_file = output_dir / f"twitter_classification_results_{session_id}.json"
    with open(results_file, "w", encoding='utf-8') as f:
        json.dump({
            "session_id": session_id,
            "start_time": batch_start.isoformat(),
            "end_time": batch_end.isoformat(),
            "total_tweets": len(tweets),
            "completed_tweets": sum(1 for r in batch_results if r.get("processing_complete")),
            "failed_tweets": sum(1 for r in batch_results if not r.get("processing_complete")),
            "results": batch_results,
            "configuration": {
                "agents_count": 17,
                "signal_integrity_agents": 5,
                "core_analysis_agents": 12,
            }
        }, f, indent=2, ensure_ascii=False, default=str)
    
    logger.info(f"Results saved: {results_file}")
    
    # Summary
    completed = sum(1 for r in batch_results if r.get("processing_complete"))
    failed = len(batch_results) - completed
    avg_scores = [r["overall_score"] for r in batch_results if r.get("overall_score", 0) > 0]
    
    logger.info(f"Summary: {completed}/{len(tweets)} completed, {failed} failed")
    if avg_scores:
        logger.info(f"Average score: {sum(avg_scores) / len(avg_scores):.2f}/10")
    logger.info(f"Duration: {(batch_end - batch_start).total_seconds():.1f}s")
    logger.success("Done!")


if __name__ == "__main__":
    asyncio.run(main())
