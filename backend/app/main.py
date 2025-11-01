import os
import logging
from typing import List

# Load .env FIRST
from dotenv import load_dotenv
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '../../.env'))

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.schemas import UserQuery, AIResponse, ChatMode, RiskScoreItem, YouTubeLinkItem
from app.athlete_profile import AthleteProfile, ProfileResponse
from app.profile_service import profile_service
from app.exercise_parser import extract_exercises
from app.youtube_db import get_youtube_links

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import AI modules
try:
    from app.ai_engine import get_ai_response
    AI_ENGINE_AVAILABLE = True
except ImportError as e:
    logger.warning(f"AI engine not available: {e}")
    AI_ENGINE_AVAILABLE = False

try:
    from app.risk_module import RiskAssessmentEngine
    RISK_MODULE_AVAILABLE = True
except ImportError as e:
    logger.warning(f"Risk module not available: {e}")
    RISK_MODULE_AVAILABLE = False

# Lifespan context manager
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manages application lifecycle."""
    logger.info("🚀 Coach Carter is starting up...")
    logger.info("✅ Startup complete")
    
    yield
    
    logger.info("👋 Coach Carter is shutting down...")
    logger.info("✅ Cleanup complete")

# Initialize FastAPI
app = FastAPI(
    title="Coach Carter API",
    description="AI-powered training program generator by Team LATECOMERS",
    version="1.0.0",
    lifespan=lifespan
)

# CORS configuration
origins = [
    "http://localhost:3000",
    "http://localhost:5173",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==========================================
# --- HEALTH & BASIC ENDPOINTS ---
# ==========================================

@app.get("/")
def root():
    """Root endpoint - confirms API is running."""
    return {
        "message": "Welcome to Coach Carter API",
        "status": "healthy",
        "version": "1.0.0",
        "team": "LATECOMERS"
    }

@app.get("/api/health")
def health_check():
    """Health check for monitoring."""
    return {
        "status": "ok",
        "service": "Coach Carter",
        "ai_engine": "ready" if AI_ENGINE_AVAILABLE else "not loaded",
        "risk_module": "ready" if RISK_MODULE_AVAILABLE else "not loaded"
    }

# ==========================================
# --- PROFILE ENDPOINTS ---
# ==========================================

@app.post("/api/profile/create", response_model=ProfileResponse)
def create_athlete_profile(profile: AthleteProfile):
    """
    Create or update athlete profile.
    
    Captures:
    - age, height, weight, gender, sport
    - experience, goals, duration, frequency
    - equipment, injuries, dietary restrictions
    """
    try:
        logger.info(f"Creating profile for user {profile.user_id}: {profile.sport} athlete")
        
        success = profile_service.save_profile(profile)
        
        if success:
            logger.info(f"✅ Profile created for user {profile.user_id}")
            return ProfileResponse(
                success=True,
                message=f"Profile created successfully for {profile.sport} athlete! ({profile.duration_weeks}-week program)",
                user_id=profile.user_id
            )
        else:
            raise HTTPException(status_code=500, detail="Failed to save profile")
            
    except Exception as e:
        logger.error(f"Error creating profile: {e}")
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/profile/{user_id}")
def get_athlete_profile(user_id: str):
    """Retrieve athlete profile"""
    try:
        profile = profile_service.get_profile(user_id)
        
        if not profile:
            raise HTTPException(status_code=404, detail="Profile not found")
        
        logger.info(f"Retrieved profile for user {user_id}")
        return profile.model_dump()
        
    except Exception as e:
        logger.error(f"Error retrieving profile: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ==========================================
# --- CHAT ENDPOINT ---
# ==========================================

@app.post("/api/chat", response_model=AIResponse)
def chat_endpoint(query: UserQuery):
    """
    Main chat endpoint for Coach Carter.
    
    Receives user queries and generates:
    - Personalized training plans
    - Risk assessments
    - Exercise recommendations
    - YouTube tutorials
    
    Uses athlete profile for context if available.
    """
    try:
        logger.info(f"Received query from user {query.user_id}: {query.text[:50]}...")
        
        # Check if AI engine is available
        if not AI_ENGINE_AVAILABLE:
            logger.warning("AI engine not loaded, returning mock response")
            return AIResponse(
                response_text=f"[MOCK] Response for '{query.text}' in {query.mode.value} mode.",
                risk_scores=[
                    RiskScoreItem(exercise="Deadlift", risk=6, effectiveness=9),
                    RiskScoreItem(exercise="Squat", risk=4, effectiveness=9)
                ],
                youtube_links=[]
            )
        
        # Get user's profile for context
        user_profile = profile_service.get_profile(query.user_id)
        
        # Prepare context with athlete profile
        profile_context = ""
        if user_profile:
            profile_context = f"""
ATHLETE PROFILE:
- Name: {user_profile.name}
- Sport: {user_profile.sport}
- Age: {user_profile.age} years
- Height: {user_profile.height_cm} cm
- Weight: {user_profile.weight_kg} kg
- Experience: {user_profile.experience_years} years
- Goals: {', '.join(user_profile.goals)}
- Training Duration: {user_profile.duration_weeks} weeks
- Sessions/Week: {user_profile.sessions_per_week}
- Equipment: {', '.join(user_profile.available_equipment) if user_profile.available_equipment else 'bodyweight only'}
- Injuries: {', '.join(user_profile.injuries) if user_profile.injuries else 'none'}
"""
        
        # Get AI response with profile context
        ai_answer_text = get_ai_response(query.text, query.mode.value, profile_context)
        
        # Extract exercises and calculate risk
        exercises = extract_exercises(ai_answer_text)
        risk_scores = []
        
        # Calculate risk scores (ONLY if module available AND user has profile)
        if RISK_MODULE_AVAILABLE and user_profile:
            for exercise in exercises:
                if not exercise or not exercise.strip():
                    continue
                    
                assessment = RiskAssessmentEngine.assess_exercise(
                    exercise,
                    {
                        'injuries': user_profile.injuries,
                        'goal': user_profile.goals[0] if user_profile.goals else 'general'
                    }
                )
                risk_scores.append(
                    RiskScoreItem(
                        exercise=assessment['exercise'],
                        risk=assessment['risk'],
                        effectiveness=assessment['effectiveness']
                    )
                )
        
        # Get YouTube links for each exercise (OUTSIDE the if block!)
        youtube_links = []
        for exercise in exercises:
            if exercise and exercise.strip():  # Make sure exercise name is NOT empty
                links = get_youtube_links(exercise)
                if links and len(links) > 0:  # Make sure links exist
                    youtube_links.append(
                        YouTubeLinkItem(
                            exercise=exercise.strip(),  # Clean up whitespace
                            url=links[0]  # First link
                        )
                    )
        
        # Assemble response
        response = AIResponse(
            response_text=ai_answer_text,
            risk_scores=risk_scores,
            youtube_links=youtube_links
        )
        
        logger.info(f"✅ Successfully generated response for user {query.user_id}")
        return response
        
    except ValueError as e:
        logger.error(f"Validation error: {e}")
        raise HTTPException(status_code=400, detail=f"Invalid input: {str(e)}")
    except Exception as e:
        logger.error(f"Error in /api/chat: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to generate response: {str(e)}")

# ==========================================
# --- TEST ENDPOINT ---
# ==========================================

@app.post("/api/test")
def test_schemas(query: UserQuery):
    """Test endpoint for schema validation."""
    return {
        "received": query.model_dump(),
        "mode_value": query.mode.value,
        "message": "Schema validation successful! ✅"
    }

# ==========================================
# --- DEVELOPMENT SERVER ---
# ==========================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
