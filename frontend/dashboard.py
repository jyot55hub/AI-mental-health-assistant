import streamlit as st
from datetime import date

from app.backend.questionnaire import (
    get_questionnaire_response
)

from app.backend.sleep import (
    get_sleep_record
)

from app.backend.meditation import (
    get_meditation_record
)

from app.backend.wellness import (
    calculate_and_save_wellness_score,
    get_wellness_score
)


# ============================================================
# DAILY MOTIVATIONAL THOUGHT
# ============================================================

def show_daily_motivation():
    """
    Display an attractive daily motivational thought.

    The thought changes automatically based on the day.
    The same thought appears throughout the day.
    """

    thoughts = [
        (
            "✨ 🌿 ✨",
            "A thought for today",
            "You are doing better than you think. 🌱",
            "A little reminder for your well-being 💚"
        ),
        (
            "🌸 ☀️ 🌸",
            "Your daily reminder",
            "Small steps every day lead to meaningful change. 🌷",
            "Be kind to yourself today. 💚"
        ),
        (
            "🌻 💫 🌻",
            "A moment for you",
            "You deserve rest, peace, and happiness. 🌼",
            "Take things one step at a time. 💚"
        ),
        (
            "🌈 🌿 🌈",
            "Today's encouragement",
            "Every day is a new opportunity to care for yourself.",
            "Your feelings matter. Always. 💚"
        ),
        (
            "🦋 ✨ 🦋",
            "A gentle reminder",
            "You don't have to be perfect to make progress.",
            "Give yourself the patience you deserve. 💚"
        ),
        (
            "🌙 💚 🌙",
            "Today's thought",
            "Rest is not a reward. It is part of taking care of yourself.",
            "Make time for yourself today. 🌿"
        ),
        (
            "🌱 ☀️ 🌱",
            "A little encouragement",
            "Believe in the small changes you make every day.",
            "You are worth taking care of. 💚"
        )
    ]

    today_index = date.today().toordinal() % len(thoughts)

    icon, heading, message, reminder = thoughts[today_index]

    motivation_html = (
        '<div style="'
        'background: linear-gradient(135deg, #e8f5e9, #e8eaf6);'
        'padding: 30px;'
        'border-radius: 20px;'
        'text-align: center;'
        'margin: 20px 0 30px 0;'
        'box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);'
        '">'
        '<div style="font-size: 38px; margin-bottom: 12px;">'
        f'{icon}'
        '</div>'
        '<div style="'
        'color: #47705a;'
        'font-size: 13px;'
        'font-weight: 700;'
        'letter-spacing: 1.5px;'
        'text-transform: uppercase;'
        'margin-bottom: 16px;'
        '">'
        f'{heading}'
        '</div>'
        '<div style="'
        'color: #244d39;'
        'font-size: 24px;'
        'font-weight: 600;'
        'line-height: 1.5;'
        '">'
        f'{message}'
        '</div>'
        '<div style="'
        'color: #789582;'
        'font-size: 13px;'
        'margin-top: 20px;'
        'letter-spacing: 0.5px;'
        '">'
        f'{reminder}'
        '</div>'
        '</div>'
    )

    st.markdown(motivation_html, unsafe_allow_html=True)


# ============================================================
# WELLNESS SCORE CARD
# ============================================================

def show_wellness_score_card(user_id):
    """
    Display the daily wellness score.

    The score is calculated only when all three required
    records exist for the same day:

    1. Seven-question questionnaire
    2. Sleep record
    3. Meditation record
    """

    today = date.today().isoformat()

    st.subheader("💚 Your Wellness Score")

    # --------------------------------------------------------
    # GET TODAY'S RECORDS
    # --------------------------------------------------------

    questionnaire_result = get_questionnaire_response(
        user_id,
        today
    )

    sleep_result = get_sleep_record(
        user_id,
        today
    )

    meditation_result = get_meditation_record(
        user_id,
        today
    )

    # --------------------------------------------------------
    # CHECK QUESTIONNAIRE COMPLETION
    # --------------------------------------------------------

    questionnaire_record = None

    if questionnaire_result.get("success"):
        questionnaire_record = questionnaire_result.get("record")

    required_questions = [
        "mood",
        "stress_level",
        "energy_level",
        "physical_activity",
        "focus",
        "social_connection",
        "self_care"
    ]

    questionnaire_complete = (
        questionnaire_record is not None
        and all(
            questionnaire_record.get(question) is not None
            for question in required_questions
        )
    )

    # --------------------------------------------------------
    # CHECK SLEEP AND MEDITATION
    # --------------------------------------------------------

    sleep_record = None

    if sleep_result.get("success"):
        sleep_record = sleep_result.get("record")

    meditation_record = None

    if meditation_result.get("success"):
        meditation_record = meditation_result.get("record")

    sleep_complete = (
        sleep_record is not None
        and sleep_record.get("sleep_hours") is not None
    )

    meditation_complete = (
        meditation_record is not None
        and meditation_record.get("meditation_minutes") is not None
    )

    # --------------------------------------------------------
    # SHOW DATA COMPLETION STATUS
    # --------------------------------------------------------

    if not (
        questionnaire_complete
        and sleep_complete
        and meditation_complete
    ):

        st.info(
            "Your wellness score is not ready yet. "
            "Complete all three daily activities to "
            "calculate your score."
        )

        st.write("### Today's progress")

        st.checkbox(
            "Daily questionnaire completed",
            value=questionnaire_complete,
            disabled=True,
            key="wellness_questionnaire_status"
        )

        st.checkbox(
            "Sleep tracking completed",
            value=sleep_complete,
            disabled=True,
            key="wellness_sleep_status"
        )

        st.checkbox(
            "Meditation completed",
            value=meditation_complete,
            disabled=True,
            key="wellness_meditation_status"
        )

        st.caption(
            "Your score will appear here once all three "
            "records are available for today."
        )

        return

    # --------------------------------------------------------
    # CALCULATE SCORE USING EXISTING BACKEND
    # --------------------------------------------------------

    score_result = calculate_and_save_wellness_score(
        user_id=user_id,
        record_date=today
    )

    if not score_result.get("success"):

        # If a score already exists, display the saved score
        existing_score = get_wellness_score(
            user_id,
            today
        )

        if existing_score.get("success"):

            score_record = existing_score.get("record", {})

            wellness_score = score_record.get("wellness_score")

            category = score_record.get(
                "category",
                "Not available"
            )

        else:

            st.warning(
                score_result.get(
                    "message",
                    "Unable to calculate your wellness score."
                )
            )

            return

    else:

        wellness_score = score_result.get("wellness_score")

        category = score_result.get(
            "category",
            "Not available"
        )

    # --------------------------------------------------------
    # DISPLAY WELLNESS SCORE
    # --------------------------------------------------------

    if wellness_score is None:

        st.info(
            "Your wellness score is not available yet."
        )

        return

    st.success(
        "Your wellness score for today is ready!"
    )

    score_col1, score_col2 = st.columns(2)

    with score_col1:

        st.metric(
            label="Daily Wellness Score",
            value=f"{float(wellness_score):.1f} / 100"
        )

    with score_col2:

        st.metric(
            label="Wellness Category",
            value=str(category)
        )

    # Visual score indicator
    st.progress(
        min(
            max(float(wellness_score) / 100, 0.0),
            1.0
        )
    )

    st.caption(
        "This is a project-specific, non-diagnostic "
        "wellness indicator."
    )

    # --------------------------------------------------------
    # SHOW COMPONENT BREAKDOWN
    # --------------------------------------------------------

    with st.expander("View score breakdown"):

        st.write(
            "Your score combines the following components:"
        )

        st.write("🌙 Sleep — Maximum 25 points")
        st.write("🧘 Meditation — Maximum 15 points")
        st.write("📝 Questionnaire — Maximum 60 points")

        st.caption(
            "The score is normalized to a range of 0–100."
        )


# ============================================================
# MAIN DASHBOARD
# ============================================================

def show_dashboard():
    """Display the MindCare dashboard."""

    user = st.session_state.get("user", {})

    user_name = user.get("name", "there")

    # --------------------------------------------------------
    # GET USER ID
    # --------------------------------------------------------

    user_id = user.get("id")

    if user_id is None:
        user_id = user.get("user_id")

    # --------------------------------------------------------
    # HEADER
    # --------------------------------------------------------

    header_html = (
        '<div class="dashboard-header">'
        '<span class="brand-icon">🌿</span>'
        f'<h1>Good to see you, {user_name}!</h1>'
        '<p>Take a moment for yourself today.</p>'
        '</div>'
    )

    st.markdown(header_html, unsafe_allow_html=True)

    st.divider()

    # --------------------------------------------------------
    # WELCOME CARD
    # --------------------------------------------------------

    welcome_html = (
        '<div class="welcome-card">'
        '<h2>How are you feeling today? 💚</h2>'
        '<p>Your well-being matters. Take small steps '
        'toward a healthier, calmer you.</p>'
        '</div>'
    )

    st.markdown(welcome_html, unsafe_allow_html=True)

    # --------------------------------------------------------
    # DAILY MOTIVATIONAL THOUGHT
    # --------------------------------------------------------

    show_daily_motivation()

    # --------------------------------------------------------
    # WELLNESS SCORE CARD
    # --------------------------------------------------------

    if user_id is not None:
        show_wellness_score_card(user_id)
    else:
        st.warning(
            "Unable to identify the logged-in user."
        )

    st.divider()

    # --------------------------------------------------------
    # WELLNESS SPACE
    # --------------------------------------------------------

    st.subheader("Your wellness space")

    col1, col2 = st.columns(2)

    with col1:

        st.markdown("### 📝 Daily Check-in")

        st.write(
            "Reflect on your mood and daily well-being."
        )

        if st.button(
            "Start check-in",
            use_container_width=True,
            key="dashboard_start_checkin"
        ):

            st.session_state["page"] = "questionnaire"
            st.rerun()

    with col2:

        st.markdown("### 🌙 Sleep Tracking")

        st.write(
            "Keep track of your sleep and rest."
        )

        if st.button(
            "Track sleep",
            use_container_width=True,
            key="dashboard_track_sleep"
        ):

            st.session_state["page"] = "sleep_tracking"
            st.rerun()

    col3, col4 = st.columns(2)

    with col3:

        st.markdown("### 🧘 Meditation")

        st.write(
            "Make time for mindfulness and relaxation."
        )

        if st.button(
            "Open meditation",
            use_container_width=True,
            key="dashboard_open_meditation"
        ):
            st.session_state["page"] = "meditation"
            st.rerun()

    with col4:

        st.markdown("### 🤖 MindCare Chat")

        st.write(
            "Talk to your AI mental health assistant."
        )

        if st.button(
            "Open chatbot",
            use_container_width=True,
            key="dashboard_open_chatbot"
        ):

            st.session_state["page"] = "chatbot"
            st.rerun()

    # --------------------------------------------------------
    # FOOTER
    # --------------------------------------------------------

    st.divider()

    st.caption(
        "MindCare provides wellness support and is not a "
        "replacement for professional mental health care."
    )

    # --------------------------------------------------------
    # LOGOUT
    # --------------------------------------------------------

    if st.button(
        "Log out",
        use_container_width=True,
        key="dashboard_logout"
    ):

        st.session_state["logged_in"] = False

        st.session_state.pop(
            "user",
            None
        )

        st.session_state["page"] = "login"

        st.rerun()