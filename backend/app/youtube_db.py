from pathlib import Path
from typing import List
import logging

logger = logging.getLogger(__name__)

class YouTubeLinksDB:
    """Load YouTube links from exercise.txt file"""
    
    def __init__(self):
        # Path to exercise.txt
        self.data_dir = Path(__file__).parent.parent / "data"
        self.exercise_file = self.data_dir / "exercise.txt"
        self.links_cache = {}
        self._load_links()
    
    def _load_links(self):
        """Load links from exercise.txt with ||| separator"""
        if not self.exercise_file.exists():
            logger.warning(f"⚠️ {self.exercise_file} not found!")
            return
        
        try:
            with open(self.exercise_file, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith('#'):  # Skip empty lines and comments
                        continue
                    
                    # Format: Exercise Name|||URL1|||URL2|||URL3
                    parts = line.split('|||')
                    if len(parts) >= 2:
                        exercise = parts[0].strip()
                        urls = [url.strip() for url in parts[1:] if url.strip()]
                        self.links_cache[exercise.lower()] = {
                            'exercise': exercise,
                            'urls': urls
                        }
            
            logger.info(f"✅ Loaded {len(self.links_cache)} exercises from exercise.txt")
        
        except Exception as e:
            logger.error(f"❌ Error loading exercise links: {e}")
    
    def get_links(self, exercise: str) -> List[str]:
        """Get YouTube links for an exercise"""
        exercise_lower = exercise.lower().strip()
        
        # Exact match first
        if exercise_lower in self.links_cache:
            return self.links_cache[exercise_lower]['urls']
        
        # Partial match (word contains)
        for key, data in self.links_cache.items():
            if exercise_lower in key or key in exercise_lower:
                return data['urls']
        
        return []
    
    def get_all_exercises(self) -> List[str]:
        """Get all available exercises"""
        return [data['exercise'] for data in self.links_cache.values()]

# Initialize once
youtube_db = YouTubeLinksDB()

def get_youtube_links(exercise: str) -> List[str]:
    """Helper function for external use"""
    return youtube_db.get_links(exercise)

def get_all_exercises() -> List[str]:
    """Get all exercises with YouTube links"""
    return youtube_db.get_all_exercises()
