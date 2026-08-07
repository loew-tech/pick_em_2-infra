import json
import os
from http import HTTPStatus

import boto3

from common.constants.constants import (
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
from router import router

_TABLE_NAME = os.environ.get(TABLE_NAME, PICK_EM_TABLE_2)
_table = boto3.resource(DYNAMO_RESOURCE).Table(_TABLE_NAME)
_activity_repo = ActivitiesRepo(_table)
_router = router(_activity_repo)


def handler(event, _):
    body, status = _router(event)
    return _response(body, status)


def _response(body, status):
    return {
        STATUS_CODE: status.value if isinstance(status, HTTPStatus) else status,
        HEADERS: {
            CONTENT_TYPE: APPLICATION_JSON,
        },
        BODY: json.dumps(body),
    }