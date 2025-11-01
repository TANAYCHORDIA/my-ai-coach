import json
from pathlib import Path
from typing import Dict, Optional
from app.athlete_profile import AthleteProfile

class UserProfileService:
    """Manages athlete profiles"""
    
    def __init__(self):
        self.data_dir = Path(__file__).parent.parent / "data"
        self.profiles_dir = self.data_dir / "profiles"
        self.profiles_dir.mkdir(parents=True, exist_ok=True)
    
    def save_profile(self, profile: AthleteProfile) -> bool:
        """Save athlete profile"""
        try:
            file_path = self.profiles_dir / f"{profile.user_id}.json"
            with open(file_path, 'w') as f:
                json.dump(profile.model_dump(), f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving profile: {e}")
            return False
    
    def get_profile(self, user_id: str) -> Optional[AthleteProfile]:
        """Retrieve athlete profile"""
        try:
            file_path = self.profiles_dir / f"{user_id}.json"
            if file_path.exists():
                with open(file_path, 'r') as f:
                    data = json.load(f)
                return AthleteProfile(**data)
            return None
        except Exception as e:
            print(f"Error loading profile: {e}")
            return None
    
    def profile_exists(self, user_id: str) -> bool:
        """Check if profile exists"""
        file_path = self.profiles_dir / f"{user_id}.json"
        return file_path.exists()

# Global instance
profile_service = UserProfileService()
