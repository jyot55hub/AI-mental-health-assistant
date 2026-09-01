"""
Wellness Scoring Engine

This module calculates a project-specific Wellness Indicator Score.

IMPORTANT:
This score is NOT a medical diagnosis or a clinically validated
mental health assessment. It is designed for educational wellness
tracking and personalized wellness recommendations.
"""


# ============================================================
# SLEEP SCORING
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
# QUESTIONNAIRE SCORING
# ============================================================

def calculate_questionnaire_score(
    mood=None,
    stress=None,
    energy=None,
    physical_activity=None,
    focus=None,
    social=None,
    self_care=None,
    stress_level=None,
    energy_level=None
):
    """
    Calculate questionnaire wellness score.

    There are 7 wellness questions.

    Each answer should be between 1 and 5.

    Returns a score from 0 to 60.

    Score conversion:

    1 = minimum wellness value
    5 = maximum wellness value

    Therefore:

    All answers = 1 -> 0/60
    All answers = 5 -> 60/60

    stress_level and energy_level are supported
    for backward compatibility with existing code.
    """

    # --------------------------------------------------------
    # BACKWARD COMPATIBILITY
    # --------------------------------------------------------

    if stress is None:
        stress = stress_level

    if energy is None:
        energy = energy_level


    # --------------------------------------------------------
    # COLLECT ANSWERS
    # --------------------------------------------------------

    answers = [
        mood,
        stress,
        energy,
        physical_activity,
        focus,
        social,
        self_care
    ]


    valid_scores = []


    # --------------------------------------------------------
    # VALIDATE AVAILABLE ANSWERS
    # --------------------------------------------------------

    for answer in answers:

        if answer is None:
            continue

        try:

            answer = float(answer)

            # Keep values within questionnaire scale
            answer = max(
                1,
                min(5, answer)
            )

            valid_scores.append(answer)

        except (ValueError, TypeError):

            continue


    # --------------------------------------------------------
    # NO VALID ANSWERS
    # --------------------------------------------------------

    if not valid_scores:

        return None


    # --------------------------------------------------------
    # CALCULATE AVERAGE ANSWER
    # --------------------------------------------------------

    average_answer = (
        sum(valid_scores)
        / len(valid_scores)
    )


    # --------------------------------------------------------
    # CONVERT 1-5 SCALE TO 0-60 SCALE
    # --------------------------------------------------------
    #
    # Formula:
    #
    # ((value - minimum) / (maximum - minimum)) * 60
    #
    # 1 -> 0
    # 5 -> 60
    #

    questionnaire_score = (
        (average_answer - 1)
        / (5 - 1)
    ) * 60


    return round(
        questionnaire_score,
        2
    )


# ============================================================
# WELLNESS INDICATOR
# ============================================================

def calculate_wellness_score(
    sleep_hours=None,
    mood=None,
    stress=None,
    energy=None,
    physical_activity=None,
    focus=None,
    social=None,
    self_care=None,
    stress_level=None,
    energy_level=None
):
    """
    Calculate a Wellness Indicator Score from 0 to 100.

    Components:

    - Sleep: maximum 25 points
    - Daily Questionnaire: maximum 60 points

    The final score is normalized to 0-100 based
    on the available information.

    NOTE:
    This is a project-specific, non-diagnostic
    wellness indicator.
    """

    component_scores = {}


    # --------------------------------------------------------
    # BACKWARD COMPATIBILITY
    # --------------------------------------------------------

    if stress is None:
        stress = stress_level

    if energy is None:
        energy = energy_level


    # --------------------------------------------------------
    # SLEEP SCORE
    # --------------------------------------------------------

    sleep_score = calculate_sleep_score(
        sleep_hours
    )


    if sleep_score is not None:

        component_scores["sleep"] = {
            "score": round(
                sleep_score,
                2
            ),
            "maximum": 25
        }


    # --------------------------------------------------------
    # QUESTIONNAIRE SCORE
    # --------------------------------------------------------

    questionnaire_score = (
        calculate_questionnaire_score(
            mood=mood,
            stress=stress,
            energy=energy,
            physical_activity=physical_activity,
            focus=focus,
            social=social,
            self_care=self_care
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


    # --------------------------------------------------------
    # NO DATA
    # --------------------------------------------------------

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


    # --------------------------------------------------------
    # CALCULATE FINAL SCORE
    # --------------------------------------------------------

    total_score = sum(
        item["score"]
        for item in component_scores.values()
    )


    maximum_score = sum(
        item["maximum"]
        for item in component_scores.values()
    )


    wellness_score = (
        total_score
        / maximum_score
    ) * 100


    wellness_score = round(
        wellness_score,
        2
    )


    category = get_wellness_category(
        wellness_score
    )


    # --------------------------------------------------------
    # RETURN RESULT
    # --------------------------------------------------------

    return {
        "wellness_score": wellness_score,
        "category": category,
        "components": component_scores,
        "message": (
            "This is a project-specific, non-diagnostic "
            "wellness indicator for educational wellness tracking."
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
# TEST PROGRAM
# ============================================================

if __name__ == "__main__":

    example_user = calculate_wellness_score(

        sleep_hours=7.5,

        mood=4,

        stress=4,

        energy=3,

        physical_activity=3,

        focus=4,

        social=3,

        self_care=4
    )


    print("\nWELLNESS SCORING TEST")

    print("=" * 55)


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

    print(
        example_user["message"]
    )