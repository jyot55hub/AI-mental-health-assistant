from app.backend.questionnaire import (
    save_questionnaire_response,
    get_questionnaire_response,
    get_questionnaire_history,
    update_questionnaire_response,
    delete_questionnaire_response
)


# ============================================================
# TEST USER
# ============================================================

USER_ID = 1

# Use a fixed test date so the test is predictable.
TEST_DATE = "2026-09-08"


# ============================================================
# SAVE QUESTIONNAIRE RESPONSE TEST
# ============================================================

print("\n" + "=" * 60)
print("SAVE QUESTIONNAIRE RESPONSE TEST")
print("=" * 60)

result = save_questionnaire_response(
    user_id=USER_ID,
    mood=4,
    stress_level=3,
    energy_level=4,
    physical_activity=3,
    focus=4,
    social_connection=3,
    self_care=4,
    record_date=TEST_DATE
)

print(result)


# ============================================================
# GET QUESTIONNAIRE RESPONSE
# ============================================================

print("\n" + "=" * 60)
print("GET QUESTIONNAIRE RESPONSE")
print("=" * 60)

result = get_questionnaire_response(
    user_id=USER_ID,
    record_date=TEST_DATE
)

print(result)


# ============================================================
# GET QUESTIONNAIRE HISTORY
# ============================================================

print("\n" + "=" * 60)
print("GET QUESTIONNAIRE HISTORY")
print("=" * 60)

result = get_questionnaire_history(
    user_id=USER_ID
)

print(result)


# ============================================================
# UPDATE QUESTIONNAIRE RESPONSE TEST
# ============================================================

print("\n" + "=" * 60)
print("UPDATE QUESTIONNAIRE RESPONSE TEST")
print("=" * 60)

result = update_questionnaire_response(
    user_id=USER_ID,
    mood=5,
    stress_level=4,
    energy_level=5,
    physical_activity=4,
    focus=5,
    social_connection=4,
    self_care=5,
    record_date=TEST_DATE
)

print(result)


# ============================================================
# VERIFY UPDATED QUESTIONNAIRE RESPONSE
# ============================================================

print("\n" + "=" * 60)
print("VERIFY UPDATED QUESTIONNAIRE RESPONSE")
print("=" * 60)

result = get_questionnaire_response(
    user_id=USER_ID,
    record_date=TEST_DATE
)

print(result)


# ============================================================
# DELETE QUESTIONNAIRE RESPONSE TEST
# ============================================================

print("\n" + "=" * 60)
print("DELETE QUESTIONNAIRE RESPONSE TEST")
print("=" * 60)

result = delete_questionnaire_response(
    user_id=USER_ID,
    record_date=TEST_DATE
)

print(result)


# ============================================================
# VERIFY DELETED QUESTIONNAIRE RESPONSE
# ============================================================

print("\n" + "=" * 60)
print("VERIFY DELETED QUESTIONNAIRE RESPONSE")
print("=" * 60)

result = get_questionnaire_response(
    user_id=USER_ID,
    record_date=TEST_DATE
)

print(result)


print("\n" + "=" * 60)
print("QUESTIONNAIRE BACKEND TEST COMPLETED")
print("=" * 60)