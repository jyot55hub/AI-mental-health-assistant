from app.backend.database import get_connection
from app.backend.auth import register_user


TEST_EMAIL = "mindcare_backend_test@example.com"
TEST_NAME = "MindCare Backend Test User"
TEST_PASSWORD = "TestPassword123!"


def get_test_user_id():
    """
    Get the dedicated backend test user's actual database ID.

    If the test user does not exist, create it first.

    This avoids hardcoding a user ID such as 1 or 5,
    so backend tests remain safe even when the database
    contains many real users.
    """

    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT id
            FROM users
            WHERE email = ?
            """,
            (TEST_EMAIL,)
        )

        row = cursor.fetchone()

        if row:
            return row[0]

    finally:
        connection.close()

    # Test user does not exist, so create it.
    result = register_user(
        name=TEST_NAME,
        email=TEST_EMAIL,
        password=TEST_PASSWORD
    )

    if not result.get("success"):
        raise RuntimeError(
            "Unable to create backend test user: "
            + result.get("message", "Unknown error")
        )

    return result["user_id"]