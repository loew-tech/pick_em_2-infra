import unittest
from unittest.mock import patch

from models.models import Activity, Tier, Pick
from services.pick import pick


class TestPick(unittest.TestCase):

    def setUp(self):
        self.activities = [
            Activity(
                activity_id="1",
                name="Watch movie",
                category="movies",
                interest=Tier.MEDIUM,
                effort=Tier.LOW,
            ),
            Activity(
                activity_id="2",
                name="Learn guitar",
                category="hobbies",
                interest=Tier.HIGH,
                effort=Tier.MEDIUM,
            ),
            Activity(
                activity_id="3",
                name="Clean garage",
                category="chores",
                interest=Tier.LOW,
                effort=Tier.HIGH,
            ),
        ]

    def test_pick_returns_matching_activity(self):
        result = pick(
            self.activities,
            interest=Tier.MEDIUM,
            effort=Tier.MEDIUM,
        )

        self.assertIsInstance(result, Pick)
        self.assertIn(
            result.name,
            {
                "Watch movie",
                "Learn guitar",
            },
        )

    def test_pick_filters_low_interest(self):
        result = pick(
            self.activities,
            interest=Tier.MEDIUM,
            effort=Tier.HIGH,
        )

        self.assertIsNotNone(result)
        self.assertNotEqual(result.name, "Clean garage")

    def test_pick_filters_high_effort(self):
        result = pick(
            self.activities,
            interest=Tier.LOW,
            effort=Tier.MEDIUM,
        )

        self.assertIsNotNone(result)
        self.assertNotEqual(result.name, "Clean garage")

    def test_pick_returns_none_when_no_match(self):
        result = pick(
            self.activities,
            interest=Tier.HIGH,
            effort=Tier.LOW,
        )

        self.assertIsNone(result)

    def test_high_interest_gets_weighted_preference(self):
        activities = [
            Activity(
                activity_id="1",
                name="Medium interest",
                category="test",
                interest=Tier.MEDIUM,
                effort=Tier.MEDIUM,
            ),
            Activity(
                activity_id="2",
                name="High interest",
                category="test",
                interest=Tier.HIGH,
                effort=Tier.MEDIUM,
            ),
        ]

        results = [
            pick(
                activities,
                interest=Tier.LOW,
                effort=Tier.HIGH,
            ).name
            for _ in range(1000)
        ]

        self.assertGreater(
            results.count("High interest"),
            results.count("Medium interest"),
        )

    def test_weighted_selection_can_select_second_item(self):
        activities = [
            Activity(
                activity_id="1",
                name="First",
                category="test",
                interest=Tier.LOW,
                effort=Tier.LOW,
            ),
            Activity(
                activity_id="2",
                name="Second",
                category="test",
                interest=Tier.HIGH,
                effort=Tier.LOW,
            ),
        ]

        # Force random selection into second range
        with patch("services.pick.randint", return_value=1):
            result = pick(
                activities,
                interest=Tier.LOW,
                effort=Tier.HIGH,
            )

        self.assertIsNotNone(result)
        self.assertEqual(result.name, "Second")


if __name__ == "__main__":
    unittest.main()
