from http import HTTPStatus

from constants.constants import ACTIVITIES, CATEGORIES, ID
from repository.activities import ActivitiesRepo


def get_category_ids(
    repo: ActivitiesRepo,
    user_id: str = 'stevebot'
) -> dict:
    ids = repo.get_category_ids(user_id)
    return {CATEGORIES: ids}

def get_category_activities(
    repo: ActivitiesRepo,
    user_id: str,
    category_id: str
) -> tuple[dict, HTTPStatus]:
    activities = repo.get_category_activities(user_id, category_id)
    return {ID: category_id, ACTIVITIES: [activity.to_dict() for activity in sorted(activities,
                                                    key=lambda activity: activity.name)]}, HTTPStatus.OK
