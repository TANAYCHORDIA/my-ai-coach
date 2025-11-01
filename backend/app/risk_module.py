from typing import Dict, List
from app.schemas import RiskScoreItem

class RiskAssessmentEngine:
    """
    Calculates risk and effectiveness scores based on exercise and user profile
    """
    
    HIGH_RISK_MAPPING = {
        'back': ['deadlift', 'squat', 'bent over row', 'overhead press', 'clean'],
        'knee': ['squat', 'lunge', 'leg extension', 'box jump', 'running'],
        'shoulder': ['overhead press', 'bench press', 'pull-up', 'dip', 'upright row'],
        'ankle': ['box jump', 'running', 'jump rope', 'burpee', 'plyometric'],
        'wrist': ['push-up', 'plank', 'handstand', 'clean', 'front squat'],
        'hip': ['squat', 'deadlift', 'lunge', 'leg press', 'running']
    }
    
    EFFECTIVENESS_MAPPING = {
        'strength': {
            'high': ['deadlift', 'squat', 'bench press', 'overhead press', 'row'],
            'medium': ['lunge', 'pull-up', 'dip', 'clean', 'snatch'],
            'low': ['bicep curl', 'tricep extension', 'calf raise', 'lateral raise']
        },
        'muscle_gain': {
            'high': ['squat', 'deadlift', 'bench press', 'pull-up', 'row', 'lunge'],
            'medium': ['leg press', 'dumbbell press', 'bicep curl', 'tricep extension'],
            'low': ['calf raise', 'wrist curl', 'neck exercise']
        },
        'fat_loss': {
            'high': ['burpee', 'sprint', 'jump rope', 'circuit training', 'hiit'],
            'medium': ['running', 'cycling', 'rowing', 'swimming'],
            'low': ['walking', 'stretching', 'yoga']
        },
        'endurance': {
            'high': ['running', 'cycling', 'swimming', 'rowing', 'jump rope'],
            'medium': ['circuit training', 'hiking', 'stair climbing'],
            'low': ['weightlifting', 'powerlifting', 'sprint']
        }
    }
    
    @staticmethod
    def calculate_risk(exercise: str, user_injuries: List[str]) -> Dict:
        """Calculate risk score for an exercise given user's injury history"""
        exercise_lower = exercise.lower()
        risk_score = 2  # Base risk
        reasons = []
        
        if not user_injuries:
            return {
                'risk': risk_score,
                'reason': 'No injury history - low baseline risk'
            }
        
        for injury in user_injuries:
            injury_lower = injury.lower()
            
            for body_part, risky_exercises in RiskAssessmentEngine.HIGH_RISK_MAPPING.items():
                if body_part in injury_lower:
                    for risky_ex in risky_exercises:
                        if risky_ex in exercise_lower:
                            risk_score += 3
                            reasons.append(f"{body_part.capitalize()} injury increases risk for {exercise}")
        
        risk_score = min(risk_score, 10)
        reason_text = '; '.join(reasons) if reasons else 'Low risk - no injury conflicts'
        
        return {
            'risk': risk_score,
            'reason': reason_text
        }
    
    @staticmethod
    def calculate_effectiveness(exercise: str, user_goal: str) -> Dict:
        """Calculate effectiveness score for an exercise given user's goal"""
        exercise_lower = exercise.lower()
        goal_lower = user_goal.lower() if user_goal else 'general'
        
        effectiveness_score = 5
        reason = 'Moderate effectiveness for general fitness'
        
        goal_mapping = {
            'strength': ['strength', 'power', 'strong'],
            'muscle_gain': ['muscle', 'hypertrophy', 'bulk', 'mass'],
            'fat_loss': ['fat loss', 'weight loss', 'cut', 'lean'],
            'endurance': ['endurance', 'cardio', 'stamina', 'conditioning']
        }
        
        mapped_goal = None
        for key, aliases in goal_mapping.items():
            if any(alias in goal_lower for alias in aliases):
                mapped_goal = key
                break
        
        if mapped_goal and mapped_goal in RiskAssessmentEngine.EFFECTIVENESS_MAPPING:
            categories = RiskAssessmentEngine.EFFECTIVENESS_MAPPING[mapped_goal]
            
            for category_ex in categories['high']:
                if category_ex in exercise_lower:
                    effectiveness_score = 9
                    reason = f'Excellent for {mapped_goal} goals'
                    break
            
            if effectiveness_score == 5:
                for category_ex in categories['medium']:
                    if category_ex in exercise_lower:
                        effectiveness_score = 6
                        reason = f'Good for {mapped_goal} goals'
                        break
            
            if effectiveness_score == 5:
                for category_ex in categories['low']:
                    if category_ex in exercise_lower:
                        effectiveness_score = 3
                        reason = f'Limited effectiveness for {mapped_goal} goals'
                        break
        
        return {
            'effectiveness': effectiveness_score,
            'reason': reason
        }
    
    @staticmethod
    def assess_exercise(exercise: str, user_profile: Dict) -> Dict:
        """Complete assessment combining risk and effectiveness"""
        injuries = user_profile.get('injuries', [])
        goal = user_profile.get('goal', 'general')
        
        risk_data = RiskAssessmentEngine.calculate_risk(exercise, injuries)
        effectiveness_data = RiskAssessmentEngine.calculate_effectiveness(exercise, goal)
        
        return {
            'exercise': exercise,
            'risk': risk_data['risk'],
            'effectiveness': effectiveness_data['effectiveness'],
            'reason': f"{effectiveness_data['reason']}. {risk_data['reason']}"
        }

def calculate_risk(exercise: str, user_injury: str) -> List[RiskScoreItem]:
    """
    FIXED: Return List[RiskScoreItem] to match main.py expectations
    """
    injuries = [user_injury] if user_injury else []
    result = RiskAssessmentEngine.calculate_risk(exercise, injuries)
    
    # Return RiskScoreItem for main.py compatibility
    return [
        RiskScoreItem(
            exercise=exercise,
            risk=result['risk'],
            effectiveness=5  # Default effectiveness
        )
    ]
