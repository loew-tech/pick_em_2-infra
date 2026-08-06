import unittest
from http import HTTPStatus
from unittest.mock import MagicMock, patch

from constants.constants import EFFORT, INTEREST
from handlers.activity import (
    add_activity,
    edit_activity,
    remove_activity,
)
from models.models import Activity, Tier


class TestActivityHandler(unittest.TestCase):

    def setUp(self):
        self.repo = MagicMock()

    @patch("handlers.activity.uuid.uuid4", return_value="abc123")
    def test_add_activity(self, _):
        body = {
            INTEREST: Tier.HIGH.value,
            EFFORT: Tier.LOW.value,
        }

        response, status = add_activity(
            repository=self.repo,
            user_id="steve",
            category_id="movies",
            name="Dune",
            body=body,
        )

        self.assertEqual(status, HTTPStatus.ACCEPTED)
        self.assertEqual(
            response,
            {"msg": "successfully added Dune to movies"},
        )

        self.repo.add_activity.assert_called_once()

        _, kwargs = self.repo.add_activity.call_args

        self.assertEqual(kwargs["user_id"], "steve")

        activity = kwargs["activity"]
        self.assertIsInstance(activity, Activity)
        self.assertEqual(activity.activity_id, "abc123")
        self.assertEqual(activity.name, "Dune")
        self.assertEqual(activity.category, "movies")
        self.assertEqual(activity.interest, Tier.HIGH)
        self.assertEqual(activity.effort, Tier.LOW)

    def test_edit_activity(self):
        self.repo.update_activity.return_value = True

        body = {
            INTEREST: Tier.MEDIUM.value,
            EFFORT: Tier.HIGH.value,
        }

        response, status = edit_activity(
            repository=self.repo,
            user_id="steve",
            category_id="movies",
            activity_id="abc",
            body=body,
        )

        self.assertEqual(status, HTTPStatus.OK)
        self.assertEqual(
            response,
            {"msg": "successfully updated abc"},
        )

        self.repo.update_activity.assert_called_once_with(
            user_id="steve",
            category_id="movies",
            activity_id="abc",
            interest=Tier.MEDIUM,
            effort=Tier.HIGH,
        )

    def test_edit_activity_invalid_tier(self):
        response, status = edit_activity(
            repository=self.repo,
            user_id="steve",
            category_id="movies",
            activity_id="abc",
            body={
                INTEREST: 999,
                EFFORT: Tier.LOW.value,
            },
        )

        self.assertEqual(status, HTTPStatus.BAD_REQUEST)
        self.assertEqual(
            response,
            {"msg": "invalid interest or effort"},
        )

        self.repo.update_activity.assert_not_called()

    def test_edit_activity_missing_interest(self):
        response, status = edit_activity(
            repository=self.repo,
            user_id="steve",
            category_id="movies",
            activity_id="abc",
            body={
                EFFORT: Tier.LOW.value,
            },
        )

        self.assertEqual(status, HTTPStatus.BAD_REQUEST)
        self.repo.update_activity.assert_not_called()

    def test_edit_activity_missing_effort(self):
        response, status = edit_activity(
            repository=self.repo,
            user_id="steve",
            category_id="movies",
            activity_id="abc",
            body={
                INTEREST: Tier.HIGH.value,
            },
        )

        self.assertEqual(status, HTTPStatus.BAD_REQUEST)
        self.repo.update_activity.assert_not_called()

    def test_edit_activity_not_found(self):
        self.repo.update_activity.return_value = False

        response, status = edit_activity(
            repository=self.repo,
            user_id="steve",
            category_id="movies",
            activity_id="abc",
            body={
                INTEREST: Tier.LOW.value,
                EFFORT: Tier.LOW.value,
            },
        )

        self.assertEqual(status, HTTPStatus.NOT_FOUND)
        self.assertEqual(
            response,
            {"msg": "activity abc not found"},
        )

    def test_remove_activity(self):
        response, status = remove_activity(
            repository=self.repo,
            user_id="steve",
            category_id="movies",
            activity_id="abc",
        )

        self.assertEqual(status, HTTPStatus.OK)
        self.assertEqual(
            response,
            {"msg": "successfully activity abc from movies"},
        )

        self.repo.delete_activity.assert_called_once_with(
            "steve",
            "movies",
            "abc",
        )

if __name__ == "__main__":
    unittest.main()
