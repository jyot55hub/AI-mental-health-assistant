def check_safety(message: str) -> dict:
    """
    Basic safety gate for the mental-health assistant.
    """

    message_lower = message.lower()

    crisis_keywords = [
        "kill myself",
        "suicide",
        "suicidal",
        "want to die",
        "end my life",
        "hurt myself",
        "self harm",
        "self-harm",
    ]

    for keyword in crisis_keywords:
        if keyword in message_lower:
            return {
                "safe": False,
                "level": "crisis"
            }

    return {
        "safe": True,
        "level": "normal"
    }