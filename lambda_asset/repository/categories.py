import logging

from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError

from constants.constants import PK, SK, ITEMS, CATEGORY
from models.models import Activity, Tier
from repository.types import DynamoTable
from repository.exceptions import RepositoryError


logger = logging.getLogger(__name__)


class CategoriesRepo:

    def __init__(self, table: DynamoTable):
        self._table = table

    def get_category_ids(self, user_id: str) -> list[str]:
        try:
            response = self._table.query(
                KeyConditionExpression=Key(PK).eq(f'USER#{user_id}'),
                ProjectionExpression=CATEGORY,
            )
        except ClientError as exc:
            logger.exception("Failed to retrieve category IDs for %s", user_id)
            raise RepositoryError(
                f"Failed to retrieve category IDs for {user_id}: "
                f"{exc.response['Error']['Code']} - "
                f"{exc.response['Error']['Message']}"
            ) from exc

        # @TODO: remove debug print
        print(f'{response.get(ITEMS, ())=}')
        return sorted({item[CATEGORY] for item in response.get(ITEMS, ())})

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

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}"
