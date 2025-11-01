import os
import logging
from typing import List

# Load .env FIRST (before other app imports)
from dotenv import load_dotenv
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '../../.env'))

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.schemas import UserQuery, AIResponse, ChatMode, RiskScoreItem, YouTubeLinkItem

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

# --- API Endpoints ---

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

@app.post("/api/chat", response_model=AIResponse)
def chat_endpoint(query: UserQuery):
    """
    Main chat endpoint for Coach Carter.
    
    Receives user queries and returns AI-generated training plans
    with risk scores and YouTube links.
    """
    try:
        logger.info(f"Received query from user {query.user_id}: {query.text[:50]}...")
        
        # Check if AI engine is available
        if not AI_ENGINE_AVAILABLE:
            logger.warning("AI engine not loaded, returning mock response")
            return AIResponse(
                response_text=f"[MOCK] Response for '{query.text}' in {query.mode.value} mode. AI engine not loaded yet.",
                risk_scores=[
                    RiskScoreItem(exercise="Deadlift", risk=6, effectiveness=9),
                    RiskScoreItem(exercise="Squat", risk=4, effectiveness=10)
                ],
                youtube_links=[]
            )
        
        # Call AI function (FastAPI automatically runs in threadpool)
        ai_answer_text = get_ai_response(query.text, query.mode.value)  # FIXED: Pass string value
        
        # Get risk analysis
        if RISK_MODULE_AVAILABLE:
            user_profile = {
                'injuries': ['lower back pain'],  # TODO: Get from database
                'goal': 'strength'  # TODO: Get from database
            }
            
            # Parse exercises from AI response (simple extraction)
            risk_scores = []
            exercises = ["Deadlift", "Squat", "Bench Press", "Row"]  # Extract from AI response in production
            
            for exercise in exercises:
                assessment = RiskAssessmentEngine.assess_exercise(exercise, user_profile)
                risk_scores.append(
                    RiskScoreItem(
                        exercise=assessment['exercise'],
                        risk=assessment['risk'],
                        effectiveness=assessment['effectiveness']
                    )
                )
        else:
            risk_scores = []
        
        # TODO: Get YouTube links
        youtube_links = []
        
        # Assemble response
        response = AIResponse(
            response_text=ai_answer_text,
            risk_scores=risk_scores,
            youtube_links=youtube_links
        )
        
        logger.info(f"Successfully generated response for user {query.user_id}")
        return response
        
    except ValueError as e:
        logger.error(f"Validation error: {e}")
        raise HTTPException(status_code=400, detail=f"Invalid input: {str(e)}")
    except Exception as e:
        logger.error(f"Error in /api/chat: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to generate response: {str(e)}")

@app.post("/api/test")
def test_schemas(query: UserQuery):
    """Test endpoint for schema validation."""
    return {
        "received": query.model_dump(),
        "mode_value": query.mode.value,
        "message": "Schema validation successful! ✅"
    }

# Development server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
