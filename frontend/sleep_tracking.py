
import streamlit as st
from datetime import date
import pandas as pd

from app.backend.sleep import (
    save_sleep_record,
    get_sleep_record,
    get_sleep_history,
)


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

    day_index = date.today().timetuple().tm_yday % len(quotes)
    return quotes[day_index]


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


def show_sleep_tracking():
    """Display the complete sleep tracking page."""

    # -----------------------------
    # Custom page styling
    # -----------------------------
    st.markdown(
        """
        <style>
        @import url(
            'https://fonts.googleapis.com/css2?family=Nunito:wght@400;500;600;700;800&display=swap'
        );

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
            box-shadow: 0 4px 14px rgba(80, 70, 130, 0.07);
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
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="sleep-page">', unsafe_allow_html=True)

    # -----------------------------
    # Page heading
    # -----------------------------
    st.title("🌙 Sleep Tracking")

    st.markdown(
        '<div class="sleep-subtitle">'
        "Track your daily sleep and maintain healthy sleep habits."
        "</div>",
        unsafe_allow_html=True,
    )

    # -----------------------------
    # Login verification
    # -----------------------------
    user_id = st.session_state.get("user_id")

    if not user_id:
        st.warning("Please log in to track your sleep.")
        st.markdown("</div>", unsafe_allow_html=True)
        return

    today = date.today().isoformat()

    # -----------------------------
    # Daily motivational quote
    # -----------------------------
    st.markdown(
        f"""
        <div class="sleep-quote">
            <div class="quote-text">
                ❝ {get_daily_quote()} ❞
            </div>
            <div class="quote-author">— MindCare</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # -----------------------------
    # Record today's sleep
    # -----------------------------
    st.markdown('<div class="sleep-card">', unsafe_allow_html=True)

    st.markdown(
        '<div class="card-heading">🛏️ Record Today\'s Sleep</div>',
        unsafe_allow_html=True,
    )

    existing_record = get_sleep_record(user_id, today)

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
            record_date=today,
        )

        if result.get("success"):
            st.session_state["sleep_success_message"] = (
                "Sleep record saved successfully! ✅"
            )
            st.rerun()
        else:
            st.error(
                result.get(
                    "message",
                    "Unable to save sleep record.",
                )
            )

    if st.session_state.get("sleep_success_message"):
        st.success(st.session_state["sleep_success_message"])
        st.session_state.pop("sleep_success_message", None)

    st.markdown("</div>", unsafe_allow_html=True)

    # -----------------------------
    # Today's sleep summary
    # -----------------------------
    st.markdown('<div class="sleep-card">', unsafe_allow_html=True)

    st.markdown(
        '<div class="card-heading">📊 Today\'s Sleep Summary</div>',
        unsafe_allow_html=True,
    )

    today_record = get_sleep_record(user_id, today)

    if today_record.get("success"):
        hours = float(today_record["record"]["sleep_hours"])

        message, message_type = get_sleep_message(hours)

        summary_col, status_col = st.columns(2)

        with summary_col:
            st.markdown(
                f"""
                <div class="summary-box">
                    <div class="summary-label">🛏️ Sleep Duration</div>
                    <div class="summary-value">{hours:.1f} hours</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with status_col:
            if message_type == "success":
                st.success(f"😊 {message}")
            elif message_type == "warning":
                st.warning(message)
            else:
                st.info(message)

        st.markdown(
            """
            <div class="recommendation-box">
                <div class="recommendation-title">
                    💡 Recommended Sleep Duration
                </div>
                <div class="recommendation-text">
                    Adults generally need 7–9 hours of sleep per night
                    for better physical and mental well-being.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    else:
        st.info("No sleep record has been added for today.")

    st.markdown("</div>", unsafe_allow_html=True)

    # -----------------------------
    # Seven-day sleep history chart
    # -----------------------------
    history_result = get_sleep_history(user_id, limit=7)

    if history_result.get("success") and history_result.get("records"):
        history = history_result["records"]

        chart_rows = []

        for record in reversed(history):
            chart_rows.append(
                {
                    "Date": str(record["record_date"])[5:],
                    "Hours Slept": float(record["sleep_hours"]),
                }
            )

        chart_df = pd.DataFrame(chart_rows)

        st.markdown('<div class="sleep-card">', unsafe_allow_html=True)

        st.markdown(
            '<div class="card-heading">📊 Your Sleep History — Last 7 Days</div>',
            unsafe_allow_html=True,
        )

        st.caption("Recommended sleep duration: 7–9 hours per night.")

        st.bar_chart(
            chart_df,
            x="Date",
            y="Hours Slept",
            height=330,
            use_container_width=True,
        )

        average_hours = chart_df["Hours Slept"].mean()

        st.markdown(
            f"""
            <div class="history-note">
                📈 <b>Your average sleep over the last 7 days is
                {average_hours:.1f} hours.</b><br>
                Try to maintain a consistent sleep schedule for
                better well-being.
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("</div>", unsafe_allow_html=True)

        # -----------------------------
        # Recent sleep history table
        # -----------------------------
        st.markdown('<div class="sleep-card">', unsafe_allow_html=True)

        st.markdown(
            '<div class="card-heading">🗓️ Recent Sleep History</div>',
            unsafe_allow_html=True,
        )

        table_rows = []

        for record in history:
            table_rows.append(
                {
                    "Date": str(record["record_date"]),
                    "Hours Slept": (
                        f"{float(record['sleep_hours']):.1f} hours"
                    ),
                }
            )

        history_df = pd.DataFrame(table_rows)

        st.dataframe(
            history_df,
            use_container_width=True,
            hide_index=True,
        )

        st.markdown("</div>", unsafe_allow_html=True)

    else:
        st.info("No sleep history available yet.")

    st.markdown("</div>", unsafe_allow_html=True)
