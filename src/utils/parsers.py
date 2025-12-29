"""
JSON parsing utilities for agent responses
"""

import json
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)


def parse_json_response(response_text: str, agent_name: str = "unknown") -> Dict[str, Any]:
    """
    Safely parse JSON response from LLM with multiple fallback strategies.
    
    Args:
        response_text: Raw response text from LLM
        agent_name: Name of the agent (for logging)
        
    Returns:
        Parsed JSON dictionary
        
    Raises:
        ValueError: If JSON cannot be parsed
    """
    # Strategy 1: Direct JSON parsing
    try:
        return json.loads(response_text)
    except json.JSONDecodeError:
        pass
    
    # Strategy 2: Extract JSON from code blocks
    try:
        if '```json' in response_text:
            start = response_text.find('```json') + 7
            end = response_text.find('```', start)
            json_content = response_text[start:end].strip()
            return json.loads(json_content)
        elif '```' in response_text:
            start = response_text.find('```') + 3
            end = response_text.find('```', start)
            json_content = response_text[start:end].strip()
            # Remove language identifier if present
            if json_content.startswith('json'):
                json_content = json_content[4:].strip()
            return json.loads(json_content)
    except (json.JSONDecodeError, ValueError):
        pass
    
    # Strategy 3: Extract JSON from curly braces
    try:
        start = response_text.find('{')
        end = response_text.rfind('}') + 1
        if start != -1 and end > start:
            json_content = response_text[start:end]
            return json.loads(json_content)
    except (json.JSONDecodeError, ValueError):
        pass
    
    # Strategy 4: Return fallback response
    logger.warning(f"JSON parsing failed for {agent_name}, using fallback")
    return {
        'error': f'JSON parsing failed for {agent_name}',
        'raw_response': response_text[:500],  # Truncate long responses
        'agent_score': 5.0,  # Fallback score
        'status': 'failed'
    }


def safe_json_loads(json_string: str, default: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Safely load JSON string with default fallback.
    
    Args:
        json_string: JSON string to parse
        default: Default value to return if parsing fails
        
    Returns:
        Parsed JSON dictionary or default value
    """
    try:
        return json.loads(json_string)
    except (json.JSONDecodeError, TypeError):
        return default or {}

