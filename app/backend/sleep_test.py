from datetime import date

from app.backend.sleep import (
    save_sleep_record,
    get_sleep_record,
    get_sleep_history,
    update_sleep_record,
    delete_sleep_record,
)


USER_ID = 1
TODAY = date.today().isoformat()


print("=" * 60)
print("SAVE SLEEP RECORD TEST")
print("=" * 60)

result = save_sleep_record(
    user_id=USER_ID,
    sleep_hours=7.5,
)

print(result)


print("\n" + "=" * 60)
print("GET TODAY'S SLEEP RECORD")
print("=" * 60)

result = get_sleep_record(
    user_id=USER_ID,
)

print(result)


print("\n" + "=" * 60)
print("GET SLEEP HISTORY")
print("=" * 60)

result = get_sleep_history(
    user_id=USER_ID,
    limit=7,
)

print(result)


print("\n" + "=" * 60)
print("UPDATE SLEEP RECORD TEST")
print("=" * 60)

update_result = update_sleep_record(
    user_id=USER_ID,
    record_date=TODAY,
    sleep_hours=8.0,
)

print(update_result)


print("\n" + "=" * 60)
print("VERIFY UPDATED RECORD")
print("=" * 60)

updated_record = get_sleep_record(
    user_id=USER_ID,
)

print(updated_record)


print("\n" + "=" * 60)
print("DELETE SLEEP RECORD TEST")
print("=" * 60)

delete_result = delete_sleep_record(
    user_id=USER_ID,
    record_date=TODAY,
)

print(delete_result)