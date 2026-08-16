import json
import os
from http import HTTPStatus

import boto3

from constants.constants import (
    APPLICATION_JSON,
    BODY,
    CONTENT_TYPE,
    DYNAMO_RESOURCE,
    HEADERS,
    PICK_EM_TABLE_2,
    STATUS_CODE,
    TABLE_NAME
)
from repository.activities import ActivitiesRepo
from repository.categories import CategoriesRepo
from router import router

_TABLE_NAME = os.environ.get(TABLE_NAME, PICK_EM_TABLE_2)
_table = boto3.resource(DYNAMO_RESOURCE).Table(_TABLE_NAME)
_activity_repo = ActivitiesRepo(_table)
_categories_repo = CategoriesRepo(_table)
_router = router(_categories_repo, _activity_repo)


def handler(event, _):
    body, status = _router(event)
    response = _response(body, status)

    # @TODO: remove debug print
    print(f'{response=}')
    return response


def _response(body, status) -> dict:
    return {
        STATUS_CODE: status.value if isinstance(status, HTTPStatus) else status,
        HEADERS: {
            CONTENT_TYPE: APPLICATION_JSON,
            "Access-Control-Allow-Origin": "http://localhost:5173",
        },
        BODY: json.dumps(body),
    }