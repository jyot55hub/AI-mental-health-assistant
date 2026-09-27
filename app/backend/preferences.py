from app.backend.database import get_connection


# ============================================================
# DEFAULT NOTIFICATION PREFERENCES
# ============================================================

DEFAULT_NOTIFICATION_PREFERENCES = {
    "wellness_reminder": True,
    "meditation_reminder": True,
    "sleep_reminder": True,
    "questionnaire_reminder": True,
    "reminder_time": "20:00"
}


# ============================================================
# GET NOTIFICATION PREFERENCES
# ============================================================

def get_notification_preferences(user_id: int):
    """
    Get notification preferences belonging to the specified user.

    If the user has never saved notification preferences,
    default values are returned.
    """

    if not user_id:

        return {
            "success": False,
            "message": "User ID is required."
        }

    connection = get_connection()
    cursor = connection.cursor()

    try:

        cursor.execute(
            """
            SELECT
                wellness_reminder,
                meditation_reminder,
                sleep_reminder,
                questionnaire_reminder,
                reminder_time
            FROM notification_preferences
            WHERE user_id = ?
            """,
            (user_id,)
        )

        row = cursor.fetchone()

        # ----------------------------------------------------
        # NO SAVED PREFERENCES YET
        # ----------------------------------------------------

        if row is None:

            return {
                "success": True,
                "preferences": (
                    DEFAULT_NOTIFICATION_PREFERENCES.copy()
                )
            }

        # ----------------------------------------------------
        # RETURN SAVED PREFERENCES
        # ----------------------------------------------------

        return {
            "success": True,
            "preferences": {

                "wellness_reminder": bool(
                    row["wellness_reminder"]
                ),

                "meditation_reminder": bool(
                    row["meditation_reminder"]
                ),

                "sleep_reminder": bool(
                    row["sleep_reminder"]
                ),

                "questionnaire_reminder": bool(
                    row["questionnaire_reminder"]
                ),

                "reminder_time": row["reminder_time"]
            }
        }

    except Exception as error:

        return {
            "success": False,
            "message": (
                "Unable to load notification preferences: "
                f"{error}"
            )
        }

    finally:

        connection.close()


# ============================================================
# SAVE NOTIFICATION PREFERENCES
# ============================================================

def save_notification_preferences(
    user_id: int,
    wellness_reminder: bool,
    meditation_reminder: bool,
    sleep_reminder: bool,
    questionnaire_reminder: bool,
    reminder_time: str
):
    """
    Create or update notification preferences for a user.
    """

    if not user_id:

        return {
            "success": False,
            "message": "User ID is required."
        }

    if not reminder_time:

        reminder_time = "20:00"

    connection = get_connection()
    cursor = connection.cursor()

    try:

        cursor.execute(
            """
            INSERT INTO notification_preferences (

                user_id,

                wellness_reminder,

                meditation_reminder,

                sleep_reminder,

                questionnaire_reminder,

                reminder_time

            )

            VALUES (?, ?, ?, ?, ?, ?)

            ON CONFLICT(user_id)

            DO UPDATE SET

                wellness_reminder =
                    excluded.wellness_reminder,

                meditation_reminder =
                    excluded.meditation_reminder,

                sleep_reminder =
                    excluded.sleep_reminder,

                questionnaire_reminder =
                    excluded.questionnaire_reminder,

                reminder_time =
                    excluded.reminder_time,

                updated_at =
                    CURRENT_TIMESTAMP
            """,
            (
                user_id,

                int(bool(wellness_reminder)),

                int(bool(meditation_reminder)),

                int(bool(sleep_reminder)),

                int(bool(questionnaire_reminder)),

                reminder_time
            )
        )

        connection.commit()

        return {
            "success": True,
            "message": (
                "Notification preferences saved successfully."
            )
        }

    except Exception as error:

        connection.rollback()

        return {
            "success": False,
            "message": (
                "Unable to save notification preferences: "
                f"{error}"
            )
        }

    finally:

        connection.close()