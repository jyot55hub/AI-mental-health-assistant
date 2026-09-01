"""
Wellness Scoring Engine

This module calculates a project-specific Wellness Indicator Score (0-100).

IMPORTANT:
This score is NOT a medical diagnosis or a clinically validated
mental health assessment. It is designed for educational wellness
tracking and personalized wellness recommendations.
"""


# ============================================================
# WELLNESS SCORING
# ============================================================

def calculate_sleep_score(sleep_hours):
    """
    Calculate wellness points based on sleep duration.

    Returns a score from 0 to 25.
    """

    if sleep_hours is None:
        return None

    try:
        sleep_hours = float(sleep_hours)
    except (ValueError, TypeError):
        return None

    if 7 <= sleep_hours <= 9:
        return 25

    elif 6 <= sleep_hours < 7:
        return 18

    elif 5 <= sleep_hours < 6:
        return 10

    elif sleep_hours < 5:
        return 5

    else:
        return 15


# ============================================================
# QUESTIONNAIRE SCORE
# ============================================================

def calculate_questionnaire_score(
    mood=None,
    stress_level=None,
    energy_level=None
):
    """
    Calculate questionnaire wellness score.

    Expected input scale:
    mood: 1 to 5
    stress_level: 1 to 5
    energy_level: 1 to 5

    Higher mood and energy improve wellness.
    Higher stress reduces wellness.

    Returns a score from 0 to 60.
    """

    scores = []

    # Mood contribution (0-20)
    if mood is not None:

        try:
            mood = float(mood)

            mood = max(1, min(5, mood))

            mood_score = ((mood - 1) / 4) * 20

            scores.append(mood_score)

        except (ValueError, TypeError):
            pass


    # Stress contribution (0-20)
    if stress_level is not None:

        try:
            stress_level = float(stress_level)

            stress_level = max(
                1,
                min(5, stress_level)
            )

            # Lower stress = better score
            stress_score = (
                (5 - stress_level) / 4
            ) * 20

            scores.append(stress_score)

        except (ValueError, TypeError):
            pass


    # Energy contribution (0-20)
    if energy_level is not None:

        try:
            energy_level = float(energy_level)

            energy_level = max(
                1,
                min(5, energy_level)
            )

            energy_score = (
                (energy_level - 1) / 4
            ) * 20

            scores.append(energy_score)

        except (ValueError, TypeError):
            pass


    if not scores:
        return None

    # Scale available answers fairly
    average_score = sum(scores) / len(scores)

    return average_score * 3


# ============================================================
# WELLNESS INDICATOR
# ============================================================

def calculate_wellness_score(
    sleep_hours=None,
    mood=None,
    stress_level=None,
    energy_level=None
):
    """
    Calculate a Wellness Indicator Score from 0 to 100.

    Components:
    - Sleep: 25 points
    - Daily questionnaire: 60 points

    If some information is unavailable,
    the score is calculated only from available information.

    NOTE:
    This is a project-specific, non-diagnostic wellness indicator.
    """

    component_scores = {}

    # Sleep
    sleep_score = calculate_sleep_score(
        sleep_hours
    )

    if sleep_score is not None:

        component_scores["sleep"] = {
            "score": round(sleep_score, 2),
            "maximum": 25
        }


    # Questionnaire
    questionnaire_score = (
        calculate_questionnaire_score(
            mood,
            stress_level,
            energy_level
        )
    )

    if questionnaire_score is not None:

        component_scores["questionnaire"] = {
            "score": round(
                questionnaire_score,
                2
            ),
            "maximum": 60
        }


    # No data
    if not component_scores:

        return {
            "wellness_score": None,
            "category": "Insufficient Data",
            "components": {},
            "message": (
                "Please provide wellness information "
                "to calculate your wellness indicator."
            )
        }


    # Calculate percentage
    total_score = sum(
        item["score"]
        for item in component_scores.values()
    )

    maximum_score = sum(
        item["maximum"]
        for item in component_scores.values()
    )

    wellness_score = (
        total_score / maximum_score
    ) * 100


    wellness_score = round(
        wellness_score,
        2
    )


    category = get_wellness_category(
        wellness_score
    )


    return {
        "wellness_score": wellness_score,
        "category": category,
        "components": component_scores,
        "message": (
            "This is a non-diagnostic wellness "
            "indicator for educational wellness tracking."
        )
    }


# ============================================================
# WELLNESS CATEGORY
# ============================================================

def get_wellness_category(score):
    """
    Convert wellness score into a category.
    """

    if score is None:
        return "Insufficient Data"

    elif score >= 75:
        return "Good"

    elif score >= 50:
        return "Moderate"

    else:
        return "Needs Attention"


# ============================================================
# TESTING
# ============================================================

if __name__ == "__main__":

    example_user = calculate_wellness_score(
        sleep_hours=7.5,
        mood=4,
        stress_level=2,
        energy_level=4
    )

    print("\nWELLNESS SCORING TEST")
    print("=" * 50)

    print(
        f"Wellness Score: "
        f"{example_user['wellness_score']}/100"
    )

    print(
        f"Category: "
        f"{example_user['category']}"
    )

    print("\nComponent Scores:")

    for component, data in (
        example_user["components"].items()
    ):
        print(
            f"{component.title()}: "
            f"{data['score']}/"
            f"{data['maximum']}"
        )

    print("\nNote:")
    print(example_user["message"])