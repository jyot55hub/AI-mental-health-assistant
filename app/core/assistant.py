from app.rag.retriever import retrieve_context
from app.safety.safety_checker import check_safety
from app.llm.gemini_client import generate_response
from app.backend.chat import save_chat_message


def get_rag_context(user_query):
    """
    Retrieves relevant knowledge from the vector database
    and formats it as context for the AI.
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

    context = "\n\n---\n\n".join(context_parts)

    return context
def is_mental_health_related(user_message):
    """
    Checks whether the user's message is related to
    mental health, emotional well-being, or student well-being.
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
        "confidence",
        "relationship",
        "coping",
        "therapy",
        "counseling",
        "counsellor"
    ]

    return any(keyword in message for keyword in mental_health_keywords)


def assistant_response(user_message, user_id=None):
    safety_result = check_safety(user_message)

    if not safety_result["safe"]:
        return (
            "I'm really sorry you're going through this. "
            "You deserve immediate support. Please reach out to someone you trust "
            "and contact local emergency or crisis services if you are in immediate danger."
        )
    if not is_mental_health_related(user_message):
        return (
            "I'm designed specifically to provide supportive and educational "
            "information about mental health and well-being. "
            "I can't help with general knowledge or unrelated questions. "
            "You can ask me about topics such as stress, anxiety, emotions, "
            "sleep, academic pressure, motivation, or other mental health concerns."
        )

    rag_context = get_rag_context(user_message)

    prompt = f"""
You are a supportive AI mental health assistant.
IMPORTANT:
You are strictly a mental health and well-being assistant.

Do not answer questions about unrelated general knowledge topics such as geography, programming, mathematics, politics, sports, history, or trivia.

If a user asks an unrelated question, politely explain that you can only assist with mental health and well-being topics.

Use the following retrieved information when it is relevant:

{rag_context}

User message:
{user_message}

Respond in a warm, supportive, and helpful manner.
Do not diagnose the user.
Do not claim to be a mental health professional.
Encourage professional help when appropriate.
"""

    ai_response = generate_response(prompt)

    if user_id is not None:
        save_chat_message(
            user_id=user_id,
            user_message=user_message,
            ai_response=ai_response
        )

    return ai_response