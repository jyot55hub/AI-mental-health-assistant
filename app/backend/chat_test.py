from app.backend.chat import (
    save_chat_message,
    get_chat_history,
    delete_chat_history
)
from app.backend.test_utils import get_test_user_id

# ============================================================
# TEST USER
# ============================================================

USER_ID = get_test_user_id()


# ============================================================
# SAVE FIRST CHAT MESSAGE
# ============================================================

print("\n" + "=" * 60)
print("SAVE FIRST CHAT MESSAGE TEST")
print("=" * 60)

result = save_chat_message(
    user_id=USER_ID,
    user_message="I am feeling stressed about my exams.",
    ai_response="It is understandable to feel stressed during exams. Try taking short breaks and focusing on one task at a time."
)

print(result)


# ============================================================
# SAVE SECOND CHAT MESSAGE
# ============================================================

print("\n" + "=" * 60)
print("SAVE SECOND CHAT MESSAGE TEST")
print("=" * 60)

result = save_chat_message(
    user_id=USER_ID,
    user_message="I am having trouble sleeping.",
    ai_response="Try maintaining a regular sleep schedule and reducing screen time before bed."
)

print(result)


# ============================================================
# GET CHAT HISTORY
# ============================================================

print("\n" + "=" * 60)
print("GET CHAT HISTORY TEST")
print("=" * 60)

result = get_chat_history(
    user_id=USER_ID
)

print(result)

print("\n" + "=" * 60)
print("DELETE CHAT HISTORY TEST")
print("=" * 60)

result = delete_chat_history(
    user_id=USER_ID
)

print(result)

print("\n" + "=" * 60)
print("VERIFY DELETED CHAT HISTORY")
print("=" * 60)

result = get_chat_history(
    user_id=USER_ID
)

print(result)