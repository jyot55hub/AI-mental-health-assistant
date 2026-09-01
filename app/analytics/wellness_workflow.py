"""
Complete Wellness Analytics Workflow

This module connects:

1. Daily Wellness Questionnaire
2. Questionnaire Scoring
3. Sleep Scoring
4. Overall Wellness Indicator
5. Wellness Category
6. Personalized Recommendations

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
    sleep_hours=None
):
    """
    Run the complete wellness analytics workflow.

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

    sleep_hours : float

        Number of hours slept.

    Returns
    -------
    Dictionary containing:

    - Questionnaire score
    - Overall wellness score
    - Wellness category
    - Component scores
    - Personalized recommendations
    """


    # ========================================================
    # VALIDATE ANSWERS OBJECT
    # ========================================================

    if not isinstance(
        answers,
        dict
    ):
        raise ValueError(
            "Answers must be provided as a dictionary."
        )


    # ========================================================
    # BACKWARD COMPATIBILITY
    # ========================================================

    # Older code may use "social".
    # Convert it to the official questionnaire key
    # "social_connection".

    if (
        "social_connection" not in answers
        and "social" in answers
    ):

        answers = answers.copy()

        answers["social_connection"] = (
            answers["social"]
        )


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
    # OVERALL WELLNESS SCORE
    # ========================================================

    wellness_result = (
        calculate_wellness_score(

            sleep_hours=sleep_hours,

            mood=mood,

            stress_level=stress_level,

            energy_level=energy_level,

            physical_activity=physical_activity,

            focus=focus,

            # wellness_scoring.py currently
            # uses the parameter name "social"
            social=social_connection,

            self_care=self_care
        )
    )


    # ========================================================
    # CONVERT STRESS SCALE FOR RECOMMENDATIONS
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

    try:

        stress_value = float(
            stress_level
        )

        recommendation_stress_level = (
            6 - stress_value
        )

    except (
        ValueError,
        TypeError
    ):

        recommendation_stress_level = None


    # ========================================================
    # GENERATE RECOMMENDATIONS
    # ========================================================

    recommendation_result = (
        generate_recommendations(

            wellness_result,

            sleep_hours=sleep_hours,

            stress_level=(
                recommendation_stress_level
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
                "components",
                {}
            ),

        "recommendations":
            recommendation_result.get(
                "recommendations",
                []
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


    print("\n" + "=" * 60)

    print(
        "COMPLETE WELLNESS ANALYTICS RESULT"
    )

    print("=" * 60)


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
        result.get(
            "disclaimer",
            "This wellness result is for educational purposes only."
        )
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
    # RUN COMPLETE WORKFLOW
    # ========================================================

    result = (
        run_wellness_workflow(

            answers=sample_answers,

            sleep_hours=(
                sample_sleep_hours
            )
        )
    )


    # ========================================================
    # DISPLAY RESULT
    # ========================================================

    display_wellness_result(
        result
    )