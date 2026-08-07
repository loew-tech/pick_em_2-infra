from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError

from constants.constants import *
from models.models import Activity, Tier
from repository.types import DynamoTable
from repository.exceptions import RepositoryError, ItemNotFoundError


class ActivitiesRepo:

    def __init__(self, table: DynamoTable):
        self._table = table

    def get_category_ids(self, user_id: str) -> list[str]:
        try:
            response = self._table.query(
                KeyConditionExpression=Key(PK).eq(f'USER#{user_id}'),
                ProjectionExpression=CATEGORY_ID,
            )
        except ClientError as exc:
            raise RepositoryError(f"Failed to retrieve category IDs for {user_id}.") from exc

        return sorted({item[CATEGORY_ID] for item in response.get(ITEMS, ())})

    def get_category_activities(self, user_id: str, category_id: str) -> list[Activity]:
        try:
            response = self._table.query(
                KeyConditionExpression=(Key(PK).eq(f'USER#{user_id}') & Key(SK).begins_with(f'CATEGORY#{category_id}#'))
            )
        except ClientError as exc:
            raise RepositoryError(f"Failed to retrieve activities for category {category_id} for {user_id}.") from exc

        return sorted((Activity.from_dict(item) for item in response.get(ITEMS, ())),
                      key=lambda activity: activity.name)

    def get_activities(self, user_id: str, category_ids: list[str]) -> list[Activity]:
        activities = []
        for category_id in category_ids:
            activities.extend(self.get_category_activities(user_id, category_id))
        return activities

    def add_activity(self, user_id: str, activity: Activity) -> None:
        try:
            self._table.put_item(
                Item={
                    PK: f"USER#{user_id}",
                    SK: f"CATEGORY#{activity.category}#ACTIVITY#{activity.activity_id}",
                    **activity.to_dict(),
                }
            )
        except ClientError as exc:
            raise RepositoryError(f"Failed to retrieve activity for {user_id}.") from exc

    def update_activity(
            self,
            user_id: str,
            category_id: str,
            activity_id: str,
            *,
            interest: Tier | None = None,
            effort: Tier | None = None,
    ) -> bool:
        expressions = []
        values = {}

        if interest is not None:
            expressions.append("interest = :interest")
            values[":interest"] = interest.value

        if effort is not None:
            expressions.append("effort = :effort")
            values[":effort"] = effort.value

        if not expressions:
            return False

        try:
            self._table.update_item(
                Key={
                    PK: f"USER#{user_id}",
                    SK: f"CATEGORY#{category_id}#ACTIVITY#{activity_id}"
                },
                UpdateExpression="SET " + ", ".join(expressions),
                ExpressionAttributeValues=values,
                ConditionExpression="attribute_exists(PK)",
            )
        except ClientError as exc:
            raise RepositoryError(f"Failed to update activity for {user_id}.") from exc

        return True

    def delete_activity(self, user_id: str, category_id: str, activity_id: str) -> None:
        try:
            self._table.delete_item(
                Key={PK: f'USER#{user_id}', SK: f'CATEGORY#{category_id}#ACTIVITY#{activity_id}'},
            )
        except ClientError as exc:
            raise RepositoryError(f"Failed to delete activity for {user_id}.") from exc
