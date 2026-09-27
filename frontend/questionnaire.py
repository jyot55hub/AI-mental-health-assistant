import streamlit as st
from datetime import date

from app.backend.questionnaire import (
    save_questionnaire_response,
    get_questionnaire_response,
    update_questionnaire_response
)


# ============================================================
# DAILY CHECK-IN QUESTIONS
# ============================================================

QUESTIONS = [
    {
        "id": "mood",
        "question": "How would you rate your overall mood today?",
        "help": "1 = Very low, 5 = Very positive"
    },
    {
        "id": "stress_level",
        "question": "How well did you manage your stress today?",
        "help": "1 = Not well, 5 = Very well"
    },
    {
        "id": "energy_level",
        "question": "How would you rate your energy level today?",
        "help": "1 = Very low, 5 = Very high"
    },
    {
        "id": "physical_activity",
        "question": "How active were you today?",
        "help": "1 = Not active, 5 = Very active"
    },
    {
        "id": "focus",
        "question": "How well were you able to focus today?",
        "help": "1 = Very difficult, 5 = Very easy"
    },
    {
        "id": "social_connection",
        "question": "How connected did you feel to others today?",
        "help": "1 = Not connected, 5 = Very connected"
    },
    {
        "id": "self_care",
        "question": "How well did you take care of yourself today?",
        "help": "1 = Not well, 5 = Very well"
    }
]


# ============================================================
# QUESTIONNAIRE-SPECIFIC STYLING
# ============================================================

def apply_questionnaire_styles():
    """
    Apply styling specifically to the questionnaire page.

    The main issue being fixed here is the
    'Save Today's Check-in' button becoming too dark
    and unreadable when White theme is selected.
    """

    theme = st.session_state.get("theme", "Dark")

    # ========================================================
    # DARK THEME
    # ========================================================

    if theme == "Dark":

        st.markdown(
            """
            <style>

            /* ================================================
               SAVE CHECK-IN BUTTON
            ================================================ */

            div[data-testid="stFormSubmitButton"] > button {
                background-color: #161922 !important;
                color: #ffffff !important;
                border: 1px solid rgba(255,255,255,0.16) !important;
                font-weight: 600 !important;
            }

            div[data-testid="stFormSubmitButton"] > button:hover {
                background-color: #315943 !important;
                color: #ffffff !important;
                border-color: #315943 !important;
            }

            div[data-testid="stFormSubmitButton"] > button p {
                color: #ffffff !important;
            }

            </style>
            """,
            unsafe_allow_html=True
        )

        return


    # ========================================================
    # WHITE THEME
    # ========================================================

    if theme == "White":

        st.markdown(
            """
            <style>

            /* ================================================
               SAVE CHECK-IN BUTTON
            ================================================ */

            div[data-testid="stFormSubmitButton"] > button {
                background-color: #ffffff !important;
                color: #1f2937 !important;
                border: 1px solid rgba(0,0,0,0.20) !important;
                font-weight: 600 !important;
                box-shadow: none !important;
            }

            div[data-testid="stFormSubmitButton"] > button:hover {
                background-color: #eef6f0 !important;
                color: #315943 !important;
                border-color: #315943 !important;
            }

            div[data-testid="stFormSubmitButton"] > button p {
                color: #1f2937 !important;
            }

            div[data-testid="stFormSubmitButton"] > button:hover p {
                color: #315943 !important;
            }

            </style>
            """,
            unsafe_allow_html=True
        )

        return


    # ========================================================
    # DEVICE THEME
    # ========================================================

    if theme == "Device":

        st.markdown(
            """
            <style>

            /* ================================================
               DEFAULT DEVICE / DARK
            ================================================ */

            div[data-testid="stFormSubmitButton"] > button {
                background-color: #161922 !important;
                color: #ffffff !important;
                border: 1px solid rgba(255,255,255,0.16) !important;
                font-weight: 600 !important;
            }

            div[data-testid="stFormSubmitButton"] > button p {
                color: #ffffff !important;
            }

            div[data-testid="stFormSubmitButton"] > button:hover {
                background-color: #315943 !important;
                color: #ffffff !important;
                border-color: #315943 !important;
            }

            div[data-testid="stFormSubmitButton"] > button:hover p {
                color: #ffffff !important;
            }


            /* ================================================
               DEVICE LIGHT MODE
            ================================================ */

            @media (prefers-color-scheme: light) {

                div[data-testid="stFormSubmitButton"] > button {
                    background-color: #ffffff !important;
                    color: #1f2937 !important;
                    border: 1px solid rgba(0,0,0,0.20) !important;
                    font-weight: 600 !important;
                    box-shadow: none !important;
                }

                div[data-testid="stFormSubmitButton"] > button p {
                    color: #1f2937 !important;
                }

                div[data-testid="stFormSubmitButton"] > button:hover {
                    background-color: #eef6f0 !important;
                    color: #315943 !important;
                    border-color: #315943 !important;
                }

                div[data-testid="stFormSubmitButton"] > button:hover p {
                    color: #315943 !important;
                }

            }

            </style>
            """,
            unsafe_allow_html=True
        )


# ============================================================
# DAILY CHECK-IN PAGE
# ============================================================

def show_questionnaire():
    """Display and save the seven-question daily check-in."""

    # --------------------------------------------------------
    # APPLY QUESTIONNAIRE STYLING
    # --------------------------------------------------------

    apply_questionnaire_styles()

    # --------------------------------------------------------
    # GET LOGGED-IN USER
    # --------------------------------------------------------

    user = st.session_state.get("user", {})

    user_id = user.get("id") or user.get("user_id")

    if user_id is None:

        st.error(
            "Unable to identify the logged-in user."
        )

        return

    today = date.today().isoformat()


    # ========================================================
    # HEADER
    # ========================================================

    st.title("📝 Daily Check-in")

    st.write(
        "Take a moment to reflect on your well-being today. "
        "There are no right or wrong answers."
    )

    st.caption(
        f"Date: {today}"
    )


    # ========================================================
    # CHECK FOR EXISTING RESPONSE
    # ========================================================

    existing_result = get_questionnaire_response(
        user_id,
        today
    )

    existing_record = None

    if existing_result.get("success"):

        existing_record = existing_result.get(
            "record"
        )

    if existing_record:

        st.info(
            "You have already completed today's check-in. "
            "You can update your responses below."
        )


    # ========================================================
    # QUESTIONNAIRE FORM
    # ========================================================

    with st.form("daily_checkin_form"):

        answers = {}


        # ----------------------------------------------------
        # DISPLAY ALL SEVEN QUESTIONS
        # ----------------------------------------------------

        for index, question_data in enumerate(QUESTIONS):

            question_id = question_data["id"]


            # ------------------------------------------------
            # QUESTION
            # ------------------------------------------------

            st.markdown(
                f"### {index + 1}. "
                f"{question_data['question']}"
            )


            # ------------------------------------------------
            # HELP TEXT
            # ------------------------------------------------

            st.caption(
                question_data["help"]
            )


            # ------------------------------------------------
            # DEFAULT ANSWER
            #
            # NEW QUESTIONNAIRE:
            #     index=None
            #
            # EXISTING QUESTIONNAIRE:
            #     previously saved answer selected
            # ------------------------------------------------

            default_index = None

            if existing_record:

                previous_answer = existing_record.get(
                    question_id
                )

                if previous_answer is not None:

                    try:

                        default_index = (
                            int(previous_answer) - 1
                        )

                    except (
                        ValueError,
                        TypeError,
                    ):

                        default_index = None


            # ------------------------------------------------
            # RADIO OPTIONS
            # ------------------------------------------------

            answers[question_id] = st.radio(
                "Choose an answer:",
                options=[1, 2, 3, 4, 5],
                index=default_index,
                horizontal=True,
                key=f"checkin_{question_id}"
            )


            # ------------------------------------------------
            # SEPARATOR
            # ------------------------------------------------

            if index < len(QUESTIONS) - 1:

                st.divider()


        st.write("")


        # ====================================================
        # SAVE BUTTON
        # ====================================================

        submitted = st.form_submit_button(
            "💚 Save Today's Check-in",
            use_container_width=True
        )


    # ========================================================
    # SAVE / UPDATE RESPONSE
    # ========================================================

    if submitted:


        # ====================================================
        # VALIDATE ALL QUESTIONS
        # ====================================================

        unanswered_questions = []

        for question_data in QUESTIONS:

            question_id = question_data["id"]

            if answers.get(question_id) is None:

                unanswered_questions.append(
                    question_data["question"]
                )


        if unanswered_questions:

            st.warning(
                "Please answer all seven questions "
                "before saving your check-in. "
                "You can also choose 'Skip for now'."
            )


        else:


            # =================================================
            # UPDATE EXISTING RESPONSE
            # =================================================

            if existing_record:

                result = update_questionnaire_response(

                    user_id=user_id,

                    mood=answers["mood"],

                    stress_level=answers["stress_level"],

                    energy_level=answers["energy_level"],

                    physical_activity=answers[
                        "physical_activity"
                    ],

                    focus=answers["focus"],

                    social_connection=answers[
                        "social_connection"
                    ],

                    self_care=answers["self_care"],

                    record_date=today
                )


            # =================================================
            # SAVE NEW RESPONSE
            # =================================================

            else:

                result = save_questionnaire_response(

                    user_id=user_id,

                    mood=answers["mood"],

                    stress_level=answers["stress_level"],

                    energy_level=answers["energy_level"],

                    physical_activity=answers[
                        "physical_activity"
                    ],

                    focus=answers["focus"],

                    social_connection=answers[
                        "social_connection"
                    ],

                    self_care=answers["self_care"],

                    record_date=today
                )


            # =================================================
            # RESULT
            # =================================================

            if result.get("success"):

                st.success(
                    "Your daily check-in has been "
                    "saved successfully! 💚"
                )

                st.session_state["page"] = "dashboard"

                st.rerun()


            else:

                st.error(
                    result.get(
                        "message",
                        "Unable to save your check-in."
                    )
                )


    # ========================================================
    # SKIP CHECK-IN
    # ========================================================

    st.divider()

    if st.button(
        "Skip for now",
        use_container_width=True
    ):

        st.session_state["page"] = "dashboard"

        st.rerun()


    # ========================================================
    # BACK TO DASHBOARD
    # ========================================================

    if st.button(
        "← Back to Dashboard",
        use_container_width=True
    ):

        st.session_state["page"] = "dashboard"

        st.rerun()