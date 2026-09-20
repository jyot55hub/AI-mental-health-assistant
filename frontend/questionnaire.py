
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
# DAILY CHECK-IN PAGE
# ============================================================

def show_questionnaire():
    """Display and save the seven-question daily check-in."""

    user = st.session_state.get("user", {})
    user_id = user.get("id") or user.get("user_id")

    if user_id is None:
        st.error("Unable to identify the logged-in user.")
        return

    today = date.today().isoformat()

    # --------------------------------------------------------
    # HEADER
    # --------------------------------------------------------

    st.title("📝 Daily Check-in")

    st.write(
        "Take a moment to reflect on your well-being today. "
        "There are no right or wrong answers."
    )

    st.caption(f"Date: {today}")

    # --------------------------------------------------------
    # CHECK FOR AN EXISTING RESPONSE
    # --------------------------------------------------------

    existing_result = get_questionnaire_response(
        user_id,
        today
    )

    existing_record = None

    if existing_result.get("success"):
        existing_record = existing_result.get("record")

    if existing_record:
        st.info(
            "You have already completed today's check-in. "
            "You can update your responses below."
        )

    # --------------------------------------------------------
    # QUESTIONNAIRE FORM
    # --------------------------------------------------------

    with st.form("daily_checkin_form"):

        answers = {}

        for index, question_data in enumerate(QUESTIONS):

            question_id = question_data["id"]

            st.markdown(
                f"### {index + 1}. {question_data['question']}"
            )

            st.caption(question_data["help"])

            # Use the existing answer as the default when available.
            default_index = 0

            if existing_record:
                previous_answer = existing_record.get(question_id)

                if previous_answer is not None:
                    default_index = int(previous_answer) - 1

            answers[question_id] = st.radio(
                "Choose an answer:",
                options=[1, 2, 3, 4, 5],
                index=default_index,
                horizontal=True,
                key=f"checkin_{question_id}"
            )

            if index < len(QUESTIONS) - 1:
                st.divider()

        st.write("")

        submitted = st.form_submit_button(
            "💚 Save Today's Check-in",
            use_container_width=True
        )

    # --------------------------------------------------------
    # SAVE OR UPDATE RESPONSE
    # --------------------------------------------------------

    if submitted:

        if existing_record:

            result = update_questionnaire_response(
                user_id=user_id,
                mood=answers["mood"],
                stress_level=answers["stress_level"],
                energy_level=answers["energy_level"],
                physical_activity=answers["physical_activity"],
                focus=answers["focus"],
                social_connection=answers["social_connection"],
                self_care=answers["self_care"],
                record_date=today
            )

        else:

            result = save_questionnaire_response(
                user_id=user_id,
                mood=answers["mood"],
                stress_level=answers["stress_level"],
                energy_level=answers["energy_level"],
                physical_activity=answers["physical_activity"],
                focus=answers["focus"],
                social_connection=answers["social_connection"],
                self_care=answers["self_care"],
                record_date=today
            )

        if result.get("success"):

            st.success(
                "Your daily check-in has been saved successfully! 💚"
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

    # --------------------------------------------------------
    # SKIP CHECK-IN
    # --------------------------------------------------------

    st.divider()

    if st.button(
        "Skip for now",
        use_container_width=True
    ):

        st.session_state["page"] = "dashboard"
        st.rerun()

    if st.button(
        "← Back to Dashboard",
        use_container_width=True
    ):

        st.session_state["page"] = "dashboard"
        st.rerun()
