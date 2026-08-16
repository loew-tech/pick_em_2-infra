import unittest
from unittest.mock import MagicMock

from botocore.exceptions import ClientError

from constants.constants import (
    CATEGORY,
    CATEGORY_ID,
    EFFORT,
    INTEREST,
    ITEMS,
    NAME,
    PK,
    SK,
)
from models.models import Activity, Tier
from repository.activities import ActivitiesRepo
from repository.exceptions import RepositoryError


class TestActivitiesRepo(unittest.TestCase):

    def setUp(self):
        self.table = MagicMock()
        self.repo = ActivitiesRepo(self.table)

    def test_get_activity(self):
        self.table.get_item.return_value = {
            "Item": {
                "activity_id": "abc",
                NAME: "Dune",
                CATEGORY: "movies",
                INTEREST: Tier.HIGH.value,
                EFFORT: Tier.LOW.value,
            }
        }

        activity = self.repo.get_activity(
            "steve",
            "movies",
            "abc",
        )

        self.assertEqual(
            activity,
            Activity(
                activity_id="abc",
                name="Dune",
                category="movies",
                interest=Tier.HIGH,
                effort=Tier.LOW,
            ),
        )

        self.table.get_item.assert_called_once_with(
            Key={
                PK: "USER#steve",
                SK: "CATEGORY#movies#ACTIVITY#abc",
            }
        )

    def test_get_activity_not_found(self):
        self.table.get_item.return_value = {}

        activity = self.repo.get_activity(
            "steve",
            "movies",
            "abc",
        )

        self.assertIsNone(activity)

        self.table.get_item.assert_called_once_with(
            Key={
                PK: "USER#steve",
                SK: "CATEGORY#movies#ACTIVITY#abc",
            }
        )

    def test_add_activity(self):
        activity = Activity(
            activity_id="abc",
            name="Dune",
            category="movies",
            interest=Tier.HIGH,
            effort=Tier.LOW,
        )

        self.repo.add_activity(
            "steve",
            activity,
        )

        _, kwargs = self.table.put_item.call_args

        item = kwargs["Item"]

        self.assertEqual(
            item,
            {
                PK: "USER#steve",
                SK: "CATEGORY#movies#ACTIVITY#abc",
                "activity_id": "abc",
                "name": "Dune",
                "category": "movies",
                "interest": Tier.HIGH.value,
                "effort": Tier.LOW.value,
            },
        )

    def test_update_activity(self):
        updated = self.repo.update_activity(
            "steve",
            "movies",
            "abc",
            interest=Tier.HIGH,
            effort=Tier.LOW,
        )

        self.assertTrue(updated)

        _, kwargs = self.table.update_item.call_args

        self.assertEqual(
            kwargs["Key"],
            {
                PK: "USER#steve",
                SK: "CATEGORY#movies#ACTIVITY#abc",
            },
        )

        self.assertEqual(
            kwargs["UpdateExpression"],
            "SET interest = :interest, effort = :effort",
        )

        self.assertEqual(
            kwargs["ExpressionAttributeValues"],
            {
                ":interest": Tier.HIGH.value,
                ":effort": Tier.LOW.value,
            },
        )

        self.assertEqual(
            kwargs["ConditionExpression"],
            "attribute_exists(PK)",
        )

    def test_update_activity_interest_only(self):
        self.repo.update_activity(
            "steve",
            "movies",
            "abc",
            interest=Tier.MEDIUM,
        )

        _, kwargs = self.table.update_item.call_args

        self.assertEqual(
            kwargs["UpdateExpression"],
            "SET interest = :interest",
        )

        self.assertEqual(
            kwargs["ExpressionAttributeValues"],
            {
                ":interest": Tier.MEDIUM.value,
            },
        )

    def test_update_activity_effort_only(self):
        self.repo.update_activity(
            "steve",
            "movies",
            "abc",
            effort=Tier.LOW,
        )

        _, kwargs = self.table.update_item.call_args

        self.assertEqual(
            kwargs["UpdateExpression"],
            "SET effort = :effort",
        )

        self.assertEqual(
            kwargs["ExpressionAttributeValues"],
            {
                ":effort": Tier.LOW.value,
            },
        )

    def test_update_activity_no_updates(self):
        updated = self.repo.update_activity(
            "steve",
            "movies",
            "abc",
        )

        self.assertFalse(updated)
        self.table.update_item.assert_not_called()

    def test_update_activity_not_found(self):
        self.table.update_item.side_effect = ClientError(
            {
                "Error": {
                    "Code": "ConditionalCheckFailedException",
                }
            },
            "UpdateItem",
        )

        updated = self.repo.update_activity(
            "steve",
            "movies",
            "abc",
            interest=Tier.HIGH,
        )

        self.assertFalse(updated)

    def test_update_activity_raises_other_client_error(self):
        self.table.update_item.side_effect = ClientError(
            {
                "Error": {
                    "Code": "ProvisionedThroughputExceededException",
                }
            },
            "UpdateItem",
        )

        with self.assertRaises(RepositoryError):
            self.repo.update_activity(
                "steve",
                "movies",
                "abc",
                interest=Tier.HIGH,
            )

    def test_delete_activity(self):
        self.repo.delete_activity(
            "steve",
            "movies",
            "abc",
        )

        _, kwargs = self.table.delete_item.call_args

        self.assertEqual(
            kwargs["Key"],
            {
                PK: "USER#steve",
                SK: "CATEGORY#movies#ACTIVITY#abc",
            },
        )

if __name__ == "__main__":
    unittest.main()
