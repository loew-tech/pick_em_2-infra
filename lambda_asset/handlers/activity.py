import uuid

from http import HTTPStatus

from constants.constants import ACTIVITIES, EFFORT, INTEREST, NAME
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


def add_activities(
    repository: ActivitiesRepo,
    user_id: str,
    category_id: str,
    body: dict,
) -> tuple[dict, HTTPStatus]:
    """Validate and add multiple activities to one category."""
    if not _is_valid_category_id(category_id):
        return {
            "msg": "category name cannot contain '/'"
        }, HTTPStatus.BAD_REQUEST

    activities_data = body.get(ACTIVITIES) if isinstance(body, dict) else None

    if not isinstance(activities_data, list) or not activities_data:
        return {
            "msg": "activities must be a non-empty list"
        }, HTTPStatus.BAD_REQUEST

    activities = []

    # Validate every activity before writing any of them.
    for index, item in enumerate(activities_data):
        if not isinstance(item, dict):
            return {
                "msg": f"activities[{index}] must be an object"
            }, HTTPStatus.BAD_REQUEST

        name = item.get(NAME)
        if not isinstance(name, str) or not name.strip():
            return {
                "msg": f"activities[{index}].name must be a non-empty string"
            }, HTTPStatus.BAD_REQUEST

        interest_value = item.get(INTEREST)
        effort_value = item.get(EFFORT)

        if (
            isinstance(interest_value, bool)
            or not isinstance(interest_value, int)
            or isinstance(effort_value, bool)
            or not isinstance(effort_value, int)
        ):
            return {
                "msg": f"activities[{index}] has invalid or missing interest/effort"
            }, HTTPStatus.BAD_REQUEST

        try:
            interest = Tier(interest_value)
            effort = Tier(effort_value)
        except ValueError:
            return {
                "msg": f"activities[{index}] has invalid or missing interest/effort"
            }, HTTPStatus.BAD_REQUEST

        activities.append(
            Activity(
                activity_id=str(uuid.uuid4()),
                name=name.strip(),
                category=category_id,
                interest=interest,
                effort=effort,
            )
        )

    repository.add_activities(
        user_id=user_id,
        activities=activities,
    )

    return {
        "msg": f"successfully added {len(activities)} activities to {category_id}",
        ACTIVITIES: [activity.to_dict() for activity in activities],
    }, HTTPStatus.CREATED


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
        return {"msg": "interest or effort not provided"}, HTTPStatus.BAD_REQUEST

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
