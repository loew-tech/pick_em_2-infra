from http import HTTPStatus

from models import Activity
from repository import ActivitiesRepo


def get_category_ids(
    repo: ActivitiesRepo,
    user_id: str = 'stevebot'
) -> dict:
    ids = repo.get_category_ids(user_id)
    return {'categories': ids}

def get_category_activities(
    repo: ActivitiesRepo,
    category_id: str
) -> tuple[dict[str, str | list[Activity]], HTTPStatus]:
    activities = repo.get_category_activities(category_id)
    return {'id': category_id, 'activities': activities}, HTTPStatus.OK
