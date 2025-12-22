#!/usr/bin/env python3
"""Twitter News Classifier - LangGraph Implementation"""

import asyncio
import json
import logging
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List

from dotenv import load_dotenv

from src.graph import create_graph
from src.api.client import APIClient
from src.models.state import AnalysisState

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


async def main():
    """Main execution function"""
    print("🎯 TWITTER NEWS CLASSIFIER - LANGGRAPH SYSTEM")
    print("=" * 50)
    
    load_dotenv()
    
    openai_api_key = os.getenv('OPENAI_API_KEY')
    if not openai_api_key:
        logger.error("❌ OPENAI_API_KEY not found in environment variables")
        return
    
    print("📊 Initializing LangGraph workflow...")
    print("   🛰️  5 Signal Integrity Agents")
    print("   📡 12 Core Analysis Agents")
    print("=" * 50)
    
    try:
        tweets_data = await load_tweets_data()
        if not tweets_data:
            logger.error("❌ No tweets data found")
            return
        
        print(f"📈 Processing {len(tweets_data)} tweets...")
        
        api_client = APIClient()
        graph = create_graph(api_client)
        
        results = await process_tweets(tweets_data, graph)
        
        output_file = await save_results(results)
        display_final_summary(results, output_file)
        
    except Exception as e:
        logger.error(f"❌ Error in main execution: {str(e)}")
        raise


async def load_tweets_data() -> List[Dict[str, Any]]:
    """Load tweets from the most recent extraction"""
    try:
        data_dir = Path("data")
        extraction_files = []
        
        if data_dir.exists():
            for item in data_dir.rglob("extracted_tweets.json"):
                if item.is_file() and item.stat().st_size > 0:
                    extraction_files.append(item)
        
        if not extraction_files:
            logger.warning("⚠️  No extracted tweets found, using sample data")
            return get_sample_tweets()
        
        latest_file = max(extraction_files, key=lambda x: x.stat().st_mtime)
        logger.info(f"📁 Loading tweets from: {latest_file}")
        
        with open(latest_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        if isinstance(data, list):
            return data[:25]
        elif isinstance(data, dict) and 'tweets' in data:
            return data['tweets'][:25]
        else:
            logger.warning("⚠️  Unexpected tweet data format, using sample data")
            return get_sample_tweets()
            
    except Exception as e:
        logger.warning(f"⚠️  Error loading tweets: {str(e)}, using sample data")
        return get_sample_tweets()


def get_sample_tweets() -> List[Dict[str, Any]]:
    """Generate sample tweets for testing"""
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


def create_initial_state(tweet_data: Dict[str, Any]) -> AnalysisState:
    """Create initial state for LangGraph"""
    return AnalysisState(
        tweet_id=tweet_data['tweet_id'],
        tweet_text=tweet_data['text'],
        tweet_data=tweet_data,
    )


async def process_tweets(tweets_data: List[Dict[str, Any]], graph) -> Dict[str, Any]:
    """Process all tweets through LangGraph"""
    results = {
        "analysis_metadata": {
            "timestamp": datetime.now().isoformat(),
            "total_tweets": len(tweets_data),
            "agents_count": 17,
            "language": "English"
        },
        "tweets_analysis": []
    }
    
    for i, tweet_data in enumerate(tweets_data, 1):
        print(f"\n🔬 PROCESSING TWEET {i}/{len(tweets_data)}")
        print(f"🐦 Tweet ID: {tweet_data['tweet_id']}")
        print(f"📝 Content: {tweet_data['text'][:100]}...")
        print("=" * 60)
        
        try:
            initial_state = create_initial_state(tweet_data)
            
            print("🔄 Executing LangGraph workflow...")
            final_state = await graph.ainvoke(initial_state)
            
            tweet_analysis = {
                "tweet_metadata": {
                    "tweet_id": tweet_data['tweet_id'],
                    "text": tweet_data['text'],
                    "created_at": tweet_data['created_at'],
                    "author_username": tweet_data['author_username'],
                    "author_id": tweet_data['author_id'],
                    "engagement_metrics": {
                        "like_count": tweet_data.get('like_count', 0),
                        "retweet_count": tweet_data.get('retweet_count', 0),
                        "reply_count": tweet_data.get('reply_count', 0),
                        "quote_count": tweet_data.get('quote_count', 0)
                    }
                },
                "signal_integrity_results": {
                    "sarcasm_detected": final_state.get("sarcasm_detected", False),
                    "sarcasm_score": final_state.get("sarcasm_score", 0.0),
                    "echo_detected": final_state.get("echo_detected", False),
                    "echo_velocity": final_state.get("echo_velocity", 0.0),
                    "latency_valid": final_state.get("latency_valid", True),
                    "content_repriced": final_state.get("content_repriced", False),
                    "quality_pass": final_state.get("quality_pass", True),
                    "quality_score": final_state.get("quality_score", 0.0),
                    "banned_phrases": final_state.get("banned_phrases", []),
                    "tone_penalty": final_state.get("tone_penalty", 0.0),
                },
                "core_analysis_results": {
                    "summary": final_state.get("summary", ""),
                    "title": final_state.get("title", ""),
                    "context_score": final_state.get("context_score", 0.0),
                    "fact_check_score": final_state.get("fact_check_score", 0.0),
                    "depth_score": final_state.get("depth_score", 0.0),
                    "relevance_score": final_state.get("relevance_score", 0.0),
                    "structure_score": final_state.get("structure_score", 0.0),
                    "reflection_score": final_state.get("reflection_score", 0.0),
                    "metadata_score": final_state.get("metadata_score", 0.0),
                    "consensus_score": final_state.get("consensus_score", 0.0),
                },
                "final_output": {
                    "overall_score": final_state.get("overall_score", 0.0),
                    "recommendation": final_state.get("recommendation", "Review"),
                    "processing_complete": True,
                }
            }
            
            results["tweets_analysis"].append(tweet_analysis)
            
            overall_score = final_state.get("overall_score", 0.0)
            recommendation = final_state.get("recommendation", "Review")
            
            print(f"🎯 FINAL SCORE: {overall_score:.3f}")
            print(f"📊 RECOMMENDATION: {recommendation}")
            print("✅ TWEET ANALYSIS COMPLETED")
            
        except Exception as e:
            logger.error(f"❌ Error processing tweet {tweet_data['tweet_id']}: {str(e)}")
            results["tweets_analysis"].append({
                "tweet_metadata": {"tweet_id": tweet_data['tweet_id']},
                "error": str(e),
                "processing_complete": False
            })
            continue
    
    return results


async def save_results(results: Dict[str, Any]) -> Path:
    """Save results to JSON file"""
    try:
        results_dir = Path("results")
        results_dir.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"twitter_analysis_results_{timestamp}.json"
        output_file = results_dir / filename
        
        results["analysis_summary"] = {
            "total_tweets_processed": len(results["tweets_analysis"]),
            "successful_analyses": len([t for t in results["tweets_analysis"] if t.get("processing_complete", False)]),
            "failed_analyses": len([t for t in results["tweets_analysis"] if not t.get("processing_complete", False)]),
            "success_rate_percentage": (
                len([t for t in results["tweets_analysis"] if t.get("processing_complete", False)]) / 
                len(results["tweets_analysis"]) * 100
                if results["tweets_analysis"] else 0
            )
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False, default=str)
        
        logger.info(f"✅ Results saved to: {output_file}")
        return output_file
        
    except Exception as e:
        logger.error(f"❌ Error saving results: {str(e)}")
        raise


def display_final_summary(results: Dict[str, Any], output_file: Path):
    """Display final execution summary"""
    print("\n" + "=" * 60)
    print("🎉 TWITTER NEWS CLASSIFIER - EXECUTION COMPLETED")
    print("=" * 60)
    
    summary = results["analysis_summary"]
    print("📊 ANALYSIS SUMMARY:")
    print(f"   ✅ Tweets Processed: {summary['total_tweets_processed']}")
    print(f"   ✅ Successful Analyses: {summary['successful_analyses']}")
    print(f"   ❌ Failed Analyses: {summary['failed_analyses']}")
    print(f"   📈 Success Rate: {summary['success_rate_percentage']:.1f}%")
    
    print("\n📁 RESULTS LOCATION:")
    print(f"   📄 File: {output_file}")
    if output_file.exists():
        print(f"   📊 Size: {output_file.stat().st_size:,} bytes")
    
    print("\n🌟 LANGGRAPH WORKFLOW SYSTEM OPERATIONAL! 🌟")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
