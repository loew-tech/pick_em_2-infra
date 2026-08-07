import unittest
from http import HTTPStatus
from unittest.mock import MagicMock

from handlers.pick import get_pick
from models.models import Activity, Tier


class TestPickHandler(unittest.TestCase):

    def test_pick(self):
        repo = MagicMock()

        repo.get_activities.return_value = [
            Activity(name="foo", category="bar", activity_id="123", effort=Tier.MEDIUM, interest=Tier.HIGH)
        ]

        body, status = get_pick(
            repo,
            "stevebot",
            {
                "categories": ["movies"],
                "interest": Tier.MEDIUM.value,
                "effort": Tier.HIGH.value,
            },
        )

        self.assertEqual(status, HTTPStatus.OK)
        repo.get_activities.assert_called_once()


if __name__ == "__main__":
    unittest.main()
