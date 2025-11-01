from pydantic import BaseModel, Field
from typing import List, Optional

class AthleteProfile(BaseModel):
    """Complete athlete profile"""
    user_id: str = Field(..., description="Unique user identifier")
    name: str = Field(..., min_length=1, description="Athlete's name")
    age: int = Field(..., ge=10, le=100, description="Age in years")
    height_cm: float = Field(..., ge=100, le=250, description="Height in cm")
    weight_kg: float = Field(..., ge=30, le=300, description="Weight in kg")
    gender: str = Field(..., description="Gender")
    sport: str = Field(..., min_length=1, description="Sport (any sport)")
    experience_years: int = Field(..., ge=0, le=60, description="Years of experience")
    goals: List[str] = Field(..., min_items=1, description="Training goals")
    duration_weeks: int = Field(..., ge=1, le=52, description="Program duration")
    sessions_per_week: int = Field(..., ge=1, le=7, description="Sessions per week")
    available_equipment: List[str] = Field(default_factory=list, description="Equipment")
    injuries: List[str] = Field(default_factory=list, description="Injuries/health issues")
    dietary_restrictions: List[str] = Field(default_factory=list, description="Dietary restrictions")
    
    class Config:
        json_schema_extra = {
            "example": {
                "user_id": "user123",
                "name": "John",
                "age": 25,
                "height_cm": 180,
                "weight_kg": 75,
                "gender": "male",
                "sport": "football",
                "experience_years": 5,
                "goals": ["speed", "strength"],
                "duration_weeks": 12,
                "sessions_per_week": 5,
                "available_equipment": [],
                "injuries": [],
                "dietary_restrictions": []
            }
        }

class ProfileResponse(BaseModel):
    """Response confirming profile saved"""
    success: bool
    message: str
    user_id: str
