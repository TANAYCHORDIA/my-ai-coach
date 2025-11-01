from pydantic import BaseModel, Field, HttpUrl, ConfigDict
from typing import List
from enum import Enum

# --- 1. Define Enums ---

class ChatMode(str, Enum):
    """Defines the two types of chat modes."""
    QUICK_TIP = "quick-tip"
    IN_DEPTH = "in-depth"

# --- 2. Define Sub-Models ---

class RiskScoreItem(BaseModel):
    """Strictly defines the structure for a risk score object."""
    exercise: str = Field(..., description="The name of the exercise.")
    risk: int = Field(..., ge=0, le=10, description="Risk score from 0 to 10.")
    effectiveness: int = Field(..., ge=0, le=10, description="Effectiveness score from 0 to 10.")
    
    # --- ADDED THIS CONFIG (Pydantic v2) ---
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "exercise": "Deadlift",
                "risk": 7,
                "effectiveness": 9
            }
        }
    )

class YouTubeLinkItem(BaseModel):
    """Strictly defines the structure for a YouTube link object."""
    exercise: str = Field(..., min_length=1, description="The name of the exercise.")
    url: HttpUrl = Field(..., description="The full URL to the YouTube video.")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "exercise": "Deadlift",
                "url": "https://youtube.com/watch?v=abc123"
            }
        }
    )


# --- 3. Your Main Schemas ---

class UserQuery(BaseModel):
    text: str = Field(..., min_length=1, description="User's query text")
    user_id: str = Field(..., description="Unique user identifier")
    mode: ChatMode = Field(..., description="Chat mode")
    
    # --- FIXED THIS SYNTAX (Pydantic v2) ---
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "text": "Create a 6-day workout plan",
                "user_id": "user123",
                "mode": "in-depth"
            }
        }
    )

class AIResponse(BaseModel):
    response_text: str = Field(..., min_length=1)
    risk_scores: List[RiskScoreItem] = Field(default_factory=list)
    youtube_links: List[YouTubeLinkItem] = Field(default_factory=list)
    
    # --- FIXED THIS SYNTAX (Pydantic v2) ---
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "response_text": "Here's your personalized plan...",
                "risk_scores": [{"exercise": "Deadlift", "risk": 7, "effectiveness": 9}],
                "youtube_links": [{"exercise": "Deadlift", "url": "https://youtube.com/watch?v=abc"}]
            }
        }
    )