from datetime import date

from app.backend.database import get_connection

from app.analytics.wellness_scoring import (
    calculate_wellness_score,
)

from app.analytics.recommendations import (
    generate_recommendations,
)

# ============================================================
# CALCULATE AND SAVE DAILY WELLNESS SCORE
# ============================================================

def calculate_and_save_wellness_score(
    user_id,
    record_date=None
):
    """
    Calculate the user's wellness score for a particular date
    using sleep, meditation, and the final 7-question
    questionnaire data.

    The calculated score is saved in the wellness_scores table.
    """

    # --------------------------------------------------------
    # USE TODAY'S DATE IF NO DATE IS PROVIDED
    # --------------------------------------------------------

    if record_date is None:
        record_date = date.today().isoformat()

    elif hasattr(record_date, "isoformat"):
        record_date = record_date.isoformat()

    connection = get_connection()
    cursor = connection.cursor()

    try:

        # ====================================================
        # GET SLEEP DATA
        # ====================================================

        cursor.execute(
            """
            SELECT sleep_hours
            FROM sleep_records
            WHERE user_id = ?
            AND record_date = ?
            """,
            (
                user_id,
                record_date
            )
        )

        sleep_row = cursor.fetchone()

        sleep_hours = (
            sleep_row["sleep_hours"]
            if sleep_row
            else None
        )

        # ====================================================
        # GET MEDITATION DATA
        # ====================================================

        cursor.execute(
            """
            SELECT meditation_minutes
            FROM meditation_records
            WHERE user_id = ?
            AND record_date = ?
            """,
            (
                user_id,
                record_date
            )
        )

        meditation_row = cursor.fetchone()

        meditation_minutes = (
            meditation_row["meditation_minutes"]
            if meditation_row
            else None
        )

        # --------------------------------------------------------
        # CAP MEDITATION AT 13 MINUTES FOR WELLNESS SCORING
        # --------------------------------------------------------

        if meditation_minutes is not None:
            scored_meditation_minutes = min(
                meditation_minutes,
                13
            )
        else:
            scored_meditation_minutes = None

        # ====================================================
        # GET FINAL 7-QUESTION QUESTIONNAIRE DATA
        # ====================================================

        cursor.execute(
            """
            SELECT
                mood,
                stress_level,
                energy_level,
                physical_activity,
                focus,
                social_connection,
                self_care
            FROM questionnaire_responses
            WHERE user_id = ?
            AND record_date = ?
            """,
            (
                user_id,
                record_date
            )
        )

        questionnaire_row = cursor.fetchone()

        # ====================================================
        # EXTRACT QUESTIONNAIRE VALUES
        # ====================================================

        if questionnaire_row:

            mood = questionnaire_row["mood"]

            stress = questionnaire_row["stress_level"]

            energy = questionnaire_row["energy_level"]

            physical_activity = (
                questionnaire_row["physical_activity"]
            )

            focus = questionnaire_row["focus"]

            social = (
                questionnaire_row["social_connection"]
            )

            self_care = questionnaire_row["self_care"]

        else:

            mood = None
            stress = None
            energy = None
            physical_activity = None
            focus = None
            social = None
            self_care = None

        # ====================================================
        # CALCULATE WELLNESS SCORE
        # ====================================================

        result = calculate_wellness_score(

            sleep_hours=sleep_hours,

            meditation_minutes=scored_meditation_minutes,

            mood=mood,

            stress=stress,

            energy=energy,

            physical_activity=physical_activity,

            focus=focus,

            social=social,

            self_care=self_care
        )

        # ====================================================
        # CHECK WHETHER THERE IS ENOUGH DATA
        # ====================================================

        if result["wellness_score"] is None:

            return {
                "success": False,
                "message": (
                    "Not enough wellness data "
                    "to calculate a score."
                ),
                "result": result
            }
                
        # ========================================================
        # GENERATE PERSONALIZED RECOMMENDATIONS
        # ========================================================

        recommendation_result = generate_recommendations(
            category=result.get("category"),
            wellness_score=result.get("wellness_score"),
            sleep_hours=sleep_hours,
            stress_level=stress,
            meditation_minutes=meditation_minutes
        )

        # ====================================================
        # GET COMPONENT SCORES
        # ====================================================

        components = result["components"]

        sleep_score = None

        if "sleep" in components:

            sleep_score = components["sleep"]["score"]

        meditation_score = None

        if "meditation" in components:

            meditation_score = (
                components["meditation"]["score"]
            )

        questionnaire_score = None

        if "questionnaire" in components:

            questionnaire_score = (
                components["questionnaire"]["score"]
            )

        # ====================================================
        # SAVE / UPDATE WELLNESS SCORE
        # ====================================================

        cursor.execute(
            """
            INSERT INTO wellness_scores (
                user_id,
                record_date,
                wellness_score,
                category,
                sleep_score,
                meditation_score,
                questionnaire_score
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)

            ON CONFLICT(user_id, record_date)
            DO UPDATE SET

                wellness_score =
                    excluded.wellness_score,

                category =
                    excluded.category,

                sleep_score =
                    excluded.sleep_score,

                meditation_score =
                    excluded.meditation_score,

                questionnaire_score =
                    excluded.questionnaire_score,

                updated_at =
                    CURRENT_TIMESTAMP
            """,
            (
                user_id,
                record_date,
                result["wellness_score"],
                result["category"],
                sleep_score,
                meditation_score,
                questionnaire_score
            )
        )

        connection.commit()

        # ====================================================
        # RETURN SUCCESS
        # ====================================================

        return {
            "success": True,
            "message": "Wellness score calculated and saved successfully.",
            "user_id": user_id,
            "record_date": record_date,
            "wellness_score": result["wellness_score"],
            "category": result["category"],
            "components": result["components"],
            "recommendations": recommendation_result.get("recommendations", []),
            "disclaimer": recommendation_result.get("disclaimer")
        }
    except Exception as error:

        connection.rollback()

        return {
            "success": False,

            "message": (
                "Failed to calculate wellness score: "
                + str(error)
            )
        }

    finally:

        connection.close()


# ============================================================
# GET WELLNESS SCORE
# ============================================================

def get_wellness_score(
    user_id,
    record_date=None
):
    """
    Retrieve a user's wellness score for a particular date.
    """

    if record_date is None:
        record_date = date.today().isoformat()

    elif hasattr(record_date, "isoformat"):
        record_date = record_date.isoformat()

    connection = get_connection()
    cursor = connection.cursor()

    try:

        cursor.execute(
            """
            SELECT
                id,
                user_id,
                record_date,
                wellness_score,
                category,
                sleep_score,
                meditation_score,
                questionnaire_score,
                created_at,
                updated_at
            FROM wellness_scores
            WHERE user_id = ?
            AND record_date = ?
            """,
            (
                user_id,
                record_date
            )
        )

        row = cursor.fetchone()

        if row is None:

            return {
                "success": False,

                "message": (
                    "No wellness score found "
                    "for this date."
                )
            }

        return {
            "success": True,

            "record": dict(row)
        }

    except Exception as error:

        return {
            "success": False,

            "message": (
                "Failed to retrieve wellness score: "
                + str(error)
            )
        }

    finally:

        connection.close()


# ============================================================
# GET WELLNESS SCORE HISTORY
# ============================================================

def get_wellness_history(user_id):
    """
    Retrieve all wellness scores for a user.
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
                wellness_score,
                category,
                sleep_score,
                meditation_score,
                questionnaire_score,
                created_at,
                updated_at
            FROM wellness_scores
            WHERE user_id = ?
            ORDER BY record_date DESC
            """,
            (user_id,)
        )

        rows = cursor.fetchall()

        return {
            "success": True,

            "records": [
                dict(row)
                for row in rows
            ]
        }

    except Exception as error:

        return {
            "success": False,

            "message": (
                "Failed to retrieve wellness history: "
                + str(error)
            )
        }

    finally:

        connection.close()


# ============================================================
# TEST PROGRAM
# ============================================================

if __name__ == "__main__":

    TEST_USER_ID = 1

    print("\n" + "=" * 60)
    print("DAILY WELLNESS SCORE TEST")
    print("=" * 60)

    # --------------------------------------------------------
    # CALCULATE AND SAVE
    # --------------------------------------------------------

    print("\nCALCULATE AND SAVE WELLNESS SCORE")
    print("=" * 60)

    result = calculate_and_save_wellness_score(
        user_id=TEST_USER_ID
    )

    print(result)

    # --------------------------------------------------------
    # GET TODAY'S SCORE
    # --------------------------------------------------------

    print("\nGET TODAY'S WELLNESS SCORE")
    print("=" * 60)

    result = get_wellness_score(
        user_id=TEST_USER_ID
    )

    print(result)

    # --------------------------------------------------------
    # GET WELLNESS HISTORY
    # --------------------------------------------------------

    print("\nGET WELLNESS HISTORY")
    print("=" * 60)

    result = get_wellness_history(
        user_id=TEST_USER_ID
    )

    print(result)