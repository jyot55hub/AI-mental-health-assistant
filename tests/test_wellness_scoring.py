import unittest

from app.analytics.wellness_scoring import (
    calculate_sleep_score,
    calculate_questionnaire_score,
    calculate_wellness_score,
    get_wellness_category
)


class TestWellnessScoring(unittest.TestCase):

    # ========================================================
    # SLEEP SCORE TESTS
    # ========================================================

    def test_healthy_sleep(self):
        self.assertEqual(
            calculate_sleep_score(8),
            25
        )

    def test_low_sleep(self):
        self.assertEqual(
            calculate_sleep_score(5.5),
            10
        )

    def test_very_low_sleep(self):
        self.assertEqual(
            calculate_sleep_score(4),
            5
        )

    def test_high_sleep(self):
        self.assertEqual(
            calculate_sleep_score(11),
            15
        )

    # ========================================================
    # QUESTIONNAIRE TESTS
    # ========================================================

    def test_questionnaire_score(self):

        score = calculate_questionnaire_score(
            mood=5,
            stress_level=1,
            energy_level=5
        )

        self.assertEqual(
            score,
            60
        )

    def test_questionnaire_missing_data(self):

        score = calculate_questionnaire_score()

        self.assertIsNone(score)

    # ========================================================
    # WELLNESS CATEGORY TESTS
    # ========================================================

    def test_good_category(self):
        self.assertEqual(
            get_wellness_category(80),
            "Good"
        )

    def test_moderate_category(self):
        self.assertEqual(
            get_wellness_category(60),
            "Moderate"
        )

    def test_needs_attention_category(self):
        self.assertEqual(
            get_wellness_category(40),
            "Needs Attention"
        )

    # ========================================================
    # COMPLETE WELLNESS SCORE TEST
    # ========================================================

    def test_complete_wellness_score(self):

        result = calculate_wellness_score(
            sleep_hours=8,
            mood=5,
            stress_level=1,
            energy_level=5
        )

        self.assertEqual(
            result["wellness_score"],
            100
        )

        self.assertEqual(
            result["category"],
            "Good"
        )

    # ========================================================
    # NO DATA TEST
    # ========================================================

    def test_no_data(self):

        result = calculate_wellness_score()

        self.assertIsNone(
            result["wellness_score"]
        )

        self.assertEqual(
            result["category"],
            "Insufficient Data"
        )


if __name__ == "__main__":
    unittest.main()