from app.backend.database import get_connection


def migrate_chat_database():
    connection = get_connection()
    cursor = connection.cursor()

    try:
        # 1. Create the conversations table if it does not exist
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                title TEXT NOT NULL DEFAULT 'New Chat',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id)
                    REFERENCES users(id)
                    ON DELETE CASCADE
            )
            """
        )

        # 2. Check whether chat_history has conversation_id
        cursor.execute("PRAGMA table_info(chat_history)")
        columns = [column["name"] for column in cursor.fetchall()]

        if "conversation_id" not in columns:
            cursor.execute(
                """
                ALTER TABLE chat_history
                ADD COLUMN conversation_id INTEGER
                """
            )
            print("Added conversation_id to chat_history.")

        # 3. Find users with old chat messages that have no conversation
        cursor.execute(
            """
            SELECT DISTINCT user_id
            FROM chat_history
            WHERE conversation_id IS NULL
            """
        )

        user_ids = [row["user_id"] for row in cursor.fetchall()]

        # 4. Move old messages into a Previous Chats conversation
        for user_id in user_ids:
            cursor.execute(
                """
                SELECT id
                FROM conversations
                WHERE user_id = ?
                ORDER BY id ASC
                LIMIT 1
                """,
                (user_id,)
            )

            existing_conversation = cursor.fetchone()

            if existing_conversation:
                conversation_id = existing_conversation["id"]
            else:
                cursor.execute(
                    """
                    INSERT INTO conversations (user_id, title)
                    VALUES (?, ?)
                    """,
                    (user_id, "Previous Chats")
                )

                conversation_id = cursor.lastrowid

            cursor.execute(
                """
                UPDATE chat_history
                SET conversation_id = ?
                WHERE user_id = ?
                  AND conversation_id IS NULL
                """,
                (conversation_id, user_id)
            )

        connection.commit()

        print("Chat database migration completed successfully.")

    except Exception as error:
        connection.rollback()
        print(f"Migration failed: {error}")

    finally:
        connection.close()


if __name__ == "__main__":
    migrate_chat_database()