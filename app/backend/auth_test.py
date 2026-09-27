from app.backend.auth import register_user, login_user
from app.backend.test_utils import (
    get_test_user_id,
    TEST_EMAIL,
    TEST_PASSWORD,
    TEST_NAME
)


print("=" * 60)
print("AUTHENTICATION BACKEND TEST")
print("=" * 60)


# ============================================================
# GET DEDICATED TEST USER
# ============================================================

print("\n" + "=" * 60)
print("GET TEST USER")
print("=" * 60)

test_user_id = get_test_user_id()

print({
    "success": True,
    "message": "Dedicated test user found.",
    "user_id": test_user_id,
    "email": TEST_EMAIL
})


# ============================================================
# DUPLICATE EMAIL REGISTRATION TEST
# ============================================================

print("\n" + "=" * 60)
print("DUPLICATE EMAIL REGISTRATION TEST")
print("=" * 60)

duplicate_registration_result = register_user(
    name=TEST_NAME,
    email=TEST_EMAIL,
    password=TEST_PASSWORD
)

print(duplicate_registration_result)


# ============================================================
# USER LOGIN TEST
# ============================================================

print("\n" + "=" * 60)
print("USER LOGIN TEST")
print("=" * 60)

login_result = login_user(
    email=TEST_EMAIL,
    password=TEST_PASSWORD
)

print(login_result)