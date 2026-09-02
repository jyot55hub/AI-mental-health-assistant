"""
Complete Wellness Analytics Workflow

This module connects:

1. Daily Wellness Questionnaire
2. Questionnaire Scoring
3. Sleep Tracking
4. Guided Meditation Tracking
5. Overall Wellness Indicator
6. Wellness Category
7. Personalized Recommendations

IMPORTANT:
This workflow is designed for educational wellness tracking only.
It is NOT a medical diagnostic system.
"""


# ============================================================
# IMPORTS
# ============================================================

from app.analytics.questionnaire import (
    get_questionnaire_questions,
    calculate_questionnaire_score
)

from app.analytics.wellness_scoring import (
    calculate_wellness_score
)

from app.analytics.recommendations import (
    generate_recommendations
)


# ============================================================
# COMPLETE WELLNESS WORKFLOW
# ============================================================

def run_wellness_workflow(
    answers,
    sleep_hours=None,
    meditation_minutes=0
):
    """
    Run the complete daily wellness analytics workflow.

    Parameters
    ----------
    answers : dict

        Dictionary containing:

        mood
        stress_level
        energy_level
        physical_activity
        focus
        social_connection
        self_care

    sleep_hours : float, optional

        Number of hours slept.

    meditation_minutes : float, optional

        Number of minutes spent meditating.

        Meditation contribution is capped at 13 minutes
        for the daily wellness score.

    Returns
    -------
    dict

        Dictionary containing:

        - Questionnaire score
        - Overall wellness score
        - Wellness category
        - Component scores
        - Personalized recommendations
        - Disclaimer
    """


    # ========================================================
    # REQUIRED QUESTIONS
    # ========================================================

    required_questions = [

        "mood",

        "stress_level",

        "energy_level",

        "physical_activity",

        "focus",

        "social_connection",

        "self_care"
    ]


    # ========================================================
    # VALIDATE ANSWERS
    # ========================================================

    for question in required_questions:

        if question not in answers:

            raise ValueError(
                f"Missing answer for question: {question}"
            )


    # ========================================================
    # QUESTIONNAIRE SCORE
    # ========================================================

    questionnaire_score = (
        calculate_questionnaire_score(
            answers
        )
    )


    # ========================================================
    # EXTRACT ANSWERS
    # ========================================================

    mood = answers["mood"]

    stress_level = (
        answers["stress_level"]
    )

    energy_level = (
        answers["energy_level"]
    )

    physical_activity = (
        answers["physical_activity"]
    )

    focus = (
        answers["focus"]
    )

    social_connection = (
        answers["social_connection"]
    )

    self_care = (
        answers["self_care"]
    )


    # ========================================================
    # VALIDATE MEDITATION MINUTES
    # ========================================================

    if meditation_minutes is None:

        meditation_minutes = 0


    if meditation_minutes < 0:

        raise ValueError(
            "Meditation minutes cannot be negative."
        )


    # ========================================================
    # CAP MEDITATION AT 13 MINUTES
    # ========================================================

    scored_meditation_minutes = min(
        meditation_minutes,
        13
    )


    # ========================================================
    # OVERALL WELLNESS SCORE
    # ========================================================

    wellness_result = (
        calculate_wellness_score(

            sleep_hours=sleep_hours,

            meditation_minutes=(
                scored_meditation_minutes
            ),

            mood=mood,

            stress_level=stress_level,

            energy_level=energy_level,

            physical_activity=(
                physical_activity
            ),

            focus=focus,

            # wellness_scoring.py currently
            # uses the parameter name "social"
            social=social_connection,

            self_care=self_care
        )
    )


    # ========================================================
    # CONVERT STRESS SCALE
    # ========================================================

    """
    Questionnaire stress scale:

    1 = Very High Stress
    2 = High Stress
    3 = Moderate Stress
    4 = Low Stress
    5 = Very Low Stress


    Recommendation engine expects:

    Higher number = Higher Stress


    Therefore:

    Questionnaire 1 -> Recommendation 5
    Questionnaire 2 -> Recommendation 4
    Questionnaire 3 -> Recommendation 3
    Questionnaire 4 -> Recommendation 2
    Questionnaire 5 -> Recommendation 1
    """

    recommendation_stress_level = (
        6 - stress_level
    )


    # ========================================================
    # GENERATE RECOMMENDATIONS
    # ========================================================

    recommendation_result = (
        generate_recommendations(

            wellness_result,

            sleep_hours=sleep_hours,

            stress_level=(
                recommendation_stress_level
            ),

            meditation_minutes=(
                meditation_minutes
            )
        )
    )


    # ========================================================
    # RETURN COMPLETE RESULT
    # ========================================================

    return {

        "questionnaire_score":
            questionnaire_score,

        "wellness_score":
            wellness_result.get(
                "wellness_score"
            ),

        "category":
            wellness_result.get(
                "category"
            ),

        "components":
            wellness_result.get(
                "components"
            ),

        "meditation_minutes":
            meditation_minutes,

        "scored_meditation_minutes":
            scored_meditation_minutes,

        "recommendations":
            recommendation_result.get(
                "recommendations"
            ),

        "disclaimer":
            recommendation_result.get(
                "disclaimer"
            )
    }


# ============================================================
# DISPLAY WELLNESS RESULT
# ============================================================

def display_wellness_result(
    result
):
    """
    Display the complete wellness workflow result.
    """


    print(
        "\n" + "=" * 60
    )

    print(
        "COMPLETE DAILY WELLNESS ANALYTICS RESULT"
    )

    print(
        "=" * 60
    )


    # ========================================================
    # QUESTIONNAIRE SCORE
    # ========================================================

    print(
        f"\nQuestionnaire Score: "
        f"{result['questionnaire_score']}/60"
    )


    # ========================================================
    # OVERALL WELLNESS SCORE
    # ========================================================

    print(
        f"Overall Wellness Score: "
        f"{result['wellness_score']}/100"
    )


    # ========================================================
    # WELLNESS CATEGORY
    # ========================================================

    print(
        f"Wellness Category: "
        f"{result['category']}"
    )


    # ========================================================
    # MEDITATION
    # ========================================================

    print(
        f"\nMeditation Completed: "
        f"{result['meditation_minutes']} minutes"
    )

    print(
        f"Meditation Counted for Score: "
        f"{result['scored_meditation_minutes']} minutes "
        f"(maximum daily target: 13 minutes)"
    )


    # ========================================================
    # COMPONENT SCORES
    # ========================================================

    print(
        "\nComponent Scores:"
    )


    components = (
        result.get(
            "components",
            {}
        )
    )


    for component, data in (
        components.items()
    ):

        print(
            f"- {component.title()}: "
            f"{data['score']}/"
            f"{data['maximum']}"
        )


    # ========================================================
    # PERSONALIZED RECOMMENDATIONS
    # ========================================================

    print(
        "\nPersonalized Recommendations:"
    )


    recommendations = (
        result.get(
            "recommendations",
            []
        )
    )


    for number, recommendation in enumerate(
        recommendations,
        start=1
    ):

        print(
            f"{number}. "
            f"{recommendation}"
        )


    # ========================================================
    # DISCLAIMER
    # ========================================================

    print(
        "\nDisclaimer:"
    )

    print(
        result["disclaimer"]
    )


    print(
        "\n" + "=" * 60
    )


# ============================================================
# TEST PROGRAM
# ============================================================

if __name__ == "__main__":


    # ========================================================
    # DISPLAY QUESTIONNAIRE
    # ========================================================

    print(
        "\nDAILY WELLNESS QUESTIONNAIRE"
    )

    print(
        "=" * 60
    )


    questions = (
        get_questionnaire_questions()
    )


    for number, question in enumerate(
        questions,
        start=1
    ):

        print(
            f"\n{number}. "
            f"{question['question']}"
        )


        for value, option in (
            question["options"].items()
        ):

            print(
                f"   {value}. "
                f"{option}"
            )


    # ========================================================
    # SAMPLE ANSWERS
    # ========================================================

    sample_answers = {

        "mood": 4,

        "stress_level": 3,

        "energy_level": 4,

        "physical_activity": 3,

        "focus": 4,

        "social_connection": 3,

        "self_care": 4
    }


    # ========================================================
    # SAMPLE SLEEP
    # ========================================================

    sample_sleep_hours = 7.5


    # ========================================================
    # SAMPLE MEDITATION
    # ========================================================

    sample_meditation_minutes = 13


    # ========================================================
    # RUN COMPLETE WORKFLOW
    # ========================================================

    result = (
        run_wellness_workflow(

            answers=sample_answers,

            sleep_hours=(
                sample_sleep_hours
            ),

            meditation_minutes=(
                sample_meditation_minutes
            )
        )
    )


    # ========================================================
    # DISPLAY RESULT
    # ========================================================

    display_wellness_result(
        result
    )