from datetime import date

from app.backend.database import get_connection


# ============================================================
# SAVE QUESTIONNAIRE RESPONSE
# ============================================================

def save_questionnaire_response(
    user_id,
    mood,
    stress_level,
    energy_level,
    physical_activity,
    focus,
    social_connection,
    self_care,
    record_date=None
):
    """
    Save a daily 7-question wellness questionnaire response.

    Each answer must be an integer from 1 to 5.

    Final questionnaire fields:
        - mood
        - stress_level
        - energy_level
        - physical_activity
        - focus
        - social_connection
        - self_care
    """

    if record_date is None:
        record_date = date.today().isoformat()

    # --------------------------------------------------------
    # VALIDATE ANSWERS
    # --------------------------------------------------------

    answers = {
        "mood": mood,
        "stress_level": stress_level,
        "energy_level": energy_level,
        "physical_activity": physical_activity,
        "focus": focus,
        "social_connection": social_connection,
        "self_care": self_care
    }

    for question_id, answer in answers.items():

        if not isinstance(answer, int):
            return {
                "success": False,
                "message": (
                    f"{question_id} must be an integer "
                    "between 1 and 5."
                )
            }

        if answer < 1 or answer > 5:
            return {
                "success": False,
                "message": (
                    f"{question_id} must be between 1 and 5."
                )
            }

    connection = get_connection()
    cursor = connection.cursor()

    try:

        cursor.execute(
            """
            INSERT INTO questionnaire_responses (
                user_id,
                record_date,
                mood,
                stress_level,
                energy_level,
                physical_activity,
                focus,
                social_connection,
                self_care
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                user_id,
                record_date,
                mood,
                stress_level,
                energy_level,
                physical_activity,
                focus,
                social_connection,
                self_care
            )
        )

        connection.commit()

        return {
            "success": True,
            "message": "Questionnaire response saved successfully.",
            "user_id": user_id,
            "record_date": record_date
        }

    except Exception as error:

        return {
            "success": False,
            "message": str(error)
        }

    finally:

        connection.close()


# ============================================================
# GET QUESTIONNAIRE RESPONSE
# ============================================================

def get_questionnaire_response(user_id, record_date=None):
    """
    Get questionnaire response for a specific date.
    """

    if record_date is None:
        record_date = date.today().isoformat()

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT *
        FROM questionnaire_responses
        WHERE user_id = ?
        AND record_date = ?
        """,
        (
            user_id,
            record_date
        )
    )

    record = cursor.fetchone()

    connection.close()

    if record is None:

        return {
            "success": False,
            "message": "No questionnaire response found for this date."
        }

    return {
        "success": True,
        "record": dict(record)
    }


# ============================================================
# GET QUESTIONNAIRE HISTORY
# ============================================================

def get_questionnaire_history(user_id):
    """
    Get all questionnaire responses for a user.
    """

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT *
        FROM questionnaire_responses
        WHERE user_id = ?
        ORDER BY record_date DESC
        """,
        (user_id,)
    )

    records = cursor.fetchall()

    connection.close()

    return {
        "success": True,
        "records": [dict(record) for record in records]
    }


# ============================================================
# UPDATE QUESTIONNAIRE RESPONSE
# ============================================================

def update_questionnaire_response(
    user_id,
    mood,
    stress_level,
    energy_level,
    physical_activity,
    focus,
    social_connection,
    self_care,
    record_date=None
):
    """
    Update an existing daily questionnaire response.
    """

    if record_date is None:
        record_date = date.today().isoformat()

    # --------------------------------------------------------
    # VALIDATE ANSWERS
    # --------------------------------------------------------

    answers = {
        "mood": mood,
        "stress_level": stress_level,
        "energy_level": energy_level,
        "physical_activity": physical_activity,
        "focus": focus,
        "social_connection": social_connection,
        "self_care": self_care
    }

    for question_id, answer in answers.items():

        if not isinstance(answer, int):
            return {
                "success": False,
                "message": (
                    f"{question_id} must be an integer "
                    "between 1 and 5."
                )
            }

        if answer < 1 or answer > 5:
            return {
                "success": False,
                "message": (
                    f"{question_id} must be between 1 and 5."
                )
            }

    connection = get_connection()
    cursor = connection.cursor()

    try:

        cursor.execute(
            """
            UPDATE questionnaire_responses

            SET
                mood = ?,
                stress_level = ?,
                energy_level = ?,
                physical_activity = ?,
                focus = ?,
                social_connection = ?,
                self_care = ?,
                updated_at = CURRENT_TIMESTAMP

            WHERE user_id = ?
            AND record_date = ?
            """,
            (
                mood,
                stress_level,
                energy_level,
                physical_activity,
                focus,
                social_connection,
                self_care,
                user_id,
                record_date
            )
        )

        connection.commit()

        updated_rows = cursor.rowcount

        if updated_rows == 0:

            return {
                "success": False,
                "message": "No questionnaire response found to update."
            }

        return {
            "success": True,
            "message": "Questionnaire response updated successfully.",
            "user_id": user_id,
            "record_date": record_date
        }

    except Exception as error:

        return {
            "success": False,
            "message": str(error)
        }

    finally:

        connection.close()


# ============================================================
# DELETE QUESTIONNAIRE RESPONSE
# ============================================================

def delete_questionnaire_response(user_id, record_date=None):
    """
    Delete a questionnaire response for a specific date.
    """

    if record_date is None:
        record_date = date.today().isoformat()

    connection = get_connection()
    cursor = connection.cursor()

    try:

        cursor.execute(
            """
            DELETE FROM questionnaire_responses
            WHERE user_id = ?
            AND record_date = ?
            """,
            (
                user_id,
                record_date
            )
        )

        connection.commit()

        deleted_rows = cursor.rowcount

        if deleted_rows == 0:

            return {
                "success": False,
                "message": "No questionnaire response found to delete."
            }

        return {
            "success": True,
            "message": "Questionnaire response deleted successfully.",
            "user_id": user_id,
            "record_date": record_date
        }

    except Exception as error:

        return {
            "success": False,
            "message": str(error)
        }

    finally:

        connection.close()