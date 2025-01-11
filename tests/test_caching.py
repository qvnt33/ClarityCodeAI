from fastapi.testclient import TestClient
from httpx import Response
from pytest_mock.plugin import MockerFixture

from app.main import app

client = TestClient(app)


def test_review_assignment_caching(mocker: MockerFixture) -> None:
    """Test for caching with Redis"""
    mock_redis = mocker.patch('app.utils.github_client.redis_client')
    mock_redis.get.return_value = None  # Cache not has data
    mock_redis.set.return_value = True  # Data caching

    payload: dict[str, str] = {
        'assignment_description': 'Test assignment',
        'github_repo_url': 'https://github.com/octocat/Hello-World',
        'candidate_level': 'Junior',
    }

    response: Response = client.post('/review-assignment', json=payload)

    assert response.status_code == 200
    mock_redis.set.assert_called_once()
