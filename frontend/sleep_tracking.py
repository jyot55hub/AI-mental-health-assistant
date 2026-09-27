import streamlit as st
from datetime import date, timedelta
from textwrap import dedent
import pandas as pd
import altair as alt

from app.backend.sleep import (
    save_sleep_record,
    get_sleep_record,
    get_sleep_history,
)

from app.backend.auth import (
    get_user_registration_date,
)


# ============================================================
# DAILY MOTIVATIONAL QUOTE
# ============================================================

def get_daily_quote():
    """Return a motivational quote that changes daily."""

    quotes = [
        "A good night's sleep is a step towards a healthier, happier you.",
        "Rest is not a luxury. It is an important part of self-care.",
        "Give your body the rest it deserves tonight.",
        "Better sleep creates brighter days.",
        "A peaceful night leads to a refreshed mind.",
        "Your well-being begins with taking care of yourself.",
        "Sleep well, breathe deeply, and begin again tomorrow.",
    ]

    day_index = (
        date.today().timetuple().tm_yday
        % len(quotes)
    )

    return quotes[day_index]


# ============================================================
# SLEEP MESSAGE
# ============================================================

def get_sleep_message(hours):
    """Return a suitable message based on sleep duration."""

    if hours < 6:
        return (
            "You may need more rest. Try to get a little extra sleep tonight. 😴",
            "warning",
        )

    elif hours < 7:
        return (
            "You may benefit from a little more sleep.",
            "info",
        )

    elif hours <= 9:
        return (
            "Your sleep duration is within a healthy range. 🌟",
            "success",
        )

    else:
        return (
            "You had a long sleep duration. Listen to your body's needs.",
            "info",
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


def get_week_days(week_start):
    """
    Return all seven dates from Monday to Sunday.
    """

    return [
        week_start + timedelta(days=i)
        for i in range(7)
    ]


def format_week_range(week_start):
    """
    Return a readable weekly date range.
    """

    week_end = week_start + timedelta(days=6)

    return (
        f"{week_start.strftime('%b %d')} – "
        f"{week_end.strftime('%b %d, %Y')}"
    )


# ============================================================
# SHOW SLEEP TRACKING
# ============================================================

def show_sleep_tracking():
    """Display the complete sleep tracking page."""

    # ========================================================
    # CUSTOM PAGE STYLING
    # ========================================================

    st.markdown(
        dedent("""
        <style>

        .sleep-page {
            font-family: 'Nunito', sans-serif;
        }

        .sleep-subtitle {
            text-align: center;
            font-size: 1.05rem;
            margin-top: -12px;
            margin-bottom: 24px;
            opacity: 0.80;
        }

        .sleep-quote {
            padding: 22px 28px;
            border-radius: 16px;
            text-align: center;
            margin: 20px 0 26px 0;

            background: linear-gradient(
                135deg,
                rgba(231, 225, 255, 0.95),
                rgba(244, 238, 255, 0.95)
            );

            color: #293b72;

            border: 1px solid rgba(150, 130, 220, 0.18);

            box-shadow:
                0 4px 14px rgba(80, 70, 130, 0.07);
        }

        .quote-text {
            font-size: 1.10rem;
            font-weight: 700;
            line-height: 1.6;
        }

        .quote-author {
            margin-top: 8px;
            font-size: 0.90rem;
            font-weight: 600;
        }

        .sleep-card {
            padding: 24px;
            border-radius: 17px;

            border: 1px solid rgba(128, 128, 128, 0.22);

            background: rgba(128, 128, 128, 0.035);

            margin: 20px 0;
        }

        .card-heading {
            font-size: 1.45rem;
            font-weight: 800;
            margin-bottom: 18px;
        }

        .summary-box {
            padding: 20px;
            border-radius: 13px;

            background: rgba(93, 161, 245, 0.13);

            border-left: 5px solid #4d91e8;

            min-height: 130px;
        }

        .summary-label {
            font-size: 0.95rem;
            font-weight: 700;
            opacity: 0.80;
        }

        .summary-value {
            font-size: 2rem;
            font-weight: 800;
            margin-top: 8px;
        }

        .recommendation-box {
            padding: 18px 22px;
            border-radius: 13px;

            background: rgba(93, 161, 245, 0.13);

            margin-top: 18px;
        }

        .recommendation-title {
            font-weight: 800;
            font-size: 1rem;
            margin-bottom: 6px;
        }

        .recommendation-text {
            font-size: 0.95rem;
        }

        .history-note {
            padding: 18px 22px;
            border-radius: 13px;

            background: rgba(93, 161, 245, 0.15);

            margin-top: 18px;

            font-size: 1rem;
        }

        .section-caption {
            font-size: 0.95rem;
            opacity: 0.75;
            margin-top: -10px;
            margin-bottom: 12px;
        }

        .week-range {
            font-size: 1.05rem;
            font-weight: 800;
        }

        .week-note {
            text-align: center;
            opacity: 0.70;
            margin-top: 15px;
            margin-bottom: 10px;
        }

        div[data-testid="stNumberInput"] input {
            font-family: 'Nunito', sans-serif;
            font-weight: 600;
        }

        div[data-testid="stButton"] button {
            border-radius: 10px;
            font-family: 'Nunito', sans-serif;
            font-weight: 700;
            min-height: 45px;
        }

        </style>
        """),
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="sleep-page">',
        unsafe_allow_html=True,
    )

    # ========================================================
    # PAGE HEADING
    # ========================================================

    st.title("🌙 Sleep Tracking")

    st.markdown(
        dedent("""
        <div class="sleep-subtitle">
            Track your daily sleep and maintain healthy sleep habits.
        </div>
        """),
        unsafe_allow_html=True,
    )

    # ========================================================
    # LOGIN VERIFICATION
    # ========================================================

    user_id = st.session_state.get("user_id")

    if not user_id:

        st.warning(
            "Please log in to track your sleep."
        )

        st.markdown(
            "</div>",
            unsafe_allow_html=True,
        )

        return

    # ========================================================
    # DATES
    # ========================================================

    today = date.today()

    today_string = today.isoformat()

    current_week_start = get_monday(today)

    # ========================================================
    # USER REGISTRATION DATE
    # ========================================================

    registration_date_string = (
        get_user_registration_date(user_id)
    )

    if registration_date_string:

        try:

            registration_date = date.fromisoformat(
                registration_date_string
            )

        except ValueError:

            registration_date = today

    else:

        registration_date = today

    registration_week_start = get_monday(
        registration_date
    )

    # ========================================================
    # WEEK NAVIGATION STATE
    # ========================================================

    if "sleep_selected_week_start" not in st.session_state:

        st.session_state[
            "sleep_selected_week_start"
        ] = current_week_start

        st.session_state[
            "sleep_week_manual_navigation"
        ] = False

    selected_week_start = st.session_state[
        "sleep_selected_week_start"
    ]

    # ========================================================
    # AUTOMATICALLY MOVE TO CURRENT WEEK
    # ========================================================

    manual_navigation = st.session_state.get(
        "sleep_week_manual_navigation",
        False,
    )

    if (
        not manual_navigation
        and selected_week_start != current_week_start
    ):

        selected_week_start = current_week_start

        st.session_state[
            "sleep_selected_week_start"
        ] = current_week_start

    # Never allow browsing before registration week.

    if selected_week_start < registration_week_start:

        selected_week_start = registration_week_start

        st.session_state[
            "sleep_selected_week_start"
        ] = registration_week_start

    # ========================================================
    # DAILY MOTIVATIONAL QUOTE
    # ========================================================

    quote_text = get_daily_quote()

    st.markdown(
        (
            '<div class="sleep-quote">'
            f'<div class="quote-text">❝ {quote_text} ❞</div>'
            '<div class="quote-author">— MindCare</div>'
            '</div>'
        ),
        unsafe_allow_html=True,
    )

    # ========================================================
    # RECORD TODAY'S SLEEP
    # ========================================================

    st.markdown(
        '<div class="sleep-card">',
        unsafe_allow_html=True,
    )

    st.markdown(
        dedent("""
        <div class="card-heading">
            🛏️ Record Today's Sleep
        </div>
        """),
        unsafe_allow_html=True,
    )

    existing_record = get_sleep_record(
        user_id,
        today_string,
    )

    default_hours = 7.0

    if existing_record.get("success"):

        default_hours = float(
            existing_record["record"]["sleep_hours"]
        )

    sleep_hours = st.number_input(
        "How many hours did you sleep last night?",
        min_value=0.0,
        max_value=24.0,
        value=default_hours,
        step=0.5,
        format="%.1f",
    )

    if st.button(
        "💾 Save Sleep Record",
        use_container_width=True,
    ):

        result = save_sleep_record(
            user_id=user_id,
            sleep_hours=sleep_hours,
            record_date=today_string,
        )

        if result.get("success"):

            st.session_state[
                "sleep_success_message"
            ] = "Sleep record saved successfully! ✅"

            st.rerun()

        else:

            st.error(
                result.get(
                    "message",
                    "Unable to save sleep record.",
                )
            )

    if st.session_state.get(
        "sleep_success_message"
    ):

        st.success(
            st.session_state[
                "sleep_success_message"
            ]
        )

        st.session_state.pop(
            "sleep_success_message",
            None,
        )

    st.markdown(
        "</div>",
        unsafe_allow_html=True,
    )

    # ========================================================
    # TODAY'S SLEEP SUMMARY
    # ========================================================

    st.markdown(
        '<div class="sleep-card">',
        unsafe_allow_html=True,
    )

    st.markdown(
        dedent("""
        <div class="card-heading">
            📊 Today's Sleep Summary
        </div>
        """),
        unsafe_allow_html=True,
    )

    today_record = get_sleep_record(
        user_id,
        today_string,
    )

    if today_record.get("success"):

        hours = float(
            today_record["record"]["sleep_hours"]
        )

        message, message_type = get_sleep_message(
            hours
        )

        summary_col, status_col = st.columns(2)

        with summary_col:

            summary_html = (
                '<div class="summary-box">'
                '<div class="summary-label">🛏️ Sleep Duration</div>'
                f'<div class="summary-value">{hours:.1f} hours</div>'
                '</div>'
            )

            st.markdown(
                summary_html,
                unsafe_allow_html=True,
            )

        with status_col:

            if message_type == "success":

                st.success(
                    f"😊 {message}"
                )

            elif message_type == "warning":

                st.warning(message)

            else:

                st.info(message)

        st.markdown(
            (
                '<div class="recommendation-box">'
                '<div class="recommendation-title">'
                '💡 Recommended Sleep Duration'
                '</div>'
                '<div class="recommendation-text">'
                'Adults generally need 7–9 hours of sleep '
                'per night for better physical and mental '
                'well-being.'
                '</div>'
                '</div>'
            ),
            unsafe_allow_html=True,
        )

    else:

        st.info(
            "No sleep record has been added for today."
        )

    st.markdown(
        "</div>",
        unsafe_allow_html=True,
    )

    # ========================================================
    # GET ALL SLEEP HISTORY
    # ========================================================

    history_result = get_sleep_history(
        user_id,
        limit=3650,
    )

    history = []

    if (
        history_result.get("success")
        and history_result.get("records")
    ):

        history = history_result["records"]

    # ========================================================
    # CONVERT HISTORY INTO DATE -> HOURS LOOKUP
    # ========================================================

    sleep_by_date = {}

    for record in history:

        record_date_string = str(
            record.get("record_date", "")
        )

        try:

            record_date = date.fromisoformat(
                record_date_string
            )

            sleep_by_date[record_date] = float(
                record.get("sleep_hours", 0)
            )

        except (
            ValueError,
            TypeError,
        ):

            continue

    # ========================================================
    # WEEKLY SLEEP PROGRESS
    # ========================================================

    st.divider()

    st.markdown(
        dedent("""
        <div class="card-heading">
            📊 Your Sleep Progress
        </div>
        """),
        unsafe_allow_html=True,
    )

    st.caption(
        "Review your sleep activity week by week."
    )

    # ========================================================
    # WEEK NAVIGATION
    # ========================================================

    previous_week_start = (
        selected_week_start
        - timedelta(days=7)
    )

    next_week_start = (
        selected_week_start
        + timedelta(days=7)
    )

    can_go_previous = (
        previous_week_start
        >= registration_week_start
    )

    can_go_next = (
        next_week_start
        <= current_week_start
    )

    navigation_left, navigation_middle, navigation_right = (
        st.columns([1, 1.4, 1])
    )

    with navigation_left:

        if st.button(
            "← Previous Week",
            use_container_width=True,
            disabled=not can_go_previous,
            key="sleep_previous_week",
        ):

            st.session_state[
                "sleep_selected_week_start"
            ] = previous_week_start

            st.session_state[
                "sleep_week_manual_navigation"
            ] = True

            st.rerun()

    with navigation_middle:

        current_theme = st.session_state.get(
            "theme",
            "Dark"
        )

        if current_theme == "White":

            week_box_background = "#ffffff"
            week_box_color = "#1f2937"
            week_box_border = "rgba(0,0,0,0.16)"

        else:

            week_box_background = "#161922"
            week_box_color = "#f5f5f5"
            week_box_border = "rgba(255,255,255,0.12)"

        st.markdown(
            f"""
            <div style="
                text-align: center;
                padding: 14px 10px;
                border-radius: 10px;
                background-color: {week_box_background};
                color: {week_box_color};
                border: 1px solid {week_box_border};
                font-size: 1rem;
                font-weight: 700;
                min-height: 20px;
            ">
                {format_week_range(selected_week_start)}
            </div>
            """,
            unsafe_allow_html=True,
        )

    with navigation_right:

        if st.button(
            "Next Week →",
            use_container_width=True,
            disabled=not can_go_next,
            key="sleep_next_week",
        ):

            st.session_state[
                "sleep_selected_week_start"
            ] = next_week_start

            if next_week_start == current_week_start:

                st.session_state[
                    "sleep_week_manual_navigation"
                ] = False

            else:

                st.session_state[
                    "sleep_week_manual_navigation"
                ] = True

            st.rerun()

    # ========================================================
    # BUILD ALL SEVEN CALENDAR DAYS
    # ========================================================

    week_days = get_week_days(
        selected_week_start
    )

    # Fixed Monday -> Sunday labels.
    day_labels = [
        current_day.strftime("%a")
        for current_day in week_days
    ]

    chart_rows = []

    # Used ONLY for the average.
    # Missing sleep records are NOT treated as zero.
    valid_average_values = []

    for current_day in week_days:

        # ----------------------------------------------------
        # DAY BEFORE REGISTRATION
        # ----------------------------------------------------

        if current_day < registration_date:

            chart_value = 0.0
            chart_status = "Before registration"

        # ----------------------------------------------------
        # FUTURE DAY
        # ----------------------------------------------------

        elif current_day > today:

            chart_value = 0.0
            chart_status = "Future"

        # ----------------------------------------------------
        # RECORDED DAY
        # ----------------------------------------------------

        elif current_day in sleep_by_date:

            chart_value = sleep_by_date[
                current_day
            ]

            chart_status = "Recorded"

            valid_average_values.append(
                chart_value
            )

        # ----------------------------------------------------
        # PAST/VALID DAY WITHOUT A RECORD
        # ----------------------------------------------------

        else:

            chart_value = 0.0
            chart_status = "No record"

        chart_rows.append(
            {
                "Day": current_day.strftime("%a"),
                "Date": current_day,
                "Hours Slept": chart_value,
                "Status": chart_status,
            }
        )

    chart_df = pd.DataFrame(
        chart_rows
    )

    # ========================================================
    # WEEKLY AVERAGE
    #
    # IMPORTANT:
    # Only actual sleep records are included.
    # Missing days are NOT counted as 0 hours.
    # ========================================================

    if valid_average_values:

        average_hours = (
            sum(valid_average_values)
            / len(valid_average_values)
        )

    else:

        average_hours = 0.0

    st.markdown(
        dedent(f"""
        <div style="
            font-size:1.05rem;
            font-weight:800;
            margin-top:22px;
            margin-bottom:12px;
        ">
            Daily average: {average_hours:.2f} hours
        </div>
        """),
        unsafe_allow_html=True,
    )

    # ========================================================
    # WEEKLY GRAPH
    #
    # Altair is used instead of st.bar_chart so that all
    # seven calendar days remain visible even when some days
    # have no recorded sleep.
    # ========================================================

    sleep_chart = (
        alt.Chart(chart_df)
        .mark_bar(
            size=55,
        )
        .encode(
            x=alt.X(
                "Day:N",
                title="Day",
                sort=day_labels,
                axis=alt.Axis(
                    labelAngle=0,
                ),
            ),
            y=alt.Y(
                "Hours Slept:Q",
                title="Hours Slept",
                scale=alt.Scale(
                    domainMin=0,
                ),
            ),
            tooltip=[
                alt.Tooltip(
                    "Date:T",
                    title="Date",
                    format="%d %b %Y",
                ),
                alt.Tooltip(
                    "Hours Slept:Q",
                    title="Sleep",
                    format=".1f",
                ),
                alt.Tooltip(
                    "Status:N",
                    title="Status",
                ),
            ],
        )
        .properties(
            height=380,
        )
    )

    st.altair_chart(
        sleep_chart,
        use_container_width=True,
    )

    # ========================================================
    # WEEK INFORMATION MESSAGE
    # ========================================================

    if selected_week_start == registration_week_start:

        if selected_week_start < current_week_start:

            st.markdown(
                dedent("""
                <div class="week-note">
                    This was your registration week.
                    Days before registration are not included
                    in the sleep average.
                </div>
                """),
                unsafe_allow_html=True,
            )

        else:

            st.markdown(
                dedent("""
                <div class="week-note">
                    This is your registration week.
                    Days before registration are blank,
                    and future days remain empty.
                </div>
                """),
                unsafe_allow_html=True,
            )

    elif selected_week_start == current_week_start:

        st.markdown(
            dedent("""
            <div class="week-note">
                This week updates as you record sleep.
                Future days remain empty.
            </div>
            """),
            unsafe_allow_html=True,
        )

    else:

        st.markdown(
            dedent("""
            <div class="week-note">
                This week shows your recorded sleep history.
                Days without a sleep record remain empty.
            </div>
            """),
            unsafe_allow_html=True,
        )

    # ========================================================
    # SLEEP HISTORY
    #
    # Only actual database records are displayed.
    # Missing days are not added to the history table.
    # ========================================================

    st.divider()

    st.markdown(
        dedent("""
        <div class="card-heading">
            🗓️ Sleep History
        </div>
        """),
        unsafe_allow_html=True,
    )

    if history:

        table_rows = []

        for record in history[:7]:

            hours = float(
                record.get(
                    "sleep_hours",
                    0,
                )
            )

            table_rows.append(
                {
                    "Date": str(
                        record.get(
                            "record_date",
                            "",
                        )
                    ),
                    "Hours Slept": (
                        f"{hours:.1f} hours"
                    ),
                }
            )

        history_df = pd.DataFrame(
            table_rows
        )

        st.dataframe(
            history_df,
            use_container_width=True,
            hide_index=True,
        )

    else:

        st.info(
            "No sleep history available yet."
        )

    # ========================================================
    # CLOSE PAGE WRAPPER
    # ========================================================

    st.markdown(
        "</div>",
        unsafe_allow_html=True,
    )