"""
Signal Integrity Prompts
========================
Prompts for signal integrity agents.
"""

from .sarcasm import get_sarcasm_detector_prompt
from .echo import get_echo_mapper_prompt
from .latency import get_latency_validator_prompt
from .quality import get_quality_filter_prompt
from .phrases import get_phrase_detector_prompt

__all__ = [
    "get_sarcasm_detector_prompt",
    "get_echo_mapper_prompt",
    "get_latency_validator_prompt",
    "get_quality_filter_prompt",
    "get_phrase_detector_prompt",
]

