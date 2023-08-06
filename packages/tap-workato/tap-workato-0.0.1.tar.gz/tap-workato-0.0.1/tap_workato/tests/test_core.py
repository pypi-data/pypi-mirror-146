"""Tests standard tap features using the built-in SDK tests library."""

from singer_sdk.testing import get_standard_tap_tests

from tap_workato.tap import TapWorkato

SAMPLE_CONFIG = {
    "user_email": "test@workato.blah",
    "user_token": "abc-123",
}


def json_resp(extras: dict = None) -> dict:
    """Utility function returning a common response for mocked API calls.

    Args:
        extras: items to be added to the contents of the json response.

    Returns:
        A json object that mocks the results of an API call.
    """
    contents = {
        "items": [
            {
                "id": 7498,
                "name": "Netsuite production",
            },
            {
                "id": 7302,
                "name": "Automation HR",
            },
        ]
    }

    if extras:
        for k, v in extras.items():
            contents[k] = v
    return contents


endpoints = [
    "https://www.workato.com/api/api_clients?per_page=100",
    "https://www.workato.com/api/api_collections?per_page=100",
    "https://www.workato.com/api/connections?per_page=100",
    "https://www.workato.com/api/roles?per_page=100",
    "https://www.workato.com/api/deployments?per_page=100",
    "https://www.workato.com/api/folders?per_page=100",
    "https://www.workato.com/api/on_prem_agents?per_page=100",
    "https://www.workato.com/api/on_prem_groups?per_page=100",
    "https://www.workato.com/api/recipes?per_page=100",
    "https://www.workato.com/api/recipes/7498/jobs?per_page=100",
    "https://www.workato.com/api/recipes/7302/jobs?per_page=100",
    "https://www.workato.com/api/managed_users?per_page=100",
]


# Run standard built-in tap tests from the SDK:
def test_standard_tap_tests(requests_mock):
    """Run standard tap tests from the SDK."""
    for endpoint in endpoints:
        requests_mock.get(endpoint, json=json_resp())
    tests = get_standard_tap_tests(TapWorkato, config=SAMPLE_CONFIG)
    for test in tests:
        test()
