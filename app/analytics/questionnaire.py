"""
Daily Wellness Questionnaire

This module defines a simple educational wellness questionnaire
and calculates a questionnaire wellness score.

IMPORTANT:
This is NOT a medical diagnostic tool. It is a project-specific
wellness tracking questionnaire.
"""


# ============================================================
# DAILY WELLNESS QUESTIONS
# ============================================================

QUESTIONS = [

    # --------------------------------------------------------
    # MOOD
    # Higher score = better wellness
    # --------------------------------------------------------
    {
        "id": "mood",
        "question": "How would you describe your overall mood today?",
        "options": {
            1: "Very Poor",
            2: "Poor",
            3: "Neutral",
            4: "Good",
            5: "Very Good"
        }
    },


    # --------------------------------------------------------
    # STRESS
    # Higher score = lower stress = better wellness
    # --------------------------------------------------------
    {
        "id": "stress_level",
        "question": "How stressed did you feel today?",
        "options": {
            1: "Very High",
            2: "High",
            3: "Moderate",
            4: "Low",
            5: "Very Low"
        }
    },


    # --------------------------------------------------------
    # ENERGY
    # Higher score = better wellness
    # --------------------------------------------------------
    {
        "id": "energy_level",
        "question": "How would you rate your energy level today?",
        "options": {
            1: "Very Low",
            2: "Low",
            3: "Moderate",
            4: "High",
            5: "Very High"
        }
    },


    # --------------------------------------------------------
    # PHYSICAL ACTIVITY
    # --------------------------------------------------------
    {
        "id": "physical_activity",
        "question": "How physically active were you today?",
        "options": {
            1: "Not Active",
            2: "Slightly Active",
            3: "Moderately Active",
            4: "Active",
            5: "Very Active"
        }
    },


    # --------------------------------------------------------
    # FOCUS
    # --------------------------------------------------------
    {
        "id": "focus",
        "question": "How well were you able to concentrate today?",
        "options": {
            1: "Very Poorly",
            2: "Poorly",
            3: "Moderately",
            4: "Well",
            5: "Very Well"
        }
    },


    # --------------------------------------------------------
    # SOCIAL CONNECTION
    # --------------------------------------------------------
    {
        "id": "social_connection",
        "question": (
            "How connected did you feel with "
            "other people today?"
        ),
        "options": {
            1: "Not Connected",
            2: "Slightly Connected",
            3: "Moderately Connected",
            4: "Connected",
            5: "Very Connected"
        }
    },


    # --------------------------------------------------------
    # SELF-CARE
    # --------------------------------------------------------
    {
        "id": "self_care",
        "question": (
            "How satisfied are you with the time "
            "you gave yourself for self-care today?"
        ),
        "options": {
            1: "Very Dissatisfied",
            2: "Dissatisfied",
            3: "Neutral",
            4: "Satisfied",
            5: "Very Satisfied"
        }
    }
]


# ============================================================
# GET QUESTIONNAIRE QUESTIONS
# ============================================================

def get_questionnaire_questions():
    """
    Return all daily wellness questionnaire questions.
    """

    return QUESTIONS


# ============================================================
# VALIDATE ANSWERS
# ============================================================

def validate_questionnaire_answers(answers):
    """
    Validate questionnaire answers.

    Every question must have an integer answer
    between 1 and 5.
    """

    if not isinstance(answers, dict):

        raise ValueError(
            "Answers must be provided as a dictionary."
        )


    question_ids = [

        question["id"]

        for question in QUESTIONS
    ]


    for question_id in question_ids:

        if question_id not in answers:

            raise ValueError(

                f"Missing answer for question: "
                f"{question_id}"

            )


        answer = answers[question_id]


        # Check answer type

        if not isinstance(answer, int):

            raise ValueError(

                f"Answer for {question_id} "
                f"must be an integer between 1 and 5."

            )


        # Check answer range

        if answer < 1 or answer > 5:

            raise ValueError(

                f"Answer for {question_id} "
                f"must be between 1 and 5."

            )


    return True


# ============================================================
# CALCULATE QUESTIONNAIRE SCORE
# ============================================================

def calculate_questionnaire_score(answers):
    """
    Calculate questionnaire wellness score out of 60.

    There are 7 questions.

    Each answer uses a scale from 1 to 5.

    IMPORTANT:

    All question scales are designed so that
    higher values represent better wellness.

    For stress:

    1 = Very High Stress
    5 = Very Low Stress

    Therefore, no additional reverse scoring
    is required.

    The questionnaire score is converted
    to a 0-60 scale.
    """


    # --------------------------------------------------------
    # VALIDATE ANSWERS
    # --------------------------------------------------------

    validate_questionnaire_answers(
        answers
    )


    # --------------------------------------------------------
    # CALCULATE RAW TOTAL
    # --------------------------------------------------------

    total = sum(

        answers[question["id"]]

        for question in QUESTIONS

    )


    # --------------------------------------------------------
    # SCORE LIMITS
    # --------------------------------------------------------

    minimum_raw_score = len(QUESTIONS) * 1

    maximum_raw_score = len(QUESTIONS) * 5


    # --------------------------------------------------------
    # CONVERT TO 0-60 SCALE
    # --------------------------------------------------------

    questionnaire_score = (

        (
            total - minimum_raw_score
        )

        /

        (
            maximum_raw_score
            - minimum_raw_score
        )

    ) * 60


    return round(

        questionnaire_score,

        2

    )


# ============================================================
# GET QUESTIONNAIRE SUMMARY
# ============================================================

def get_questionnaire_summary(answers):
    """
    Return validated answers and the calculated
    questionnaire wellness score.
    """


    score = calculate_questionnaire_score(
        answers
    )


    return {

        "answers": answers,

        "questionnaire_score": score,

        "maximum_score": 60,

        "message": (

            "This questionnaire provides a "
            "project-specific, non-diagnostic "
            "wellness indicator for educational "
            "wellness tracking."

        )

    }


# ============================================================
# TEST PROGRAM
# ============================================================

if __name__ == "__main__":


    # --------------------------------------------------------
    # SAMPLE ANSWERS
    # --------------------------------------------------------

    sample_answers = {

        "mood": 4,

        "stress_level": 4,

        "energy_level": 3,

        "physical_activity": 3,

        "focus": 4,

        "social_connection": 3,

        "self_care": 4

    }


    # --------------------------------------------------------
    # DISPLAY HEADER
    # --------------------------------------------------------

    print("\n" + "=" * 55)

    print(
        "DAILY WELLNESS QUESTIONNAIRE TEST"
    )

    print("=" * 55)


    # --------------------------------------------------------
    # DISPLAY QUESTIONS
    # --------------------------------------------------------

    print(
        "\nQUESTIONNAIRE QUESTIONS:\n"
    )


    for number, question in enumerate(

        QUESTIONS,

        start=1

    ):

        print(

            f"{number}. "

            f"{question['question']}"

        )


    # --------------------------------------------------------
    # CALCULATE SCORE
    # --------------------------------------------------------

    score = calculate_questionnaire_score(

        sample_answers

    )


    # --------------------------------------------------------
    # DISPLAY SAMPLE ANSWERS
    # --------------------------------------------------------

    print("\n" + "-" * 55)

    print(
        "SAMPLE ANSWERS:"
    )


    for question_id, answer in (

        sample_answers.items()

    ):

        print(

            f"{question_id}: "

            f"{answer}/5"

        )


    # --------------------------------------------------------
    # DISPLAY SCORE
    # --------------------------------------------------------

    print(
        "\nQUESTIONNAIRE WELLNESS SCORE:"
    )

    print(
        f"{score}/60"
    )


    # --------------------------------------------------------
    # DISCLAIMER
    # --------------------------------------------------------

    print(
        "\nDisclaimer:"
    )

    print(

        "This questionnaire provides a "
        "project-specific, non-diagnostic wellness "
        "indicator for educational wellness "
        "tracking purposes."

    )


    print(
        "\n" + "=" * 55
    )