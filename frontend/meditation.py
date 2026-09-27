import streamlit as st
import time
import pandas as pd
import altair as alt
from datetime import date, datetime, timedelta

from streamlit_autorefresh import st_autorefresh

from app.backend.auth import get_user_registration_date

from app.backend.meditation import (
    save_meditation_record,
    get_meditation_record,
    get_meditation_history,
    update_meditation_record,
)


# ============================================================
# MEDITATION SESSIONS
# ============================================================

MEDITATION_SESSIONS = {
    "🌬️ Calm Breathing": {
        "duration": 5,
        "description": (
            "A gentle breathing exercise to help calm your mind."
        ),
        "steps": [
            "Sit comfortably and relax your shoulders.",
            "Close your eyes or soften your gaze.",
            "Breathe in slowly through your nose.",
            "Hold your breath gently.",
            "Breathe out slowly.",
            "Repeat the breathing cycle at your own pace.",
        ],
    },

    "🌿 Stress Relief": {
        "duration": 10,
        "description": (
            "A guided practice to help release tension and stress."
        ),
        "steps": [
            "Find a comfortable and quiet place.",
            "Take three slow, deep breaths.",
            "Relax your forehead and jaw.",
            "Relax your neck and shoulders.",
            "Relax your arms and hands.",
            "Release tension from your legs and feet.",
            "Allow your thoughts to come and go.",
            "Take one final deep breath.",
        ],
    },

    "🌙 Sleep Meditation": {
        "duration": 10,
        "description": (
            "A peaceful meditation to help prepare your mind for rest."
        ),
        "steps": [
            "Lie down or sit in a comfortable position.",
            "Dim the lights and remove distractions.",
            "Take a slow and comfortable breath.",
            "Relax your face, shoulders, and hands.",
            "Notice your body becoming heavier and calmer.",
            "Imagine yourself in a peaceful place.",
            "Let the day's worries gently pass.",
            "Allow yourself to become relaxed.",
        ],
    },

    "🧘‍♀️ Mindful Awareness": {
        "duration": 5,
        "description": (
            "A mindfulness exercise to bring your attention to the present."
        ),
        "steps": [
            "Sit comfortably and take a deep breath.",
            "Notice five things you can see.",
            "Notice four things you can physically feel.",
            "Notice three sounds around you.",
            "Notice two things you can smell.",
            "Notice one thing you appreciate right now.",
        ],
    },
}


# ============================================================
# MEDITATION-SPECIFIC LIVE GUIDANCE
# ============================================================

MEDITATION_GUIDANCE = {
    "🌬️ Calm Breathing": [
        ("🌬️ Breathe in slowly", 4),
        ("⏸️ Hold gently", 2),
        ("🌿 Breathe out slowly", 6),
    ],

    "🌿 Stress Relief": [
        ("Relax your forehead", 8),
        ("Relax your jaw", 8),
        ("Relax your shoulders", 8),
        ("Relax your hands", 8),
        ("Release body tension", 8),
    ],

    "🌙 Sleep Meditation": [
        ("Relax your entire body", 10),
        ("Take a slow, comfortable breath", 10),
        ("Feel your body becoming relaxed", 10),
        ("Imagine a peaceful place", 10),
        ("Let your worries gently pass", 10),
        ("Prepare your mind for rest", 10),
    ],

    "🧘‍♀️ Mindful Awareness": [
        ("Notice 5 things you can see", 10),
        ("Notice 4 things you can feel", 10),
        ("Notice 3 sounds around you", 10),
        ("Notice 2 things you can smell", 10),
        ("Notice 1 thing you appreciate", 10),
    ],
}


# ============================================================
# GET CURRENT MEDITATION INSTRUCTION
# ============================================================

def get_meditation_instruction(
    elapsed_seconds,
    meditation_type
):
    """Return the current instruction and remaining phase seconds."""

    phases = MEDITATION_GUIDANCE.get(
        meditation_type,
        MEDITATION_GUIDANCE["🌬️ Calm Breathing"],
    )

    cycle_duration = sum(
        duration for _, duration in phases
    )

    position = int(elapsed_seconds) % cycle_duration
    elapsed_in_phase = 0

    for instruction, duration in phases:

        if position < elapsed_in_phase + duration:

            phase_remaining = duration - (
                position - elapsed_in_phase
            )

            return instruction, phase_remaining

        elapsed_in_phase += duration

    return phases[0]


# ============================================================
# SAVE COMPLETED MEDITATION
# ============================================================

def save_completed_meditation(user_id, minutes):
    """Add completed meditation time to today's record."""

    if minutes <= 0:
        return {
            "success": False,
            "message": "No completed meditation time to save.",
        }

    today = date.today().isoformat()

    existing = get_meditation_record(
        user_id,
        today
    )

    if existing.get("success") and existing.get("record"):

        previous_minutes = float(
            existing["record"].get(
                "meditation_minutes",
                0
            )
        )

        return update_meditation_record(
            user_id=user_id,
            meditation_minutes=(
                previous_minutes + minutes
            ),
            record_date=today,
        )

    return save_meditation_record(
        user_id=user_id,
        meditation_minutes=minutes,
        record_date=today,
    )


# ============================================================
# WEEK HELPERS
# ============================================================

def get_monday(any_date):
    """
    Return the Monday of the week containing any_date.
    """

    return any_date - timedelta(
        days=any_date.weekday()
    )


def get_week_dates(week_start):
    """
    Return all seven dates from Monday to Sunday.
    """

    return [
        week_start + timedelta(days=i)
        for i in range(7)
    ]


def format_week_range(
    week_start,
    week_end
):
    """
    Format the weekly date range.
    """

    if week_start.year == week_end.year:

        return (
            f"{week_start.strftime('%b %d')} – "
            f"{week_end.strftime('%b %d, %Y')}"
        )

    return (
        f"{week_start.strftime('%b %d, %Y')} – "
        f"{week_end.strftime('%b %d, %Y')}"
    )


# ============================================================
# BUILD WEEKLY GRAPH DATA
# ============================================================

def build_weekly_meditation_data(
    history,
    registration_date,
    week_start,
    today
):
    """
    Build a complete Monday-Sunday dataset.

    Rules:

    - Before registration -> blank
    - After registration with no record -> 0
    - Future dates -> blank
    - Recorded dates -> actual meditation minutes
    """

    registration_date = date.fromisoformat(
        registration_date
    )

    records_by_date = {}

    for record in history:

        record_date_string = record.get(
            "record_date"
        )

        if not record_date_string:
            continue

        try:
            record_date = date.fromisoformat(
                str(record_date_string)
            )
        except ValueError:
            continue

        records_by_date[record_date] = float(
            record.get(
                "meditation_minutes",
                0
            )
        )

    rows = []

    week_dates = get_week_dates(
        week_start
    )

    for current_date in week_dates:

        # ----------------------------------------------------
        # Before user registration
        # ----------------------------------------------------

        if current_date < registration_date:

            minutes = None

        # ----------------------------------------------------
        # Future date
        # ----------------------------------------------------

        elif current_date > today:

            minutes = None

        # ----------------------------------------------------
        # Existing meditation record
        # ----------------------------------------------------

        elif current_date in records_by_date:

            minutes = records_by_date[
                current_date
            ]

        # ----------------------------------------------------
        # Eligible day but no meditation
        # ----------------------------------------------------

        else:

            minutes = 0.0

        rows.append(
            {
                "Date": current_date,
                "Day": current_date.strftime("%a"),
                "Minutes": minutes,
            }
        )

    return pd.DataFrame(rows)


# ============================================================
# PAGE
# ============================================================

def show_meditation():
    """Display the guided meditation page."""

    # ========================================================
    # PAGE STYLING
    # ========================================================

    st.markdown(
        """
        <style>

        .meditation-subtitle {
            text-align: center;
            font-size: 1.05rem;
            opacity: 0.8;
            margin-top: -12px;
            margin-bottom: 24px;
        }

        .meditation-quote {
            padding: 22px;
            border-radius: 17px;
            text-align: center;
            background: linear-gradient(
                135deg,
                rgba(225, 216, 255, 0.95),
                rgba(245, 237, 255, 0.95)
            );
            color: #304477;
            margin-bottom: 25px;
        }

        .quote-text {
            font-size: 1.1rem;
            font-weight: 700;
            line-height: 1.6;
        }

        .quote-author {
            margin-top: 8px;
            font-weight: 600;
        }

        .meditation-heading {
            font-size: 1.45rem;
            font-weight: 800;
            margin-top: 20px;
            margin-bottom: 12px;
        }

        .session-description {
            font-size: 1rem;
            opacity: 0.8;
            margin-bottom: 15px;
        }

        .breathing-card {
            text-align: center;
            padding: 30px;
            border-radius: 20px;
            background: linear-gradient(
                135deg,
                #e8f5e9,
                #e8eaf6
            );
            color: #263238;
            margin: 20px 0;
        }

        .breathing-instruction {
            font-size: 30px;
            font-weight: 800;
            margin-bottom: 15px;
        }

        .breathing-number {
            font-size: 70px;
            font-weight: 800;
            margin: 10px 0;
        }

        .breathing-time {
            font-size: 20px;
            margin-top: 10px;
        }

        .breathing-message {
            font-size: 16px;
            margin-top: 18px;
        }

        .weekly-average {
            font-size: 1.05rem;
            font-weight: 700;
            margin-top: 10px;
            margin-bottom: 18px;
        }

        .week-range {
            font-size: 1rem;
            font-weight: 600;
            opacity: 0.8;
            margin-bottom: 15px;
        }

        div[data-testid="stButton"] button {
            border-radius: 10px;
            font-weight: 700;
            min-height: 45px;
        }

        </style>
        """,
        unsafe_allow_html=True,
    )

    # ========================================================
    # PAGE HEADER
    # ========================================================

    st.title("🧘‍♀️ Guided Meditation")

    st.markdown(
        (
            '<div class="meditation-subtitle">'
            "Take a moment to relax, breathe, and "
            "reconnect with yourself."
            "</div>"
        ),
        unsafe_allow_html=True,
    )

    user_id = st.session_state.get(
        "user_id"
    )

    if not user_id:

        st.warning(
            "Please log in to access guided meditation."
        )

        return

    # ========================================================
    # USER REGISTRATION DATE
    # ========================================================

    registration_date_string = (
        get_user_registration_date(user_id)
    )

    if not registration_date_string:

        st.error(
            "Unable to determine your registration date."
        )

        return

    try:

        registration_date = date.fromisoformat(
            registration_date_string
        )

    except ValueError:

        st.error(
            "Invalid registration date found."
        )

        return

    today = date.today()

    # ========================================================
    # DAILY MOTIVATIONAL QUOTE
    # ========================================================

    quotes = [
        "Give yourself permission to pause and breathe.",
        "Peace begins with a single mindful breath.",
        "You deserve a moment of calm today.",
        "Slow down. Breathe deeply. Be present.",
        "Your mind deserves rest and kindness.",
        "A few quiet minutes can make a meaningful difference.",
        "Take care of your inner world, one breath at a time.",
    ]

    quote = quotes[
        today.timetuple().tm_yday % len(quotes)
    ]

    st.markdown(
        f"""
        <div class="meditation-quote">
            <div class="quote-text">
                ❝ {quote} ❞
            </div>
            <div class="quote-author">
                — MindCare
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ========================================================
    # TIMER STATE
    # ========================================================

    if "meditation_running" not in st.session_state:
        st.session_state[
            "meditation_running"
        ] = False

    if "meditation_start_time" not in st.session_state:
        st.session_state[
            "meditation_start_time"
        ] = None

    if "meditation_elapsed" not in st.session_state:
        st.session_state[
            "meditation_elapsed"
        ] = 0

    if "meditation_active_session" not in st.session_state:
        st.session_state[
            "meditation_active_session"
        ] = None

    # ========================================================
    # SELECT MEDITATION TYPE
    # ========================================================

    st.markdown(
        (
            '<div class="meditation-heading">'
            "🌸 Choose Your Meditation"
            "</div>"
        ),
        unsafe_allow_html=True,
    )

    selected_session = st.selectbox(
        "What would you like to focus on today?",
        options=list(
            MEDITATION_SESSIONS.keys()
        ),
        key="selected_meditation_session",
        disabled=st.session_state[
            "meditation_running"
        ],
    )

    session = MEDITATION_SESSIONS[
        selected_session
    ]

    st.markdown(
        f"""
        <div class="session-description">
            {session["description"]}
            <br><br>
            ⏱️ Suggested duration:
            <b>{session["duration"]} minutes</b>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ========================================================
    # DETERMINE ACTIVE SESSION
    # ========================================================

    active_session = st.session_state.get(
        "meditation_active_session"
    )

    if (
        st.session_state["meditation_running"]
        and active_session
    ):

        running_session = MEDITATION_SESSIONS[
            active_session
        ]

        running_session_name = active_session

    else:

        running_session = session
        running_session_name = selected_session

    session_minutes = running_session[
        "duration"
    ]

    total_seconds = session_minutes * 60

    # ========================================================
    # START OR RUN MEDITATION
    # ========================================================

    if not st.session_state[
        "meditation_running"
    ]:

        if st.button(
            "▶️ Start Meditation",
            use_container_width=True,
            key="start_live_meditation",
        ):

            st.session_state[
                "meditation_running"
            ] = True

            st.session_state[
                "meditation_start_time"
            ] = time.time()

            st.session_state[
                "meditation_elapsed"
            ] = 0

            st.session_state[
                "meditation_active_session"
            ] = selected_session

            st.rerun()

    else:

        st_autorefresh(
            interval=1000,
            key="meditation_timer_refresh",
        )

        start_time = st.session_state.get(
            "meditation_start_time"
        )

        if start_time is None:

            st.session_state[
                "meditation_running"
            ] = False

            st.session_state[
                "meditation_active_session"
            ] = None

            st.rerun()

        elapsed = int(
            time.time() - start_time
        )

        remaining_seconds = max(
            total_seconds - elapsed,
            0
        )

        st.session_state[
            "meditation_elapsed"
        ] = elapsed

        if remaining_seconds > 0:

            minutes_left = (
                remaining_seconds // 60
            )

            seconds_left = (
                remaining_seconds % 60
            )

            instruction, phase_remaining = (
                get_meditation_instruction(
                    elapsed,
                    running_session_name,
                )
            )

            breathing_html = (
                '<div class="breathing-card">'
                '<div class="breathing-instruction">'
                f"{instruction}"
                "</div>"
                '<div class="breathing-number">'
                f"{phase_remaining}"
                "</div>"
                '<div class="breathing-time">'
                "Time remaining: "
                f"<b>{minutes_left:02d}:"
                f"{seconds_left:02d}</b>"
                "</div>"
                '<div class="breathing-message">'
                "Stay present and follow the "
                "guidance gently."
                "</div>"
                "</div>"
            )

            st.markdown(
                breathing_html,
                unsafe_allow_html=True,
            )

            if st.button(
                "⏹️ Stop Meditation",
                use_container_width=True,
                key="stop_live_meditation",
            ):

                # Save actual elapsed time.
                completed_minutes = round(
                    elapsed / 60,
                    2
                )

                if completed_minutes > 0:

                    save_completed_meditation(
                        user_id=user_id,
                        minutes=completed_minutes,
                    )

                st.session_state[
                    "meditation_running"
                ] = False

                st.session_state[
                    "meditation_start_time"
                ] = None

                st.session_state[
                    "meditation_elapsed"
                ] = 0

                st.session_state[
                    "meditation_active_session"
                ] = None

                if completed_minutes > 0:

                    st.success(
                        f"You completed "
                        f"{completed_minutes:.2f} "
                        "minute(s) of meditation."
                    )

                else:

                    st.info(
                        "Meditation stopped before "
                        "any measurable time was completed."
                    )

                st.rerun()

    # ========================================================
    # TODAY'S MEDITATION SUMMARY
    # ========================================================

    st.divider()

    st.markdown(
        (
            '<div class="meditation-heading">'
            "📊 Today's Meditation Summary"
            "</div>"
        ),
        unsafe_allow_html=True,
    )

    today_result = get_meditation_record(
        user_id,
        today.isoformat(),
    )

    if (
        today_result.get("success")
        and today_result.get("record")
    ):

        total_minutes = float(
            today_result["record"].get(
                "meditation_minutes",
                0
            )
        )

        st.metric(
            label="Meditation Completed Today",
            value=f"{total_minutes:.2f} minutes",
        )

        if total_minutes >= 10:

            st.success(
                "You made time for yourself today. "
                "Keep going! 🌟"
            )

        else:

            st.info(
                "Even a few mindful minutes can be "
                "valuable. 🌱"
            )

    else:

        st.info(
            "You have not completed a meditation "
            "session today."
        )

    # ========================================================
    # GET COMPLETE MEDITATION HISTORY
    # ========================================================

    history_result = get_meditation_history(
        user_id
    )

    history = []

    if (
        history_result.get("success")
        and history_result.get("records")
    ):

        history = history_result[
            "records"
        ]

    # ========================================================
    # WEEKLY MEDITATION PROGRESS
    # ========================================================

    st.divider()

    st.markdown(
        (
            '<div class="meditation-heading">'
            "📈 Your Meditation Progress"
            "</div>"
        ),
        unsafe_allow_html=True,
    )

    st.caption(
        "Review your meditation activity week by week."
    )

    # ========================================================
    # INITIALIZE WEEK NAVIGATION
    # ========================================================

    registration_week_start = get_monday(
        registration_date
    )

    current_week_start = get_monday(
        today
    )

    if (
        "meditation_week_start"
        not in st.session_state
    ):

        st.session_state[
            "meditation_week_start"
        ] = current_week_start

    selected_week_start = st.session_state[
        "meditation_week_start"
    ]

    # Safety: never allow navigation before
    # registration week.

    if selected_week_start < registration_week_start:

        selected_week_start = (
            registration_week_start
        )

        st.session_state[
            "meditation_week_start"
        ] = selected_week_start

    # ========================================================
    # WEEK NAVIGATION BUTTONS
    # ========================================================

    previous_week_start = (
        selected_week_start
        - timedelta(days=7)
    )

    next_week_start = (
        selected_week_start
        + timedelta(days=7)
    )

    previous_disabled = (
        previous_week_start
        < registration_week_start
    )

    next_disabled = (
        next_week_start
        > current_week_start
    )

    nav_left, nav_middle, nav_right = st.columns(
        [1, 2, 1]
    )

    with nav_left:

        if st.button(
            "← Previous Week",
            use_container_width=True,
            disabled=previous_disabled,
            key="meditation_previous_week",
        ):

            st.session_state[
                "meditation_week_start"
            ] = previous_week_start

            st.rerun()

    with nav_middle:

        selected_week_end = (
            selected_week_start
            + timedelta(days=6)
        )

        st.markdown(
            (
                '<div class="week-range" '
                'style="text-align:center;">'
                f"{format_week_range(
                    selected_week_start,
                    selected_week_end
                )}"
                "</div>"
            ),
            unsafe_allow_html=True,
        )

    with nav_right:

        if st.button(
            "Next Week →",
            use_container_width=True,
            disabled=next_disabled,
            key="meditation_next_week",
        ):

            st.session_state[
                "meditation_week_start"
            ] = next_week_start

            st.rerun()

    # ========================================================
    # BUILD WEEKLY DATA
    # ========================================================

    weekly_df = build_weekly_meditation_data(
        history=history,
        registration_date=registration_date_string,
        week_start=selected_week_start,
        today=today,
    )

    # ========================================================
    # WEEKLY AVERAGE
    # ========================================================

    eligible_minutes = weekly_df[
        weekly_df["Minutes"].notna()
    ]["Minutes"]

    if len(eligible_minutes) > 0:

        weekly_average = (
            eligible_minutes.mean()
        )

        st.markdown(
            (
                '<div class="weekly-average">'
                f"Daily average: "
                f"{weekly_average:.2f} minutes"
                "</div>"
            ),
            unsafe_allow_html=True,
        )

    # ========================================================
    # GRAPH DATA
    # ========================================================

    chart_df = weekly_df[
        ["Date", "Day", "Minutes"]
    ].copy()

    # Keep the original Minutes column unchanged.
    # It is used for calculating the average correctly.
    #
    # For the graph only:
    # - None = blank day
    # - 0 = no meditation
    # - actual number = meditation completed
    #
    # Altair needs a numeric value to keep every day
    # visible on the x-axis, so blank days are plotted
    # at zero height.

    chart_df["Graph Minutes"] = (
        chart_df["Minutes"]
        .fillna(0)
        .astype(float)
    )

    # Create a readable label for every calendar day.
    chart_df["Day Label"] = chart_df["Day"]

    # ========================================================
    # WEEKLY GRAPH
    # ========================================================

    weekly_chart = (
        alt.Chart(chart_df)
        .mark_bar()
        .encode(
            x=alt.X(
                "Day Label:N",
                sort=chart_df["Day Label"].tolist(),
                title="Day",
                axis=alt.Axis(
                    labelAngle=0
                ),
            ),
            y=alt.Y(
                "Graph Minutes:Q",
                title="Meditation Minutes",
                scale=alt.Scale(
                    zero=True
                ),
            ),
            tooltip=[
                alt.Tooltip(
                    "Date:T",
                    title="Date",
                    format="%d %b %Y",
                ),
                alt.Tooltip(
                    "Graph Minutes:Q",
                    title="Meditation Minutes",
                    format=".2f",
                ),
            ],
        )
        .properties(
            height=400,
        )
    )

    st.altair_chart(
        weekly_chart,
        use_container_width=True,
    )
    # ========================================================
    # WEEKLY INFORMATION
    # ========================================================

    if selected_week_start == current_week_start:

        st.caption(
            "This week updates as you record meditation. "
            "Future days remain empty."
        )

    elif selected_week_start == registration_week_start:

        st.caption(
            "This is your registration week. "
            "Days before registration are not included "
            "in your meditation average."
        )

    else:

        st.caption(
            "Showing your complete meditation activity "
            "for this week."
        )

    # ========================================================
    # MEDITATION HISTORY
    # ========================================================

    st.divider()

    st.markdown(
        (
            '<div class="meditation-heading">'
            "🗓️ Meditation History"
            "</div>"
        ),
        unsafe_allow_html=True,
    )

    if history:

        history_rows = []

        for record in history:

            minutes = float(
                record.get(
                    "meditation_minutes",
                    0
                )
            )

            history_rows.append(
                {
                    "Date": record.get(
                        "record_date",
                        ""
                    ),

                    "Meditation Minutes": (
                        f"{minutes:.2f} minutes"
                    ),
                }
            )

        st.table(history_rows)

    else:

        st.info(
            "No meditation history available yet."
        )