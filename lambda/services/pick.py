from dataclasses import dataclass
from random import randint

from models.models import Activity, Tier, Pick


TIER_WEIGHTS = {
    Tier.LOW: 1,
    Tier.MEDIUM: 3,
    Tier.HIGH: 12,
}

@dataclass(frozen=True)
class _WeightedOption:
    activity: Activity
    start: int
    weight: int


def pick(
    activities: list[Activity],
    interest: Tier,
    effort: Tier,
) -> Pick | None:
    if not (options := _get_options(activities, interest, effort)):
        return None
    selected = _pick_item(options)
    return Pick(name=selected.name, category=selected.category)


def _get_options(
    activities: list[Activity],
    interest: Tier,
    effort: Tier,
) -> list[_WeightedOption]:
    options = []
    for activity in activities:
        if activity.effort > effort or activity.interest < interest:
            continue
        start = options[-1].start + options[-1].weight if options else 0
        # @TODO: is this how I want to handle interest < effort
        weight = max(1, TIER_WEIGHTS[activity.interest] // TIER_WEIGHTS[activity.effort])
        options.append(_WeightedOption(
            start=start, weight=weight, activity=activity))
    return options


def _pick_item(options: list[_WeightedOption]) -> Activity:
    start, stop = 0, len(options) - 1
    selection = randint(start, options[-1].start + options[-1].weight - 1)
    while start <= stop:
        mid = (start + stop) // 2
        end = options[mid].start + options[mid].weight
        if options[mid].start <= selection < end:
            return options[mid].activity
        elif end <= selection:
            start = mid + 1
        else:
            stop = mid - 1
    raise RuntimeError("Weighted selection failed.")
