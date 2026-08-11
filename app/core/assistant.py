from app.safety.safety_checker import check_safety
from app.llm.gemini_client import generate_response
from app.rag.retriever import retrieve_documents


def assistant_response(message: str) -> str:
    # Step 1: Safety check
    safety_result = check_safety(message)

    if not safety_result["safe"]:
        return (
            "I'm really sorry you're going through this. "
            "You deserve immediate support from a trusted person or "
            "qualified mental-health professional. "
            "If you may be in immediate danger, please contact your "
            "local emergency service or go to the nearest emergency department."
        )

    # Step 2: Retrieve relevant knowledge from our RAG database
    retrieved_documents = retrieve_documents(message, top_k=3)

    context = "\n\n".join(retrieved_documents)

    # Step 3: Give Gemini the retrieved context
    prompt = f"""
You are a supportive mental-health information assistant.

Use the provided knowledge below to help answer the user's question.

IMPORTANT RULES:
- Use the retrieved knowledge as your primary source.
- Do not diagnose the user.
- Do not claim to replace a mental-health professional.
- Be supportive, calm, and clear.
- If the retrieved knowledge does not contain enough information,
  say that you do not have enough information rather than inventing facts.

RETRIEVED KNOWLEDGE:
{context}

USER QUESTION:
{message}

Answer the user's question in a helpful and supportive way.
"""

    # Step 4: Generate the final answer
    return generate_response(prompt)