import unittest
from dataclasses import FrozenInstanceError

from common.constants.constants import (
    ACTIVITY_ID,
    CATEGORY,
    EFFORT,
    INTEREST,
    NAME,
    ID,
)
from models.models import (
    Activity,
    Category,
    Pick,
    Tier,
)


class TestActivity(unittest.TestCase):

    def test_from_dict(self):
        data = {
            ACTIVITY_ID: "abc123",
            NAME: "Watch Dune",
            CATEGORY: "movies",
            INTEREST: Tier.HIGH.value,
            EFFORT: Tier.LOW.value,
        }

        activity = Activity.from_dict(data)

        self.assertEqual(
            activity,
            Activity(
                activity_id="abc123",
                name="Watch Dune",
                category="movies",
                interest=Tier.HIGH,
                effort=Tier.LOW,
            ),
        )

    def test_to_dict(self):
        activity = Activity(
            activity_id="abc123",
            name="Watch Dune",
            category="movies",
            interest=Tier.HIGH,
            effort=Tier.LOW,
        )

        self.assertEqual(
            activity.to_dict(),
            {
                ACTIVITY_ID: "abc123",
                NAME: "Watch Dune",
                CATEGORY: "movies",
                INTEREST: Tier.HIGH.value,
                EFFORT: Tier.LOW.value,
            },
        )

    def test_from_dict_converts_tiers(self):
        activity = Activity.from_dict(
            {
                ACTIVITY_ID: "abc123",
                NAME: "Watch Dune",
                CATEGORY: "movies",
                INTEREST: 3,
                EFFORT: 1,
            }
        )

        self.assertIsInstance(activity.interest, Tier)
        self.assertIsInstance(activity.effort, Tier)

    def test_activity_is_immutable(self):
        activity = Activity(
            activity_id="abc123",
            name="Dune",
            category="movies",
            interest=Tier.HIGH,
            effort=Tier.LOW,
        )

        with self.assertRaises(FrozenInstanceError):
            setattr(activity, "name", "Something else")


class TestCategory(unittest.TestCase):

    def test_from_dict(self):
        category = Category.from_dict(
            {
                ID: "movies",
            }
        )

        self.assertEqual(
            category,
            Category(id="movies"),
        )

    def test_category_is_immutable(self):
        category = Category(id="movies")

        with self.assertRaises(FrozenInstanceError):
            setattr(category, "id", "Something else")


class TestPick(unittest.TestCase):

    def test_to_dict(self):
        pick = Pick(
            name="Watch Dune",
            category="movies",
        )

        self.assertEqual(
            pick.to_dict(),
            {
                NAME: "Watch Dune",
                CATEGORY: "movies",
            },
        )


if __name__ == "__main__":
    unittest.main()
