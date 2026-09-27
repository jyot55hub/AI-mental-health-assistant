import sqlite3
from pathlib import Path


# ============================================================
# PROJECT PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent.parent

DATA_DIR = BASE_DIR / "data"

DATABASE_PATH = DATA_DIR / "mental_health.db"


# ============================================================
# DATABASE CONNECTION
# ============================================================

def get_connection():
    """
    Create and return a connection to the SQLite database.
    """

    DATA_DIR.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(DATABASE_PATH)

    connection.row_factory = sqlite3.Row

    connection.execute("PRAGMA foreign_keys = ON")

    return connection


# ============================================================
# CHAT MIGRATION
# ============================================================

def migrate_chat_history(connection):
    """
    Add conversation support to the existing chat history.

    Existing messages are preserved and moved into a
    'Previous Chats' conversation for each user.
    """

    cursor = connection.cursor()

    # --------------------------------------------------------
    # Create conversations table
    # --------------------------------------------------------

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

    # --------------------------------------------------------
    # Check whether conversation_id already exists
    # --------------------------------------------------------

    cursor.execute("PRAGMA table_info(chat_history)")

    columns = [column["name"] for column in cursor.fetchall()]

    if "conversation_id" not in columns:

        cursor.execute(
            """
            ALTER TABLE chat_history
            ADD COLUMN conversation_id INTEGER
            """
        )

    # --------------------------------------------------------
    # Create an index for faster conversation-based searches
    # --------------------------------------------------------

    cursor.execute(
        """
        CREATE INDEX IF NOT EXISTS idx_chat_history_conversation
        ON chat_history(conversation_id)
        """
    )

    # --------------------------------------------------------
    # Move existing messages into Previous Chats
    # --------------------------------------------------------

    cursor.execute(
        """
        SELECT DISTINCT user_id
        FROM chat_history
        WHERE conversation_id IS NULL
        """
    )

    users_with_old_messages = cursor.fetchall()

    for user_row in users_with_old_messages:

        user_id = user_row["user_id"]

        # Check whether a Previous Chats conversation exists
        cursor.execute(
            """
            SELECT id
            FROM conversations
            WHERE user_id = ?
              AND title = 'Previous Chats'
            ORDER BY id ASC
            LIMIT 1
            """,
            (user_id,)
        )

        conversation = cursor.fetchone()

        if conversation:

            conversation_id = conversation["id"]

        else:

            cursor.execute(
                """
                INSERT INTO conversations (
                    user_id,
                    title
                )
                VALUES (?, ?)
                """,
                (
                    user_id,
                    "Previous Chats"
                )
            )

            conversation_id = cursor.lastrowid

        # Assign old messages to this conversation
        cursor.execute(
            """
            UPDATE chat_history
            SET conversation_id = ?
            WHERE user_id = ?
              AND conversation_id IS NULL
            """,
            (
                conversation_id,
                user_id
            )
        )
    # ========================================================
    # NOTIFICATION PREFERENCES TABLE
    # ========================================================

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS notification_preferences (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            user_id INTEGER NOT NULL UNIQUE,

            wellness_reminder INTEGER NOT NULL DEFAULT 1,

            meditation_reminder INTEGER NOT NULL DEFAULT 1,

            sleep_reminder INTEGER NOT NULL DEFAULT 1,

            questionnaire_reminder INTEGER NOT NULL DEFAULT 1,

            reminder_time TEXT NOT NULL DEFAULT '20:00',

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY (user_id)
                REFERENCES users(id)
                ON DELETE CASCADE

        )
        """
    )
    connection.commit()

# ============================================================
# USER PROFILE MIGRATION
# ============================================================

def migrate_user_profile(connection):
    """
    Add profile-related fields to the existing users table.

    Existing users are preserved. New profile fields receive
    safe default values.
    """

    cursor = connection.cursor()

    # --------------------------------------------------------
    # Check existing users table columns
    # --------------------------------------------------------

    cursor.execute("PRAGMA table_info(users)")

    columns = [
        column["name"]
        for column in cursor.fetchall()
    ]

    # --------------------------------------------------------
    # Add username
    # --------------------------------------------------------

    if "username" not in columns:

        cursor.execute(
            """
            ALTER TABLE users
            ADD COLUMN username TEXT
            """
        )

    # --------------------------------------------------------
    # Add bio
    # --------------------------------------------------------

    if "bio" not in columns:

        cursor.execute(
            """
            ALTER TABLE users
            ADD COLUMN bio TEXT DEFAULT ''
            """
        )

    # --------------------------------------------------------
    # Add avatar
    # --------------------------------------------------------

    if "avatar" not in columns:

        cursor.execute(
            """
            ALTER TABLE users
            ADD COLUMN avatar TEXT DEFAULT '🌿'
            """
        )

    connection.commit()
# ============================================================
# INITIALIZE DATABASE
# ============================================================

def initialize_database():
    """
    Create all required database tables and run migrations.
    """

    connection = get_connection()

    cursor = connection.cursor()

    # ========================================================
    # USERS TABLE
    # ========================================================

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            name TEXT NOT NULL,

            email TEXT UNIQUE NOT NULL,

            password_hash TEXT NOT NULL,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

        )
        """
    )

    # ========================================================
    # SLEEP RECORDS TABLE
    # ========================================================

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS sleep_records (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            user_id INTEGER NOT NULL,

            record_date DATE NOT NULL,

            sleep_hours REAL NOT NULL,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY (user_id)
                REFERENCES users(id)
                ON DELETE CASCADE,

            UNIQUE(user_id, record_date)

        )
        """
    )

    # ========================================================
    # CHAT HISTORY TABLE
    # ========================================================

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS chat_history (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            user_id INTEGER NOT NULL,

            user_message TEXT NOT NULL,

            ai_response TEXT NOT NULL,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY (user_id)
                REFERENCES users(id)
                ON DELETE CASCADE

        )
        """
    )

    # ========================================================
    # MEDITATION RECORDS TABLE
    # ========================================================

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS meditation_records (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            user_id INTEGER NOT NULL,

            record_date DATE NOT NULL,

            meditation_minutes INTEGER NOT NULL,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY (user_id)
                REFERENCES users(id)
                ON DELETE CASCADE,

            UNIQUE(user_id, record_date)

        )
        """
    )

    # ========================================================
    # QUESTIONNAIRE RESPONSES TABLE
    # ========================================================

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS questionnaire_responses (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            user_id INTEGER NOT NULL,

            record_date DATE NOT NULL,

            mood INTEGER NOT NULL,

            stress_level INTEGER NOT NULL,

            energy_level INTEGER NOT NULL,

            physical_activity INTEGER NOT NULL,

            focus INTEGER NOT NULL,

            social_connection INTEGER NOT NULL,

            self_care INTEGER NOT NULL,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY (user_id)
                REFERENCES users(id)
                ON DELETE CASCADE,

            UNIQUE(user_id, record_date)

        )
        """
    )

    # ========================================================
    # WELLNESS SCORES TABLE
    # ========================================================

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS wellness_scores (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            user_id INTEGER NOT NULL,

            record_date DATE NOT NULL,

            wellness_score REAL NOT NULL,

            category TEXT NOT NULL,

            sleep_score REAL,

            meditation_score REAL,

            questionnaire_score REAL,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY (user_id)
                REFERENCES users(id)
                ON DELETE CASCADE,

            UNIQUE(user_id, record_date)

        )
        """
    )
    # ========================================================
    # JOURNAL ENTRIES TABLE
    # ========================================================

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS journal_entries (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            user_id INTEGER NOT NULL,

            title TEXT NOT NULL,

            content TEXT NOT NULL,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY (user_id)
                REFERENCES users(id)
                ON DELETE CASCADE

        )
        """
    )
    # ========================================================
    # NOTIFICATION PREFERENCES TABLE
    # ========================================================

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS notification_preferences (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            user_id INTEGER NOT NULL UNIQUE,

            wellness_reminder INTEGER NOT NULL DEFAULT 1,

            meditation_reminder INTEGER NOT NULL DEFAULT 1,

            sleep_reminder INTEGER NOT NULL DEFAULT 1,

            questionnaire_reminder INTEGER NOT NULL DEFAULT 1,

            reminder_time TEXT NOT NULL DEFAULT '20:00',

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY (user_id)
                REFERENCES users(id)
                ON DELETE CASCADE

        )
        """
    )
    connection.commit()

    # ========================================================
    # RUN CHAT CONVERSATION MIGRATION
    # ========================================================

    migrate_chat_history(connection)

    # ========================================================
    # RUN USER PROFILE MIGRATION
    # ========================================================

    migrate_user_profile(connection)

    connection.close()

    print("Database initialized successfully.")
    print(f"Database location: {DATABASE_PATH}")


# ============================================================
# RUN DATABASE INITIALIZATION
# ============================================================

if __name__ == "__main__":
    initialize_database()