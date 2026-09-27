import sys
from pathlib import Path

# -------------------------------------------------
# Add project root to Python path
# -------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


import streamlit as st

from app.backend.database import initialize_database
from app.backend.auth import get_user_profile

from frontend.login import show_login
from frontend.registration import show_registration
from frontend.dashboard import show_dashboard
from frontend.questionnaire import show_questionnaire
from frontend.chatbot import show_chatbot
from frontend.sleep_tracking import show_sleep_tracking
from frontend.meditation import show_meditation
from frontend.user_profile import show_profile
from frontend.settings import show_settings


# =================================================
# PAGE CONFIGURATION
# =================================================

st.set_page_config(
    page_title="MindCare",
    page_icon="🌿",
    layout="centered",
    initial_sidebar_state="expanded"
)


# =================================================
# SESSION STATE
# =================================================

def initialize_session():

    if "page" not in st.session_state:
        st.session_state["page"] = "login"

    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False

    if "theme" not in st.session_state:
        st.session_state["theme"] = "Dark"


# =================================================
# GLOBAL STYLING
# =================================================

def apply_global_styles():

    theme = st.session_state.get("theme", "Dark")


    # =================================================
    # DARK THEME
    # =================================================

    if theme == "Dark":

        st.markdown(
            """
<style>

.stApp {
    background-color: #0e1117 !important;
    color: #f5f5f5 !important;
}

[data-testid="stAppViewContainer"] {
    background-color: #0e1117 !important;
}


/* -----------------------------------------
   Sidebar
----------------------------------------- */

section[data-testid="stSidebar"],
section[data-testid="stSidebar"] > div {
    background-color: #262630 !important;
}

section[data-testid="stSidebar"] * {
    color: #f5f5f5;
}

section[data-testid="stSidebar"]
[data-testid="stCaptionContainer"] {
    color: #9ca3af !important;
}


/* -----------------------------------------
   Sidebar navigation buttons
----------------------------------------- */

section[data-testid="stSidebar"] .stButton > button {
    width: 100% !important;

    background: transparent !important;

    color: #f5f5f5 !important;

    border: none !important;

    border-radius: 10px !important;

    min-height: 42px !important;

    text-align: left !important;
}

section[data-testid="stSidebar"] .stButton > button:hover {
    background-color: rgba(49, 89, 67, 0.18) !important;

    color: #ffffff !important;
}


/* -----------------------------------------
   Main text
----------------------------------------- */

.stMarkdown,
.stMarkdown p,
.stMarkdown span,
.stText,
label,
h1,
h2,
h3,
h4,
h5,
h6,
p {
    color: #f5f5f5 !important;
}


/* -----------------------------------------
   Inputs
----------------------------------------- */

input,
textarea {
    background-color: #262630 !important;

    color: #ffffff !important;

    border-color: rgba(255,255,255,0.16) !important;
}

input::placeholder,
textarea::placeholder {
    color: #9ca3af !important;
}


/* -----------------------------------------
   Select boxes
----------------------------------------- */

div[data-baseweb="select"] > div {
    background-color: #262630 !important;

    color: #ffffff !important;

    border-color: rgba(255,255,255,0.16) !important;
}


/* -----------------------------------------
   Main buttons
----------------------------------------- */

.stButton > button {
    background-color: #161922 !important;

    color: #ffffff !important;

    border: 1px solid rgba(255,255,255,0.14) !important;

    border-radius: 10px !important;
}

.stButton > button:hover {
    background-color: #315943 !important;

    color: #ffffff !important;

    border-color: #315943 !important;
}


/* -----------------------------------------
   Radio buttons
----------------------------------------- */

div[data-testid="stRadio"] label {
    color: #f5f5f5 !important;
}


/* -----------------------------------------
   Checkbox
----------------------------------------- */

div[data-testid="stCheckbox"] label {
    color: #f5f5f5 !important;
}


/* -----------------------------------------
   Chat input
----------------------------------------- */

[data-testid="stChatInput"] {
    background-color: #161922 !important;
}

[data-testid="stChatInput"] textarea {
    background-color: #262630 !important;

    color: #ffffff !important;
}


/* -----------------------------------------
   Links
----------------------------------------- */

a {
    color: #9fd3b1 !important;
}


/* -----------------------------------------
   Tables
----------------------------------------- */

[data-testid="stDataFrame"] {
    background-color: #161922 !important;
}


/* -----------------------------------------
   Metrics
----------------------------------------- */

[data-testid="stMetricValue"],
[data-testid="stMetricLabel"] {
    color: #f5f5f5 !important;
}


/* -----------------------------------------
   Expanders
----------------------------------------- */

[data-testid="stExpander"] {
    background-color: #161922 !important;

    border-color: rgba(255,255,255,0.12) !important;
}


/* -----------------------------------------
   Alerts
----------------------------------------- */

[data-testid="stAlert"] {
    color: #f5f5f5 !important;
}


/* -----------------------------------------
   Theme selector
----------------------------------------- */

.mindcare-theme-label {
    color: #9ca3af !important;

    font-size: 0.78rem;

    font-weight: 500;

    margin-bottom: 0.4rem;
}


/* -----------------------------------------
   Account section
----------------------------------------- */

.mindcare-account-label {
    color: #9ca3af !important;

    font-size: 0.78rem;

    font-weight: 500;

    margin-bottom: 0.45rem;
}

</style>
""",
            unsafe_allow_html=True
        )

        return


    # =================================================
    # WHITE THEME
    # =================================================

    if theme == "White":

        st.markdown(
            """
<style>

.stApp {
    background-color: #ffffff !important;
    color: #1f2937 !important;
}

[data-testid="stAppViewContainer"] {
    background-color: #ffffff !important;
}


/* -----------------------------------------
   Sidebar
----------------------------------------- */

section[data-testid="stSidebar"],
section[data-testid="stSidebar"] > div {
    background-color: #f5f7f6 !important;
}

section[data-testid="stSidebar"] * {
    color: #1f2937 !important;
}

section[data-testid="stSidebar"]
[data-testid="stCaptionContainer"] {
    color: #64748b !important;
}


/* -----------------------------------------
   Sidebar navigation
----------------------------------------- */

section[data-testid="stSidebar"] .stButton > button {
    width: 100% !important;

    background-color: transparent !important;

    color: #1f2937 !important;

    border: none !important;

    border-radius: 10px !important;

    min-height: 42px !important;

    text-align: left !important;
}

section[data-testid="stSidebar"] .stButton > button:hover {
    background-color: rgba(49, 89, 67, 0.10) !important;

    color: #315943 !important;
}


/* -----------------------------------------
   Main text
----------------------------------------- */

.stMarkdown,
.stMarkdown p,
.stMarkdown span,
.stText,
label,
h1,
h2,
h3,
h4,
h5,
h6,
p {
    color: #1f2937 !important;
}


/* -----------------------------------------
   Inputs
----------------------------------------- */

input,
textarea {
    background-color: #ffffff !important;

    color: #1f2937 !important;

    border: 1px solid rgba(0,0,0,0.20) !important;
}

input::placeholder,
textarea::placeholder {
    color: #64748b !important;
}


/* -----------------------------------------
   Select boxes
----------------------------------------- */

div[data-baseweb="select"] > div {
    background-color: #ffffff !important;

    color: #1f2937 !important;

    border: 1px solid rgba(0,0,0,0.20) !important;
}


/* Dropdown menu options */

div[data-baseweb="popover"] {
    background-color: #ffffff !important;
}

div[data-baseweb="popover"] * {
    color: #1f2937 !important;
}


/* -----------------------------------------
   Main buttons
----------------------------------------- */

.stButton > button {
    background-color: #ffffff !important;

    color: #1f2937 !important;

    border: 1px solid rgba(0,0,0,0.18) !important;

    border-radius: 10px !important;
}

.stButton > button:hover {
    background-color: #eef6f0 !important;

    color: #315943 !important;

    border-color: #315943 !important;
}


/* -----------------------------------------
   Radio buttons
----------------------------------------- */

div[data-testid="stRadio"] label {
    color: #1f2937 !important;
}


/* -----------------------------------------
   Checkbox
----------------------------------------- */

div[data-testid="stCheckbox"] label {
    color: #1f2937 !important;
}


/* -----------------------------------------
   Chat input
----------------------------------------- */

[data-testid="stChatInput"] {
    background-color: #ffffff !important;
}

[data-testid="stChatInput"] textarea {
    background-color: #ffffff !important;

    color: #1f2937 !important;

    border: 1px solid rgba(0,0,0,0.18) !important;
}


/* -----------------------------------------
   Links
----------------------------------------- */

a {
    color: #315943 !important;
}


/* -----------------------------------------
   Tables
----------------------------------------- */

[data-testid="stDataFrame"] {
    background-color: #ffffff !important;
}


/* -----------------------------------------
   Metrics
----------------------------------------- */

[data-testid="stMetricValue"],
[data-testid="stMetricLabel"] {
    color: #1f2937 !important;
}


/* -----------------------------------------
   Expanders
----------------------------------------- */

[data-testid="stExpander"] {
    background-color: #ffffff !important;

    border-color: rgba(0,0,0,0.12) !important;
}


/* -----------------------------------------
   Alerts
----------------------------------------- */

[data-testid="stAlert"] {
    color: #1f2937 !important;
}


/* -----------------------------------------
   Theme selector
----------------------------------------- */

.mindcare-theme-label {
    color: #64748b !important;

    font-size: 0.78rem;

    font-weight: 500;

    margin-bottom: 0.4rem;
}


/* -----------------------------------------
   Account section
----------------------------------------- */

.mindcare-account-label {
    color: #64748b !important;

    font-size: 0.78rem;

    font-weight: 500;

    margin-bottom: 0.45rem;
}


/* -----------------------------------------
   Profile button in light mode
----------------------------------------- */

section[data-testid="stSidebar"]
button[kind="secondary"] {
    color: #1f2937 !important;
}

</style>
""",
            unsafe_allow_html=True
        )

        return


    # =================================================
    # DEVICE THEME
    # =================================================

    if theme == "Device":

        st.markdown(
            """
<style>

/* =========================================
   DEFAULT DEVICE THEME
========================================= */

.stApp {
    background-color: #0e1117;
    color: #f5f5f5;
}

[data-testid="stAppViewContainer"] {
    background-color: #0e1117;
}

section[data-testid="stSidebar"],
section[data-testid="stSidebar"] > div {
    background-color: #262630;
}


/* =========================================
   DEVICE LIGHT MODE
========================================= */

@media (prefers-color-scheme: light) {

    .stApp {
        background-color: #ffffff !important;

        color: #1f2937 !important;
    }

    [data-testid="stAppViewContainer"] {
        background-color: #ffffff !important;
    }


    /* Sidebar */

    section[data-testid="stSidebar"],
    section[data-testid="stSidebar"] > div {
        background-color: #f5f7f6 !important;
    }

    section[data-testid="stSidebar"] * {
        color: #1f2937 !important;
    }


    /* Main text */

    .stMarkdown,
    .stMarkdown p,
    .stMarkdown span,
    .stText,
    label,
    h1,
    h2,
    h3,
    h4,
    h5,
    h6,
    p {
        color: #1f2937 !important;
    }


    /* Sidebar buttons */

    section[data-testid="stSidebar"] .stButton > button {
        background-color: transparent !important;

        color: #1f2937 !important;

        border: none !important;
    }

    section[data-testid="stSidebar"] .stButton > button:hover {
        background-color: rgba(49, 89, 67, 0.10) !important;

        color: #315943 !important;
    }


    /* Main buttons */

    .stButton > button {
        background-color: #ffffff !important;

        color: #1f2937 !important;

        border: 1px solid rgba(0,0,0,0.18) !important;
    }

    .stButton > button:hover {
        background-color: #eef6f0 !important;

        color: #315943 !important;

        border-color: #315943 !important;
    }


    /* Inputs */

    input,
    textarea {
        background-color: #ffffff !important;

        color: #1f2937 !important;

        border-color: rgba(0,0,0,0.18) !important;
    }

    input::placeholder,
    textarea::placeholder {
        color: #64748b !important;
    }


    /* Select */

    div[data-baseweb="select"] > div {
        background-color: #ffffff !important;

        color: #1f2937 !important;
    }


    /* Chat input */

    [data-testid="stChatInput"] {
        background-color: #ffffff !important;
    }

    [data-testid="stChatInput"] textarea {
        background-color: #ffffff !important;

        color: #1f2937 !important;
    }


    /* Links */

    a {
        color: #315943 !important;
    }


    /* Theme label */

    .mindcare-theme-label {
        color: #64748b !important;
    }


    /* Account label */

    .mindcare-account-label {
        color: #64748b !important;
    }

}

</style>
""",
            unsafe_allow_html=True
        )


# =================================================
# MINDCARE BRANDING
# =================================================

def show_branding():

    branding_html = (
        '<div style="text-align:center; padding:1rem 0 1.5rem 0;">'
        '<div style="'
        'color:#315943; '
        'font-size:3rem; '
        'font-weight:700; '
        'line-height:1.2; '
        'margin-bottom:0.5rem;'
        '">'
        '🌿 MindCare'
        '</div>'
        '<div style="'
        'color:#6B8074; '
        'font-size:1.1rem; '
        'margin-bottom:1.5rem;'
        '">'
        'Your space for everyday well-being'
        '</div>'
        '</div>'
    )

    st.markdown(
        branding_html,
        unsafe_allow_html=True
    )


# =================================================
# SIDEBAR NAVIGATION
# =================================================

def show_sidebar_navigation():

    st.sidebar.title("🌿 MindCare")

    st.sidebar.caption(
        "Your space for everyday well-being"
    )

    st.sidebar.markdown(
        "<div style='height: 0.8rem;'></div>",
        unsafe_allow_html=True
    )


    # ---------------------------------------------
    # Navigation items
    # ---------------------------------------------

    navigation = [

        ("🏠", "Dashboard", "dashboard"),

        ("📝", "Questionnaire", "questionnaire"),

        ("💬", "Chatbot", "chatbot"),

        ("😴", "Sleep Tracking", "sleep_tracking"),

        ("🧘", "Meditation", "meditation"),

        ("⚙️", "Settings", "settings"),

    ]


    # ---------------------------------------------
    # Navigation buttons
    # ---------------------------------------------

    for icon, label, page_key in navigation:

        button_label = f"{icon}  {label}"

        if st.sidebar.button(
            button_label,
            key=f"nav_{page_key}",
            use_container_width=True
        ):

            if st.session_state.get("page") != page_key:

                st.session_state["page"] = page_key

                st.rerun()


# =================================================
# THEME SELECTOR
# =================================================

def show_theme_selector():

    st.sidebar.markdown(
        "<div style='height: 1rem;'></div>",
        unsafe_allow_html=True
    )

    st.sidebar.markdown(
        """
<div class="mindcare-theme-label">
    APPEARANCE
</div>
""",
        unsafe_allow_html=True
    )

    current_theme = st.session_state.get(
        "theme",
        "Dark"
    )

    selected_theme = st.sidebar.selectbox(
        "Appearance",
        ["Dark", "White", "Device"],
        index=[
            "Dark",
            "White",
            "Device"
        ].index(current_theme),
        label_visibility="collapsed",
        key="theme_selector"
    )

    if selected_theme != current_theme:

        st.session_state["theme"] = selected_theme

        st.rerun()


# =================================================
# SIDEBAR PROFILE / ACCOUNT
# =================================================

def show_sidebar_profile():

    user_id = st.session_state.get("user_id")

    if not user_id:
        return


    profile_result = get_user_profile(user_id)

    if not profile_result.get("success"):
        return


    profile = profile_result["profile"]

    name = profile.get("name") or "User"

    avatar = profile.get("avatar") or "🌿"


    # ---------------------------------------------
    # Account heading
    # ---------------------------------------------

    st.sidebar.markdown(
        "<div style='height: 0.8rem;'></div>",
        unsafe_allow_html=True
    )

    st.sidebar.markdown(
        """
<div class="mindcare-account-label">
    ACCOUNT
</div>
""",
        unsafe_allow_html=True
    )


    # ---------------------------------------------
    # Profile button
    # ---------------------------------------------

    if st.sidebar.button(
        f"{avatar}   {name}   ›",
        key="sidebar_profile_button",
        use_container_width=True
    ):

        st.session_state["page"] = "profile"

        st.rerun()


# =================================================
# LOGOUT
# =================================================

def logout_user():

    # Remove logged-in user information
    st.session_state.pop("user", None)
    st.session_state.pop("user_id", None)

    # Mark the user as logged out
    st.session_state["logged_in"] = False

    # Return to login page
    st.session_state["page"] = "login"

    # Refresh the application
    st.rerun()


# =================================================
# MAIN APPLICATION
# =================================================

def main():

    # ---------------------------------------------
    # Initialize database
    # ---------------------------------------------

    initialize_database()


    # ---------------------------------------------
    # Initialize session
    # ---------------------------------------------

    initialize_session()


    # ---------------------------------------------
    # Apply selected appearance
    # ---------------------------------------------

    apply_global_styles()


    # =================================================
    # LOGGED-IN USER
    # =================================================

    if st.session_state["logged_in"]:

        # -----------------------------------------
        # Main navigation
        # -----------------------------------------

        show_sidebar_navigation()


        # -----------------------------------------
        # Current page
        # -----------------------------------------

        current_page = st.session_state.get(
            "page",
            "dashboard"
        )


        # -----------------------------------------
        # Dashboard
        # -----------------------------------------

        if current_page == "dashboard":

            show_dashboard()


        # -----------------------------------------
        # Questionnaire
        # -----------------------------------------

        elif current_page == "questionnaire":

            show_questionnaire()


        # -----------------------------------------
        # Chatbot
        # -----------------------------------------

        elif current_page == "chatbot":

            show_chatbot()


        # -----------------------------------------
        # Sleep Tracking
        # -----------------------------------------

        elif current_page == "sleep_tracking":

            show_sleep_tracking()


        # -----------------------------------------
        # Meditation
        # -----------------------------------------

        elif current_page == "meditation":

            show_meditation()


        # -----------------------------------------
        # Settings
        # -----------------------------------------

        elif current_page == "settings":

            show_settings()


        # -----------------------------------------
        # Profile
        # -----------------------------------------

        elif current_page == "profile":

            show_profile()


        # -----------------------------------------
        # Fallback
        # -----------------------------------------

        else:

            st.session_state["page"] = "dashboard"

            show_dashboard()


        # -----------------------------------------
        # Bottom sidebar controls
        # -----------------------------------------

        show_theme_selector()

        show_sidebar_profile()


        # -----------------------------------------
        # Logout
        # -----------------------------------------

        if st.sidebar.button(
            "🚪 Logout",
            key="sidebar_logout_button",
            use_container_width=True
        ):

            logout_user()

        return


    # =================================================
    # AUTHENTICATION
    # =================================================

    show_branding()


    page = st.radio(
        "Choose an option",
        ["Login", "Register"],
        horizontal=True,
        index=(
            0
            if st.session_state["page"] == "login"
            else 1
        )
    )


    st.session_state["page"] = (
        "login"
        if page == "Login"
        else "register"
    )


    # ---------------------------------------------
    # Login
    # ---------------------------------------------

    if st.session_state["page"] == "login":

        show_login()


    # ---------------------------------------------
    # Registration
    # ---------------------------------------------

    else:

        show_registration()


# =================================================
# APPLICATION ENTRY POINT
# =================================================

if __name__ == "__main__":

    main()