from datetime import date

from app.backend.database import get_connection


# ============================================================
# SAVE OR UPDATE DAILY SLEEP RECORD
# ============================================================

def save_sleep_record(
    user_id: int,
    sleep_hours: float,
    record_date: str = None
):
    """
    Save a user's daily sleep record.

    If a record already exists for the same user and date,
    the sleep hours will be updated.
    """

    # --------------------------------------------------------
    # VALIDATE USER ID
    # --------------------------------------------------------

    if not user_id:
        return {
            "success": False,
            "message": "User ID is required."
        }

    # --------------------------------------------------------
    # VALIDATE SLEEP HOURS
    # --------------------------------------------------------

    try:
        sleep_hours = float(sleep_hours)

    except (ValueError, TypeError):

        return {
            "success": False,
            "message": "Sleep hours must be a valid number."
        }

    if sleep_hours < 0 or sleep_hours > 24:

        return {
            "success": False,
            "message": "Sleep hours must be between 0 and 24."
        }

    # --------------------------------------------------------
    # SET DATE
    # --------------------------------------------------------

    if record_date is None:
        record_date = date.today().isoformat()

    # --------------------------------------------------------
    # DATABASE OPERATION
    # --------------------------------------------------------

    connection = get_connection()

    cursor = connection.cursor()

    try:

        # Check whether the user exists
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
                "message": "User does not exist."
            }

        # Insert or update daily sleep record
        cursor.execute(
            """
            INSERT INTO sleep_records (
                user_id,
                record_date,
                sleep_hours
            )
            VALUES (?, ?, ?)

            ON CONFLICT(user_id, record_date)

            DO UPDATE SET
                sleep_hours = excluded.sleep_hours,
                updated_at = CURRENT_TIMESTAMP
            """,
            (
                user_id,
                record_date,
                sleep_hours
            )
        )

        connection.commit()

        return {
            "success": True,
            "message": "Sleep record saved successfully.",
            "user_id": user_id,
            "record_date": record_date,
            "sleep_hours": sleep_hours
        }

    except Exception as error:

        connection.rollback()

        return {
            "success": False,
            "message": f"Failed to save sleep record: {error}"
        }

    finally:

        connection.close()


# ============================================================
# GET DAILY SLEEP RECORD
# ============================================================

def get_sleep_record(
    user_id: int,
    record_date: str = None
):
    """
    Get a user's sleep record for a specific date.
    """

    if record_date is None:
        record_date = date.today().isoformat()

    connection = get_connection()

    cursor = connection.cursor()

    try:

        cursor.execute(
            """
            SELECT
                id,
                user_id,
                record_date,
                sleep_hours,
                created_at,
                updated_at
            FROM sleep_records
            WHERE user_id = ?
            AND record_date = ?
            """,
            (
                user_id,
                record_date
            )
        )

        record = cursor.fetchone()

        if record is None:

            return {
                "success": False,
                "message": "No sleep record found for this date."
            }

        return {
            "success": True,
            "record": dict(record)
        }

    finally:

        connection.close()


# ============================================================
# GET SLEEP HISTORY
# ============================================================

def get_sleep_history(user_id, limit=7):
    """
    Get recent sleep records for a user.

    Args:
        user_id: ID of the user
        limit: Maximum number of records to return

    Returns:
        Dictionary containing sleep history
    """

    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            SELECT
                id,
                user_id,
                record_date,
                sleep_hours,
                created_at,
                updated_at
            FROM sleep_records
            WHERE user_id = ?
            ORDER BY record_date DESC
            LIMIT ?
            """,
            (user_id, limit)
        )

        rows = cursor.fetchall()

        records = []

        for row in rows:
            records.append(dict(row))

        return {
            "success": True,
            "records": records
        }

    except Exception as error:

        return {
            "success": False,
            "message": f"Failed to retrieve sleep history: {error}"
        }

    finally:
        connection.close()

def update_sleep_record(user_id, record_date, sleep_hours):
    """
    Update an existing sleep record.
    """

    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            UPDATE sleep_records
            SET
                sleep_hours = ?,
                updated_at = CURRENT_TIMESTAMP
            WHERE user_id = ?
            AND record_date = ?
            """,
            (
                sleep_hours,
                user_id,
                record_date
            )
        )

        connection.commit()

        if cursor.rowcount == 0:
            return {
                "success": False,
                "message": "No sleep record found to update."
            }

        return {
            "success": True,
            "message": "Sleep record updated successfully.",
            "user_id": user_id,
            "record_date": record_date,
            "sleep_hours": sleep_hours
        }

    except Exception as error:

        return {
            "success": False,
            "message": f"Failed to update sleep record: {error}"
        }

    finally:
        connection.close()

def delete_sleep_record(user_id, record_date):
    """
    Delete a sleep record for a specific user and date.
    """

    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            DELETE FROM sleep_records
            WHERE user_id = ?
            AND record_date = ?
            """,
            (user_id, record_date)
        )

        connection.commit()

        if cursor.rowcount == 0:
            return {
                "success": False,
                "message": "No sleep record found for this date."
            }

        return {
            "success": True,
            "message": "Sleep record deleted successfully.",
            "user_id": user_id,
            "record_date": record_date
        }

    except Exception as error:

        return {
            "success": False,
            "message": f"Failed to delete sleep record: {error}"
        }

    finally:
        connection.close()