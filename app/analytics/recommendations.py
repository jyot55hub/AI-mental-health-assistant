"""
Personalized Wellness Recommendation Engine

This module provides general wellness recommendations based on a
user's wellness indicator and available wellness information.

IMPORTANT:
Recommendations are educational and supportive only.
They are NOT medical diagnosis or professional treatment advice.
"""


# ============================================================
# CATEGORY-BASED RECOMMENDATIONS
# ============================================================

def get_category_recommendations(category):
    """
    Return general recommendations based on wellness category.
    """

    recommendations = []

    if category == "Good":

        recommendations.extend([
            "Maintain your current healthy wellness routine.",
            "Continue following a regular sleep schedule.",
            "Take regular breaks during study or work.",
            "Continue activities that help you relax and recharge."
        ])

    elif category == "Moderate":

        recommendations.extend([
            "Try to maintain a more consistent daily routine.",
            "Take short breaks when you feel stressed or overwhelmed.",
            "Prioritize adequate sleep and rest.",
            "Consider relaxation activities such as breathing exercises or mindfulness."
        ])

    elif category == "Needs Attention":

        recommendations.extend([
            "Consider taking additional time for rest and self-care.",
            "Try breaking large tasks into smaller manageable steps.",
            "Talk with a trusted friend, family member, mentor, or counselor.",
            "If distress is persistent or worsening, consider seeking support from a qualified mental health professional."
        ])

    else:

        recommendations.append(
            "Provide more wellness information to receive personalized suggestions."
        )

    return recommendations


# ============================================================
# SLEEP-BASED RECOMMENDATIONS
# ============================================================

def get_sleep_recommendations(sleep_hours):
    """
    Return recommendations based on sleep duration.
    """

    recommendations = []

    if sleep_hours is None:
        return recommendations

    try:
        sleep_hours = float(sleep_hours)

    except (ValueError, TypeError):
        return recommendations

    if sleep_hours < 6:

        recommendations.append(
            "Try to prioritize adequate sleep and maintain a consistent sleep schedule."
        )

    elif sleep_hours > 10:

        recommendations.append(
            "Very long sleep patterns can sometimes be worth monitoring. Consider maintaining a consistent routine."
        )

    else:

        recommendations.append(
            "Your reported sleep duration is within a generally healthy range for many adults."
        )

    return recommendations


# ============================================================
# STRESS-BASED RECOMMENDATIONS
# ============================================================

def get_stress_recommendations(stress_level):
    """
    Return recommendations based on reported stress level.

    Expected scale: 1 to 5
    Higher number = higher stress.
    """

    recommendations = []

    if stress_level is None:
        return recommendations

    try:
        stress_level = float(stress_level)

    except (ValueError, TypeError):
        return recommendations

    if stress_level >= 4:

        recommendations.extend([
            "Try taking short breaks between demanding tasks.",
            "Consider simple stress-management activities such as breathing exercises or mindfulness.",
            "Break large academic or personal tasks into smaller steps."
        ])

    elif stress_level >= 3:

        recommendations.append(
            "Monitor your stress level and make time for regular rest and relaxation."
        )

    else:

        recommendations.append(
            "Continue using the strategies that help you manage stress."
        )

    return recommendations


# ============================================================
# MEDITATION-BASED RECOMMENDATIONS
# ============================================================

def get_meditation_recommendations(meditation_minutes):
    """
    Return recommendations based on daily meditation duration.

    The project's daily meditation target is 13 minutes.
    Additional wellness points are capped at 13 minutes.
    """

    recommendations = []

    if meditation_minutes is None:

        recommendations.append(
            "Consider trying a short guided breathing or meditation session as part of your daily wellness routine."
        )

        return recommendations

    try:
        meditation_minutes = float(meditation_minutes)

    except (ValueError, TypeError):

        return recommendations

    if meditation_minutes <= 0:

        recommendations.append(
            "Consider starting with a short guided breathing or meditation session."
        )

    elif meditation_minutes < 13:

        remaining_minutes = 13 - meditation_minutes

        recommendations.append(
            f"You completed {meditation_minutes:g} minutes of meditation today. "
            f"You can continue for about {remaining_minutes:g} more minutes to reach the daily 13-minute wellness target."
        )

    else:

        recommendations.append(
            "You completed the daily 13-minute meditation wellness target. Keep following the practices that help you relax and recharge."
        )

    return recommendations


# ============================================================
# MAIN RECOMMENDATION FUNCTION
# ============================================================

def generate_recommendations(
    wellness_result,
    sleep_hours=None,
    stress_level=None,
    meditation_minutes=None
):
    """
    Generate personalized wellness recommendations.

    Parameters
    ----------
    wellness_result : dict
        Dictionary returned by calculate_wellness_score().

    sleep_hours : float
        Number of hours slept.

    stress_level : float
        Stress level on a scale where higher means higher stress.

    meditation_minutes : float
        Number of minutes of meditation completed today.

    Returns
    -------
    dict
        Dictionary containing category, score, recommendations,
        and disclaimer.
    """

    if not wellness_result:

        return {
            "category": "Insufficient Data",
            "recommendations": [
                "Please provide wellness information to receive suggestions."
            ],
            "disclaimer": (
                "These suggestions are for general wellness support "
                "and are not medical advice."
            )
        }

    category = wellness_result.get(
        "category",
        "Insufficient Data"
    )

    recommendations = []

    # Category recommendations
    recommendations.extend(
        get_category_recommendations(category)
    )

    # Sleep recommendations
    recommendations.extend(
        get_sleep_recommendations(sleep_hours)
    )

    # Stress recommendations
    recommendations.extend(
        get_stress_recommendations(stress_level)
    )

    # Meditation recommendations
    recommendations.extend(
        get_meditation_recommendations(
            meditation_minutes
        )
    )

    # Remove duplicates while preserving order
    recommendations = list(
        dict.fromkeys(recommendations)
    )

    return {
        "category": category,

        "wellness_score": wellness_result.get(
            "wellness_score"
        ),

        "recommendations": recommendations,

        "disclaimer": (
            "These recommendations are general wellness suggestions "
            "for educational purposes and are not a medical diagnosis "
            "or professional treatment advice."
        )
    }


# ============================================================
# TESTING
# ============================================================

if __name__ == "__main__":

    from app.analytics.wellness_scoring import (
        calculate_wellness_score
    )

    wellness_result = calculate_wellness_score(
        sleep_hours=7.5,
        mood=4,
        stress_level=3,
        energy_level=4,
        physical_activity=3,
        focus=4,
        social=3,
        self_care=4,
        meditation_minutes=13
    )

    result = generate_recommendations(
        wellness_result,
        sleep_hours=7.5,
        stress_level=3,
        meditation_minutes=13
    )

    print("\nPERSONALIZED WELLNESS RECOMMENDATIONS")
    print("=" * 55)

    print(
        f"Wellness Score: "
        f"{result['wellness_score']}/100"
    )

    print(
        f"Category: "
        f"{result['category']}"
    )

    print("\nRecommendations:")

    for number, recommendation in enumerate(
        result["recommendations"],
        start=1
    ):

        print(
            f"{number}. {recommendation}"
        )

    print("\nDisclaimer:")
    print(result["disclaimer"])