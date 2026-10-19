# Lambda Plan — Bulk Add Response

## Goal

Change `add_activities` so a successful bulk add returns `201 Created` without the created activity objects, reducing response payload / network cost.

This plan is for the lambda repo only. It is not part of the web app's `bulk_add_plan.md`.

## Current state (observed)

- Handler: `lambda_asset/handlers/activity.py`, `add_activities` (bulk `POST /categories/{category_id}/activities/bulk`).
- It validates the category and every activity before writing any of them, then calls `repository.add_activities(user_id=..., activities=...)`.
- On success it currently returns `HTTPStatus.CREATED` with both fields:

```python
return {
    "msg": f"successfully added {len(activities)} activities to {category_id}",
    ACTIVITIES: [activity.to_dict() for activity in activities],
}, HTTPStatus.CREATED
```

- Router (`lambda_asset/router.py`) passes the handler's `(body, status)` through unchanged, so no router change is needed.
- `ACTIVITIES` (from `constants.constants`) is also used in the same function to read `body.get(ACTIVITIES)`, so the import must stay.

## Proposed change

In `lambda_asset/handlers/activity.py`, `add_activities` only — drop the created objects from the success return:

```python
return {
    "msg": f"successfully added {len(activities)} activities to {category_id}"
}, HTTPStatus.CREATED
```

Nothing else changes: validation order, error bodies/statuses (`400` cases), name trimming, generated `activity_id`s, and the single `repository.add_activities(...)` write all stay exactly as they are. `add_activity` (single add) is untouched.

## Files to change

| File | Change |
| --- | --- |
| `lambda_asset/handlers/activity.py` | Remove `ACTIVITIES: [activity.to_dict() for activity in activities]` from the `add_activities` success return. Keep the `ACTIVITIES` import (still used for request parsing). |
| `tests/handler/activities.py` | In `test_add_activities`, replace the assertion on `response[ACTIVITIES]` with an exact-response assertion: status `HTTPStatus.CREATED` and `response == {"msg": "successfully added 2 activities to movies"}` (which also proves no `activities` key is returned). Repository-call assertions unchanged. |
| `tests/router.py` | Optional consistency only: the `test_add_activities` mock fixture may be trimmed to `{"msg": ...}` to mirror the real handler. The router test mocks the handler, so it passes either way; no router code changes. |

No other handlers, repository code, models, constants, or infrastructure files change.

## Tests

- Update `tests/handler/activities.py::test_add_activities` as above. Run it before the handler edit if a red-first check is wanted: the new exact-response assertion fails against the current return (extra `activities` key), then passes after.
- Run the focused handler suite, then the router suite, e.g. `python -m pytest tests/handler/activities.py tests/router.py` (or the repo's usual unittest invocation if pytest is not the runner — confirm from repo config before running).
- Existing error-path tests (`invalid category`, `missing/empty list`, invalid item, boolean tier, name trimming) must pass unchanged.

## Contract impact

- Response contract breaks for any client reading `activities` (including generated `activity_id`s) from the bulk-add response: a `201` now carries only `{ "msg": ... }`.
- Clients must not expect created objects from this endpoint after this change. How the web client adapts is tracked separately and is deliberately not specified here.
- Request contract, status code (`201`), and all error responses are unchanged, so no API Gateway / route changes are expected.

## Acceptance criteria

- Successful bulk add returns `201` with body exactly `{"msg": "successfully added N activities to {category_id}"}` and no `activities` key.
- All activities are still validated before any write and persisted via one `repository.add_activities` call.
- All pre-existing handler/router tests pass, with only the `test_add_activities` response assertion updated.

## Recommended next step

Approve this plan, then make the one-line handler edit plus the handler-test update, run the focused tests above, and report results. Do not deploy or touch the web app as part of this change.