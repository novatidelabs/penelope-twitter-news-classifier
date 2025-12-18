"""
Configuration module using Pydantic Settings
"""
from .settings import Settings

# Create global settings instance
settings = Settings()

__all__ = ['Settings', 'settings']

