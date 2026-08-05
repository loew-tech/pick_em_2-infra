import json
import os

import boto3


from handlers.activity import add_activity, edit_activity, remove_activity
from handlers.category import get_category_ids, get_category_activities
from repository import ActivitiesRepo


TABLE_NAME = os.environ['TABLE_NAME']

table = boto3.resource('dynamodb').Table(TABLE_NAME)
repo = ActivitiesRepo(table)

def handler(event, context):
    # TODO: Replace with Cognito/JWT
    user_id = "stevebot"
    method = event["requestContext"]["http"]["method"]
    path = event["rawPath"]
    path_parameters = event.get("pathParameters") or {}
    body = event.get("body")

    if method == "POST":
        body = json.loads(body)


