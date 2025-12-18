"""
Tweet Data Model

Pydantic model for tweet data structure.
"""
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime


class UserMetadata(BaseModel):
    """User metadata model"""
    user_id: str
    username: str
    display_name: str
    description: Optional[str] = None
    verified: bool = False
    followers_count: int = 0
    following_count: int = 0
    tweet_count: int = 0
    profile_image_url: Optional[str] = None


class MediaAttachment(BaseModel):
    """Media attachment model"""
    links_analyzed: List[str] = Field(default_factory=list)
    images_analyzed: List[Dict[str, Any]] = Field(default_factory=list)
    total_processing_time: float = 0.0


class ThreadContext(BaseModel):
    """Thread context model"""
    is_thread: bool = False
    conversation_id: Optional[str] = None
    in_reply_to_user_id: Optional[str] = None
    thread_position: Optional[int] = None


class TweetData(BaseModel):
    """
    Tweet data model for LangGraph workflow.
    
    Represents a tweet with all its metadata and context.
    """
    tweet_id: str
    text: str
    created_at: datetime
    author_username: str
    author_id: str
    like_count: int = 0
    retweet_count: int = 0
    reply_count: int = 0
    quote_count: int = 0
    user_metadata: Optional[UserMetadata] = None
    media_attachments: Optional[MediaAttachment] = None
    external_links: List[str] = Field(default_factory=list)
    thread_context: Optional[ThreadContext] = None
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

