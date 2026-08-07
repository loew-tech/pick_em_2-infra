import unittest
from http import HTTPStatus
from unittest.mock import MagicMock

from common.constants.constants import ACTIVITIES, CATEGORIES, ID
from handlers.category import (
    get_category_activities,
    get_category_ids,
)
from models.models import Activity, Tier


class TestCategoryHandler(unittest.TestCase):

    def setUp(self):
        self.repo = MagicMock()

    def test_get_category_ids(self):
        self.repo.get_category_ids.return_value = [
            "movies",
            "games",
        ]

        response = get_category_ids(
            self.repo,
            "steve",
        )

        self.assertEqual(
            response,
            {
                CATEGORIES: [
                    "movies",
                    "games",
                ]
            },
        )

        self.repo.get_category_ids.assert_called_once_with(
            "steve",
        )

    def test_get_category_activities(self):
        self.repo.get_category_activities.return_value = [
            Activity(
                activity_id="2",
                name="Zulu",
                category="movies",
                interest=Tier.HIGH,
                effort=Tier.LOW,
            ),
            Activity(
                activity_id="1",
                name="Alpha",
                category="movies",
                interest=Tier.LOW,
                effort=Tier.HIGH,
            ),
        ]

        response, status = get_category_activities(
            self.repo,
            "steve",
            "movies",
        )

        self.assertEqual(status, HTTPStatus.OK)

        self.assertEqual(
            response,
            {
                ID: "movies",
                ACTIVITIES: [
                    {
                        "activity_id": "1",
                        "name": "Alpha",
                        "category": "movies",
                        "interest": Tier.LOW.value,
                        "effort": Tier.HIGH.value,
                    },
                    {
                        "activity_id": "2",
                        "name": "Zulu",
                        "category": "movies",
                        "interest": Tier.HIGH.value,
                        "effort": Tier.LOW.value,
                    },
                ],
            },
        )

        self.repo.get_category_activities.assert_called_once_with(
            "steve",
            "movies",
        )

if __name__ == "__main__":
    unittest.main()
