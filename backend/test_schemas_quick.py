from app.schemas import UserQuery, AIResponse, ChatMode, RiskScoreItem, YouTubeLinkItem
from pydantic import ValidationError

print("=" * 50)
print("TESTING SCHEMAS.PY")
print("=" * 50)

# Test 1: Valid UserQuery
print("\n✅ Test 1: Valid UserQuery")
try:
    query = UserQuery(
        text="Give me a workout plan",
        user_id="user123",
        mode="in-depth"
    )
    print(f"SUCCESS: {query.model_dump()}")
except Exception as e:
    print(f"FAILED: {e}")

# Test 2: Invalid ChatMode
print("\n❌ Test 2: Invalid ChatMode (should fail)")
try:
    bad_query = UserQuery(
        text="Hello",
        user_id="user123",
        mode="medium-tip"  # Wrong mode!
    )
    print(f"FAILED: Should have rejected invalid mode")
except ValidationError as e:
    print(f"SUCCESS: Correctly rejected - {e.errors()[0]['msg']}")

# Test 3: Empty text field
print("\n❌ Test 3: Empty text (should fail)")
try:
    bad_query = UserQuery(
        text="",
        user_id="user123",
        mode="quick-tip"
    )
    print(f"FAILED: Should have rejected empty text")
except ValidationError as e:
    print(f"SUCCESS: Correctly rejected - {e.errors()[0]['msg']}")

# Test 4: Valid AIResponse
print("\n✅ Test 4: Valid AIResponse")
try:
    response = AIResponse(
        response_text="Here's your plan...",
        risk_scores=[
            RiskScoreItem(exercise="Deadlift", risk=7, effectiveness=9)
        ],
        youtube_links=[
            YouTubeLinkItem(exercise="Deadlift", url="https://youtube.com/watch?v=abc")
        ]
    )
    print(f"SUCCESS: {response.model_dump()}")
except Exception as e:
    print(f"FAILED: {e}")

# Test 5: Invalid URL
print("\n❌ Test 5: Invalid URL (should fail)")
try:
    bad_response = AIResponse(
        response_text="Plan...",
        youtube_links=[
            YouTubeLinkItem(exercise="Squat", url="not-a-url")
        ]
    )
    print(f"FAILED: Should have rejected invalid URL")
except ValidationError as e:
    print(f"SUCCESS: Correctly rejected - {e.errors()[0]['msg']}")

# Test 6: Risk score out of range
print("\n❌ Test 6: Risk score > 10 (should fail)")
try:
    bad_item = RiskScoreItem(exercise="Squat", risk=15, effectiveness=9)
    print(f"FAILED: Should have rejected risk > 10")
except ValidationError as e:
    print(f"SUCCESS: Correctly rejected - {e.errors()[0]['msg']}")

# Test 7: Enum usage in code
print("\n✅ Test 7: Using ChatMode enum")
print(f"Available modes: {[mode.value for mode in ChatMode]}")
print(f"Quick tip mode: {ChatMode.QUICK_TIP}")
print(f"In-depth mode: {ChatMode.IN_DEPTH}")

print("\n" + "=" * 50)
print("ALL TESTS COMPLETED")
print("=" * 50)
