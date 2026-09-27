import html
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

# NEW: Existing recommendation engine
from app.analytics.recommendations import (
    generate_recommendations
)


# ============================================================
# THEME HELPERS
# ============================================================

def get_dashboard_theme():

    theme = st.session_state.get(
        "theme",
        "Dark"
    )

    if theme == "White":

        return {
            "card_bg": "#ffffff",
            "soft_bg": "#f8fafc",

            "hero_bg_1": "#eefaf2",
            "hero_bg_2": "#f1f8f5",

            "primary": "#315943",
            "heading": "#1e293b",
            "text": "#475569",
            "muted": "#64748b",

            "border": "#dbe5df",
            "soft_border": "#e2e8f0",

            "green": "#315943",
            "green_soft": "#e8f5e9",

            "pending_bg": "#f8fafc",
            "pending_border": "#cbd5e1",
            "pending_text": "#64748b",

            "score_bg": "#f0fdf4",
            "score_border": "#bbf7d0",

            "action_hover": "#f8fafc",

            "shadow": (
                "0 5px 18px rgba(15, 23, 42, 0.06)"
            )
        }

    if theme == "Dark":

        return {
            "card_bg": "#151922",
            "soft_bg": "#171b24",

            "hero_bg_1": "#15251e",
            "hero_bg_2": "#142329",

            "primary": "#9de0b2",
            "heading": "#f1f5f9",
            "text": "#cbd5e1",
            "muted": "#94a3b8",

            "border": "#303746",
            "soft_border": "#374151",

            "green": "#4ade80",
            "green_soft": "#173222",

            "pending_bg": "#20242e",
            "pending_border": "#4b5563",
            "pending_text": "#a8b3c2",

            "score_bg": "#14261c",
            "score_border": "#28543a",

            "action_hover": "#1b2029",

            "shadow": (
                "0 5px 18px rgba(0, 0, 0, 0.20)"
            )
        }

    # --------------------------------------------------------
    # DEVICE
    # --------------------------------------------------------

    return {
        "card_bg": "#ffffff",
        "soft_bg": "#f8fafc",

        "hero_bg_1": "#eefaf2",
        "hero_bg_2": "#f1f8f5",

        "primary": "#315943",
        "heading": "#1e293b",
        "text": "#475569",
        "muted": "#64748b",

        "border": "#dbe5df",
        "soft_border": "#e2e8f0",

        "green": "#315943",
        "green_soft": "#e8f5e9",

        "pending_bg": "#f8fafc",
        "pending_border": "#cbd5e1",
        "pending_text": "#64748b",

        "score_bg": "#f0fdf4",
        "score_border": "#bbf7d0",

        "action_hover": "#f8fafc",

        "shadow": (
            "0 5px 18px rgba(15, 23, 42, 0.06)"
        )
    }


# ============================================================
# DASHBOARD STYLES
# ============================================================

def apply_dashboard_styles():

    colors = get_dashboard_theme()

    st.markdown(
        f"""
<style>

/* ========================================================
   HERO
   ======================================================== */

.mindcare-hero {{
    background:
        linear-gradient(
            135deg,
            {colors["hero_bg_1"]},
            {colors["hero_bg_2"]}
        );

    border: 1px solid {colors["border"]};

    border-radius: 22px;

    padding: 30px 32px;

    margin: 4px 0 26px 0;

    box-shadow: {colors["shadow"]};

    position: relative;

    overflow: hidden;
}}

.mindcare-hero::after {{
    content: "✦";

    position: absolute;

    right: 32px;

    top: 16px;

    font-size: 68px;

    opacity: 0.07;
}}

.mindcare-hero-icon {{
    font-size: 36px;

    margin-bottom: 6px;
}}

.mindcare-hero-title {{
    color: {colors["heading"]};

    font-size: 32px;

    font-weight: 750;

    margin-bottom: 7px;
}}

.mindcare-hero-subtitle {{
    color: {colors["text"]};

    font-size: 15px;

    line-height: 1.6;

    max-width: 680px;

    margin-bottom: 17px;
}}

.mindcare-hero-badge {{
    display: inline-block;

    background: {colors["card_bg"]};

    color: {colors["primary"]};

    border: 1px solid {colors["border"]};

    border-radius: 999px;

    padding: 7px 13px;

    font-size: 11px;

    font-weight: 750;

    letter-spacing: 1px;

    text-transform: uppercase;
}}


/* ========================================================
   WELCOME
   ======================================================== */

.dashboard-welcome {{
    margin: 4px 0 20px 0;
}}

.dashboard-welcome-label {{
    color: {colors["primary"]};

    font-size: 11px;

    font-weight: 750;

    letter-spacing: 1.4px;

    text-transform: uppercase;

    margin-bottom: 5px;
}}

.dashboard-welcome-title {{
    color: {colors["heading"]};

    font-size: 28px;

    font-weight: 750;

    margin-bottom: 5px;
}}

.dashboard-welcome-text {{
    color: {colors["muted"]};

    font-size: 14px;

    line-height: 1.5;
}}


/* ========================================================
   MOTIVATION
   ======================================================== */

.motivation-card {{
    background:
        linear-gradient(
            135deg,
            {colors["hero_bg_1"]},
            {colors["card_bg"]}
        );

    border: 1px solid {colors["border"]};

    border-radius: 18px;

    padding: 22px 25px;

    margin: 18px 0 25px 0;

    box-shadow: {colors["shadow"]};
}}

.motivation-icon {{
    font-size: 28px;

    margin-bottom: 6px;
}}

.motivation-heading {{
    color: {colors["primary"]};

    font-size: 11px;

    font-weight: 750;

    letter-spacing: 1.3px;

    text-transform: uppercase;

    margin-bottom: 8px;
}}

.motivation-message {{
    color: {colors["heading"]};

    font-size: 20px;

    font-weight: 650;

    line-height: 1.45;
}}

.motivation-reminder {{
    color: {colors["muted"]};

    font-size: 12px;

    margin-top: 10px;
}}


/* ========================================================
   SECTION TITLE
   ======================================================== */

.dashboard-section-title {{
    color: {colors["heading"]};

    font-size: 21px;

    font-weight: 720;

    margin: 20px 0 13px 0;
}}


/* ========================================================
   PROGRESS CARDS
   ======================================================== */

.progress-card {{
    background: {colors["card_bg"]};

    border: 1px solid {colors["border"]};

    border-radius: 15px;

    padding: 17px;

    min-height: 112px;

    box-shadow: {colors["shadow"]};

    transition: transform 0.15s ease;
}}

.progress-card:hover {{
    transform: translateY(-2px);
}}

.progress-icon {{
    font-size: 24px;

    margin-bottom: 6px;
}}

.progress-title {{
    color: {colors["heading"]};

    font-size: 14px;

    font-weight: 700;

    margin-bottom: 6px;
}}

.progress-status-complete {{
    color: {colors["green"]};

    font-size: 12px;

    font-weight: 650;
}}

.progress-status-pending {{
    color: {colors["pending_text"]};

    font-size: 12px;

    font-weight: 600;
}}


/* ========================================================
   WELLNESS SCORE
   ======================================================== */

.score-card {{
    background: {colors["score_bg"]};

    border: 1px solid {colors["score_border"]};

    border-radius: 18px;

    padding: 23px;

    margin: 21px 0 10px 0;

    box-shadow: {colors["shadow"]};
}}

.score-label {{
    color: {colors["primary"]};

    font-size: 11px;

    font-weight: 750;

    letter-spacing: 1.2px;

    text-transform: uppercase;

    margin-bottom: 6px;
}}

.score-number {{
    color: {colors["heading"]};

    font-size: 35px;

    font-weight: 750;
}}

.score-category {{
    color: {colors["primary"]};

    font-size: 14px;

    font-weight: 700;

    margin-top: 2px;
}}

.score-description {{
    color: {colors["muted"]};

    font-size: 12px;

    margin-top: 9px;

    line-height: 1.5;
}}


/* ========================================================
   RECOMMENDATIONS
   ======================================================== */

.recommendation-card {{
    background: {colors["card_bg"]};

    border: 1px solid {colors["border"]};

    border-radius: 18px;

    padding: 23px;

    margin: 18px 0 10px 0;

    box-shadow: {colors["shadow"]};
}}

.recommendation-title {{
    color: {colors["heading"]};

    font-size: 20px;

    font-weight: 720;

    margin-bottom: 6px;
}}

.recommendation-subtitle {{
    color: {colors["muted"]};

    font-size: 13px;

    margin-bottom: 15px;

    line-height: 1.5;
}}

.recommendation-item {{
    color: {colors["text"]};

    font-size: 14px;

    line-height: 1.55;

    padding: 10px 0;

    border-bottom: 1px solid {colors["soft_border"]};
}}

.recommendation-item:last-child {{
    border-bottom: none;
}}

.recommendation-disclaimer {{
    color: {colors["muted"]};

    font-size: 11px;

    line-height: 1.5;

    margin-top: 16px;
}}


/* ========================================================
   ACTION CARDS
   ======================================================== */

.action-card {{
    background: {colors["card_bg"]};

    border: 1px solid {colors["border"]};

    border-radius: 17px;

    padding: 19px;

    min-height: 145px;

    box-shadow: {colors["shadow"]};

    margin-bottom: 7px;

    transition:
        transform 0.15s ease,
        background 0.15s ease;
}}

.action-card:hover {{
    transform: translateY(-2px);

    background: {colors["action_hover"]};
}}

.action-icon {{
    font-size: 27px;

    margin-bottom: 6px;
}}

.action-title {{
    color: {colors["heading"]};

    font-size: 16px;

    font-weight: 700;

    margin-bottom: 5px;
}}

.action-description {{
    color: {colors["muted"]};

    font-size: 12px;

    line-height: 1.45;

    min-height: 36px;
}}


/* ========================================================
   STREAMLIT BUTTONS
   ======================================================== */

div[data-testid="stButton"] > button {{
    border-radius: 11px;

    min-height: 40px;

    font-weight: 600;
}}


/* ========================================================
   DIVIDERS
   ======================================================== */

hr {{
    border-color: {colors["soft_border"]};
}}


/* ========================================================
   RESPONSIVE
   ======================================================== */

@media (max-width: 768px) {{

    .mindcare-hero {{
        padding: 24px 20px;
    }}

    .mindcare-hero-title {{
        font-size: 27px;
    }}

    .dashboard-welcome-title {{
        font-size: 24px;
    }}

    .motivation-message {{
        font-size: 18px;
    }}

    .progress-card {{
        margin-bottom: 10px;
    }}

    .action-card {{
        min-height: auto;
    }}
}}

</style>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# DAILY MOTIVATIONAL THOUGHT
# ============================================================

def show_daily_motivation():

    thoughts = [
        (
            "🌿",
            "A thought for today",
            "You are doing better than you think.",
            "A little reminder for your well-being 💚"
        ),
        (
            "🌸",
            "Your daily reminder",
            "Small steps every day lead to meaningful change.",
            "Be kind to yourself today. 💚"
        ),
        (
            "🌻",
            "A moment for you",
            "You deserve rest, peace, and happiness.",
            "Take things one step at a time. 💚"
        ),
        (
            "🌈",
            "Today's encouragement",
            "Every day is a new opportunity to care for yourself.",
            "Your feelings matter. Always. 💚"
        ),
        (
            "🦋",
            "A gentle reminder",
            "You don't have to be perfect to make progress.",
            "Give yourself the patience you deserve. 💚"
        ),
        (
            "🌙",
            "Today's thought",
            "Rest is not a reward. It is part of taking care of yourself.",
            "Make time for yourself today. 🌿"
        ),
        (
            "🌱",
            "A little encouragement",
            "Believe in the small changes you make every day.",
            "You are worth taking care of. 💚"
        )
    ]

    today_index = (
        date.today().toordinal()
        % len(thoughts)
    )

    icon, heading, message, reminder = (
        thoughts[today_index]
    )

    icon = html.escape(icon)
    heading = html.escape(heading)
    message = html.escape(message)
    reminder = html.escape(reminder)

    motivation_html = (
        '<div class="motivation-card">'

        f'<div class="motivation-icon">'
        f'{icon}'
        f'</div>'

        f'<div class="motivation-heading">'
        f'{heading}'
        f'</div>'

        f'<div class="motivation-message">'
        f'{message}'
        f'</div>'

        f'<div class="motivation-reminder">'
        f'{reminder}'
        f'</div>'

        '</div>'
    )

    st.markdown(
        motivation_html,
        unsafe_allow_html=True
    )


# ============================================================
# TODAY'S PROGRESS
# ============================================================

def show_today_progress(
    questionnaire_complete,
    sleep_complete,
    meditation_complete
):

    items = [
        (
            "📝",
            "Daily Check-in",
            questionnaire_complete
        ),
        (
            "🌙",
            "Sleep Tracking",
            sleep_complete
        ),
        (
            "🧘",
            "Meditation",
            meditation_complete
        )
    ]

    st.markdown(
        '<div class="dashboard-section-title">'
        'Today\'s progress'
        '</div>',
        unsafe_allow_html=True
    )

    columns = st.columns(3)

    for column, (
        icon,
        title,
        completed
    ) in zip(columns, items):

        with column:

            if completed:

                status = (
                    "✓ Completed today"
                )

                status_class = (
                    "progress-status-complete"
                )

            else:

                status = (
                    "○ Not completed yet"
                )

                status_class = (
                    "progress-status-pending"
                )

            card_html = (
                '<div class="progress-card">'

                f'<div class="progress-icon">'
                f'{icon}'
                f'</div>'

                f'<div class="progress-title">'
                f'{title}'
                f'</div>'

                f'<div class="{status_class}">'
                f'{status}'
                f'</div>'

                '</div>'
            )

            st.markdown(
                card_html,
                unsafe_allow_html=True
            )


# ============================================================
# PERSONALIZED RECOMMENDATIONS
# ============================================================

def show_personalized_recommendations(
    category,
    wellness_score,
    sleep_record,
    questionnaire_record,
    meditation_record
):
    sleep_hours = sleep_record.get("sleep_hours")
    stress_level = questionnaire_record.get("stress_level")
    meditation_minutes = meditation_record.get("meditation_minutes")

    recommendation_result = generate_recommendations(
        category=category,
        wellness_score=wellness_score,
        sleep_hours=sleep_hours,
        stress_level=stress_level,
        meditation_minutes=meditation_minutes
    )

    recommendations = recommendation_result.get(
        "recommendations",
        []
    )

    disclaimer = recommendation_result.get(
        "disclaimer",
        ""
    )

    if not recommendations:
        return

    # -----------------------------------------------------
    # PERSONALIZED RECOMMENDATIONS
    # -----------------------------------------------------

    st.markdown(
        '<div class="recommendation-card">'
        '<div class="recommendation-title">'
        '💡 Personalized Recommendations'
        '</div>'
        '<div class="recommendation-subtitle">'
        'Based on your wellness information for today.'
        '</div>'
        '</div>',
        unsafe_allow_html=True
    )

    # -----------------------------------------------------
    # COLLAPSED RECOMMENDATIONS DROPDOWN
    # -----------------------------------------------------

    with st.expander(
        "💡 View Personalized Recommendations",
        expanded=False
    ):

        for recommendation in recommendations:

            safe_recommendation = html.escape(
                str(recommendation)
            )

            recommendation_html = (
                '<div class="recommendation-item">'
                f'💚 {safe_recommendation}'
                '</div>'
            )

            st.markdown(
                recommendation_html,
                unsafe_allow_html=True
            )

        # -------------------------------------------------
        # DISCLAIMER
        # -------------------------------------------------

        if disclaimer:

            safe_disclaimer = html.escape(
                str(disclaimer)
            )

            disclaimer_html = (
                '<div class="recommendation-disclaimer">'
                f'{safe_disclaimer}'
                '</div>'
            )

            st.markdown(
                disclaimer_html,
                unsafe_allow_html=True
            )

# ============================================================
# WELLNESS SCORE
# ============================================================

def show_wellness_score_card(user_id):

    today = date.today().isoformat()

    # --------------------------------------------------------
    # GET TODAY'S RECORDS
    # --------------------------------------------------------

    questionnaire_result = (
        get_questionnaire_response(
            user_id,
            today
        )
    )

    sleep_result = (
        get_sleep_record(
            user_id,
            today
        )
    )

    meditation_result = (
        get_meditation_record(
            user_id,
            today
        )
    )

    # --------------------------------------------------------
    # QUESTIONNAIRE
    # --------------------------------------------------------

    questionnaire_record = None

    if questionnaire_result.get(
        "success"
    ):

        questionnaire_record = (
            questionnaire_result.get(
                "record"
            )
        )

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
            questionnaire_record.get(
                question
            ) is not None
            for question in required_questions
        )
    )

    # --------------------------------------------------------
    # SLEEP
    # --------------------------------------------------------

    sleep_record = None

    if sleep_result.get(
        "success"
    ):

        sleep_record = (
            sleep_result.get(
                "record"
            )
        )

    sleep_complete = (
        sleep_record is not None
        and sleep_record.get(
            "sleep_hours"
        ) is not None
    )

    # --------------------------------------------------------
    # MEDITATION
    # --------------------------------------------------------

    meditation_record = None

    if meditation_result.get(
        "success"
    ):

        meditation_record = (
            meditation_result.get(
                "record"
            )
        )

    meditation_complete = (
        meditation_record is not None
        and meditation_record.get(
            "meditation_minutes"
        ) is not None
    )

    # --------------------------------------------------------
    # TODAY'S PROGRESS
    # --------------------------------------------------------

    show_today_progress(
        questionnaire_complete,
        sleep_complete,
        meditation_complete
    )

    # --------------------------------------------------------
    # SCORE ONLY WHEN ALL THREE ARE COMPLETE
    # --------------------------------------------------------

    if not (
        questionnaire_complete
        and sleep_complete
        and meditation_complete
    ):

        st.info(
            "Your wellness score will appear here "
            "once your questionnaire, sleep tracking, "
            "and meditation records are all completed "
            "for today."
        )

        return

    # --------------------------------------------------------
    # CALCULATE SCORE
    # --------------------------------------------------------

    score_result = (
        calculate_and_save_wellness_score(
            user_id=user_id,
            record_date=today
        )
    )

    if not score_result.get(
        "success"
    ):

        existing_score = (
            get_wellness_score(
                user_id,
                today
            )
        )

        if existing_score.get(
            "success"
        ):

            score_record = (
                existing_score.get(
                    "record",
                    {}
                )
            )

            wellness_score = (
                score_record.get(
                    "wellness_score"
                )
            )

            category = (
                score_record.get(
                    "category",
                    "Not available"
                )
            )

        else:

            st.warning(
                score_result.get(
                    "message",
                    "Unable to calculate "
                    "your wellness score."
                )
            )

            return

    else:

        wellness_score = (
            score_result.get(
                "wellness_score"
            )
        )

        category = (
            score_result.get(
                "category",
                "Not available"
            )
        )

    # --------------------------------------------------------
    # SCORE NOT AVAILABLE
    # --------------------------------------------------------

    if wellness_score is None:

        st.info(
            "Your wellness score is not available yet."
        )

        return

    # --------------------------------------------------------
    # SCORE CARD
    # --------------------------------------------------------

    try:

        numeric_score = float(
            wellness_score
        )

    except (
        TypeError,
        ValueError
    ):

        st.warning(
            "Unable to display the wellness score."
        )

        return

    score_html = (
        '<div class="score-card">'

        '<div class="score-label">'
        'Your wellness score'
        '</div>'

        '<div class="score-number">'
        f'{numeric_score:.1f} / 100'
        '</div>'

        '<div class="score-category">'
        f'{html.escape(str(category))}'
        '</div>'

        '<div class="score-description">'
        'Your score combines your questionnaire, '
        'sleep, and meditation data for today.'
        '</div>'

        '</div>'
    )

    st.markdown(
        score_html,
        unsafe_allow_html=True
    )

    # --------------------------------------------------------
    # SCORE PROGRESS
    # --------------------------------------------------------

    st.progress(
        min(
            max(
                numeric_score / 100,
                0.0
            ),
            1.0
        )
    )

    st.caption(
        "This is a project-specific, non-diagnostic "
        "wellness indicator."
    )

    # --------------------------------------------------------
    # BREAKDOWN
    # --------------------------------------------------------

    with st.expander(
        "📊 View score breakdown"
    ):

        st.write(
            "Your score combines the following components:"
        )

        st.write(
            "🌙 Sleep — Maximum 25 points"
        )

        st.write(
            "🧘 Meditation — Maximum 15 points"
        )

        st.write(
            "📝 Questionnaire — Maximum 60 points"
        )

        st.caption(
            "The score is normalized to a range of 0–100."
        )

    # --------------------------------------------------------
    # PERSONALIZED RECOMMENDATIONS
    # --------------------------------------------------------

    show_personalized_recommendations(
        category=category,
        wellness_score=numeric_score,
        sleep_record=sleep_record,
        questionnaire_record=questionnaire_record,
        meditation_record=meditation_record
    )


# ============================================================
# QUICK ACTION
# ============================================================

def show_action_card(
    icon,
    title,
    description,
    button_text,
    page_key,
    button_key
):

    action_html = (
        '<div class="action-card">'

        f'<div class="action-icon">'
        f'{icon}'
        f'</div>'

        f'<div class="action-title">'
        f'{html.escape(title)}'
        f'</div>'

        f'<div class="action-description">'
        f'{html.escape(description)}'
        f'</div>'

        '</div>'
    )

    st.markdown(
        action_html,
        unsafe_allow_html=True
    )

    if st.button(
        button_text,
        use_container_width=True,
        key=button_key
    ):

        st.session_state[
            "page"
        ] = page_key

        st.rerun()


# ============================================================
# MAIN DASHBOARD
# ============================================================

def show_dashboard():

    # --------------------------------------------------------
    # APPLY DASHBOARD STYLES
    # --------------------------------------------------------

    apply_dashboard_styles()

    # --------------------------------------------------------
    # GET USER
    # --------------------------------------------------------

    user = st.session_state.get(
        "user",
        {}
    )

    user_name = (
        user.get(
            "name",
            "there"
        )
        or "there"
    )

    user_id = user.get(
        "id"
    )

    if user_id is None:

        user_id = user.get(
            "user_id"
        )

    safe_user_name = html.escape(
        str(user_name)
    )

    # ========================================================
    # HERO
    # ========================================================

    hero_html = (
        '<div class="mindcare-hero">'

        '<div class="mindcare-hero-icon">'
        '🌿'
        '</div>'

        '<div class="mindcare-hero-title">'
        'MindCare'
        '</div>'

        '<div class="mindcare-hero-subtitle">'
        'A gentle space to pause, reflect, '
        'and take care of yourself.'
        '</div>'

        '<div class="mindcare-hero-badge">'
        'YOUR WELL-BEING MATTERS'
        '</div>'

        '</div>'
    )

    st.markdown(
        hero_html,
        unsafe_allow_html=True
    )

    # ========================================================
    # WELCOME
    # ========================================================

    welcome_html = (
        '<div class="dashboard-welcome">'

        '<div class="dashboard-welcome-label">'
        'Your personal wellness space'
        '</div>'

        f'<div class="dashboard-welcome-title">'
        f'Welcome, {safe_user_name}! 💚'
        f'</div>'

        '<div class="dashboard-welcome-text">'
        'We are glad you are here. '
        'Take a moment for yourself today.'
        '</div>'

        '</div>'
    )

    st.markdown(
        welcome_html,
        unsafe_allow_html=True
    )

    # ========================================================
    # DAILY MOTIVATION
    # ========================================================

    show_daily_motivation()

    # ========================================================
    # WELLNESS SCORE + PROGRESS
    # ========================================================

    if user_id is not None:

        show_wellness_score_card(
            user_id
        )

    else:

        st.warning(
            "Unable to identify the logged-in user."
        )

    # ========================================================
    # WELLNESS SPACE
    # ========================================================

    st.markdown(
        '<div class="dashboard-section-title">'
        'Your wellness space'
        '</div>',
        unsafe_allow_html=True
    )

    # --------------------------------------------------------
    # ROW 1
    # --------------------------------------------------------

    col1, col2 = st.columns(2)

    with col1:

        show_action_card(
            icon="📝",
            title="Daily Check-in",
            description=(
                "Reflect on your mood and "
                "daily well-being."
            ),
            button_text="Start check-in",
            page_key="questionnaire",
            button_key="dashboard_start_checkin"
        )

    with col2:

        show_action_card(
            icon="🌙",
            title="Sleep Tracking",
            description=(
                "Keep track of your sleep "
                "and rest."
            ),
            button_text="Track sleep",
            page_key="sleep_tracking",
            button_key="dashboard_track_sleep"
        )

    # --------------------------------------------------------
    # ROW 2
    # --------------------------------------------------------

    col3, col4 = st.columns(2)

    with col3:

        show_action_card(
            icon="🧘",
            title="Meditation",
            description=(
                "Make time for mindfulness "
                "and relaxation."
            ),
            button_text="Open meditation",
            page_key="meditation",
            button_key="dashboard_open_meditation"
        )

    with col4:

        show_action_card(
            icon="🤖",
            title="MindCare Chat",
            description=(
                "Talk to your AI mental "
                "health assistant."
            ),
            button_text="Open chatbot",
            page_key="chatbot",
            button_key="dashboard_open_chatbot"
        )

    # ========================================================
    # FOOTER
    # ========================================================

    st.divider()

    st.caption(
        "MindCare provides wellness support and is not "
        "a replacement for professional mental health care."
    )