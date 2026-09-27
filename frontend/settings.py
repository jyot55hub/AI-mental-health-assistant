import streamlit as st

from app.backend.auth import (
    delete_user_account,
    change_user_password
)

from app.backend.preferences import (
    get_notification_preferences,
    save_notification_preferences
)


# ---------------------------------------------------------
# SETTINGS PAGE
# ---------------------------------------------------------

def show_settings():

    st.title("⚙️ Settings")

    st.caption(
        "Customize your MindCare experience."
    )

    # -----------------------------------------------------
    # CURRENT THEME
    # -----------------------------------------------------

    current_theme = st.session_state.get(
        "theme",
        "Dark"
    )

    # -----------------------------------------------------
    # PAGE STYLING
    # -----------------------------------------------------

    if current_theme == "White":

        card_background = "#ffffff"
        card_border = "#e2e8f0"
        card_text = "#1e293b"
        muted_text = "#64748b"
        accent_background = "#f0fdf4"
        accent_border = "#bbf7d0"

    elif current_theme == "Device":

        card_background = "rgba(255,255,255,0.06)"
        card_border = "rgba(255,255,255,0.15)"
        card_text = "inherit"
        muted_text = "inherit"
        accent_background = "rgba(16,185,129,0.10)"
        accent_border = "rgba(16,185,129,0.25)"

    else:

        card_background = "#17221c"
        card_border = "#30483a"
        card_text = "#f8fafc"
        muted_text = "#b8c5bd"
        accent_background = "#14261b"
        accent_border = "#315943"

    # -----------------------------------------------------
    # PAGE CSS
    # -----------------------------------------------------

    st.markdown(
        f"""
<style>

.settings-card {{
    padding: 24px;
    border-radius: 18px;
    background: {card_background};
    border: 1px solid {card_border};
    margin-bottom: 22px;
}}

.settings-card h3 {{
    margin-top: 0;
    margin-bottom: 8px;
    color: {card_text};
}}

.settings-description {{
    color: {muted_text};
    font-size: 14px;
    line-height: 1.6;
    margin-bottom: 0;
}}

.settings-option {{
    padding: 16px;
    border-radius: 14px;
    background: {accent_background};
    border: 1px solid {accent_border};
    margin-top: 12px;
    min-height: 108px;
    height: 108px;
    box-sizing: border-box;
}}

.settings-option-title {{
    font-weight: 600;
    color: {card_text};
    margin-bottom: 4px;
}}

.settings-option-text {{
    color: {muted_text};
    font-size: 13px;
    line-height: 1.5;
}}

</style>
        """,
        unsafe_allow_html=True
    )

    # =====================================================
    # APPEARANCE
    # =====================================================

    st.subheader(
        "🎨 Appearance"
    )

    st.markdown(
        f"""
<div class="settings-card">
<h3>Choose your theme</h3>
<p class="settings-description">
Select how MindCare should look.
Your current theme is <strong>{current_theme}</strong>.
</p>
</div>
        """,
        unsafe_allow_html=True
    )

    # -----------------------------------------------------
    # THEME SELECTOR
    # -----------------------------------------------------

    selected_theme = st.selectbox(
        "Theme",
        [
            "Dark",
            "White",
            "Device"
        ],
        index=[
            "Dark",
            "White",
            "Device"
        ].index(current_theme),
        key="settings_theme_selector"
    )

    # -----------------------------------------------------
    # UPDATE THEME
    # -----------------------------------------------------

    if selected_theme != st.session_state.get(
        "theme"
    ):

        st.session_state["theme"] = selected_theme

        # Keep sidebar selector synchronized.
        st.session_state["theme_selector"] = selected_theme

        st.rerun()

    # -----------------------------------------------------
    # THEME EXPLANATION
    # -----------------------------------------------------

    col1, col2, col3 = st.columns(3)

    with col1:

        st.markdown(
            """
<div class="settings-option">
<div class="settings-option-title">🌙 Dark</div>
<div class="settings-option-text">
A darker interface designed for comfortable
viewing in low-light environments.
</div>
</div>
            """,
            unsafe_allow_html=True
        )

    with col2:

        st.markdown(
            """
<div class="settings-option">
<div class="settings-option-title">☀️ White</div>
<div class="settings-option-text">
A bright and clean interface for a light
appearance.
</div>
</div>
            """,
            unsafe_allow_html=True
        )

    with col3:

        st.markdown(
            """
<div class="settings-option">
<div class="settings-option-title">💻 Device</div>
<div class="settings-option-text">
Uses the appearance preference configured
on your device or browser.
</div>
</div>
            """,
            unsafe_allow_html=True
        )

    # =====================================================
    # NOTIFICATIONS
    # =====================================================

    st.divider()

    st.subheader(
        "🔔 Notifications"
    )

    st.markdown(
        """
<div class="settings-card">
<h3>🔔 Wellness reminders</h3>
<p class="settings-description">
Choose which daily wellness reminders you would like
MindCare to keep enabled.
</p>
</div>
        """,
        unsafe_allow_html=True
    )

    user_id = st.session_state.get(
        "user_id"
    )

    notification_preferences = {}

    if user_id:

        notification_preferences = get_notification_preferences(
            user_id
        )

    # -----------------------------------------------------
    # DEFAULT NOTIFICATION VALUES
    # -----------------------------------------------------

    wellness_reminder_default = notification_preferences.get(
        "wellness_reminder",
        True
    )

    meditation_reminder_default = notification_preferences.get(
        "meditation_reminder",
        True
    )

    sleep_reminder_default = notification_preferences.get(
        "sleep_reminder",
        True
    )

    questionnaire_reminder_default = notification_preferences.get(
        "questionnaire_reminder",
        True
    )

    reminder_time_default = notification_preferences.get(
        "reminder_time",
        "20:00"
    )

    # -----------------------------------------------------
    # NOTIFICATION CHECKBOXES
    # -----------------------------------------------------

    wellness_reminder = st.checkbox(
        "🌿 Daily Wellness Reminder",
        value=bool(wellness_reminder_default),
        key="notification_wellness_reminder"
    )

    meditation_reminder = st.checkbox(
        "🧘 Meditation Reminder",
        value=bool(meditation_reminder_default),
        key="notification_meditation_reminder"
    )

    sleep_reminder = st.checkbox(
        "😴 Sleep Tracking Reminder",
        value=bool(sleep_reminder_default),
        key="notification_sleep_reminder"
    )

    questionnaire_reminder = st.checkbox(
        "📝 Questionnaire Reminder",
        value=bool(questionnaire_reminder_default),
        key="notification_questionnaire_reminder"
    )

    # -----------------------------------------------------
    # REMINDER TIME
    # -----------------------------------------------------

    reminder_time_options = []

    for hour in range(24):

        for minute in (
            0,
            15,
            30,
            45
        ):

            reminder_time_options.append(
                f"{hour:02d}:{minute:02d}"
            )

    if reminder_time_default not in reminder_time_options:

        reminder_time_default = "20:00"

    reminder_time_index = reminder_time_options.index(
        reminder_time_default
    )

    selected_reminder_time = st.selectbox(
        "⏰ Reminder Time",
        reminder_time_options,
        index=reminder_time_index,
        format_func=lambda value: (
            __import__("datetime")
            .datetime
            .strptime(value, "%H:%M")
            .strftime("%I:%M %p")
        ),
        key="notification_reminder_time"
    )

    # -----------------------------------------------------
    # SAVE NOTIFICATION PREFERENCES
    # -----------------------------------------------------

    if st.button(
        "🔔 Save Notification Preferences",
        use_container_width=True,
        key="save_notification_preferences"
    ):

        if not user_id:

            st.error(
                "Unable to identify your account."
            )

        else:

            result = save_notification_preferences(
                user_id=user_id,
                wellness_reminder=wellness_reminder,
                meditation_reminder=meditation_reminder,
                sleep_reminder=sleep_reminder,
                questionnaire_reminder=questionnaire_reminder,
                reminder_time=selected_reminder_time
            )

            if result.get("success"):

                st.success(
                    "✅ Notification preferences saved successfully."
                )

            else:

                st.error(
                    result.get(
                        "message",
                        "Unable to save notification preferences."
                    )
                )

    # =====================================================
    # PRIVACY & DATA
    # =====================================================

    st.divider()

    st.subheader(
        "🔒 Privacy & Data"
    )

    st.markdown(
        f"""
<div class="settings-card">

<h3>🗂️ Your MindCare Data</h3>

<p class="settings-description">
Your MindCare account information and wellness records
are stored for your account and are used to provide the
features available in the application.
</p>

<br>

<h3>👤 Account Privacy</h3>

<p class="settings-description">
Your account data is associated with your registered
MindCare account. Other users cannot access your
personal account information through the application.
</p>

<br>

<h3>📝 Journal Privacy</h3>

<p class="settings-description">
Your personal journal entries are stored privately and
are associated with your own account.
</p>

<br>

<h3>🤖 AI & Chat</h3>

<p class="settings-description">
MindCare can make mistakes. AI responses may not always
be accurate or appropriate. MindCare is a supportive
wellness application and does not replace professional
mental-health care, medical diagnosis, or emergency care.
</p>

</div>
        """,
        unsafe_allow_html=True
    )

    # =====================================================
    # ABOUT MINDCARE
    # =====================================================

    st.divider()

    st.subheader(
        "ℹ️ About MindCare"
    )

    st.markdown(
        """
<div class="settings-card">
<h3>🌿 Learn more about MindCare</h3>
<p class="settings-description">
Visit the MindCare webpage to learn more about the
application, its features, privacy information, and
important usage guidance.
</p>
</div>
        """,
        unsafe_allow_html=True
    )

    st.link_button(
        "ℹ️ Open About MindCare",
        "https://jyot55hub.github.io/mindcare-website/",
        use_container_width=True
    )

    # =====================================================
    # ACCOUNT
    # =====================================================

    st.divider()

    st.subheader(
        "Account"
    )

    st.markdown(
        """
<p style="opacity: 0.75;">
Manage your MindCare account and password.
</p>
        """,
        unsafe_allow_html=True
    )

    # =====================================================
    # CHANGE PASSWORD
    # =====================================================

    st.subheader(
        "🔐 Change Password"
    )

    st.markdown(
        """
<div class="settings-card">
<h3>🔑 Update your password</h3>
<p class="settings-description">
Change your MindCare account password securely.
You will need to enter your current password first.
</p>
</div>
        """,
        unsafe_allow_html=True
    )

    current_password = st.text_input(
        "Current Password",
        type="password",
        key="change_current_password"
    )

    new_password = st.text_input(
        "New Password",
        type="password",
        key="change_new_password"
    )

    confirm_password = st.text_input(
        "Confirm New Password",
        type="password",
        key="change_confirm_password"
    )

    if st.button(
        "🔐 Change Password",
        use_container_width=True,
        key="change_password_button"
    ):

        if not current_password:

            st.warning(
                "Please enter your current password."
            )

        elif not new_password:

            st.warning(
                "Please enter a new password."
            )

        elif not confirm_password:

            st.warning(
                "Please confirm your new password."
            )

        elif new_password != confirm_password:

            st.error(
                "New password and confirmation password do not match."
            )

        else:

            logged_in_user = st.session_state.get(
                "user"
            )

            current_user_id = st.session_state.get(
                "user_id"
            )

            # -------------------------------------------------
            # FALLBACK TO USER OBJECT IF NECESSARY
            # -------------------------------------------------

            if not current_user_id and logged_in_user:

                current_user_id = logged_in_user.get(
                    "id"
                )

            if not current_user_id:

                st.error(
                    "Your session could not be verified. "
                    "Please log in again."
                )

            else:

                result = change_user_password(
                    user_id=current_user_id,
                    current_password=current_password,
                    new_password=new_password
                )

                if result.get("success"):

                    st.success(
                        "✅ Password changed successfully."
                    )

                else:

                    st.error(
                        result.get(
                            "message",
                            "Unable to change your password."
                        )
                    )

    # =====================================================
    # DELETE ACCOUNT
    # =====================================================

    st.divider()

    st.markdown(
        """
<p style="opacity: 0.75;">
Permanently delete your MindCare account and all associated data.
</p>
        """,
        unsafe_allow_html=True
    )

    # -----------------------------------------------------
    # DELETE ACCOUNT BUTTON
    # -----------------------------------------------------

    if st.button(
        "🗑️ Delete My Account",
        key="settings_delete_account_button",
        use_container_width=True
    ):

        current_version = st.session_state.get(
            "delete_confirmation_version",
            0
        )

        st.session_state[
            "delete_confirmation_version"
        ] = current_version + 1

        st.session_state[
            "show_delete_confirmation"
        ] = True

        st.rerun()

    # -----------------------------------------------------
    # DELETE ACCOUNT CONFIRMATION
    # -----------------------------------------------------

    if st.session_state.get(
        "show_delete_confirmation",
        False
    ):

        st.warning(
            "This will permanently delete your account and "
            "all associated data. This action cannot be undone."
        )

        confirmation_version = st.session_state.get(
            "delete_confirmation_version",
            0
        )

        confirm_delete = st.checkbox(
            "I understand that my account and all associated "
            "data will be permanently deleted.",
            key=f"confirm_account_deletion_{confirmation_version}"
        )

        col1, col2 = st.columns(2)

        # -------------------------------------------------
        # CANCEL
        # -------------------------------------------------

        with col1:

            if st.button(
                "❌ Cancel",
                key="cancel_delete_account",
                use_container_width=True
            ):

                st.session_state[
                    "show_delete_confirmation"
                ] = False

                st.rerun()

        # -------------------------------------------------
        # PERMANENT DELETE
        # -------------------------------------------------

        with col2:

            if st.button(
                "🗑️ Permanently Delete",
                key="permanently_delete_account",
                use_container_width=True,
                disabled=not confirm_delete
            ):

                delete_user_id = st.session_state.get(
                    "user_id"
                )

                result = delete_user_account(
                    delete_user_id
                )

                if result.get("success"):

                    # -------------------------------------
                    # CLEAR USER SESSION
                    # -------------------------------------

                    st.session_state.pop(
                        "user",
                        None
                    )

                    st.session_state.pop(
                        "user_id",
                        None
                    )

                    st.session_state[
                        "logged_in"
                    ] = False

                    st.session_state[
                        "page"
                    ] = "login"

                    st.session_state[
                        "show_delete_confirmation"
                    ] = False

                    st.success(
                        "Your account has been permanently deleted."
                    )

                    st.rerun()

                else:

                    st.error(
                        result.get(
                            "message",
                            "Unable to delete your account."
                        )
                    )

    # =====================================================
    # BACK TO DASHBOARD
    # =====================================================

    st.divider()

    if st.button(
        "← Back to Dashboard",
        use_container_width=True
    ):

        st.session_state[
            "page"
        ] = "dashboard"

        st.rerun()