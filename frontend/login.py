
import streamlit as st
from app.backend.auth import login_user


def show_login():
    """Display the MindCare login form."""

    st.markdown(
        """
        <div class="auth-heading">
            <h1>Welcome back! ✨</h1>
            <p>Sign in to continue your MindCare journey.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    with st.form("login_form"):
        email = st.text_input(
            "Email address",
            placeholder="Enter your email",
            key="login_email"
        )

        password = st.text_input(
            "Password",
            type="password",
            placeholder="Enter your password",
            key="login_password"
        )

        submitted = st.form_submit_button(
            "Sign in →",
            use_container_width=True
        )

    if submitted:
        if not email.strip() or not password:
            st.error("Please enter your email and password.")
            return

        result = login_user(email.strip(), password)

        if result.get("success"):
            st.session_state["logged_in"] = True
            st.session_state["user"] = result["user"]
            st.session_state["user_id"] = result["user"]["id"]
            st.session_state["page"] = "dashboard"
            st.success("Login successful!")
            st.rerun()
        else:
            st.error(
                result.get("message", "Invalid email or password.")
            )

    st.markdown(
        "<p class='auth-footer'>Your well-being matters. 💚</p>",
        unsafe_allow_html=True
    )