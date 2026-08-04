from dataclasses import dataclass
from enum import IntEnum
from typing import TypedDict


class ActivityDict(TypedDict):
    name: str
    category: str
    interest: int
    effort: int


class CategoryDict(TypedDict):
    id: str


class Tier(IntEnum):
    LOW = 1
    MEDIUM = 3
    HIGH = 12


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
    name: str
    category: str
    interest: Tier
    effort: Tier

    @classmethod
    def from_dict(cls, d: ActivityDict) -> 'Activity':
        return cls(
            name=d['name'],
            category=d['category'],
            interest=Tier(d['interest']),
            effort=Tier(d['effort']),
        )


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
        return cls(id=d['id'])
