from app.rag.retriever import retrieve_context
from app.safety.safety_checker import check_safety
from app.llm.gemini_client import generate_response
from app.backend.chat import save_chat_message


# ============================================================
# RAG CONTEXT
# ============================================================

def get_rag_context(user_query):
    """
    Retrieve relevant information from the vector database.
    """

    results = retrieve_context(user_query)

    context_parts = []

    for result in results:
        source = result.get("source", "Unknown")
        text = result.get("text", "")

        context_parts.append(
            f"Source: {source}\n"
            f"Information:\n{text}"
        )

    return "\n\n---\n\n".join(context_parts)


# ============================================================
# MENTAL HEALTH TOPIC CHECK
# ============================================================

def is_mental_health_related(user_message):
    """
    Check whether the message is related to mental health,
    emotional well-being, or student-related concerns.
    """

    message = user_message.lower()

    mental_health_keywords = [
        "mental health",
        "mental wellbeing",
        "mental well-being",
        "wellbeing",
        "well-being",
        "stress",
        "stressed",
        "anxiety",
        "anxious",
        "panic",
        "worried",
        "worry",
        "depression",
        "depressed",
        "sad",
        "sadness",
        "lonely",
        "loneliness",
        "alone",
        "emotion",
        "emotional",
        "feel",
        "feeling",
        "feelings",
        "overwhelmed",
        "upset",
        "sleep",
        "insomnia",
        "tired",
        "fatigue",
        "burnout",
        "burned out",
        "burnt out",
        "motivation",
        "unmotivated",
        "procrastination",
        "procrastinate",
        "academic stress",
        "exam stress",
        "exam anxiety",
        "study stress",
        "college stress",
        "pressure",
        "concentration",
        "focus",
        "can't focus",
        "cannot focus",
        "self esteem",
        "self-esteem",
        "confidence",
        "relationship",
        "coping",
        "therapy",
        "counseling",
        "counselling",
        "counsellor",
        "hopeless",
        "helpless",
        "self-care",
        "self care",
        "study",
        "studies",
        "studying",
        "exam",
        "exams",
        "marks",
        "low marks",
        "academic",
        "study plan",
        "manage studies",
        "time management",
        "assignments",
        "homework",
        "results",
        "failure"
    ]

    return any(
        keyword in message
        for keyword in mental_health_keywords
    )


# ============================================================
# GREETING CHECK
# ============================================================

def is_greeting(user_message):
    """
    Check whether the user is simply greeting the assistant.
    """

    message = user_message.lower().strip()

    greetings = [
        "hi",
        "hello",
        "hey",
        "hii",
        "hiii",
        "holla",
        "hollaa",
        "hola",
        "hi hi",
        "hi hi hi",
        "hello hello",
        "hey hey",
        "good morning",
        "good afternoon",
        "good evening"
    ]

    return message in greetings


# ============================================================
# SAVE RESPONSE HELPER
# ============================================================

def save_response(
    user_id,
    user_message,
    response,
    conversation_id=None
):
    """
    Save a response to the selected conversation.
    """

    if user_id is not None:
        save_chat_message(
            user_id=user_id,
            user_message=user_message,
            ai_response=response,
            conversation_id=conversation_id
        )


# ============================================================
# ASSISTANT RESPONSE
# ============================================================

def assistant_response(
    user_message,
    user_id=None,
    conversation_id=None
):
    """
    Generate a concise and supportive MindCare response.
    """

    user_message = user_message.strip()

    # --------------------------------------------------------
    # SAFETY CHECK
    # --------------------------------------------------------

    safety_result = check_safety(user_message)

    if not safety_result["safe"]:
        response = (
            "I'm sorry you're going through this. 💚 "
            "Please reach out to someone you trust and seek immediate "
            "professional or emergency support if you are in danger."
        )

        save_response(
            user_id,
            user_message,
            response,
            conversation_id
        )

        return response

    # --------------------------------------------------------
    # GREETING RESPONSE
    # --------------------------------------------------------

    if is_greeting(user_message):
        response = (
            "Hello! 🌿 I'm MindCare, your mental health assistant. "
            "I'm here to support you with stress, emotions, studies, "
            "sleep, anxiety, and overall well-being. "
            "How are you feeling today?"
        )

        save_response(
            user_id,
            user_message,
            response,
            conversation_id
        )

        return response

    # --------------------------------------------------------
    # REJECT UNRELATED QUESTIONS
    # --------------------------------------------------------

    if not is_mental_health_related(user_message):
        response = (
            "I'm here to help with mental health and well-being topics. 🌿 "
            "You can ask me about stress, anxiety, emotions, sleep, "
            "academic pressure, motivation, or coping strategies."
        )

        save_response(
            user_id,
            user_message,
            response,
            conversation_id
        )

        return response

    # --------------------------------------------------------
    # RETRIEVE RELEVANT INFORMATION
    # --------------------------------------------------------

    rag_context = get_rag_context(user_message)

    # --------------------------------------------------------
    # CONCISE RESPONSE PROMPT
    # --------------------------------------------------------

    prompt = f"""
You are MindCare, a supportive AI mental health assistant.

Your role is to provide brief, practical, and empathetic support
for mental health and student well-being.

RESPONSE RULES:
1. Keep your response short and easy to read.
2. Use a maximum of 80 to 120 words for normal questions.
3. Use 3 to 5 short paragraphs or bullet points.
4. Do not repeat the user's question.
5. Give only the most useful advice.
6. Avoid lengthy explanations.
7. Ask at most one helpful follow-up question.
8. Use simple and friendly language.
9. Do not diagnose the user.
10. Do not claim to be a mental health professional.
11. Recommend professional support only when relevant.
12. Do not answer unrelated general knowledge questions.

Use the retrieved information only when relevant.

Retrieved information:
{rag_context}

User message:
{user_message}

Now provide a concise, warm, and practical response.
"""

    try:
        ai_response = generate_response(prompt)
    except Exception:
        ai_response = None

    if not ai_response:
        ai_response = (
            "I'm here to listen and support you. 💚 "
            "Could you tell me a little more about how you're feeling?"
        )

    # --------------------------------------------------------
    # SAVE RESPONSE IN THE SELECTED CONVERSATION
    # --------------------------------------------------------

    save_response(
        user_id,
        user_message,
        ai_response,
        conversation_id
    )

    return ai_response