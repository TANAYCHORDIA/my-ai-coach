from typing import List
from app.youtube_db import get_all_exercises

def extract_exercises(ai_response: str) -> List[str]:
    """Extract unique exercises from AI response using available exercises"""
    found_exercises = set()
    response_lower = ai_response.lower()
    
    # Get all available exercises from youtube_links.txt or exercise.txt
    available_exercises = get_all_exercises()
    
    for exercise in available_exercises:
        if exercise.lower() in response_lower:
            found_exercises.add(exercise)
    
    # Return top exercises (limit to 8 for response)
    return list(found_exercises)[:8]
