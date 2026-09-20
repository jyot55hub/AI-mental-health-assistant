from app.backend.database import get_connection


# ============================================================
# CREATE CONVERSATION
# ============================================================

def create_conversation(user_id, title="New Chat"):
    """
    Create a new conversation for a specific user.
    """

    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            INSERT INTO conversations (user_id, title)
            VALUES (?, ?)
            """,
            (user_id, title)
        )

        connection.commit()

        return {
            "success": True,
            "conversation_id": cursor.lastrowid,
            "title": title
        }

    except Exception as error:
        return {
            "success": False,
            "message": f"Failed to create conversation: {error}"
        }

    finally:
        connection.close()


# ============================================================
# GET USER CONVERSATIONS
# ============================================================

def get_user_conversations(user_id):
    """
    Retrieve all conversations belonging to a specific user.
    """

    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            SELECT
                id,
                user_id,
                title,
                created_at,
                updated_at
            FROM conversations
            WHERE user_id = ?
            ORDER BY updated_at DESC, id DESC
            """,
            (user_id,)
        )

        rows = cursor.fetchall()

        conversations = []

        for row in rows:
            conversations.append(
                {
                    "id": row["id"],
                    "user_id": row["user_id"],
                    "title": row["title"],
                    "created_at": row["created_at"],
                    "updated_at": row["updated_at"]
                }
            )

        return {
            "success": True,
            "conversations": conversations
        }

    except Exception as error:
        return {
            "success": False,
            "message": f"Failed to retrieve conversations: {error}"
        }

    finally:
        connection.close()


# ============================================================
# SAVE CHAT MESSAGE
# ============================================================

def save_chat_message(user_id, user_message, ai_response, conversation_id=None):
    """
    Save a user's message and the AI response.

    If conversation_id is provided, the message is saved
    inside that conversation.
    """

    connection = get_connection()
    cursor = connection.cursor()

    try:
        if conversation_id is None:
            conversation_result = create_conversation(
                user_id,
                "New Chat"
            )

            if not conversation_result["success"]:
                return conversation_result

            conversation_id = conversation_result["conversation_id"]

        # Verify that the conversation belongs to this user
        cursor.execute(
            """
            SELECT id
            FROM conversations
            WHERE id = ? AND user_id = ?
            """,
            (conversation_id, user_id)
        )

        conversation = cursor.fetchone()

        if conversation is None:
            return {
                "success": False,
                "message": "Invalid conversation."
            }

        cursor.execute(
            """
            INSERT INTO chat_history (
                user_id,
                user_message,
                ai_response,
                conversation_id
            )
            VALUES (?, ?, ?, ?)
            """,
            (
                user_id,
                user_message,
                ai_response,
                conversation_id
            )
        )

        cursor.execute(
            """
            UPDATE conversations
            SET updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
            """,
            (conversation_id,)
        )

        connection.commit()

        return {
            "success": True,
            "message": "Chat message saved successfully.",
            "chat_id": cursor.lastrowid,
            "conversation_id": conversation_id
        }

    except Exception as error:
        return {
            "success": False,
            "message": f"Failed to save chat message: {error}"
        }

    finally:
        connection.close()


# ============================================================
# GET CHAT HISTORY FOR ONE CONVERSATION
# ============================================================

def get_chat_history(user_id, conversation_id=None, limit=100):
    """
    Retrieve chat history for one user conversation.
    """

    connection = get_connection()
    cursor = connection.cursor()

    try:
        if conversation_id is None:
            cursor.execute(
                """
                SELECT
                    id,
                    user_id,
                    user_message,
                    ai_response,
                    created_at,
                    conversation_id
                FROM chat_history
                WHERE user_id = ?
                ORDER BY created_at ASC, id ASC
                LIMIT ?
                """,
                (user_id, limit)
            )
        else:
            cursor.execute(
                """
                SELECT
                    id,
                    user_id,
                    user_message,
                    ai_response,
                    created_at,
                    conversation_id
                FROM chat_history
                WHERE user_id = ?
                  AND conversation_id = ?
                ORDER BY created_at ASC, id ASC
                LIMIT ?
                """,
                (user_id, conversation_id, limit)
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
                    "created_at": row["created_at"],
                    "conversation_id": row["conversation_id"]
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


# ============================================================
# UPDATE CONVERSATION TITLE
# ============================================================

def update_conversation_title(user_id, conversation_id, title):
    """
    Update the title of a user's conversation.
    """

    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            UPDATE conversations
            SET title = ?,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = ? AND user_id = ?
            """,
            (title, conversation_id, user_id)
        )

        connection.commit()

        return {
            "success": True,
            "message": "Conversation title updated successfully."
        }

    except Exception as error:
        return {
            "success": False,
            "message": f"Failed to update conversation title: {error}"
        }

    finally:
        connection.close()


# ============================================================
# DELETE ONE CONVERSATION
# ============================================================

def delete_conversation(user_id, conversation_id):
    """
    Delete one conversation and its messages.
    """

    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            DELETE FROM chat_history
            WHERE user_id = ? AND conversation_id = ?
            """,
            (user_id, conversation_id)
        )

        cursor.execute(
            """
            DELETE FROM conversations
            WHERE id = ? AND user_id = ?
            """,
            (conversation_id, user_id)
        )

        connection.commit()

        return {
            "success": True,
            "message": "Conversation deleted successfully."
        }

    except Exception as error:
        return {
            "success": False,
            "message": f"Failed to delete conversation: {error}"
        }

    finally:
        connection.close()


# ============================================================
# DELETE ALL CHAT HISTORY FOR A USER
# ============================================================

def delete_chat_history(user_id: int):
    """
    Delete all conversations and chat history for a user.
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

        cursor.execute(
            """
            DELETE FROM conversations
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
            "deleted_conversations": deleted_count
        }

    except Exception as error:
        return {
            "success": False,
            "message": f"Failed to delete chat history: {error}"
        }

    finally:
        connection.close()