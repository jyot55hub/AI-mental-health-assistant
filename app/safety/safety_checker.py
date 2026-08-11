import re


def check_safety(message: str) -> dict:
    """
    Check a user message for potential mental-health crisis language.

    Returns:
        {
            "safe": bool,
            "level": str
        }

    This is a conservative keyword/phrase-based safety layer.
    It is not a clinical risk assessment.
    """

    # Normalize the message so small formatting differences
    # do not prevent detection.
    message_lower = message.lower().strip()

    message_normalized = re.sub(r"[\-_]+", " ", message_lower)
    message_normalized = re.sub(r"\s+", " ", message_normalized)

    crisis_phrases = [
        # Suicide / self-harm
        "kill myself",
        "kill me",
        "suicide",
        "suicidal",
        "want to die",
        "wanna die",
        "don't want to live",
        "dont want to live",
        "do not want to live",
        "don't want to be alive",
        "dont want to be alive",
        "do not want to be alive",
        "end my life",
        "ending my life",
        "end it all",
        "take my life",
        "hurt myself",
        "harm myself",
        "self harm",
        "self-harm",
        "cut myself",
        "cutting myself",
        "wish i were dead",
        "wish i was dead",
        "better off dead",
        "life isn't worth living",
        "life is not worth living",
        "can't go on",
        "cant go on",
        "cannot go on",
    ]

    for phrase in crisis_phrases:
        if phrase in message_normalized:
            return {
                "safe": False,
                "level": "crisis"
            }

    return {
        "safe": True,
        "level": "normal"
    }