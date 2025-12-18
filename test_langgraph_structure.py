#!/usr/bin/env python3
"""
Test script to verify LangGraph foundation structure

Tests:
1. All imports work correctly
2. Configuration loads properly
3. API client initializes
4. Models work correctly
5. Example agent (context_evaluator) can be imported and used
"""
import sys
import os
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

def test_imports():
    """Test that all modules can be imported"""
    print("Testing imports...")
    
    try:
        from src.models import AnalysisState, TweetData
        print("  ✅ Models imported")
    except Exception as e:
        print(f"  ❌ Models import failed: {e}")
        return False
    
    try:
        from src.config import settings
        print("  ✅ Config imported")
    except Exception as e:
        print(f"  ❌ Config import failed: {e}")
        return False
    
    try:
        from src.api import APIClient
        print("  ✅ API client imported")
    except Exception as e:
        print(f"  ❌ API client import failed: {e}")
        return False
    
    try:
        from src.agents.core.base_agent import BaseAgent
        print("  ✅ Base agent imported")
    except Exception as e:
        print(f"  ❌ Base agent import failed: {e}")
        return False
    
    try:
        from src.agents.specialized.context_evaluator import context_evaluator_agent
        print("  ✅ Context evaluator agent imported")
    except Exception as e:
        print(f"  ❌ Context evaluator import failed: {e}")
        return False
    
    return True


def test_configuration():
    """Test configuration loading"""
    print("\nTesting configuration...")
    
    try:
        from src.config import settings
        assert settings.app_name == "TwitterNewsClassifier"
        assert settings.app_version == "2.0"
        print(f"  ✅ App name: {settings.app_name}")
        print(f"  ✅ App version: {settings.app_version}")
        print(f"  ✅ OpenAI model: {settings.openai_model}")
        return True
    except Exception as e:
        print(f"  ❌ Configuration test failed: {e}")
        return False


def test_models():
    """Test model creation"""
    print("\nTesting models...")
    
    try:
        from src.models.state import AnalysisState
        from src.models.tweet import TweetData
        from datetime import datetime
        
        # Test AnalysisState (TypedDict)
        state: AnalysisState = {
            'tweet_id': '123',
            'tweet_text': 'Test tweet',
            'context_score': 8.0
        }
        assert state['tweet_id'] == '123'
        print("  ✅ AnalysisState works")
        
        # Test TweetData (Pydantic)
        tweet = TweetData(
            tweet_id='123',
            text='Test tweet',
            created_at=datetime.now(),
            author_username='test_user',
            author_id='456'
        )
        assert tweet.tweet_id == '123'
        print("  ✅ TweetData works")
        
        return True
    except Exception as e:
        print(f"  ❌ Models test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_api_client():
    """Test API client initialization"""
    print("\nTesting API client...")
    
    try:
        from src.api import APIClient
        
        client = APIClient()
        assert client is not None
        print("  ✅ API client initialized")
        print(f"  ✅ OpenAI client: {'configured' if client.openai_client else 'not configured (expected if no API key)'}")
        return True
    except Exception as e:
        print(f"  ❌ API client test failed: {e}")
        return False


def test_agent_structure():
    """Test agent structure"""
    print("\nTesting agent structure...")
    
    try:
        from src.agents.specialized.context_evaluator import context_evaluator_agent
        from src.agents.specialized.context_evaluator.prompt import get_context_evaluator_prompt
        
        # Test prompt generation
        prompt = get_context_evaluator_prompt("Test input")
        assert "Context Evaluator" in prompt
        assert "Test input" in prompt
        print("  ✅ Prompt generation works")
        
        # Test agent function signature
        import inspect
        sig = inspect.signature(context_evaluator_agent)
        params = list(sig.parameters.keys())
        assert 'state' in params
        assert 'api_client' in params
        print("  ✅ Agent function signature correct")
        
        return True
    except Exception as e:
        print(f"  ❌ Agent structure test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests"""
    print("=" * 60)
    print("LANGGRAPH FOUNDATION STRUCTURE TEST")
    print("=" * 60)
    
    tests = [
        ("Imports", test_imports),
        ("Configuration", test_configuration),
        ("Models", test_models),
        ("API Client", test_api_client),
        ("Agent Structure", test_agent_structure),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n❌ {name} test crashed: {e}")
            results.append((name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{name}: {status}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! LangGraph foundation structure is ready.")
        return 0
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Please review errors above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())

