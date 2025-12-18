"""
Context Evaluator Agent

Evaluates content context and overall quality for social media content.
"""
import json
import logging
from typing import Dict, Any
from src.models.state import AnalysisState
from src.api.client import APIClient
from .prompt import get_context_evaluator_prompt


async def context_evaluator_agent(
    state: AnalysisState,
    api_client: APIClient
) -> Dict[str, Any]:
    """
    Context Evaluator agent function for LangGraph.
    
    Evaluates content context and overall quality across multiple dimensions.
    
    Args:
        state: Current analysis state
        api_client: Unified API client
        
    Returns:
        Dictionary with state updates including context_score
    """
    logger = logging.getLogger(__name__)
    
    try:
        # Extract tweet text from state
        tweet_text = state.get('tweet_text', '') or state.get('tweet_data', {}).get('text', '')
        
        if not tweet_text:
            logger.warning("No tweet text found in state")
            return {
                'context_score': 5.0,
                'agent_responses': {
                    'context_evaluator': {
                        'error': 'No tweet text available',
                        'agent_score': 5.0
                    }
                }
            }
        
        # Prepare comprehensive input
        comprehensive_input = f"""
TWEET CONTENT:
{tweet_text}

AUTHOR INFORMATION:
- Username: {state.get('tweet_data', {}).get('author_username', 'N/A')}
- Tweet ID: {state.get('tweet_id', 'N/A')}
"""
        
        # Generate prompt
        prompt = get_context_evaluator_prompt(comprehensive_input)
        
        # Call OpenAI API
        response_text = await api_client.call_openai(prompt)
        
        # Parse response
        try:
            # Try to extract JSON from response
            if '```json' in response_text:
                start = response_text.find('```json') + 7
                end = response_text.find('```', start)
                json_content = response_text[start:end].strip()
                response_data = json.loads(json_content)
            elif '{' in response_text:
                start = response_text.find('{')
                end = response_text.rfind('}') + 1
                json_content = response_text[start:end]
                response_data = json.loads(json_content)
            else:
                response_data = json.loads(response_text)
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON response: {e}")
            logger.debug(f"Response text: {response_text[:500]}")
            response_data = {
                'agent_score': 5.0,
                'error': 'JSON parsing failed',
                'raw_response': response_text[:500]
            }
        
        # Extract context score
        context_score = response_data.get('agent_score', 5.0)
        
        # Return state updates
        return {
            'context_score': float(context_score),
            'agent_responses': {
                'context_evaluator': response_data
            }
        }
        
    except Exception as e:
        logger.error(f"Error in context_evaluator_agent: {e}")
        return {
            'context_score': 5.0,
            'agent_responses': {
                'context_evaluator': {
                    'error': str(e),
                    'agent_score': 5.0
                }
            }
        }

