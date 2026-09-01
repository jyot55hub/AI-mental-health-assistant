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
    # QUESTIONNAIRE SCORE TESTS
    # ========================================================

    def test_questionnaire_score(self):

        score = calculate_questionnaire_score(
            mood=5,
            stress_level=5,
            energy_level=5,
            physical_activity=5,
            focus=5,
            social=5,
            self_care=5
        )

        self.assertEqual(
            score,
            60
        )


    def test_questionnaire_missing_data(self):

        score = calculate_questionnaire_score()

        self.assertIsNone(
            score
        )


    def test_questionnaire_low_score(self):

        score = calculate_questionnaire_score(
            mood=1,
            stress_level=1,
            energy_level=1,
            physical_activity=1,
            focus=1,
            social=1,
            self_care=1
        )

        self.assertEqual(
            score,
            0
        )


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


    def test_insufficient_data_category(self):

        self.assertEqual(
            get_wellness_category(None),
            "Insufficient Data"
        )


    # ========================================================
    # COMPLETE WELLNESS SCORE TEST
    # ========================================================

    def test_complete_wellness_score(self):

        result = calculate_wellness_score(

            sleep_hours=8,

            mood=5,

            stress_level=5,

            energy_level=5,

            physical_activity=5,

            focus=5,

            social=5,

            self_care=5
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
    # PARTIAL WELLNESS SCORE TEST
    # ========================================================

    def test_partial_wellness_score(self):

        result = calculate_wellness_score(

            sleep_hours=8,

            mood=3,

            stress_level=3,

            energy_level=3,

            physical_activity=3,

            focus=3,

            social=3,

            self_care=3
        )


        self.assertIsNotNone(
            result["wellness_score"]
        )


        self.assertGreaterEqual(
            result["wellness_score"],
            0
        )


        self.assertLessEqual(
            result["wellness_score"],
            100
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