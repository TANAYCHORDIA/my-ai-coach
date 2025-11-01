# backend/test_ai.py

from app.ai_engine import get_ai_response

print("\n" + "="*70)
print("🧪 TESTING COACH CARTER AI ENGINE")
print("="*70 + "\n")

# TEST 1: Safety Question (tests RAG)
print("📝 TEST 1: Is deadlift safe for back pain?")
print("-" * 70)

response1 = get_ai_response(
    user_query="Is a deadlift safe for someone with lower back pain?",
    mode="quick"
)

print("RESPONSE:")
print(response1)
print("\n" + "="*70 + "\n")

# TEST 2: Program Generation (tests in-depth mode)
print("📝 TEST 2: Generate 3-day strength plan")
print("-" * 70)

response2 = get_ai_response(
    user_query="Give me a 3-day strength training plan for a beginner",
    mode="in-depth",
    user_profile={
        'goal': 'strength',
        'experience_level': 'beginner',
        'injuries': []
    }
)

print("RESPONSE:")
print(response2)
print("\n" + "="*70 + "\n")

# TEST 3: Basketball Training (tests sport-specific RAG)
print("📝 TEST 3: Basketball training recommendations")
print("-" * 70)

response3 = get_ai_response(
    user_query="What exercises should I do for basketball?",
    mode="in-depth",
    user_profile={
        'goal': 'athletic performance',
        'sport': 'basketball',
        'injuries': ['ankle sprain history']
    }
)

print("RESPONSE:")
print(response3)
print("\n" + "="*70 + "\n")

print("✅ ALL TESTS COMPLETE!")
