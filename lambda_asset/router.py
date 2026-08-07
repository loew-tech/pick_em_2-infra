import json
from http import HTTPStatus, HTTPMethod
from typing import Any
from collections.abc import Callable


from common.constants.constants import *
from handlers.activity import add_activity, edit_activity, remove_activity
from handlers.category import get_category_ids, get_category_activities
from handlers.pick import get_pick
from repository.activities import ActivitiesRepo


RouteResponse = tuple[dict[str, Any], HTTPStatus]
Router = Callable[[dict[str, Any]], RouteResponse]


def router(activity_repo: ActivitiesRepo) -> Router:
    def route(event: dict[str, Any]) -> RouteResponse:
        method = event[REQUEST_CONTEXT][HTTP_STR][METHOD]
        path = event[REQUEST_CONTEXT][HTTP_STR][PATH_STR]

        user_id = _get_user_id(event)
        if method == HTTPMethod.GET and path == CATEGORIES_PATH:
            body, status = get_category_ids(activity_repo, user_id)
        elif method == HTTPMethod.GET and path.startswith(f'{CATEGORIES_PATH}/'):
            category_id = event[PATH_PARAMETERS][CATEGORY_ID]
            body, status = get_category_activities(activity_repo, user_id, category_id)
        elif method == HTTPMethod.POST and f'{ACTIVITIES_PATH}/' in path:
            params = event[PATH_PARAMETERS]
            body, status = add_activity(repository=activity_repo,
                                        user_id=user_id,
                                        category_id=params[CATEGORY_ID],
                                        name=params[NAME],
                                        body=json.loads(event[BODY]))
        elif method == HTTPMethod.POST and path == PICK_PATH:
            body, status = get_pick(
                repo=activity_repo,
                user_id=user_id,
                body=json.loads(event[BODY])
            )
        elif method == HTTPMethod.PUT and f'{ACTIVITIES_PATH}/' in path:
            params = event[PATH_PARAMETERS]
            body, status = edit_activity(repository=activity_repo,
                                         user_id=user_id,
                                         category_id=params[CATEGORY_ID],
                                         activity_id=params[ACTIVITY_ID],
                                         body=json.loads(event[BODY]))
        elif method == HTTPMethod.DELETE and f'{ACTIVITIES_PATH}/' in path:
            params = event[PATH_PARAMETERS]
            body, status = remove_activity(repository=activity_repo,
                                           user_id=user_id,
                                           category_id=params[CATEGORY_ID],
                                           activity_id=params[ACTIVITY_ID])
        else:
            body, status = {"msg": "ROUTE NOT FOUND"}, HTTPStatus.NOT_FOUND

        return body, status

    return route


# @TODO implement using JWT or similar
def _get_user_id(event) -> str:
    return "stevebot"