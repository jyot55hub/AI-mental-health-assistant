from datetime import date
import math

from app.backend.database import get_connection


# ============================================================
# VALIDATE AND NORMALIZE MEDITATION MINUTES
# ============================================================

def normalize_meditation_minutes(minutes):
    """
    Convert meditation time into a valid decimal value
    rounded to two decimal places.
    """

    try:
        minutes = float(minutes)
    except (ValueError, TypeError):
        raise ValueError("Meditation time must be a number.")

    if not math.isfinite(minutes):
        raise ValueError("Meditation time must be a valid number.")

    if minutes < 0:
        raise ValueError("Meditation time cannot be negative.")

    return round(minutes, 2)


# ============================================================
# SAVE MEDITATION RECORD
# ============================================================

def save_meditation_record(
    user_id,
    meditation_minutes,
    record_date=None
):
    """Save a meditation record for a user."""

    if record_date is None:
        record_date = date.today().isoformat()

    try:
        meditation_minutes = normalize_meditation_minutes(
            meditation_minutes
        )
    except ValueError as error:
        return {
            "success": False,
            "message": str(error)
        }

    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            INSERT INTO meditation_records (
                user_id,
                record_date,
                meditation_minutes
            )
            VALUES (?, ?, ?)
            """,
            (
                user_id,
                record_date,
                meditation_minutes
            )
        )

        connection.commit()

        return {
            "success": True,
            "message": "Meditation record saved successfully.",
            "user_id": user_id,
            "record_date": record_date,
            "meditation_minutes": meditation_minutes
        }

    except Exception as error:
        return {
            "success": False,
            "message": str(error)
        }

    finally:
        connection.close()


# ============================================================
# GET MEDITATION RECORD
# ============================================================

def get_meditation_record(user_id, record_date=None):
    """Get a user's meditation record for a specific date."""

    if record_date is None:
        record_date = date.today().isoformat()

    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            SELECT *
            FROM meditation_records
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
                "message": "No meditation record found for this date."
            }

        return {
            "success": True,
            "record": dict(record)
        }

    finally:
        connection.close()


# ============================================================
# GET MEDITATION HISTORY
# ============================================================

def get_meditation_history(user_id):
    """Get all meditation records for a user."""

    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            SELECT *
            FROM meditation_records
            WHERE user_id = ?
            ORDER BY record_date DESC
            """,
            (user_id,)
        )

        records = cursor.fetchall()

        return {
            "success": True,
            "records": [
                dict(record)
                for record in records
            ]
        }

    finally:
        connection.close()


# ============================================================
# UPDATE MEDITATION RECORD
# ============================================================

def update_meditation_record(
    user_id,
    meditation_minutes,
    record_date=None
):
    """Update a user's meditation record."""

    if record_date is None:
        record_date = date.today().isoformat()

    try:
        meditation_minutes = normalize_meditation_minutes(
            meditation_minutes
        )
    except ValueError as error:
        return {
            "success": False,
            "message": str(error)
        }

    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            UPDATE meditation_records
            SET meditation_minutes = ?,
                updated_at = CURRENT_TIMESTAMP
            WHERE user_id = ?
            AND record_date = ?
            """,
            (
                meditation_minutes,
                user_id,
                record_date
            )
        )

        connection.commit()

        if cursor.rowcount == 0:
            return {
                "success": False,
                "message": "No meditation record found to update."
            }

        return {
            "success": True,
            "message": "Meditation record updated successfully.",
            "user_id": user_id,
            "record_date": record_date,
            "meditation_minutes": meditation_minutes
        }

    finally:
        connection.close()


# ============================================================
# DELETE MEDITATION RECORD
# ============================================================

def delete_meditation_record(user_id, record_date=None):
    """Delete a meditation record."""

    if record_date is None:
        record_date = date.today().isoformat()

    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            DELETE FROM meditation_records
            WHERE user_id = ?
            AND record_date = ?
            """,
            (
                user_id,
                record_date
            )
        )

        connection.commit()

        if cursor.rowcount == 0:
            return {
                "success": False,
                "message": "No meditation record found to delete."
            }

        return {
            "success": True,
            "message": "Meditation record deleted successfully.",
            "user_id": user_id,
            "record_date": record_date
        }

    finally:
        connection.close()