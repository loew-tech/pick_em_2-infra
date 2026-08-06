from dataclasses import dataclass
from enum import IntEnum
from typing import TypedDict

from constants.constants import *


class ActivityDict(TypedDict):
    activity_id: str
    name: str
    category: str
    interest: int
    effort: int


class CategoryDict(TypedDict):
    id: str


class Tier(IntEnum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3


@dataclass(frozen=True)
class Activity:
    """
    A user activity that can be selected.

    Attributes:
        name: Display name of the activity.
        category: Category the activity belongs to.
        interest: User's interest level.
        effort: Required effort level.
    """
    activity_id: str
    name: str
    category: str
    interest: Tier
    effort: Tier

    @classmethod
    def from_dict(cls, d: ActivityDict) -> 'Activity':
        return cls(
            activity_id=d[ACTIVITY_ID],
            name=d[NAME],
            category=d[CATEGORY],
            interest=Tier(d[INTEREST]),
            effort=Tier(d[EFFORT]),
        )

    def to_dict(self) -> ActivityDict:
        return {
            ACTIVITY_ID: self.activity_id,
            CATEGORY: self.category,
            NAME: self.name,
            INTEREST: self.interest.value,
            EFFORT: self.effort.value,
        }


@dataclass(frozen=True)
class Category:
    """
    A category containing activities.

    Categories are currently derived from activities,
    not stored as separate DynamoDB entities.

    Attributes:
        id: Unique identifier of the category.
    """
    id: str

    @classmethod
    def from_dict(cls, d: CategoryDict) -> 'Category':
        return cls(id=d[ID])


@dataclass(frozen=True)
class Pick:
    name: str
    category: str

    def to_dict(self) -> dict:
        return {
            NAME: self.name,
            CATEGORY: self.category,
        }
