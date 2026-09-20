from app.backend.database import get_connection


def cleanup_empty_conversations():
    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            DELETE FROM conversations
            WHERE title = 'New Chat'
              AND id NOT IN (
                  SELECT DISTINCT conversation_id
                  FROM chat_history
                  WHERE conversation_id IS NOT NULL
              )
            """
        )

        deleted_count = cursor.rowcount
        connection.commit()

        print(f"Deleted {deleted_count} empty New Chat conversation(s).")
        print("Cleanup completed successfully.")

    except Exception as error:
        connection.rollback()
        print(f"Cleanup failed: {error}")

    finally:
        connection.close()


if __name__ == "__main__":
    cleanup_empty_conversations()