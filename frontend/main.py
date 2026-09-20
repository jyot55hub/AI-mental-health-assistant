
import sys
from pathlib import Path

# Add the project root to Python's import path
PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import streamlit as st

from app.backend.database import initialize_database
from frontend.login import show_login
from frontend.registration import show_registration
from frontend.dashboard import show_dashboard
from frontend.questionnaire import show_questionnaire
from frontend.chatbot import show_chatbot
from frontend.sleep_tracking import show_sleep_tracking
from frontend.meditation import show_meditation

# -------------------------------------------------
# Page configuration
# -------------------------------------------------

st.set_page_config(
    page_title="MindCare",
    page_icon="🌿",
    layout="centered",
    initial_sidebar_state="collapsed"
)


# -------------------------------------------------
# Custom styling
# -------------------------------------------------

st.markdown(
    """
    <style>
        #MainMenu {
            visibility: hidden;
        }

        footer {
            visibility: hidden;
        }

        [data-testid="stHeader"] {
            background: transparent;
        }

        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
            max-width: 760px;
        }
    </style>
    """,
    unsafe_allow_html=True
)


# -------------------------------------------------
# Session state
# -------------------------------------------------

def initialize_session():

    if "page" not in st.session_state:
        st.session_state["page"] = "login"

    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False


# -------------------------------------------------
# MindCare branding
# -------------------------------------------------

def show_branding():

    st.markdown(
        """
        <div style="text-align: center; padding: 1rem 0 1.5rem 0;">
            <h1 style="color: #315943; font-size: 3rem;">
                🌿 MindCare
            </h1>
            <p style="color: #6B8074; font-size: 1.1rem;">
                Your space for everyday well-being
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )


# -------------------------------------------------
# Main application
# -------------------------------------------------

def main():

    # Initialize the existing database
    initialize_database()

    # Initialize session variables
    initialize_session()

    # -------------------------------------------------
    # Logged-in user navigation
    # -------------------------------------------------

    if st.session_state["logged_in"]:

        st.sidebar.title("🌿 MindCare")
        st.sidebar.write("Navigate to a section")

        page_options = [
            "🏠 Dashboard",
            "📝 Questionnaire",
            "💬 Chatbot",
            "🌙 Sleep Tracking",
            "🧘‍♀️ Meditation"
        ]

        page_keys = [
            "dashboard",
            "questionnaire",
            "chatbot",
            "sleep_tracking",
            "meditation"
        ]

        current_page = st.session_state.get("page", "dashboard")

        # Use Dashboard as the default for invalid page values
        if current_page not in page_keys:
            current_page = "dashboard"
            st.session_state["page"] = current_page

        # Select the correct sidebar option based on the current page
        selected_index = page_keys.index(current_page)

        selected_page = st.sidebar.radio(
            "Choose a page",
            page_options,
            index=selected_index
        )

        selected_page_index = page_options.index(selected_page)
        selected_page_key = page_keys[selected_page_index]

        # Change page only when the user selects a different sidebar option
        if selected_page_key != st.session_state.get("page"):
            st.session_state["page"] = selected_page_key
            st.rerun()

        # -------------------------------------------------
        # Display the selected page
        # -------------------------------------------------

        if st.session_state["page"] == "questionnaire":
            show_questionnaire()

        elif st.session_state["page"] == "chatbot":
            show_chatbot()

        elif st.session_state["page"] == "sleep_tracking":
            show_sleep_tracking()

        elif st.session_state["page"] == "meditation":
            show_meditation()

        else:
            show_dashboard()

        return

    # -------------------------------------------------
    # Authentication pages
    # -------------------------------------------------

    show_branding()

    page = st.radio(
        "Choose an option",
        ["Login", "Register"],
        horizontal=True,
        index=0 if st.session_state["page"] == "login" else 1
    )

    st.session_state["page"] = (
        "login" if page == "Login" else "register"
    )

    # Display the selected authentication page
    if st.session_state["page"] == "login":
        show_login()
    else:
        show_registration()


# -------------------------------------------------
# Application entry point
# -------------------------------------------------

if __name__ == "__main__":
    main()
