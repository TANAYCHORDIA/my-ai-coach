# backend/test_risk.py

from app.risk_module import RiskAssessmentEngine, calculate_risk

print("=" * 60)
print("🧪 TESTING RISK MODULE")
print("=" * 60)

# Test 1: Simple risk calculation
print("\n📝 TEST 1: Deadlift with back pain")
result = calculate_risk("deadlift", "lower back pain")
print(f"Risk: {result['risk']}/10")
print(f"Effectiveness: {result['effectiveness']}/10")

# Test 2: Advanced assessment
print("\n📝 TEST 2: Squat for strength goal with knee injury")
user_profile = {
    'goal': 'strength',
    'injuries': ['knee injury']
}
result = RiskAssessmentEngine.assess_exercise("squat", user_profile)
print(f"Exercise: {result['exercise']}")
print(f"Risk: {result['risk']}/10")
print(f"Effectiveness: {result['effectiveness']}/10")
print(f"Reason: {result['reason']}")

# Test 3: Safe exercise
print("\n📝 TEST 3: Swimming for fat loss, no injuries")
user_profile = {
    'goal': 'fat loss',
    'injuries': []
}
result = RiskAssessmentEngine.assess_exercise("swimming", user_profile)
print(f"Exercise: {result['exercise']}")
print(f"Risk: {result['risk']}/10")
print(f"Effectiveness: {result['effectiveness']}/10")
print(f"Reason: {result['reason']}")

print("\n" + "=" * 60)
print("✅ ALL RISK MODULE TESTS COMPLETE!")
print("=" * 60)
