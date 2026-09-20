
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
# LOAD CONVERSATIONS
# ============================================================

def load_user_conversations(user_id):
    """Load conversations belonging only to the current user."""

    result = get_user_conversations(user_id)

    if result.get("success"):
        return result.get("conversations", [])

    return []


# ============================================================
# LOAD ONE CONVERSATION'S MESSAGES
# ============================================================

def load_conversation_messages(user_id, conversation_id):
    """Load messages from one specific conversation."""

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
                    "content": record.get("user_message", "")
                }
            )

            messages.append(
                {
                    "role": "assistant",
                    "content": record.get("ai_response", "")
                }
            )

    return messages


# ============================================================
# CREATE NEW CONVERSATION
# ============================================================

def start_new_conversation(user_id):
    """Create and select a new conversation."""

    result = create_conversation(user_id, "New Chat")

    if result.get("success"):
        conversation_id = result["conversation_id"]

        st.session_state["active_conversation_id"] = conversation_id
        st.session_state["chat_messages"] = []

        st.session_state["user_conversations"] = (
            load_user_conversations(user_id)
        )

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
    """Display the MindCare AI chatbot."""

    user_id = get_logged_in_user_id()

    if user_id is None:
        st.error("User session not found. Please log in again.")
        return

    current_user_id = str(user_id)

    # --------------------------------------------------------
    # Reset chatbot state when the logged-in user changes
    # --------------------------------------------------------

    if st.session_state.get("chat_user_id") != current_user_id:
        st.session_state["chat_user_id"] = current_user_id
        st.session_state["active_conversation_id"] = None
        st.session_state["chat_messages"] = []
        st.session_state["user_conversations"] = (
            load_user_conversations(user_id)
        )

    # --------------------------------------------------------
    # Sidebar
    # --------------------------------------------------------

    with st.sidebar:
        st.markdown("## 💬 MindCare Chats")

        if st.button(
            "＋ New Chat",
            use_container_width=True
        ):
            start_new_conversation(user_id)

        st.divider()

        conversations = st.session_state.get(
            "user_conversations",
            []
        )

        if not conversations:
            st.caption("No conversations yet.")

        for conversation in conversations:
            conversation_id = conversation["id"]
            title = conversation.get("title", "New Chat")

            # Create two columns: chat title and delete button
            chat_column, delete_column = st.columns([5, 1])

            with chat_column:
                if st.button(
                    f"💬 {title}",
                    key=f"conversation_{conversation_id}",
                    use_container_width=True
                ):
                    st.session_state["active_conversation_id"] = (
                        conversation_id
                    )

                    st.session_state["chat_messages"] = (
                        load_conversation_messages(
                            user_id,
                            conversation_id
                        )
                    )

                    st.rerun()

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
                            ) == conversation_id
                        ):
                            st.session_state[
                                "active_conversation_id"
                            ] = None
                            st.session_state["chat_messages"] = []

                        st.session_state["user_conversations"] = (
                            load_user_conversations(user_id)
                        )

                        st.rerun()
                    else:
                        st.error(
                            result.get(
                                "message",
                                "Unable to delete conversation."
                            )
                        )

    # --------------------------------------------------------
    # Main chat area
    # --------------------------------------------------------

    st.title("💬 MindCare Chat")

    st.write(
        "Talk to your AI mental health assistant. "
        "You can share your feelings, concerns, or questions "
        "about well-being."
    )

    active_conversation_id = st.session_state.get(
        "active_conversation_id"
    )

    # --------------------------------------------------------
    # Automatically select the first conversation
    # --------------------------------------------------------

    if active_conversation_id is None:
        conversations = st.session_state.get(
            "user_conversations",
            []
        )

        if conversations:
            active_conversation_id = conversations[0]["id"]

            st.session_state["active_conversation_id"] = (
                active_conversation_id
            )

            st.session_state["chat_messages"] = (
                load_conversation_messages(
                    user_id,
                    active_conversation_id
                )
            )

    # --------------------------------------------------------
    # Display messages
    # --------------------------------------------------------

    for message in st.session_state.get("chat_messages", []):
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # --------------------------------------------------------
    # Receive a new message
    # --------------------------------------------------------

    user_message = st.chat_input(
        "How are you feeling today?"
    )

    if user_message:

        # Create a conversation automatically if needed
        if active_conversation_id is None:
            result = create_conversation(user_id, "New Chat")

            if not result.get("success"):
                st.error("Unable to create a conversation.")
                return

            active_conversation_id = result["conversation_id"]

            st.session_state["active_conversation_id"] = (
                active_conversation_id
            )

            st.session_state["user_conversations"] = (
                load_user_conversations(user_id)
            )

        # Display the user's message
        st.session_state["chat_messages"].append(
            {
                "role": "user",
                "content": user_message
            }
        )

        # Generate the AI response
        with st.spinner("MindCare is thinking..."):
            try:
                response = assistant_response(
                    user_message,
                    user_id=user_id,
                    conversation_id=active_conversation_id
                )

            except Exception as error:
                error_message = str(error)

                if (
                    "503" in error_message
                    or "UNAVAILABLE" in error_message
                ):
                    response = (
                        "I'm having trouble connecting right now. 🌿 "
                        "Please try sending your message again "
                        "in a moment."
                    )
                else:
                    response = (
                        "Sorry, something went wrong while "
                        "processing your message. Please try again."
                    )

        # Display the AI response
        st.session_state["chat_messages"].append(
            {
                "role": "assistant",
                "content": response
            }
        )

        # Automatically title the conversation only once
        current_conversation = next(
            (
                conversation
                for conversation in st.session_state["user_conversations"]
                if conversation["id"] == active_conversation_id
            ),
            None
        )

        if (
            current_conversation
            and current_conversation.get("title") == "New Chat"
        ):
            conversation_title = user_message.strip()[:40]

            if len(user_message.strip()) > 40:
                conversation_title += "..."

            update_conversation_title(
                user_id,
                active_conversation_id,
                conversation_title
            )

        # Refresh the conversation list
        st.session_state["user_conversations"] = (
            load_user_conversations(user_id)
        )

        st.rerun()

    # --------------------------------------------------------
    # Back to dashboard
    # --------------------------------------------------------

    st.divider()

    if st.button(
        "← Back to Dashboard",
        use_container_width=True
    ):
        st.session_state["page"] = "dashboard"
        st.rerun()
