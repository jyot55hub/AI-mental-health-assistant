from app.backend.database import get_connection


# ============================================================
# SAVE CHAT MESSAGE
# ============================================================

def save_chat_message(user_id, user_message, ai_response):
    """
    Save a user's message and the AI response to chat history.
    """

    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            INSERT INTO chat_history (
                user_id,
                user_message,
                ai_response
            )
            VALUES (?, ?, ?)
            """,
            (
                user_id,
                user_message,
                ai_response
            )
        )

        connection.commit()

        return {
            "success": True,
            "message": "Chat message saved successfully.",
            "chat_id": cursor.lastrowid
        }

    except Exception as error:

        return {
            "success": False,
            "message": f"Failed to save chat message: {error}"
        }

    finally:
        connection.close()


# ============================================================
# GET CHAT HISTORY
# ============================================================

def get_chat_history(user_id, limit=50):
    """
    Retrieve chat history for a specific user.
    """

    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            SELECT
                id,
                user_id,
                user_message,
                ai_response,
                created_at

            FROM chat_history

            WHERE user_id = ?

            ORDER BY created_at ASC, id ASC

            LIMIT ?
            """,
            (
                user_id,
                limit
            )
        )

        rows = cursor.fetchall()

        chat_history = []

        for row in rows:
            chat_history.append(
                {
                    "id": row["id"],
                    "user_id": row["user_id"],
                    "user_message": row["user_message"],
                    "ai_response": row["ai_response"],
                    "created_at": row["created_at"]
                }
            )

        return {
            "success": True,
            "history": chat_history
        }

    except Exception as error:

        return {
            "success": False,
            "message": f"Failed to retrieve chat history: {error}"
        }

    finally:
        connection.close()

def delete_chat_history(user_id: int):
    """
    Delete all chat history for a specific user.
    """

    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            DELETE FROM chat_history
            WHERE user_id = ?
            """,
            (user_id,)
        )

        deleted_count = cursor.rowcount

        connection.commit()

        return {
            "success": True,
            "message": "Chat history deleted successfully.",
            "user_id": user_id,
            "deleted_messages": deleted_count
        }

    except Exception as error:

        return {
            "success": False,
            "message": f"Failed to delete chat history: {error}"
        }

    finally:
        connection.close()