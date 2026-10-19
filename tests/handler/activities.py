import unittest
from http import HTTPStatus
from unittest.mock import MagicMock, patch


from constants.constants import ACTIVITIES, EFFORT, INTEREST, NAME
from handlers.activity import (
    add_activities,
    add_activity,
    edit_activity,
    get_activity,
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

    def test_add_activity_invalid_category_id(self):
        body = {
            INTEREST: Tier.HIGH.value,
            EFFORT: Tier.LOW.value,
        }

        response, status = add_activity(
            repository=self.repo,
            user_id="steve",
            category_id="physical/activity",
            name="Running",
            body=body,
        )

        self.assertEqual(status, HTTPStatus.BAD_REQUEST)
        self.assertEqual(
            response,
            {"msg": "category name cannot contain '/'"},
        )

        self.repo.add_activity.assert_not_called()

    @patch("handlers.activity.uuid.uuid4", side_effect=["abc123", "def456"])
    def test_add_activities(self, _):
        body = {
            ACTIVITIES: [
                {
                    NAME: "Dune",
                    INTEREST: Tier.HIGH.value,
                    EFFORT: Tier.LOW.value,
                },
                {
                    NAME: "Running",
                    INTEREST: Tier.MEDIUM.value,
                    EFFORT: Tier.HIGH.value,
                },
            ],
        }

        response, status = add_activities(
            repository=self.repo,
            user_id="steve",
            category_id="movies",
            body=body,
        )

        self.assertEqual(status, HTTPStatus.CREATED)
        self.assertEqual(
            response["msg"],
            "successfully added 2 activities to movies",
        )

        self.repo.add_activities.assert_called_once()
        self.repo.add_activity.assert_not_called()

        _, kwargs = self.repo.add_activities.call_args
        self.assertEqual(kwargs["user_id"], "steve")

        activities = kwargs["activities"]
        self.assertEqual(len(activities), 2)

        self.assertEqual(
            activities[0],
            Activity(
                activity_id="abc123",
                name="Dune",
                category="movies",
                interest=Tier.HIGH,
                effort=Tier.LOW,
            ),
        )
        self.assertEqual(
            activities[1],
            Activity(
                activity_id="def456",
                name="Running",
                category="movies",
                interest=Tier.MEDIUM,
                effort=Tier.HIGH,
            ),
        )

        self.assertEqual(
            response,
            {"msg": "successfully added 2 activities to movies"},
        )
        self.assertNotIn(ACTIVITIES, response)

    def test_add_activities_invalid_category_id(self):
        response, status = add_activities(
            repository=self.repo,
            user_id="steve",
            category_id="physical/activity",
            body={
                ACTIVITIES: [
                    {
                        NAME: "Running",
                        INTEREST: Tier.HIGH.value,
                        EFFORT: Tier.LOW.value,
                    },
                ],
            },
        )

        self.assertEqual(status, HTTPStatus.BAD_REQUEST)
        self.assertEqual(
            response,
            {"msg": "category name cannot contain '/'"},
        )
        self.repo.add_activities.assert_not_called()

    def test_add_activities_missing_list(self):
        response, status = add_activities(
            repository=self.repo,
            user_id="steve",
            category_id="movies",
            body={},
        )

        self.assertEqual(status, HTTPStatus.BAD_REQUEST)
        self.assertEqual(
            response,
            {"msg": "activities must be a non-empty list"},
        )
        self.repo.add_activities.assert_not_called()

    def test_add_activities_empty_list(self):
        response, status = add_activities(
            repository=self.repo,
            user_id="steve",
            category_id="movies",
            body={ACTIVITIES: []},
        )

        self.assertEqual(status, HTTPStatus.BAD_REQUEST)
        self.assertEqual(
            response,
            {"msg": "activities must be a non-empty list"},
        )
        self.repo.add_activities.assert_not_called()

    def test_add_activities_rejects_invalid_activity_without_writing(self):
        body = {
            ACTIVITIES: [
                {
                    NAME: "Dune",
                    INTEREST: Tier.HIGH.value,
                    EFFORT: Tier.LOW.value,
                },
                {
                    NAME: "Running",
                    INTEREST: 999,
                    EFFORT: Tier.LOW.value,
                },
            ],
        }

        response, status = add_activities(
            repository=self.repo,
            user_id="steve",
            category_id="movies",
            body=body,
        )

        self.assertEqual(status, HTTPStatus.BAD_REQUEST)
        self.assertEqual(
            response,
            {"msg": "activities[1] has invalid or missing interest/effort"},
        )
        self.repo.add_activities.assert_not_called()

    def test_add_activities_rejects_missing_name(self):
        response, status = add_activities(
            repository=self.repo,
            user_id="steve",
            category_id="movies",
            body={
                ACTIVITIES: [
                    {
                        INTEREST: Tier.HIGH.value,
                        EFFORT: Tier.LOW.value,
                    },
                ],
            },
        )

        self.assertEqual(status, HTTPStatus.BAD_REQUEST)
        self.assertEqual(
            response,
            {"msg": "activities[0].name must be a non-empty string"},
        )
        self.repo.add_activities.assert_not_called()

    def test_add_activities_rejects_non_object_item(self):
        response, status = add_activities(
            repository=self.repo,
            user_id="steve",
            category_id="movies",
            body={ACTIVITIES: ["Dune"]},
        )

        self.assertEqual(status, HTTPStatus.BAD_REQUEST)
        self.assertEqual(
            response,
            {"msg": "activities[0] must be an object"},
        )
        self.repo.add_activities.assert_not_called()

    def test_add_activities_rejects_boolean_tier(self):
        response, status = add_activities(
            repository=self.repo,
            user_id="steve",
            category_id="movies",
            body={
                ACTIVITIES: [
                    {
                        NAME: "Dune",
                        INTEREST: True,
                        EFFORT: Tier.LOW.value,
                    },
                ],
            },
        )

        self.assertEqual(status, HTTPStatus.BAD_REQUEST)
        self.assertEqual(
            response,
            {"msg": "activities[0] has invalid or missing interest/effort"},
        )
        self.repo.add_activities.assert_not_called()

    def test_add_activities_trims_names(self):
        response, status = add_activities(
            repository=self.repo,
            user_id="steve",
            category_id="movies",
            body={
                ACTIVITIES: [
                    {
                        NAME: "  Dune  ",
                        INTEREST: Tier.HIGH.value,
                        EFFORT: Tier.LOW.value,
                    },
                ],
            },
        )

        self.assertEqual(status, HTTPStatus.CREATED)
        activities = self.repo.add_activities.call_args.kwargs["activities"]
        self.assertEqual(activities[0].name, "Dune")

    def test_get_activity(self):
        activity = Activity(
            activity_id="abc",
            name="Dune",
            category="movies",
            interest=Tier.HIGH,
            effort=Tier.LOW,
        )
        self.repo.get_activity.return_value = activity

        response, status = get_activity(
            repository=self.repo,
            user_id="steve",
            category_id="movies",
            activity_id="abc",
        )

        self.assertEqual(status, HTTPStatus.OK)
        self.assertEqual(activity.to_dict(), response)

        self.repo.get_activity.assert_called_once_with(
            user_id="steve",
            category_id="movies",
            activity_id="abc",
        )

    def test_get_activity_not_found(self):
        self.repo.get_activity.return_value = None

        response, status = get_activity(
            repository=self.repo,
            user_id="steve",
            category_id="movies",
            activity_id="abc",
        )

        self.assertEqual(status, HTTPStatus.NOT_FOUND)
        self.assertEqual({"msg": "activity abc not found"}, response)

        self.repo.get_activity.assert_called_once_with(
            user_id="steve",
            category_id="movies",
            activity_id="abc",
        )

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
        self.assertEqual(response, {"msg": "successfully updated abc"})

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
        self.assertEqual(response, {"msg": "invalid interest or effort"})
        self.repo.update_activity.assert_not_called()

    def test_edit_activity_missing_interest(self):
        response, status = edit_activity(
            repository=self.repo,
            user_id="steve",
            category_id="movies",
            activity_id="abc",
            body={EFFORT: Tier.LOW.value},
        )

        self.assertEqual(status, HTTPStatus.BAD_REQUEST)
        self.repo.update_activity.assert_not_called()

    def test_edit_activity_missing_effort(self):
        response, status = edit_activity(
            repository=self.repo,
            user_id="steve",
            category_id="movies",
            activity_id="abc",
            body={INTEREST: Tier.HIGH.value},
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
        self.assertEqual(response, {"msg": "activity abc not found"})

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
