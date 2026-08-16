import unittest
from http import HTTPMethod, HTTPStatus
from unittest.mock import MagicMock, patch

from lambda_asset.router import router
from models.models import Tier
from tests.helpers import api_gateway_event


class TestRouter(unittest.TestCase):

    def setUp(self):
        self.category_repo = MagicMock()
        self.activity_repo = MagicMock()
        self.router = router(
            self.category_repo,
            self.activity_repo,
        )

    @patch(
        "lambda_asset.router._get_user_id",
        return_value="user123",
    )
    @patch("lambda_asset.router.get_category_ids")
    def test_get_category_ids(
        self,
        get_category_ids,
        _get_user_id,
    ):
        get_category_ids.return_value = (
            {"categories": ["movies"]},
            HTTPStatus.OK,
        )

        event = api_gateway_event(
            HTTPMethod.GET,
            "/categories",
        )

        body, status = self.router(event)

        self.assertEqual(status, HTTPStatus.OK)
        self.assertEqual(
            body,
            {"categories": ["movies"]},
        )

        get_category_ids.assert_called_once_with(
            self.category_repo,
            "user123",
        )

    @patch(
        "lambda_asset.router._get_user_id",
        return_value="user123",
    )
    @patch("lambda_asset.router.get_category_activities")
    def test_get_category_activities(
        self,
        get_category_activities,
        _get_user_id,
    ):
        get_category_activities.return_value = (
            {
                "id": "movies",
                "activities": [],
            },
            HTTPStatus.OK,
        )

        event = api_gateway_event(
            HTTPMethod.GET,
            "/categories/movies",
            path_parameters={
                "category_id": "movies",
            },
        )

        body, status = self.router(event)

        self.assertEqual(status, HTTPStatus.OK)
        self.assertEqual(
            body,
            {
                "id": "movies",
                "activities": [],
            },
        )

        get_category_activities.assert_called_once_with(
            self.category_repo,
            "user123",
            "movies",
        )

    @patch(
        "lambda_asset.router._get_user_id",
        return_value="user123",
    )
    @patch("lambda_asset.router.get_activity")
    def test_get_activity(
        self,
        get_activity,
        _get_user_id,
    ):
        get_activity.return_value = (
            {
                "activity_id": "abc123",
                "name": "Dune",
                "category": "movies",
                "interest": Tier.HIGH.value,
                "effort": Tier.LOW.value,
            },
            HTTPStatus.OK,
        )

        event = api_gateway_event(
            HTTPMethod.GET,
            "/categories/movies/activities/abc123",
            path_parameters={
                "category_id": "movies",
                "activity_id": "abc123",
            },
        )

        body, status = self.router(event)

        self.assertEqual(status, HTTPStatus.OK)
        self.assertEqual(
            body,
            {
                "activity_id": "abc123",
                "name": "Dune",
                "category": "movies",
                "interest": Tier.HIGH.value,
                "effort": Tier.LOW.value,
            },
        )

        get_activity.assert_called_once_with(
            repository=self.activity_repo,
            user_id="user123",
            category_id="movies",
            activity_id="abc123",
        )

    @patch(
        "lambda_asset.router._get_user_id",
        return_value="user123",
    )
    @patch("lambda_asset.router.get_activity")
    def test_get_activity_not_found(
        self,
        get_activity,
        _get_user_id,
    ):
        get_activity.return_value = (
            {"msg": "activity abc123 not found"},
            HTTPStatus.NOT_FOUND,
        )

        event = api_gateway_event(
            HTTPMethod.GET,
            "/categories/movies/activities/abc123",
            path_parameters={
                "category_id": "movies",
                "activity_id": "abc123",
            },
        )

        body, status = self.router(event)

        self.assertEqual(status, HTTPStatus.NOT_FOUND)
        self.assertEqual(
            body,
            {"msg": "activity abc123 not found"},
        )

        get_activity.assert_called_once_with(
            repository=self.activity_repo,
            user_id="user123",
            category_id="movies",
            activity_id="abc123",
        )

    @patch(
        "lambda_asset.router._get_user_id",
        return_value="user123",
    )
    @patch("lambda_asset.router.add_activity")
    def test_add_activity(
        self,
        add_activity,
        _get_user_id,
    ):
        add_activity.return_value = (
            {"msg": "success"},
            HTTPStatus.ACCEPTED,
        )

        event = api_gateway_event(
            HTTPMethod.POST,
            "/categories/movies/activities",
            path_parameters={
                "category_id": "movies",
            },
            body={
                "name": "Dune",
                "body": {
                    "interest": Tier.HIGH.value,
                    "effort": Tier.LOW.value,
                },
            },
        )

        body, status = self.router(event)

        self.assertEqual(status, HTTPStatus.ACCEPTED)
        self.assertEqual(
            body,
            {"msg": "success"},
        )

        add_activity.assert_called_once_with(
            repository=self.activity_repo,
            user_id="user123",
            category_id="movies",
            name="Dune",
            body={
                "interest": Tier.HIGH.value,
                "effort": Tier.LOW.value,
            },
        )

    @patch(
        "lambda_asset.router._get_user_id",
        return_value="user123",
    )
    @patch("lambda_asset.router.edit_activity")
    def test_edit_activity(
        self,
        edit_activity,
        _get_user_id,
    ):
        edit_activity.return_value = (
            {"msg": "updated"},
            HTTPStatus.OK,
        )

        event = api_gateway_event(
            HTTPMethod.PUT,
            "/categories/movies/activities/abc123",
            path_parameters={
                "category_id": "movies",
                "activity_id": "abc123",
            },
            body={
                "interest": "MEDIUM",
            },
        )

        body, status = self.router(event)

        self.assertEqual(status, HTTPStatus.OK)
        self.assertEqual(
            body,
            {"msg": "updated"},
        )

        edit_activity.assert_called_once_with(
            repository=self.activity_repo,
            user_id="user123",
            category_id="movies",
            activity_id="abc123",
            body={
                "interest": "MEDIUM",
            },
        )

    @patch(
        "lambda_asset.router._get_user_id",
        return_value="user123",
    )
    @patch("lambda_asset.router.remove_activity")
    def test_remove_activity(
        self,
        remove_activity,
        _get_user_id,
    ):
        remove_activity.return_value = (
            {"msg": "removed"},
            HTTPStatus.OK,
        )

        event = api_gateway_event(
            HTTPMethod.DELETE,
            "/categories/movies/activities/abc123",
            path_parameters={
                "category_id": "movies",
                "activity_id": "abc123",
            },
        )

        body, status = self.router(event)

        self.assertEqual(status, HTTPStatus.OK)
        self.assertEqual(
            body,
            {"msg": "removed"},
        )

        remove_activity.assert_called_once_with(
            repository=self.activity_repo,
            user_id="user123",
            category_id="movies",
            activity_id="abc123",
        )

    @patch(
        "lambda_asset.router._get_user_id",
        return_value="user123",
    )
    def test_unknown_route(self, _get_user_id):
        event = api_gateway_event(
            HTTPMethod.GET,
            "/does/not/exist",
        )

        body, status = self.router(event)

        self.assertEqual(
            status,
            HTTPStatus.NOT_FOUND,
        )
        self.assertEqual(
            body,
            {"msg": "ROUTE NOT FOUND"},
        )

    @patch(
        "lambda_asset.router._get_user_id",
        return_value="user123",
    )
    @patch("lambda_asset.router.get_pick")
    def test_get_pick(
        self,
        get_pick,
        _get_user_id,
    ):
        get_pick.return_value = (
            {
                "name": "Watch Dune",
                "category": "movies",
            },
            HTTPStatus.OK,
        )

        event = api_gateway_event(
            HTTPMethod.POST,
            "/pick",
            body={
                "categories": [
                    "movies",
                    "games",
                ],
                "interest": Tier.MEDIUM.value,
                "effort": Tier.HIGH.value,
            },
        )

        body, status = self.router(event)

        self.assertEqual(status, HTTPStatus.OK)
        self.assertEqual(
            body,
            {
                "name": "Watch Dune",
                "category": "movies",
            },
        )

        get_pick.assert_called_once_with(
            repo=self.category_repo,
            user_id="user123",
            body={
                "categories": [
                    "movies",
                    "games",
                ],
                "interest": Tier.MEDIUM.value,
                "effort": Tier.HIGH.value,
            },
        )


if __name__ == "__main__":
    unittest.main()
