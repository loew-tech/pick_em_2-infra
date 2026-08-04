# handlers/activities.py

from models import Activity, Tier


def add_activity(
    repository,
    user_id: str,
    category_id: str,
    name: str,
    body: dict,
) -> dict:
    """
    Add a new activity.
    """

    activity = Activity(
        name=name,
        category=category_id,
        interest=Tier(body["interest"]),
        effort=Tier(body["effort"]),
    )

    repository.add_activity(
        user_id=user_id,
        activity=activity,
    )

    return {
        "msg": f"successfully added {name} to {category_id}"
    }


def edit_activity(
    repository,
    user_id: str,
    category_id: str,
    name: str,
    body: dict,
) -> dict:
    """
    Update an existing activity.
    """

    updated = repository.update_activity(
        user_id=user_id,
        category_id=category_id,
        name=name,
        interest=body.get("interest"),
        effort=body.get("effort"),
    )

    if not updated:
        return {
            "msg": f"name {name} not found"
        }

    return {
        "msg": (
            f"successfully updated "
            f"{name} in {category_id}"
        )
    }


def remove_activity(
    repository,
    user_id: str,
    category_id: str,
    name: str,
) -> dict:
    """
    Remove an activity.
    """

    removed = repository.delete_activity(
        user_id=user_id,
        category_id=category_id,
        name=name,
    )

    if not removed:
        return {
            "msg": (
                f"name {name} "
                f"not found in {category_id}"
            )
        }

    return {
        "msg": (
            f"successfully removed "
            f"{name} from {category_id}"
        )
    }