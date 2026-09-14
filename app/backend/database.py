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

    # Create the data folder if it does not already exist
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(DATABASE_PATH)

    # Return rows as dictionary-like objects
    connection.row_factory = sqlite3.Row

    # Enable foreign key support
    connection.execute("PRAGMA foreign_keys = ON")

    return connection


# ============================================================
# INITIALIZE DATABASE
# ============================================================

def initialize_database():
    """
    Create all required database tables.
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

    connection.commit()

    connection.close()

    print("Database initialized successfully.")
    print(f"Database location: {DATABASE_PATH}")

# ============================================================
# RUN DATABASE INITIALIZATION
# ============================================================

if __name__ == "__main__":
    initialize_database()