from http import HTTPStatus

from common.constants.constants import *
from models.models import Tier
from repository.activities import ActivitiesRepo
from services.pick import pick


def get_pick(repo: ActivitiesRepo, user_id: str, body: dict) -> tuple[dict, HTTPStatus]:
    categories = body[CATEGORIES]
    interest = Tier(body[INTEREST])
    effort = Tier(body[EFFORT])

    activities = repo.get_activities(user_id, categories)
    if (selection := pick(activities, interest, effort)) is None:
        return {"msg": "No matching activities found."}, HTTPStatus.NOT_FOUND
    return selection.to_dict(), HTTPStatus.OK
