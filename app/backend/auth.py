import bcrypt

from app.backend.database import get_connection


# ============================================================
# PASSWORD FUNCTIONS
# ============================================================

def hash_password(password: str) -> str:
    """
    Convert a plain-text password into a secure password hash.
    """

    password_bytes = password.encode("utf-8")

    hashed_password = bcrypt.hashpw(
        password_bytes,
        bcrypt.gensalt()
    )

    return hashed_password.decode("utf-8")


def verify_password(password: str, password_hash: str) -> bool:
    """
    Check whether a password matches its stored hash.
    """

    return bcrypt.checkpw(
        password.encode("utf-8"),
        password_hash.encode("utf-8")
    )


# ============================================================
# USER REGISTRATION
# ============================================================

def register_user(
    name: str,
    email: str,
    password: str
):
    """
    Register a new user.
    """

    # Basic validation
    name = name.strip()
    email = email.strip().lower()

    if not name:
        return {
            "success": False,
            "message": "Name is required."
        }

    if not email:
        return {
            "success": False,
            "message": "Email is required."
        }

    if len(password) < 6:
        return {
            "success": False,
            "message": "Password must contain at least 6 characters."
        }

    connection = get_connection()
    cursor = connection.cursor()

    try:

        password_hash = hash_password(password)

        cursor.execute(
            """
            INSERT INTO users (
                name,
                email,
                password_hash
            )
            VALUES (?, ?, ?)
            """,
            (
                name,
                email,
                password_hash
            )
        )

        connection.commit()

        user_id = cursor.lastrowid

        return {
            "success": True,
            "message": "Registration successful.",
            "user_id": user_id
        }

    except Exception as error:

        connection.rollback()

        # Check duplicate email
        if "UNIQUE constraint failed" in str(error):

            return {
                "success": False,
                "message": "An account with this email already exists."
            }

        return {
            "success": False,
            "message": f"Registration failed: {error}"
        }

    finally:

        connection.close()


# ============================================================
# USER LOGIN
# ============================================================

def login_user(
    email: str,
    password: str
):
    """
    Authenticate a user using email and password.
    """

    email = email.strip().lower()

    if not email or not password:

        return {
            "success": False,
            "message": "Email and password are required."
        }

    connection = get_connection()

    cursor = connection.cursor()

    try:

        cursor.execute(
            """
            SELECT
                id,
                name,
                email,
                password_hash
            FROM users
            WHERE email = ?
            """,
            (email,)
        )

        user = cursor.fetchone()

        if user is None:

            return {
                "success": False,
                "message": "Invalid email or password."
            }

        password_is_correct = verify_password(
            password,
            user["password_hash"]
        )

        if not password_is_correct:

            return {
                "success": False,
                "message": "Invalid email or password."
            }

        return {
            "success": True,
            "message": "Login successful.",
            "user": {
                "id": user["id"],
                "name": user["name"],
                "email": user["email"]
            }
        }

    finally:

        connection.close()