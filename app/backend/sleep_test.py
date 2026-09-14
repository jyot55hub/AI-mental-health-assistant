from app.backend.sleep import (
    save_sleep_record,
    get_sleep_record,
    get_sleep_history,
    update_sleep_record,
    delete_sleep_record
)


USER_ID = 1


print("=" * 60)
print("SAVE SLEEP RECORD TEST")
print("=" * 60)

result = save_sleep_record(
    user_id=USER_ID,
    sleep_hours=7.5
)

print(result)


print("\n" + "=" * 60)
print("GET TODAY'S SLEEP RECORD")
print("=" * 60)

result = get_sleep_record(
    user_id=USER_ID
)

print(result)


print("\n" + "=" * 60)
print("GET SLEEP HISTORY")
print("=" * 60)

result = get_sleep_history(
    user_id=USER_ID,
    limit=7
)

print(result)

print("\n" + "=" * 60)
print("SLEEP HISTORY TEST")
print("=" * 60)

history_result = get_sleep_history(
    user_id=USER_ID,
    limit=7
)

print(history_result)

print("\n" + "=" * 60)
print("UPDATE SLEEP RECORD TEST")
print("=" * 60)

update_result = update_sleep_record(
    user_id=USER_ID,
    record_date="2026-09-04",
    sleep_hours=8.0
)

print(update_result)

print("\n" + "=" * 60)
print("VERIFY UPDATED RECORD")
print("=" * 60)

updated_record = get_sleep_record(
    user_id=USER_ID
)

print(updated_record)

print("\n" + "=" * 60)
print("DELETE SLEEP RECORD TEST")
print("=" * 60)

result = delete_sleep_record(
    user_id=USER_ID,
    record_date="2026-09-04"
)

print(result)