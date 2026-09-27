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
# ============================================================
# CHANGE USER PASSWORD
# ============================================================

def change_user_password(
    user_id: int,
    current_password: str,
    new_password: str
):
    """
    Change the password of an authenticated user.

    The current password must be verified before the new
    password is stored.
    """

    if not user_id:
        return {
            "success": False,
            "message": "User ID is required."
        }

    if not current_password:
        return {
            "success": False,
            "message": "Current password is required."
        }

    if not new_password:
        return {
            "success": False,
            "message": "New password is required."
        }

    if len(new_password) < 6:
        return {
            "success": False,
            "message": "New password must contain at least 6 characters."
        }

    connection = get_connection()
    cursor = connection.cursor()

    try:

        # ----------------------------------------------------
        # Get the user's current password hash
        # ----------------------------------------------------

        cursor.execute(
            """
            SELECT password_hash
            FROM users
            WHERE id = ?
            """,
            (user_id,)
        )

        user = cursor.fetchone()

        if user is None:
            return {
                "success": False,
                "message": "User account not found."
            }

        # ----------------------------------------------------
        # Verify the current password
        # ----------------------------------------------------

        password_is_correct = verify_password(
            current_password,
            user["password_hash"]
        )

        if not password_is_correct:
            return {
                "success": False,
                "message": "Current password is incorrect."
            }

        # ----------------------------------------------------
        # Prevent reusing the same password
        # ----------------------------------------------------

        if verify_password(
            new_password,
            user["password_hash"]
        ):
            return {
                "success": False,
                "message": "New password must be different from your current password."
            }

        # ----------------------------------------------------
        # Hash the new password
        # ----------------------------------------------------

        new_password_hash = hash_password(
            new_password
        )

        # ----------------------------------------------------
        # Update the password
        # ----------------------------------------------------

        cursor.execute(
            """
            UPDATE users
            SET password_hash = ?
            WHERE id = ?
            """,
            (
                new_password_hash,
                user_id
            )
        )

        if cursor.rowcount == 0:
            connection.rollback()

            return {
                "success": False,
                "message": "Unable to update the password."
            }

        # ----------------------------------------------------
        # Save the new password
        # ----------------------------------------------------

        connection.commit()

        return {
            "success": True,
            "message": "Password changed successfully."
        }

    except Exception as error:

        connection.rollback()

        return {
            "success": False,
            "message": f"Password change failed: {error}"
        }

    finally:

        connection.close()

# ============================================================
# GET USER REGISTRATION DATE
# ============================================================

def get_user_registration_date(user_id: int):
    """
    Get the date on which the user registered.

    Returns:
        Registration date as YYYY-MM-DD string,
        or None if the user does not exist.
    """

    if not user_id:
        return None

    connection = get_connection()
    cursor = connection.cursor()

    try:

        cursor.execute(
            """
            SELECT created_at
            FROM users
            WHERE id = ?
            """,
            (user_id,)
        )

        user = cursor.fetchone()

        if user is None:
            return None

        created_at = user["created_at"]

        if created_at is None:
            return None

        return str(created_at)[:10]

    finally:

        connection.close()


# ============================================================
# CHECK USERNAME AVAILABILITY
# ============================================================

def is_username_available(
    username: str,
    current_user_id=None
):
    """
    Check whether a username is available.

    The current user's existing username can remain unchanged.
    """

    username = username.strip().lower()

    if not username:
        return False

    connection = get_connection()
    cursor = connection.cursor()

    try:

        if current_user_id:

            cursor.execute(
                """
                SELECT id
                FROM users
                WHERE LOWER(username) = ?
                  AND id != ?
                LIMIT 1
                """,
                (
                    username,
                    current_user_id
                )
            )

        else:

            cursor.execute(
                """
                SELECT id
                FROM users
                WHERE LOWER(username) = ?
                LIMIT 1
                """,
                (username,)
            )

        existing_user = cursor.fetchone()

        return existing_user is None

    finally:

        connection.close()


# ============================================================
# GET USER PROFILE
# ============================================================

def get_user_profile(user_id: int):
    """
    Retrieve the profile information of a user.
    """

    if not user_id:

        return {
            "success": False,
            "message": "User ID is required."
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
                username,
                bio,
                avatar,
                created_at
            FROM users
            WHERE id = ?
            """,
            (user_id,)
        )

        user = cursor.fetchone()

        if user is None:

            return {
                "success": False,
                "message": "User profile not found."
            }

        return {
            "success": True,
            "profile": dict(user)
        }

    finally:

        connection.close()


# ============================================================
# UPDATE USER NAME
# ============================================================

def update_user_name(
    user_id: int,
    name: str
):
    """
    Update the user's display name.
    """

    if not user_id:

        return {
            "success": False,
            "message": "User ID is required."
        }

    name = name.strip()

    if not name:

        return {
            "success": False,
            "message": "Name cannot be empty."
        }

    connection = get_connection()
    cursor = connection.cursor()

    try:

        cursor.execute(
            """
            UPDATE users
            SET name = ?
            WHERE id = ?
            """,
            (
                name,
                user_id
            )
        )

        if cursor.rowcount == 0:

            return {
                "success": False,
                "message": "User not found."
            }

        connection.commit()

        return {
            "success": True,
            "message": "Name updated successfully."
        }

    finally:

        connection.close()


# ============================================================
# UPDATE USERNAME
# ============================================================

def update_username(
    user_id: int,
    username: str
):
    """
    Update the user's username.
    """

    if not user_id:

        return {
            "success": False,
            "message": "User ID is required."
        }

    username = username.strip().lower()

    if not username:

        return {
            "success": False,
            "message": "Username cannot be empty."
        }

    if len(username) < 3:

        return {
            "success": False,
            "message": "Username must contain at least 3 characters."
        }

    if len(username) > 30:

        return {
            "success": False,
            "message": "Username must contain at most 30 characters."
        }

    # Allow letters, numbers, underscore and dot.
    allowed_characters = (
        "abcdefghijklmnopqrstuvwxyz"
        "0123456789"
        "_."
    )

    if any(
        character not in allowed_characters
        for character in username
    ):

        return {
            "success": False,
            "message": (
                "Username can contain only letters, "
                "numbers, underscores and dots."
            )
        }

    if not is_username_available(
        username,
        current_user_id=user_id
    ):

        return {
            "success": False,
            "message": "This username is already taken."
        }

    connection = get_connection()
    cursor = connection.cursor()

    try:

        cursor.execute(
            """
            UPDATE users
            SET username = ?
            WHERE id = ?
            """,
            (
                username,
                user_id
            )
        )

        if cursor.rowcount == 0:

            return {
                "success": False,
                "message": "User not found."
            }

        connection.commit()

        return {
            "success": True,
            "message": "Username updated successfully."
        }

    finally:

        connection.close()


# ============================================================
# UPDATE USER BIO
# ============================================================

def update_user_bio(
    user_id: int,
    bio: str
):
    """
    Update the user's profile bio.
    """

    if not user_id:

        return {
            "success": False,
            "message": "User ID is required."
        }

    bio = bio.strip()

    if len(bio) > 300:

        return {
            "success": False,
            "message": "Bio must contain at most 300 characters."
        }

    connection = get_connection()
    cursor = connection.cursor()

    try:

        cursor.execute(
            """
            UPDATE users
            SET bio = ?
            WHERE id = ?
            """,
            (
                bio,
                user_id
            )
        )

        if cursor.rowcount == 0:

            return {
                "success": False,
                "message": "User not found."
            }

        connection.commit()

        return {
            "success": True,
            "message": "Bio updated successfully."
        }

    finally:

        connection.close()


# ============================================================
# UPDATE USER AVATAR
# ============================================================

def update_user_avatar(
    user_id: int,
    avatar: str
):
    """
    Update the user's selected avatar.
    """

    if not user_id:

        return {
            "success": False,
            "message": "User ID is required."
        }

    avatar = avatar.strip()

    if not avatar:

        return {
            "success": False,
            "message": "Avatar is required."
        }

    connection = get_connection()
    cursor = connection.cursor()

    try:

        cursor.execute(
            """
            UPDATE users
            SET avatar = ?
            WHERE id = ?
            """,
            (
                avatar,
                user_id
            )
        )

        if cursor.rowcount == 0:

            return {
                "success": False,
                "message": "User not found."
            }

        connection.commit()

        return {
            "success": True,
            "message": "Avatar updated successfully."
        }

    finally:

        connection.close()
# ============================================================
# DELETE USER ACCOUNT
# ============================================================

def delete_user_account(user_id: int):
    """
    Permanently delete a user's account.

    Because the related tables use ON DELETE CASCADE,
    the user's associated records are also deleted.
    """

    if not user_id:
        return {
            "success": False,
            "message": "User ID is required."
        }

    connection = get_connection()
    cursor = connection.cursor()

    try:

        # ----------------------------------------------------
        # Check whether the user exists
        # ----------------------------------------------------

        cursor.execute(
            """
            SELECT id
            FROM users
            WHERE id = ?
            """,
            (user_id,)
        )

        user = cursor.fetchone()

        if user is None:
            return {
                "success": False,
                "message": "User account not found."
            }

        # ----------------------------------------------------
        # Delete the user
        # ----------------------------------------------------
        #
        # SQLite foreign-key cascading will automatically
        # remove related records belonging to this user.
        #

        cursor.execute(
            """
            DELETE FROM users
            WHERE id = ?
            """,
            (user_id,)
        )

        if cursor.rowcount == 0:
            connection.rollback()

            return {
                "success": False,
                "message": "Unable to delete the user account."
            }

        # ----------------------------------------------------
        # Save deletion
        # ----------------------------------------------------

        connection.commit()

        return {
            "success": True,
            "message": "Account deleted successfully."
        }

    except Exception as error:

        connection.rollback()

        return {
            "success": False,
            "message": f"Account deletion failed: {error}"
        }

    finally:

        connection.close()