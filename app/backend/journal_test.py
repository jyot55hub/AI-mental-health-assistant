from app.backend.database import get_connection, initialize_database
from app.backend.journal import (
    create_journal_entry,
    get_journal_entries,
    get_journal_entry,
    update_journal_entry,
    delete_journal_entry
)


# ============================================================
# TEST USER
# ============================================================

TEST_USER_ID = 4


# ============================================================
# DATABASE SETUP
# ============================================================

initialize_database()


# ============================================================
# CLEAN OLD TEST ENTRIES
# ============================================================

connection = get_connection()
cursor = connection.cursor()

cursor.execute(
    """
    DELETE FROM journal_entries
    WHERE user_id = ?
    """,
    (TEST_USER_ID,)
)

connection.commit()
connection.close()


print("\n" + "=" * 60)
print("MINDCARE JOURNAL BACKEND TEST")
print("=" * 60)


# ============================================================
# 1. CREATE
# ============================================================

print("\n1. CREATE JOURNAL ENTRY")
print("-" * 60)

create_result = create_journal_entry(
    user_id=TEST_USER_ID,
    title="My First Journal Entry",
    content=(
        "Today I started using the MindCare journal. "
        "This is my first saved thought."
    )
)

print(create_result)

assert create_result["success"] is True

journal_id = create_result["journal_id"]

print("✓ Create test passed")


# ============================================================
# 2. GET ALL ENTRIES
# ============================================================

print("\n2. GET JOURNAL ENTRIES")
print("-" * 60)

list_result = get_journal_entries(
    TEST_USER_ID
)

print(list_result)

assert list_result["success"] is True
assert len(list_result["entries"]) == 1
assert list_result["entries"][0]["id"] == journal_id

print("✓ Get entries test passed")


# ============================================================
# 3. GET ONE ENTRY
# ============================================================

print("\n3. GET SINGLE JOURNAL ENTRY")
print("-" * 60)

single_result = get_journal_entry(
    user_id=TEST_USER_ID,
    journal_id=journal_id
)

print(single_result)

assert single_result["success"] is True
assert single_result["entry"]["id"] == journal_id
assert single_result["entry"]["title"] == (
    "My First Journal Entry"
)

print("✓ Get single entry test passed")


# ============================================================
# 4. UPDATE
# ============================================================

print("\n4. UPDATE JOURNAL ENTRY")
print("-" * 60)

update_result = update_journal_entry(
    user_id=TEST_USER_ID,
    journal_id=journal_id,
    title="My Updated Journal Entry",
    content=(
        "I updated this journal entry successfully. "
        "The changes should remain saved in the database."
    )
)

print(update_result)

assert update_result["success"] is True

updated_result = get_journal_entry(
    user_id=TEST_USER_ID,
    journal_id=journal_id
)

print(updated_result)

assert updated_result["success"] is True
assert updated_result["entry"]["title"] == (
    "My Updated Journal Entry"
)

print("✓ Update test passed")


# ============================================================
# 5. USER ISOLATION
# ============================================================

print("\n5. USER ISOLATION TEST")
print("-" * 60)

# User 999 should NOT be able to access
# User 1's journal entry.

other_user_result = get_journal_entry(
    user_id=999,
    journal_id=journal_id
)

print(other_user_result)

assert other_user_result["success"] is False

print("✓ User isolation test passed")


# ============================================================
# 6. DELETE
# ============================================================

print("\n6. DELETE JOURNAL ENTRY")
print("-" * 60)

delete_result = delete_journal_entry(
    user_id=TEST_USER_ID,
    journal_id=journal_id
)

print(delete_result)

assert delete_result["success"] is True

deleted_result = get_journal_entry(
    user_id=TEST_USER_ID,
    journal_id=journal_id
)

print(deleted_result)

assert deleted_result["success"] is False

print("✓ Delete test passed")


# ============================================================
# FINAL RESULT
# ============================================================

print("\n" + "=" * 60)
print("✓ ALL JOURNAL BACKEND TESTS PASSED")
print("=" * 60)