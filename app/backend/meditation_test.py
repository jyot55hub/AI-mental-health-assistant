from app.backend.meditation import (
    save_meditation_record,
    get_meditation_record,
    get_meditation_history,
    update_meditation_record,
    delete_meditation_record
)
from app.backend.test_utils import get_test_user_id

# ============================================================
# TEST USER
# ============================================================

USER_ID = get_test_user_id()


# ============================================================
# SAVE MEDITATION RECORD TEST
# ============================================================

print("\n" + "=" * 60)
print("SAVE MEDITATION RECORD TEST")
print("=" * 60)

result = save_meditation_record(
    user_id=USER_ID,
    meditation_minutes=10
)

print(result)


# ============================================================
# GET TODAY'S MEDITATION RECORD
# ============================================================

print("\n" + "=" * 60)
print("GET TODAY'S MEDITATION RECORD")
print("=" * 60)

result = get_meditation_record(
    user_id=USER_ID
)

print(result)


# ============================================================
# GET MEDITATION HISTORY
# ============================================================

print("\n" + "=" * 60)
print("GET MEDITATION HISTORY")
print("=" * 60)

result = get_meditation_history(
    user_id=USER_ID
)

print(result)


# ============================================================
# UPDATE MEDITATION RECORD TEST
# ============================================================

print("\n" + "=" * 60)
print("UPDATE MEDITATION RECORD TEST")
print("=" * 60)

result = update_meditation_record(
    user_id=USER_ID,
    meditation_minutes=20
)

print(result)


# ============================================================
# VERIFY UPDATED RECORD
# ============================================================

print("\n" + "=" * 60)
print("VERIFY UPDATED MEDITATION RECORD")
print("=" * 60)

result = get_meditation_record(
    user_id=USER_ID
)

print(result)


# ============================================================
# DELETE MEDITATION RECORD TEST
# ============================================================

print("\n" + "=" * 60)
print("DELETE MEDITATION RECORD TEST")
print("=" * 60)

result = delete_meditation_record(
    user_id=USER_ID
)

print(result)


# ============================================================
# VERIFY DELETED RECORD
# ============================================================

print("\n" + "=" * 60)
print("VERIFY DELETED MEDITATION RECORD")
print("=" * 60)

result = get_meditation_record(
    user_id=USER_ID
)

print(result)