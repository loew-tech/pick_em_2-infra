from http import HTTPStatus

from constants.constants import ACTIVITIES, CATEGORIES, ID
from repository.categories import CategoriesRepo


def get_category_ids(
    repo: CategoriesRepo,
    user_id,
) -> tuple[dict, HTTPStatus]:
    ids = repo.get_category_ids(user_id)
    return {CATEGORIES: ids}, HTTPStatus.OK

def get_category_activities(
    repo: CategoriesRepo,
    user_id: str,
    category_id: str
) -> tuple[dict, HTTPStatus]:
    activities = repo.get_category_activities(user_id, category_id)
    return {ID: category_id, ACTIVITIES: [activity.to_dict() for activity in sorted(activities,
                                                    key=lambda activity: activity.name)]}, HTTPStatus.OK
