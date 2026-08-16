import unittest
from unittest.mock import MagicMock

from constants.constants import (
    CATEGORY,
    EFFORT,
    INTEREST,
    ITEMS,
    NAME,
)
from repository.categories import CategoriesRepo


class TestActivitiesRepo(unittest.TestCase):

    def setUp(self):
        self.table = MagicMock()
        self.repo = CategoriesRepo(self.table)

    def test_get_category_ids(self):
        self.table.query.return_value = {
            ITEMS: [
                {CATEGORY: "movies"},
                {CATEGORY: "games"},
                {CATEGORY: "movies"},
            ]
        }

        categories = self.repo.get_category_ids("steve")

        self.assertEqual(categories, ["games", "movies"])

        _, kwargs = self.table.query.call_args

        self.assertEqual(
            kwargs["ProjectionExpression"],
            CATEGORY,
        )

    def test_get_category_activities(self):
        self.table.query.return_value = {
            ITEMS: [
                {
                    "activity_id": "2",
                    NAME: "Zulu",
                    CATEGORY: "movies",
                    INTEREST: 3,
                    EFFORT: 1,
                },
                {
                    "activity_id": "1",
                    NAME: "Alpha",
                    CATEGORY: "movies",
                    INTEREST: 1,
                    EFFORT: 3,
                },
            ]
        }

        activities = self.repo.get_category_activities(
            "steve",
            "movies",
        )

        self.assertEqual(
            [a.name for a in activities],
            ["Alpha", "Zulu"],
        )

        self.table.query.assert_called_once()


if __name__ == "__main__":
    unittest.main()
