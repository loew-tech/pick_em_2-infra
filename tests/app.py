import json
import unittest
from http import HTTPStatus
from unittest.mock import patch

from lambda_asset import app


class TestApp(unittest.TestCase):

    @patch("lambda_asset.app._router")
    def test_handler_returns_json_response(self, router):
        router.return_value = (
            {"msg": "success"},
            HTTPStatus.OK,
        )

        response = app.handler({}, None)

        self.assertEqual(response["statusCode"], 200)
        self.assertEqual(
            response["headers"]["Content-Type"],
            "application/json",
        )
        self.assertEqual(
            json.loads(response["body"]),
            {"msg": "success"},
        )

    def test_response_serializes_body(self):
        response = app._response(
            {"a": 1},
            HTTPStatus.CREATED,
        )

        self.assertEqual(response["statusCode"], 201)
        self.assertEqual(
            json.loads(response["body"]),
            {"a": 1},
        )

if __name__ == "__main__":
    unittest.main()
