import html
import streamlit as st

from app.backend.auth import (
    get_user_profile,
    update_user_name,
    update_username,
    update_user_bio,
    update_user_avatar
)

from app.backend.journal import (
    create_journal_entry,
    get_journal_entries,
    get_journal_entry,
    update_journal_entry,
    delete_journal_entry
)


# =========================================================
# PROFILE PAGE
# =========================================================

def show_profile():

    st.title("👤 My Profile")

    st.caption(
        "Manage your personal profile information."
    )

    # -----------------------------------------------------
    # GET LOGGED-IN USER
    # -----------------------------------------------------

    user_id = st.session_state.get("user_id")

    if not user_id:
        st.error(
            "Please log in to access your profile."
        )
        return

    # -----------------------------------------------------
    # LOAD PROFILE
    # -----------------------------------------------------

    result = get_user_profile(user_id)

    if not result.get("success"):
        st.error(
            result.get(
                "message",
                "Unable to load profile."
            )
        )
        return

    profile = result["profile"]

    # -----------------------------------------------------
    # PREPARE PROFILE DATA
    # -----------------------------------------------------

    avatar = html.escape(
        str(profile.get("avatar") or "🌿")
    )

    display_name = html.escape(
        str(profile.get("name") or "User")
    )

    email = html.escape(
        str(profile.get("email") or "")
    )

    username = profile.get("username")

    if username:
        username_display = "@" + html.escape(
            str(username)
        )
    else:
        username_display = "Username not set"

    # =====================================================
    # CURRENT THEME
    # =====================================================

    selected_theme = st.session_state.get(
        "theme",
        "Device"
    )

    # -----------------------------------------------------
    # THEME COLORS
    # -----------------------------------------------------

    if selected_theme == "Dark":

        profile_bg_1 = "#17251f"
        profile_bg_2 = "#10262a"
        profile_border = "#315443"

        profile_name_color = "#d8f3df"
        secondary_text = "#a8b3c2"
        normal_text = "#d7dee8"

        section_border = "#303746"

        journal_bg = "#151922"
        journal_border = "#303746"
        journal_title = "#e5edf7"
        journal_text = "#c4cedb"
        journal_date = "#8f9bab"

        empty_bg = "#151922"
        empty_border = "#3a4352"
        empty_text = "#9ca8b7"

        input_bg = "#20242e"
        input_text = "#f1f5f9"

        button_bg = "#20242e"
        button_text = "#f1f5f9"
        button_border = "#414b5b"

    else:

        profile_bg_1 = "#f0fdf4"
        profile_bg_2 = "#ecfeff"
        profile_border = "#d1fae5"

        profile_name_color = "#315943"
        secondary_text = "#64748b"
        normal_text = "#475569"

        section_border = "#e2e8f0"

        journal_bg = "#f8fafc"
        journal_border = "#dbeafe"
        journal_title = "#334155"
        journal_text = "#475569"
        journal_date = "#64748b"

        empty_bg = "#f8fafc"
        empty_border = "#cbd5e1"
        empty_text = "#64748b"

        input_bg = "#ffffff"
        input_text = "#1e293b"

        button_bg = "#ffffff"
        button_text = "#1e293b"
        button_border = "#cbd5e1"

    # =====================================================
    # PROFILE + JOURNAL CSS
    # =====================================================

    st.markdown(
        f"""
<style>

/* =====================================================
   PROFILE HEADER
   ===================================================== */

.profile-card {{
    padding: 28px;
    border-radius: 18px;
    background: linear-gradient(
        135deg,
        {profile_bg_1},
        {profile_bg_2}
    );
    border: 1px solid {profile_border};
    margin-bottom: 25px;
    text-align: center;
}}

.profile-avatar {{
    font-size: 72px;
    line-height: 1.2;
    margin-bottom: 8px;
}}

.profile-name {{
    font-size: 28px;
    font-weight: 700;
    color: {profile_name_color};
    margin-bottom: 5px;
}}

.profile-email {{
    color: {secondary_text};
    font-size: 15px;
    margin-bottom: 4px;
}}

.profile-username {{
    color: {normal_text};
    font-size: 15px;
}}


/* =====================================================
   JOURNAL CARDS
   ===================================================== */

.journal-card {{
    padding: 20px;
    border-radius: 16px;
    border: 1px solid {journal_border};
    background: {journal_bg};
    margin-top: 18px;
    margin-bottom: 14px;
}}

.journal-title {{
    font-size: 20px;
    font-weight: 700;
    color: {journal_title};
    margin-bottom: 8px;
}}

.journal-date {{
    font-size: 13px;
    color: {journal_date};
    margin-bottom: 12px;
}}

.journal-content {{
    font-size: 15px;
    color: {journal_text};
    line-height: 1.6;
    white-space: pre-wrap;
}}


/* =====================================================
   EMPTY JOURNAL
   ===================================================== */

.journal-empty {{
    padding: 32px;
    border-radius: 16px;
    border: 1px dashed {empty_border};
    background: {empty_bg};
    text-align: center;
    color: {empty_text};
    margin-top: 14px;
    margin-bottom: 10px;
}}


/* =====================================================
   JOURNAL SECTION
   ===================================================== */

div[data-testid="stExpander"] {{
    border: 1px solid {section_border};
    border-radius: 16px;
    overflow: hidden;
}}

div[data-testid="stExpander"] summary {{
    color: {journal_title};
}}


/* =====================================================
   INPUTS
   ===================================================== */

div[data-testid="stTextInput"] input,
div[data-testid="stTextArea"] textarea {{
    background-color: {input_bg};
    color: {input_text};
    border-color: {section_border};
}}

div[data-testid="stTextInput"] input::placeholder,
div[data-testid="stTextArea"] textarea::placeholder {{
    color: {secondary_text};
}}


/* =====================================================
   BUTTONS
   ===================================================== */

div[data-testid="stButton"] > button {{
    background-color: {button_bg};
    color: {button_text};
    border: 1px solid {button_border};
}}

div[data-testid="stButton"] > button:hover {{
    border-color: {profile_border};
}}


/* =====================================================
   MOBILE
   ===================================================== */

@media (max-width: 768px) {{

    .profile-card {{
        padding: 22px;
    }}

    .profile-avatar {{
        font-size: 60px;
    }}

    .profile-name {{
        font-size: 24px;
    }}

    .journal-card {{
        padding: 16px;
    }}

}}

</style>
        """,
        unsafe_allow_html=True
    )

    # =====================================================
    # PROFILE HEADER
    # =====================================================

    profile_header = (
        '<div class="profile-card">'
        f'<div class="profile-avatar">{avatar}</div>'
        f'<div class="profile-name">{display_name}</div>'
        f'<div class="profile-email">{email}</div>'
        f'<div class="profile-username">{username_display}</div>'
        '</div>'
    )

    st.markdown(
        profile_header,
        unsafe_allow_html=True
    )

    # =====================================================
    # PERSONAL INFORMATION
    # =====================================================

    st.subheader(
        "✏️ Personal Information"
    )

    with st.form(
        "profile_personal_form"
    ):

        name = st.text_input(
            "Full Name",
            value=profile.get("name") or "",
            placeholder="Enter your name"
        )

        username_input = st.text_input(
            "Username",
            value=profile.get("username") or "",
            placeholder="Choose a username",
            help=(
                "3–30 characters. Letters, numbers, "
                "underscore (_) and dot (.) are allowed."
            )
        )

        bio = st.text_area(
            "Bio",
            value=profile.get("bio") or "",
            placeholder=(
                "Tell us a little about yourself..."
            ),
            max_chars=300,
            height=120
        )

        save_personal = st.form_submit_button(
            "💾 Save Changes",
            use_container_width=True
        )

        if save_personal:

            # ---------------------------------------------
            # UPDATE NAME
            # ---------------------------------------------

            if name.strip() != (
                profile.get("name") or ""
            ).strip():

                name_result = update_user_name(
                    user_id=user_id,
                    name=name
                )

                if not name_result.get("success"):

                    st.error(
                        name_result.get(
                            "message",
                            "Unable to update name."
                        )
                    )

                    return

            # ---------------------------------------------
            # UPDATE USERNAME
            # ---------------------------------------------

            current_username = (
                profile.get("username") or ""
            )

            if (
                username_input.strip().lower()
                != current_username.lower()
            ):

                username_result = update_username(
                    user_id=user_id,
                    username=username_input
                )

                if not username_result.get("success"):

                    st.error(
                        username_result.get(
                            "message",
                            "Unable to update username."
                        )
                    )

                    return

            # ---------------------------------------------
            # UPDATE BIO
            # ---------------------------------------------

            if bio != (
                profile.get("bio") or ""
            ):

                bio_result = update_user_bio(
                    user_id=user_id,
                    bio=bio
                )

                if not bio_result.get("success"):

                    st.error(
                        bio_result.get(
                            "message",
                            "Unable to update bio."
                        )
                    )

                    return

            st.success(
                "Profile updated successfully! ✅"
            )

            st.rerun()

    # =====================================================
    # PROFILE AVATAR
    # =====================================================

    st.divider()

    st.subheader(
        "🎨 Profile Avatar"
    )

    avatars = [
        "🌿",
        "😊",
        "🌸",
        "🌻",
        "🌈",
        "🦋",
        "🐼",
        "🐨",
        "🦊",
        "🐱",
        "🐶",
        "🌙",
        "⭐",
        "💜",
        "💙"
    ]

    current_avatar = (
        profile.get("avatar") or "🌿"
    )

    if current_avatar not in avatars:

        avatars.insert(
            0,
            current_avatar
        )

    selected_avatar = st.selectbox(
        "Choose your avatar",
        avatars,
        index=avatars.index(
            current_avatar
        )
    )

    # -----------------------------------------------------
    # AVATAR PREVIEW
    # -----------------------------------------------------

    avatar_preview = (
        '<div style="'
        'text-align:center;'
        'font-size:70px;'
        'padding:15px;'
        '">'
        f'{html.escape(str(selected_avatar))}'
        '</div>'
    )

    st.markdown(
        avatar_preview,
        unsafe_allow_html=True
    )

    # -----------------------------------------------------
    # SAVE AVATAR
    # -----------------------------------------------------

    if st.button(
        "💾 Save Avatar",
        use_container_width=True
    ):

        if selected_avatar != current_avatar:

            avatar_result = update_user_avatar(
                user_id=user_id,
                avatar=selected_avatar
            )

            if avatar_result.get("success"):

                st.success(
                    "Avatar updated successfully! ✅"
                )

                st.rerun()

            else:

                st.error(
                    avatar_result.get(
                        "message",
                        "Unable to update avatar."
                    )
                )

        else:

            st.info(
                "Your selected avatar is already saved."
            )

    # =====================================================
    # JOURNAL
    # =====================================================

    st.divider()

    st.subheader(
        "📔 My Journal"
    )

    st.caption(
        "Write down your thoughts, experiences, "
        "or anything you would like to remember."
    )

    # =====================================================
    # CREATE NEW JOURNAL ENTRY
    # =====================================================

    with st.expander(
        "✍️ Write a New Journal Entry",
        expanded=False
    ):

        with st.form(
            "create_journal_form",
            clear_on_submit=True
        ):

            new_title = st.text_input(
                "Title",
                placeholder="Give your entry a title..."
            )

            new_content = st.text_area(
                "Your Thoughts",
                placeholder="Write your thoughts here...",
                height=180
            )

            create_entry = st.form_submit_button(
                "💾 Save Journal Entry",
                use_container_width=True
            )

            if create_entry:

                journal_result = create_journal_entry(
                    user_id=user_id,
                    title=new_title,
                    content=new_content
                )

                if journal_result.get("success"):

                    st.success(
                        "Journal entry saved successfully! 📔"
                    )

                    st.rerun()

                else:

                    st.error(
                        journal_result.get(
                            "message",
                            "Unable to save journal entry."
                        )
                    )

    # =====================================================
    # LOAD JOURNAL ENTRIES
    # =====================================================

    journal_result = get_journal_entries(
        user_id
    )

    if not journal_result.get("success"):

        st.error(
            journal_result.get(
                "message",
                "Unable to load journal entries."
            )
        )

    else:

        journal_entries = journal_result.get(
            "entries",
            []
        )

        # =================================================
        # YOUR ENTRIES COLLAPSIBLE SECTION
        # =================================================

        with st.expander(
            f"📝 Your Entries ({len(journal_entries)})",
            expanded=False
        ):

            # ---------------------------------------------
            # NO ENTRIES
            # ---------------------------------------------

            if not journal_entries:

                empty_journal = (
                    '<div class="journal-empty">'
                    '<div style="font-size:42px;">📖</div>'
                    '<div style="'
                    'font-size:18px;'
                    'font-weight:600;'
                    'margin-top:8px;'
                    '">'
                    'No journal entries yet'
                    '</div>'
                    '<div style="'
                    'margin-top:6px;'
                    '">'
                    'Your saved thoughts will appear here.'
                    '</div>'
                    '</div>'
                )

                st.markdown(
                    empty_journal,
                    unsafe_allow_html=True
                )

            # ---------------------------------------------
            # ENTRIES EXIST
            # ---------------------------------------------

            else:

                st.caption(
                    "Select a journal title to view its contents."
                )

                # -----------------------------------------
                # CURRENTLY SELECTED ENTRY
                # -----------------------------------------

                selected_journal_id = st.session_state.get(
                    "selected_journal_id"
                )

                # -----------------------------------------
                # TITLE BOXES IN PARALLEL
                # -----------------------------------------

                for index in range(
                    0,
                    len(journal_entries),
                    2
                ):

                    row_entries = journal_entries[
                        index:index + 2
                    ]

                    columns = st.columns(2)

                    for column, entry in zip(
                        columns,
                        row_entries
                    ):

                        journal_id = entry.get(
                            "id"
                        )

                        title = (
                            entry.get("title")
                            or "Untitled Entry"
                        )

                        with column:

                            if st.button(
                                f"📔 {title}",
                                key=(
                                    f"journal_title_"
                                    f"{journal_id}"
                                ),
                                use_container_width=True
                            ):

                                st.session_state[
                                    "selected_journal_id"
                                ] = journal_id

                                st.session_state.pop(
                                    "editing_journal_id",
                                    None
                                )

                                st.session_state.pop(
                                    "delete_journal_id",
                                    None
                                )

                                st.rerun()

                # -----------------------------------------
                # SELECTED ENTRY
                # -----------------------------------------

                if selected_journal_id:

                    selected_entry_result = (
                        get_journal_entry(
                            user_id=user_id,
                            journal_id=selected_journal_id
                        )
                    )

                    if selected_entry_result.get(
                        "success"
                    ):

                        selected_entry = (
                            selected_entry_result["entry"]
                        )

                        selected_title = html.escape(
                            str(
                                selected_entry.get(
                                    "title"
                                )
                                or "Untitled Entry"
                            )
                        )

                        selected_content = html.escape(
                            str(
                                selected_entry.get(
                                    "content"
                                )
                                or ""
                            )
                        )

                        selected_date = (
                            selected_entry.get(
                                "updated_at"
                            )
                            or selected_entry.get(
                                "created_at"
                            )
                            or "Date unavailable"
                        )

                        # ---------------------------------
                        # ENTRY CONTENT CARD
                        # ---------------------------------

                        selected_card = (
                            '<div class="journal-card">'
                            f'<div class="journal-title">'
                            f'📔 {selected_title}'
                            f'</div>'
                            f'<div class="journal-date">'
                            f'Last updated: '
                            f'{html.escape(str(selected_date))}'
                            f'</div>'
                            f'<div class="journal-content">'
                            f'{selected_content}'
                            f'</div>'
                            '</div>'
                        )

                        st.markdown(
                            selected_card,
                            unsafe_allow_html=True
                        )

                        # ---------------------------------
                        # EDIT / DELETE
                        # ---------------------------------

                        edit_col, delete_col = st.columns(2)

                        with edit_col:

                            edit_button = st.button(
                                "✏️ Edit",
                                key=(
                                    f"edit_selected_"
                                    f"{selected_journal_id}"
                                ),
                                use_container_width=True
                            )

                        with delete_col:

                            delete_button = st.button(
                                "🗑️ Delete",
                                key=(
                                    f"delete_selected_"
                                    f"{selected_journal_id}"
                                ),
                                use_container_width=True
                            )

                        # ---------------------------------
                        # EDIT
                        # ---------------------------------

                        if edit_button:

                            st.session_state[
                                "editing_journal_id"
                            ] = selected_journal_id

                            st.session_state[
                                "editing_journal_title"
                            ] = selected_entry.get(
                                "title",
                                ""
                            )

                            st.session_state[
                                "editing_journal_content"
                            ] = selected_entry.get(
                                "content",
                                ""
                            )

                            st.rerun()

                        # ---------------------------------
                        # DELETE
                        # ---------------------------------

                        if delete_button:

                            st.session_state[
                                "delete_journal_id"
                            ] = selected_journal_id

                            st.rerun()

                        # ---------------------------------
                        # DELETE CONFIRMATION
                        # ---------------------------------

                        if st.session_state.get(
                            "delete_journal_id"
                        ) == selected_journal_id:

                            st.warning(
                                "Are you sure you want to delete "
                                "this journal entry?"
                            )

                            confirm_col, cancel_col = st.columns(2)

                            with confirm_col:

                                confirm_delete = st.button(
                                    "Yes, Delete",
                                    key=(
                                        f"confirm_delete_"
                                        f"{selected_journal_id}"
                                    ),
                                    use_container_width=True
                                )

                            with cancel_col:

                                cancel_delete = st.button(
                                    "Cancel",
                                    key=(
                                        f"cancel_delete_"
                                        f"{selected_journal_id}"
                                    ),
                                    use_container_width=True
                                )

                            if confirm_delete:

                                delete_result = (
                                    delete_journal_entry(
                                        user_id=user_id,
                                        journal_id=selected_journal_id
                                    )
                                )

                                if delete_result.get(
                                    "success"
                                ):

                                    st.session_state.pop(
                                        "selected_journal_id",
                                        None
                                    )

                                    st.session_state.pop(
                                        "delete_journal_id",
                                        None
                                    )

                                    st.success(
                                        "Journal entry deleted successfully."
                                    )

                                    st.rerun()

                                else:

                                    st.error(
                                        delete_result.get(
                                            "message",
                                            "Unable to delete "
                                            "journal entry."
                                        )
                                    )

                            if cancel_delete:

                                st.session_state.pop(
                                    "delete_journal_id",
                                    None
                                )

                                st.rerun()

                        # ---------------------------------
                        # EDIT FORM
                        # ---------------------------------

                        if st.session_state.get(
                            "editing_journal_id"
                        ) == selected_journal_id:

                            st.markdown(
                                "#### ✏️ Edit Journal Entry"
                            )

                            edit_title = st.text_input(
                                "Title",
                                value=st.session_state.get(
                                    "editing_journal_title",
                                    ""
                                ),
                                key=(
                                    f"edit_title_"
                                    f"{selected_journal_id}"
                                )
                            )

                            edit_content = st.text_area(
                                "Your Thoughts",
                                value=st.session_state.get(
                                    "editing_journal_content",
                                    ""
                                ),
                                height=180,
                                key=(
                                    f"edit_content_"
                                    f"{selected_journal_id}"
                                )
                            )

                            save_col, cancel_col = st.columns(2)

                            with save_col:

                                save_edit = st.button(
                                    "💾 Save Changes",
                                    key=(
                                        f"save_edit_"
                                        f"{selected_journal_id}"
                                    ),
                                    use_container_width=True
                                )

                            with cancel_col:

                                cancel_edit = st.button(
                                    "Cancel",
                                    key=(
                                        f"cancel_edit_"
                                        f"{selected_journal_id}"
                                    ),
                                    use_container_width=True
                                )

                            if save_edit:

                                update_result = (
                                    update_journal_entry(
                                        user_id=user_id,
                                        journal_id=selected_journal_id,
                                        title=edit_title,
                                        content=edit_content
                                    )
                                )

                                if update_result.get(
                                    "success"
                                ):

                                    st.session_state.pop(
                                        "editing_journal_id",
                                        None
                                    )

                                    st.session_state.pop(
                                        "editing_journal_title",
                                        None
                                    )

                                    st.session_state.pop(
                                        "editing_journal_content",
                                        None
                                    )

                                    st.success(
                                        "Journal entry updated successfully."
                                    )

                                    st.rerun()

                                else:

                                    st.error(
                                        update_result.get(
                                            "message",
                                            "Unable to update "
                                            "journal entry."
                                        )
                                    )

                            if cancel_edit:

                                st.session_state.pop(
                                    "editing_journal_id",
                                    None
                                )

                                st.session_state.pop(
                                    "editing_journal_title",
                                    None
                                )

                                st.session_state.pop(
                                    "editing_journal_content",
                                    None
                                )

                                st.rerun()

                    else:

                        st.warning(
                            selected_entry_result.get(
                                "message",
                                "Unable to load journal entry."
                            )
                        )

    # =====================================================
    # ACCOUNT INFORMATION
    # =====================================================

    st.subheader(
        "🔐 Account Information"
    )

    col1, col2 = st.columns(2)

    with col1:

        st.markdown(
            "**Email**"
        )

        st.write(
            profile.get(
                "email",
                ""
            )
        )

    with col2:

        st.markdown(
            "**Member Since**"
        )

        created_at = profile.get(
            "created_at"
        )

        if created_at:

            st.write(
                str(created_at)[:10]
            )

        else:

            st.write(
                "Not available"
            )

    st.info(
        "Your email address is used for login "
        "and cannot be changed from this page."
    )