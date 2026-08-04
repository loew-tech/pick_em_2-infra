
import boto3

from boto3.dynamodb.conditions import Key

from constants import *
from models import Activity


class ActivitiesRepo:

    def __init__(self):
        table = boto3.resource('dynamodb')
        self.table = table.Table("PickEmActivities")

    def get_category_ids(self, user_id='stevebot') -> list[str]:
        response = self.table.query(
            KeyConditionExpression=Key("PK").eq(f'USER#{user_id}'),
            ProjectionExpression=CATEGORY_ID,
        )

        return sorted({item[CATEGORY_ID] for item in response.get(ITEMS, ())})

    def get_category_activities(self, user_id='stevebot', category_id='') -> list[Activity]:
        response = self.table.query(
            KeyConditionExpression=(Key('PK').eq(f'USER#{user_id}') & Key('SK').begins_with(f'CATEGORY#{category_id}#'))
        )
        return sorted([Activity.from_dict(item) for item in response.get(ITEMS, ())],
                      key=lambda activity: activity.name)
