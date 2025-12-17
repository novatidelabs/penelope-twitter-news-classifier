"""
Tweet Data Model
===============
Pydantic model for tweet data structure.
"""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


class UserMetadata(BaseModel):
    """User metadata model"""
    user_id: str
    username: str
    display_name: Optional[str] = None
    created_at: Optional[datetime] = None
    description: Optional[str] = None
    verified: bool = False
    profile_image_url: Optional[str] = None
    public_metrics: Dict[str, int] = Field(default_factory=dict)


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
    Tweet data model for LangGraph state.
    
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
    
    @property
    def engagement_score(self) -> float:
        """Calculate engagement score (0-10 scale)"""
        total_engagement = (
            self.like_count * 1.0 +
            self.retweet_count * 2.0 +
            self.reply_count * 1.5 +
            self.quote_count * 2.5
        )
        # Normalize to 0-10 scale (logarithmic)
        import math
        if total_engagement == 0:
            return 0.0
        return min(10.0, math.log10(total_engagement + 1) * 2.0)
    
    @property
    def has_media(self) -> bool:
        """Check if tweet has media attachments"""
        return (
            self.media_attachments is not None and
            (len(self.media_attachments.links_analyzed) > 0 or
             len(self.media_attachments.images_analyzed) > 0)
        )
    
    @property
    def is_thread_tweet(self) -> bool:
        """Check if tweet is part of a thread"""
        return (
            self.thread_context is not None and
            self.thread_context.is_thread
        )

