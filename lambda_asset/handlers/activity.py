import uuid

from http import HTTPStatus

from constants.constants import EFFORT, INTEREST
from repository.activities import ActivitiesRepo
from models.models import Activity, Tier, ActivityDict


def add_activity(
    repository: ActivitiesRepo,
    user_id: str,
    category_id: str,
    name: str,
    body: dict,
) -> tuple[dict[str, str], HTTPStatus]:
    """
    Add a new activity.
    """
    if not _is_valid_category_id(category_id):
        return {
            "msg": "category name cannot contain '/'"
        }, HTTPStatus.BAD_REQUEST

    activity = Activity(
        activity_id=str(uuid.uuid4()),
        name=name,
        category=category_id,
        interest=Tier(body[INTEREST]),
        effort=Tier(body[EFFORT]),
    )

    repository.add_activity(
        user_id=user_id,
        activity=activity,
    )

    return {
        "msg": f"successfully added {name} to {category_id}"
    }, HTTPStatus.ACCEPTED


def get_activity(
    repository: ActivitiesRepo,
    user_id: str,
    category_id: str,
    activity_id: str,
) -> tuple[dict[str, str], HTTPStatus] | tuple[ActivityDict, HTTPStatus]:
    """
    Get an activity by ID.
    """
    activity = repository.get_activity(
        user_id=user_id,
        category_id=category_id,
        activity_id=activity_id,
    )

    if activity is None:
        return {
            "msg": f"activity {activity_id} not found"
        }, HTTPStatus.NOT_FOUND

    return activity.to_dict(), HTTPStatus.OK


def _is_valid_category_id(category_id: str) -> bool:
    return "/" not in category_id


def edit_activity(
    repository: ActivitiesRepo,
    user_id: str,
    category_id: str,
    activity_id: str,
    body: dict,
) -> tuple[dict[str, str], HTTPStatus]:
    updates = {}

    try:
        if INTEREST in body:
            updates[INTEREST] = Tier(body[INTEREST])

        if EFFORT in body:
            updates[EFFORT] = Tier(body[EFFORT])
    except ValueError:
        return {"msg": "invalid interest or effort"}, HTTPStatus.BAD_REQUEST

    if EFFORT not in updates or INTEREST not in updates:
        return {"msg": "interest or effort"}, HTTPStatus.BAD_REQUEST

    updated = repository.update_activity(
        user_id=user_id,
        category_id=category_id,
        activity_id=activity_id,
        **updates,
    )

    if not updated:
        return {
            "msg": f"activity {activity_id} not found"
        }, HTTPStatus.NOT_FOUND

    return {
        "msg": f"successfully updated {activity_id}"
    }, HTTPStatus.OK


def remove_activity(
    repository: ActivitiesRepo,
    user_id: str,
    category_id: str,
    activity_id: str,
) -> tuple[dict[str, str], HTTPStatus]:
    """
    Remove an activity.
    """

    repository.delete_activity(
        user_id,
        category_id,
        activity_id
    )

    return {
        "msg": f"successfully activity {activity_id} from {category_id}"
    }, HTTPStatus.OK
