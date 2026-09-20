
import streamlit as st
from app.backend.auth import register_user


def show_registration():
    st.markdown("## Create your account 🌿")
    st.write("Join MindCare and start your well-being journey.")

    with st.form("registration_form"):
        name = st.text_input(
            "Full name",
            placeholder="Enter your full name"
        )

        email = st.text_input(
            "Email address",
            placeholder="Enter your email"
        )

        password = st.text_input(
            "Password",
            type="password",
            placeholder="At least 6 characters"
        )

        confirm_password = st.text_input(
            "Confirm password",
            type="password"
        )

        submitted = st.form_submit_button(
            "Create account",
            type="primary",
            use_container_width=True
        )

    if submitted:
        if not name.strip() or not email.strip() or not password:
            st.error("Please fill in all fields.")
            return

        if password != confirm_password:
            st.error("Passwords do not match.")
            return

        result = register_user(name, email, password)

        if result.get("success"):
            st.success("Registration successful! Please log in.")
            st.session_state["page"] = "login"
            st.rerun()
        else:
            st.error(result.get("message", "Registration failed."))