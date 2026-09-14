from app.backend.auth import register_user, login_user


print("=" * 60)
print("USER REGISTRATION TEST")
print("=" * 60)

registration_result = register_user(
    name="Test User",
    email="testuser@example.com",
    password="testpassword123"
)

print(registration_result)


print("\n" + "=" * 60)
print("USER LOGIN TEST")
print("=" * 60)

login_result = login_user(
    email="testuser@example.com",
    password="testpassword123"
)

print(login_result)