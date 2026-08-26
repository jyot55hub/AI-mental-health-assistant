from app.rag.retriever import retrieve_context
from app.safety.safety_checker import check_safety
from app.llm.gemini_client import generate_response


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


def assistant_response(user_message):
    safety_result = check_safety(user_message)

    if not safety_result["safe"]:
        return (
            "I'm really sorry you're going through this. "
            "You deserve immediate support. Please reach out to someone you trust "
            "and contact local emergency or crisis services if you are in immediate danger."
        )

    rag_context = get_rag_context(user_message)

    prompt = f"""
You are a supportive AI mental health assistant.

Use the following retrieved information when it is relevant:

{rag_context}

User message:
{user_message}

Respond in a warm, supportive, and helpful manner.
Do not diagnose the user.
Do not claim to be a mental health professional.
Encourage professional help when appropriate.
"""

    return generate_response(prompt)