from app.backend.database import get_connection


# ============================================================
# CREATE JOURNAL ENTRY
# ============================================================

def create_journal_entry(user_id, title, content):
    """
    Create a new journal entry for a user.
    """

    if not user_id:
        return {
            "success": False,
            "message": "User ID is required."
        }

    title = (title or "").strip()
    content = (content or "").strip()

    if not title:
        return {
            "success": False,
            "message": "Journal title is required."
        }

    if not content:
        return {
            "success": False,
            "message": "Journal content is required."
        }

    connection = get_connection()
    cursor = connection.cursor()

    try:

        cursor.execute(
            """
            INSERT INTO journal_entries (
                user_id,
                title,
                content
            )
            VALUES (?, ?, ?)
            """,
            (
                user_id,
                title,
                content
            )
        )

        connection.commit()

        journal_id = cursor.lastrowid

        return {
            "success": True,
            "message": "Journal entry created successfully.",
            "journal_id": journal_id
        }

    except Exception as error:

        connection.rollback()

        return {
            "success": False,
            "message": f"Unable to create journal entry: {error}"
        }

    finally:

        connection.close()


# ============================================================
# GET ALL JOURNAL ENTRIES
# ============================================================

def get_journal_entries(user_id):
    """
    Get all journal entries belonging to the specified user.

    Newest/most recently updated entries are returned first.
    """

    if not user_id:
        return {
            "success": False,
            "message": "User ID is required.",
            "entries": []
        }

    connection = get_connection()
    cursor = connection.cursor()

    try:

        cursor.execute(
            """
            SELECT
                id,
                user_id,
                title,
                content,
                created_at,
                updated_at
            FROM journal_entries
            WHERE user_id = ?
            ORDER BY updated_at DESC, id DESC
            """,
            (user_id,)
        )

        rows = cursor.fetchall()

        entries = [
            dict(row)
            for row in rows
        ]

        return {
            "success": True,
            "entries": entries
        }

    except Exception as error:

        return {
            "success": False,
            "message": f"Unable to load journal entries: {error}",
            "entries": []
        }

    finally:

        connection.close()


# ============================================================
# GET ONE JOURNAL ENTRY
# ============================================================

def get_journal_entry(user_id, journal_id):
    """
    Get one journal entry belonging to the specified user.

    The user_id condition is important because it prevents
    one user from accessing another user's journal entry.
    """

    if not user_id:
        return {
            "success": False,
            "message": "User ID is required."
        }

    if not journal_id:
        return {
            "success": False,
            "message": "Journal entry ID is required."
        }

    connection = get_connection()
    cursor = connection.cursor()

    try:

        cursor.execute(
            """
            SELECT
                id,
                user_id,
                title,
                content,
                created_at,
                updated_at
            FROM journal_entries
            WHERE id = ?
              AND user_id = ?
            LIMIT 1
            """,
            (
                journal_id,
                user_id
            )
        )

        row = cursor.fetchone()

        if row is None:

            return {
                "success": False,
                "message": "Journal entry not found."
            }

        return {
            "success": True,
            "entry": dict(row)
        }

    except Exception as error:

        return {
            "success": False,
            "message": f"Unable to load journal entry: {error}"
        }

    finally:

        connection.close()


# ============================================================
# UPDATE JOURNAL ENTRY
# ============================================================

def update_journal_entry(
    user_id,
    journal_id,
    title,
    content
):
    """
    Update a journal entry belonging to the specified user.
    """

    if not user_id:
        return {
            "success": False,
            "message": "User ID is required."
        }

    if not journal_id:
        return {
            "success": False,
            "message": "Journal entry ID is required."
        }

    title = (title or "").strip()
    content = (content or "").strip()

    if not title:
        return {
            "success": False,
            "message": "Journal title is required."
        }

    if not content:
        return {
            "success": False,
            "message": "Journal content is required."
        }

    connection = get_connection()
    cursor = connection.cursor()

    try:

        # First make sure the entry belongs to this user.
        cursor.execute(
            """
            SELECT id
            FROM journal_entries
            WHERE id = ?
              AND user_id = ?
            LIMIT 1
            """,
            (
                journal_id,
                user_id
            )
        )

        existing_entry = cursor.fetchone()

        if existing_entry is None:

            return {
                "success": False,
                "message": "Journal entry not found."
            }

        cursor.execute(
            """
            UPDATE journal_entries
            SET
                title = ?,
                content = ?,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
              AND user_id = ?
            """,
            (
                title,
                content,
                journal_id,
                user_id
            )
        )

        connection.commit()

        return {
            "success": True,
            "message": "Journal entry updated successfully."
        }

    except Exception as error:

        connection.rollback()

        return {
            "success": False,
            "message": f"Unable to update journal entry: {error}"
        }

    finally:

        connection.close()


# ============================================================
# DELETE JOURNAL ENTRY
# ============================================================

def delete_journal_entry(user_id, journal_id):
    """
    Delete a journal entry belonging to the specified user.
    """

    if not user_id:
        return {
            "success": False,
            "message": "User ID is required."
        }

    if not journal_id:
        return {
            "success": False,
            "message": "Journal entry ID is required."
        }

    connection = get_connection()
    cursor = connection.cursor()

    try:

        # Make sure the entry belongs to this user.
        cursor.execute(
            """
            SELECT id
            FROM journal_entries
            WHERE id = ?
              AND user_id = ?
            LIMIT 1
            """,
            (
                journal_id,
                user_id
            )
        )

        existing_entry = cursor.fetchone()

        if existing_entry is None:

            return {
                "success": False,
                "message": "Journal entry not found."
            }

        cursor.execute(
            """
            DELETE FROM journal_entries
            WHERE id = ?
              AND user_id = ?
            """,
            (
                journal_id,
                user_id
            )
        )

        connection.commit()

        return {
            "success": True,
            "message": "Journal entry deleted successfully."
        }

    except Exception as error:

        connection.rollback()

        return {
            "success": False,
            "message": f"Unable to delete journal entry: {error}"
        }

    finally:

        connection.close()