import streamlit as st

from app.core.assistant import assistant_response
from app.backend.chat import (
    create_conversation,
    get_user_conversations,
    get_chat_history,
    update_conversation_title,
    delete_conversation,
)


# ============================================================
# GET LOGGED-IN USER ID
# ============================================================

def get_logged_in_user_id():
    """Get the logged-in user's ID from the Streamlit session."""

    user_id = (
        st.session_state.get("user_id")
        or st.session_state.get("id")
    )

    if user_id is not None:
        return user_id

    user = st.session_state.get("user")

    if isinstance(user, dict):
        return (
            user.get("user_id")
            or user.get("id")
            or user.get("userId")
        )

    return None


# ============================================================
# CHAT INPUT THEME STYLING
# ============================================================

def apply_chat_input_theme():
    """
    Apply theme-specific styling to the Streamlit chatbot
    input and its fixed bottom container.
    """

    theme = st.session_state.get("theme", "Dark")

    # ========================================================
    # WHITE THEME
    # ========================================================

    if theme == "White":

        st.markdown(
            """
            <style>

            /* =================================================
               STREAMLIT FIXED BOTTOM CHAT AREA
            ================================================= */

            [data-testid="stBottom"] {
                background-color: #ffffff !important;
                background: #ffffff !important;
            }

            [data-testid="stBottom"] > div {
                background-color: #ffffff !important;
                background: #ffffff !important;
            }

            [data-testid="stBottom"] > div > div {
                background-color: #ffffff !important;
                background: #ffffff !important;
            }

            [data-testid="stBottom"]::before {
                background-color: #ffffff !important;
            }


            /* =================================================
               CHAT INPUT OUTER CONTAINER
            ================================================= */

            [data-testid="stChatInput"] {
                background-color: #ffffff !important;
                background: #ffffff !important;

                border: 1px solid rgba(0, 0, 0, 0.16) !important;

                border-radius: 12px !important;

                box-shadow: none !important;
            }

            [data-testid="stChatInput"] > div {
                background-color: #ffffff !important;
                background: #ffffff !important;

                border: none !important;

                box-shadow: none !important;
            }

            [data-testid="stChatInput"] form {
                background-color: #ffffff !important;
                background: #ffffff !important;

                border: none !important;

                box-shadow: none !important;
            }


            /* =================================================
               CHAT TEXT AREA
            ================================================= */

            [data-testid="stChatInput"] textarea {
                background-color: #ffffff !important;
                background: #ffffff !important;

                color: #1f2937 !important;

                caret-color: #1f2937 !important;

                border: none !important;

                box-shadow: none !important;
            }

            [data-testid="stChatInput"] textarea::placeholder {
                color: #64748b !important;

                opacity: 1 !important;
            }

            [data-testid="stChatInput"] textarea:focus {
                background-color: #ffffff !important;

                color: #1f2937 !important;

                outline: none !important;
            }


            /* =================================================
               SEND BUTTON
            ================================================= */

            [data-testid="stChatInput"] button {
                background-color: #f5f7f6 !important;

                color: #1f2937 !important;

                border: 1px solid rgba(0, 0, 0, 0.10) !important;

                box-shadow: none !important;
            }

            [data-testid="stChatInput"] button:hover {
                background-color: #eef6f0 !important;

                color: #315943 !important;
            }

            </style>
            """,
            unsafe_allow_html=True
        )

        return


    # ========================================================
    # DARK THEME
    # ========================================================

    if theme == "Dark":

        st.markdown(
            """
            <style>

            /* =================================================
               STREAMLIT FIXED BOTTOM CHAT AREA
            ================================================= */

            [data-testid="stBottom"] {
                background-color: #0e1117 !important;
                background: #0e1117 !important;
            }

            [data-testid="stBottom"] > div {
                background-color: #0e1117 !important;
                background: #0e1117 !important;
            }

            [data-testid="stBottom"] > div > div {
                background-color: #0e1117 !important;
                background: #0e1117 !important;
            }


            /* =================================================
               CHAT INPUT
            ================================================= */

            [data-testid="stChatInput"] {
                background-color: #1f2028 !important;
                background: #1f2028 !important;

                border: 1px solid rgba(255, 255, 255, 0.12) !important;

                border-radius: 12px !important;

                box-shadow: none !important;
            }

            [data-testid="stChatInput"] > div {
                background-color: #1f2028 !important;
                background: #1f2028 !important;

                border: none !important;
            }

            [data-testid="stChatInput"] form {
                background-color: #1f2028 !important;
                background: #1f2028 !important;

                border: none !important;
            }

            [data-testid="stChatInput"] textarea {
                background-color: #262630 !important;
                background: #262630 !important;

                color: #ffffff !important;

                caret-color: #ffffff !important;

                border: none !important;
            }

            [data-testid="stChatInput"] textarea::placeholder {
                color: #9ca3af !important;

                opacity: 1 !important;
            }

            [data-testid="stChatInput"] button {
                background-color: #30313d !important;

                color: #ffffff !important;
            }

            [data-testid="stChatInput"] button:hover {
                background-color: #315943 !important;

                color: #ffffff !important;
            }

            </style>
            """,
            unsafe_allow_html=True
        )

        return


    # ========================================================
    # DEVICE THEME
    # ========================================================

    if theme == "Device":

        st.markdown(
            """
            <style>

            [data-testid="stChatInput"] {
                border-radius: 12px !important;
            }


            /* =================================================
               DEVICE LIGHT MODE
            ================================================= */

            @media (prefers-color-scheme: light) {

                [data-testid="stBottom"] {
                    background-color: #ffffff !important;
                    background: #ffffff !important;
                }

                [data-testid="stBottom"] > div {
                    background-color: #ffffff !important;
                    background: #ffffff !important;
                }

                [data-testid="stBottom"] > div > div {
                    background-color: #ffffff !important;
                    background: #ffffff !important;
                }

                [data-testid="stChatInput"] {
                    background-color: #ffffff !important;
                    background: #ffffff !important;

                    border: 1px solid rgba(0, 0, 0, 0.16) !important;
                }

                [data-testid="stChatInput"] > div {
                    background-color: #ffffff !important;
                    background: #ffffff !important;
                }

                [data-testid="stChatInput"] form {
                    background-color: #ffffff !important;
                    background: #ffffff !important;
                }

                [data-testid="stChatInput"] textarea {
                    background-color: #ffffff !important;
                    background: #ffffff !important;

                    color: #1f2937 !important;

                    caret-color: #1f2937 !important;
                }

                [data-testid="stChatInput"] textarea::placeholder {
                    color: #64748b !important;
                }

                [data-testid="stChatInput"] button {
                    background-color: #f5f7f6 !important;

                    color: #1f2937 !important;
                }

                [data-testid="stChatInput"] button:hover {
                    background-color: #eef6f0 !important;

                    color: #315943 !important;
                }
            }


            /* =================================================
               DEVICE DARK MODE
            ================================================= */

            @media (prefers-color-scheme: dark) {

                [data-testid="stBottom"] {
                    background-color: #0e1117 !important;
                    background: #0e1117 !important;
                }

                [data-testid="stBottom"] > div {
                    background-color: #0e1117 !important;
                    background: #0e1117 !important;
                }

                [data-testid="stBottom"] > div > div {
                    background-color: #0e1117 !important;
                    background: #0e1117 !important;
                }

                [data-testid="stChatInput"] {
                    background-color: #1f2028 !important;
                    background: #1f2028 !important;

                    border: 1px solid rgba(255, 255, 255, 0.12) !important;
                }

                [data-testid="stChatInput"] > div {
                    background-color: #1f2028 !important;
                    background: #1f2028 !important;
                }

                [data-testid="stChatInput"] form {
                    background-color: #1f2028 !important;
                    background: #1f2028 !important;
                }

                [data-testid="stChatInput"] textarea {
                    background-color: #262630 !important;
                    background: #262630 !important;

                    color: #ffffff !important;

                    caret-color: #ffffff !important;
                }

                [data-testid="stChatInput"] textarea::placeholder {
                    color: #9ca3af !important;
                }

                [data-testid="stChatInput"] button {
                    background-color: #30313d !important;

                    color: #ffffff !important;
                }

                [data-testid="stChatInput"] button:hover {
                    background-color: #315943 !important;

                    color: #ffffff !important;
                }
            }

            </style>
            """,
            unsafe_allow_html=True
        )


# ============================================================
# LOAD CONVERSATIONS
# ============================================================

def load_user_conversations(user_id):

    result = get_user_conversations(user_id)

    if result.get("success"):
        return result.get("conversations", [])

    return []


# ============================================================
# LOAD CONVERSATION MESSAGES
# ============================================================

def load_conversation_messages(
    user_id,
    conversation_id
):

    result = get_chat_history(
        user_id,
        conversation_id=conversation_id
    )

    messages = []

    if result.get("success"):

        for record in result.get("history", []):

            messages.append(
                {
                    "role": "user",
                    "content": record.get(
                        "user_message",
                        ""
                    )
                }
            )

            messages.append(
                {
                    "role": "assistant",
                    "content": record.get(
                        "ai_response",
                        ""
                    )
                }
            )

    return messages


# ============================================================
# START NEW CONVERSATION
# ============================================================

def start_new_conversation(user_id):

    result = create_conversation(
        user_id,
        "New Chat"
    )

    if result.get("success"):

        conversation_id = result["conversation_id"]

        st.session_state[
            "active_conversation_id"
        ] = conversation_id

        st.session_state[
            "chat_messages"
        ] = []

        st.session_state[
            "user_conversations"
        ] = load_user_conversations(user_id)

        st.rerun()

    else:

        st.error(
            result.get(
                "message",
                "Unable to create a new chat."
            )
        )


# ============================================================
# SHOW CHATBOT
# ============================================================

def show_chatbot():

    user_id = get_logged_in_user_id()

    if user_id is None:

        st.error(
            "User session not found. Please log in again."
        )

        return

    current_user_id = str(user_id)

    # ========================================================
    # RESET CHAT STATE WHEN USER CHANGES
    # ========================================================

    if (
        st.session_state.get("chat_user_id")
        != current_user_id
    ):

        st.session_state[
            "chat_user_id"
        ] = current_user_id

        st.session_state[
            "active_conversation_id"
        ] = None

        st.session_state[
            "chat_messages"
        ] = []

        st.session_state[
            "user_conversations"
        ] = load_user_conversations(
            user_id
        )

    # ========================================================
    # SIDEBAR CHAT LIST
    # ========================================================

    with st.sidebar:

        st.markdown(
            "## 💬 MindCare Chats"
        )

        # ----------------------------------------------------
        # NEW CHAT
        # ----------------------------------------------------

        if st.button(
            "＋ New Chat",
            use_container_width=True
        ):

            start_new_conversation(
                user_id
            )

        st.divider()

        conversations = (
            st.session_state.get(
                "user_conversations",
                []
            )
        )

        if not conversations:

            st.caption(
                "No conversations yet."
            )

        for conversation in conversations:

            conversation_id = conversation["id"]

            title = conversation.get(
                "title",
                "New Chat"
            )

            chat_column, delete_column = st.columns(
                [5, 1]
            )

            # ------------------------------------------------
            # OPEN CHAT
            # ------------------------------------------------

            with chat_column:

                if st.button(
                    f"💬 {title}",
                    key=f"conversation_{conversation_id}",
                    use_container_width=True
                ):

                    st.session_state[
                        "active_conversation_id"
                    ] = conversation_id

                    st.session_state[
                        "chat_messages"
                    ] = load_conversation_messages(
                        user_id,
                        conversation_id
                    )

                    st.rerun()

            # ------------------------------------------------
            # DELETE CHAT
            # ------------------------------------------------

            with delete_column:

                if st.button(
                    "🗑️",
                    key=f"delete_{conversation_id}",
                    help="Delete this conversation"
                ):

                    result = delete_conversation(
                        user_id,
                        conversation_id
                    )

                    if result.get("success"):

                        if (
                            st.session_state.get(
                                "active_conversation_id"
                            )
                            == conversation_id
                        ):

                            st.session_state[
                                "active_conversation_id"
                            ] = None

                            st.session_state[
                                "chat_messages"
                            ] = []

                        st.session_state[
                            "user_conversations"
                        ] = load_user_conversations(
                            user_id
                        )

                        st.rerun()

                    else:

                        st.error(
                            result.get(
                                "message",
                                "Unable to delete conversation."
                            )
                        )

    # ========================================================
    # MAIN CHAT AREA
    # ========================================================

    st.title(
        "💬 MindCare Chat"
    )

    st.write(
        "Talk to your AI mental health assistant. "
        "You can share your feelings, concerns, or questions "
        "about well-being."
    )

    # ========================================================
    # AI DISCLAIMER
    # ========================================================

    st.info(
        "🤖 MindCare can make mistakes. "
        "AI responses may not always be accurate or appropriate. "
        "MindCare is a supportive wellness assistant and does not "
        "replace professional mental-health care, medical diagnosis, "
        "or emergency services."
    )

    active_conversation_id = (
        st.session_state.get(
            "active_conversation_id"
        )
    )

    # ========================================================
    # AUTOMATICALLY SELECT FIRST CONVERSATION
    # ========================================================

    if active_conversation_id is None:

        conversations = (
            st.session_state.get(
                "user_conversations",
                []
            )
        )

        if conversations:

            active_conversation_id = (
                conversations[0]["id"]
            )

            st.session_state[
                "active_conversation_id"
            ] = active_conversation_id

            st.session_state[
                "chat_messages"
            ] = load_conversation_messages(
                user_id,
                active_conversation_id
            )

    # ========================================================
    # DISPLAY CHAT MESSAGES
    # ========================================================

    for message in st.session_state.get(
        "chat_messages",
        []
    ):

        with st.chat_message(
            message["role"]
        ):

            st.markdown(
                message["content"]
            )

    # ========================================================
    # THEME-AWARE CHAT INPUT
    # ========================================================

    apply_chat_input_theme()

    # ========================================================
    # CHAT INPUT
    # ========================================================

    user_message = st.chat_input(
        "How are you feeling today?"
    )

    # ========================================================
    # PROCESS USER MESSAGE
    # ========================================================

    if user_message:

        # ----------------------------------------------------
        # CREATE CONVERSATION IF NONE EXISTS
        # ----------------------------------------------------

        if active_conversation_id is None:

            result = create_conversation(
                user_id,
                "New Chat"
            )

            if not result.get("success"):

                st.error(
                    "Unable to create a conversation."
                )

                return

            active_conversation_id = (
                result["conversation_id"]
            )

            st.session_state[
                "active_conversation_id"
            ] = active_conversation_id

            st.session_state[
                "user_conversations"
            ] = load_user_conversations(
                user_id
            )

        # ----------------------------------------------------
        # ADD USER MESSAGE
        # ----------------------------------------------------

        st.session_state[
            "chat_messages"
        ].append(
            {
                "role": "user",
                "content": user_message
            }
        )

        # ----------------------------------------------------
        # GENERATE AI RESPONSE
        # ----------------------------------------------------

        with st.spinner(
            "MindCare is thinking..."
        ):

            try:

                response = assistant_response(
                    user_message,
                    user_id=user_id,
                    conversation_id=(
                        active_conversation_id
                    )
                )

            except Exception as error:

                error_message = str(error)

                if (
                    "503" in error_message
                    or "UNAVAILABLE" in error_message
                ):

                    response = (
                        "I'm having trouble connecting "
                        "right now. 🌿 Please try sending "
                        "your message again in a moment."
                    )

                else:

                    response = (
                        "Sorry, something went wrong while "
                        "processing your message. Please try again."
                    )

        # ----------------------------------------------------
        # ADD AI RESPONSE
        # ----------------------------------------------------

        st.session_state[
            "chat_messages"
        ].append(
            {
                "role": "assistant",
                "content": response
            }
        )

        # ----------------------------------------------------
        # AUTOMATICALLY TITLE NEW CHAT
        # ----------------------------------------------------

        current_conversation = next(
            (
                conversation
                for conversation
                in st.session_state[
                    "user_conversations"
                ]
                if conversation["id"]
                == active_conversation_id
            ),
            None
        )

        if (
            current_conversation
            and current_conversation.get(
                "title"
            ) == "New Chat"
        ):

            conversation_title = (
                user_message.strip()[:40]
            )

            if len(
                user_message.strip()
            ) > 40:

                conversation_title += "..."

            update_conversation_title(
                user_id,
                active_conversation_id,
                conversation_title
            )

        # ----------------------------------------------------
        # REFRESH CONVERSATION LIST
        # ----------------------------------------------------

        st.session_state[
            "user_conversations"
        ] = load_user_conversations(
            user_id
        )

        st.rerun()

    # ========================================================
    # BACK TO DASHBOARD
    # ========================================================

    st.divider()

    if st.button(
        "← Back to Dashboard",
        use_container_width=True
    ):

        st.session_state[
            "page"
        ] = "dashboard"

        st.rerun()