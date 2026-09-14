
"""
Recommendation engine for the AI-Powered Mental Health Assistant.

Generates personalized wellness recommendations based on:
- Overall wellness category
- Sleep duration
- Stress level from the questionnaire
- Meditation duration

Stress scale used by the project:
    1 = Very High Stress
    2 = High Stress
    3 = Moderate Stress
    4 = Low Stress
    5 = Very Low St  ress

Meditation target:
    13 minutes per day.
    Meditation beyond 13 minutes does not provide additional
    wellness-score points.
"""


def get_category_recommendations(category):
    """
    Return recommendations based on the overall wellness category.
    """

    if category == "Good":
        return [
            "Keep maintaining your healthy daily habits.",
            "Continue getting adequate sleep and taking regular breaks.",
            "Continue using activities that support your mental wellbeing."
        ]

    elif category == "Moderate":
        return [
            "Try to maintain a consistent sleep schedule.",
            "Take regular breaks during study or work.",
            "Consider spending a few minutes each day on relaxation or meditation.",
            "Pay attention to changes in your stress and wellbeing."
        ]

    elif category == "Needs Attention":
        return [
            "Give extra attention to your mental wellbeing today.",
            "Try to maintain a regular sleep routine.",
            "Consider relaxation, breathing exercises, or guided meditation.",
            "Talk to someone you trust if you feel overwhelmed.",
            "If difficulties persist or significantly affect daily life, consider seeking support from a qualified mental-health professional."
        ]

    else:
        return [
            "There is not enough information to provide a personalized recommendation yet."
        ]


def get_sleep_recommendations(sleep_hours):
    """
    Return recommendations based on sleep duration.

    Args:
        sleep_hours: Sleep duration in hours. Can be int, float,
                     numeric string, or None.
    """

    if sleep_hours is None:
        return [
            "Track your sleep duration so that your sleep pattern can be considered in your wellness recommendations."
        ]

    try:
        sleep_hours = float(sleep_hours)
    except (TypeError, ValueError):
        return [
            "Track your sleep duration using a valid number of hours."
        ]

    if sleep_hours < 6:
        return [
            "Try to get more sleep tonight. Consistently getting too little sleep can affect your energy, concentration, and wellbeing."
        ]

    elif sleep_hours <= 10:
        return [
            "Your sleep duration is within a generally healthy range. Try to maintain a consistent sleep schedule."
        ]

    else:
        return [
            "You slept for more than 10 hours. If this happens frequently, pay attention to your sleep pattern and how rested you feel."
        ]


def get_stress_recommendations(stress_level):
    """
    Return recommendations based on the project's questionnaire
    stress scale.

    Project questionnaire scale:
        1 = Very High Stress
        2 = High Stress
        3 = Moderate Stress
        4 = Low Stress
        5 = Very Low Stress

    IMPORTANT:
        Lower values indicate higher stress.
    """

    if stress_level is None:
        return [
            "Complete the stress-related questionnaire so that stress-based recommendations can be personalized."
        ]

    try:
        stress_level = int(stress_level)
    except (TypeError, ValueError):
        return [
            "Use a valid stress level from 1 to 5."
        ]

    if stress_level < 1 or stress_level > 5:
        return [
            "Use a stress level between 1 and 5."
        ]

    # 1 = Very High Stress, 2 = High Stress
    if stress_level <= 2:
        return [
            "Your responses indicate a higher level of stress. Consider taking a short break and trying a relaxation or breathing exercise.",
            "If possible, identify the main sources of stress and break difficult tasks into smaller steps.",
            "Consider talking to someone you trust if stress is becoming difficult to manage."
        ]

    # 3 = Moderate Stress
    elif stress_level == 3:
        return [
            "Your responses indicate a moderate level of stress. Make time for regular breaks and relaxation.",
            "Try to maintain a healthy balance between study, work, sleep, and personal time."
        ]

    # 4 = Low Stress, 5 = Very Low Stress
    else:
        return [
            "Your responses indicate a relatively low level of stress. Continue the habits and activities that help you maintain your wellbeing.",
            "Keep making time for rest, relaxation, and activities you enjoy."
        ]


def get_meditation_recommendations(meditation_minutes):
    """
    Return recommendations based on daily meditation duration.

    The project's wellness rule uses 13 minutes as the daily target.
    Meditation beyond 13 minutes does not provide additional
    meditation wellness points.
    """

    if meditation_minutes is None:
        return [
            "Try guided meditation or breathing exercises as part of your daily wellbeing routine."
        ]

    try:
        meditation_minutes = float(meditation_minutes)
    except (TypeError, ValueError):
        return [
            "Track your meditation duration using a valid number of minutes."
        ]

    if meditation_minutes < 0:
        return [
            "Meditation duration cannot be negative."
        ]

    if meditation_minutes == 0:
        return [
            "Try starting with a short guided meditation or breathing exercise today."
        ]

    elif meditation_minutes < 13:
        remaining = 13 - meditation_minutes

        # Display whole numbers without unnecessary decimal places.
        if remaining.is_integer():
            remaining_display = int(remaining)
        else:
            remaining_display = round(remaining, 1)

        return [
            f"You completed {int(meditation_minutes) if meditation_minutes.is_integer() else round(meditation_minutes, 1)} minutes of meditation. Try about {remaining_display} more minutes to reach the daily 13-minute wellness target."
        ]

    else:
        return [
            "You completed the daily 13-minute meditation target. Keep maintaining this healthy habit."
        ]


def generate_recommendations(
    category,
    wellness_score=None,
    sleep_hours=None,
    stress_level=None,
    meditation_minutes=None
):
    """
    Generate combined personalized wellness recommendations.

    Args:
        category: Overall wellness category.
        wellness_score: Overall wellness score.
        sleep_hours: Daily sleep duration.
        stress_level: Questionnaire stress level (1-5).
        meditation_minutes: Daily meditation duration.

    Returns:
        dict containing:
            category
            wellness_score
            recommendations
            disclaimer
    """

    recommendations = []

    # Overall wellness category
    recommendations.extend(
        get_category_recommendations(category)
    )

    # Sleep
    recommendations.extend(
        get_sleep_recommendations(sleep_hours)
    )

    # Stress
    recommendations.extend(
        get_stress_recommendations(stress_level)
    )

    # Meditation
    recommendations.extend(
        get_meditation_recommendations(meditation_minutes)
    )

    # Remove duplicate recommendations while preserving order.
    unique_recommendations = []
    seen = set()

    for recommendation in recommendations:
        if recommendation not in seen:
            unique_recommendations.append(recommendation)
            seen.add(recommendation)

    return {
        "category": category,
        "wellness_score": wellness_score,
        "recommendations": unique_recommendations,
        "disclaimer": (
            "These recommendations are general wellness suggestions "
            "and are not a medical diagnosis or a substitute for "
            "professional mental-health care."
        )
    }

