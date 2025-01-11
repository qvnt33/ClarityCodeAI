from fastapi.testclient import TestClient
from httpx import Response
from pytest_mock.plugin import MockerFixture

from app.main import app

client = TestClient(app)


def test_review_assignment_gpt_error(mocker: MockerFixture) -> None:
    """Test for ChatGPT API"""
    mocker.patch(
        'app.main.analyze_code_with_gpt',
        side_effect=Exception('GPT API error'),
    )

    payload: dict[str, str] = {
        'assignment_description': 'Test assignment',
        'github_repo_url': 'https://github.com/octocat/Hello-World',
        'candidate_level': 'Junior',
    }

    response: Response = client.post('/review-assignment', json=payload)
    assert response.status_code == 500
    assert 'GPT API error' in response.json()['detail']
