import json
from http import HTTPMethod


def api_gateway_event(
    method: HTTPMethod,
    path: str,
    *,
    path_parameters: dict | None = None,
    body: dict | None = None,
) -> dict:
    return {
        "requestContext": {
            "http": {
                "method": method,
                "path": path,
            }
        },
        "pathParameters": path_parameters or {},
        "body": json.dumps(body) if body is not None else None,
    }
