import pytest
from fastapi.testclient import TestClient
from httpx import Response

from app.main import app

client = TestClient(app)


def test_review_assignment_success() -> None:
    """Test for checking success execution of endpoint '/review-assignment`"""
    payload: dict[str, str] = {
        'assignment_description': 'Test assignment',
        'github_repo_url': 'https://github.com/octocat/Hello-World',
        'candidate_level': 'Junior',
    }

    response: Response = client.post('/review-assignment', json=payload)

    assert response.status_code == 200

    data = response.json()

    assert 'downsides_comments' in data
    assert 'rating' in data
    assert 'conclusion' in data
    assert 'file_list' in data


def test_review_assignment_invalid_repo_url() -> None:
    """Test for checking reaction for incorrect URL"""
    payload: dict[str, str] = {
        'assignment_description': 'Test assignment',
        'github_repo_url': 'https://github.com/invalid/repo',
        'candidate_level': 'Junior',
    }

    response: Response = client.post('/review-assignment', json=payload)

    assert response.status_code == 500
    assert 'GitHub API error' in response.json()['detail']


def test_review_assignment_missing_field() -> None:
    """Test for checking reaction for miss required field"""
    payload: dict[str, str] = {
        'github_repo_url': 'https://github.com/octocat/Hello-World',
        'candidate_level': 'Junior',
    }

    response: Response = client.post('/review-assignment', json=payload)

    assert response.status_code == 422
    assert 'assignment_description' in response.json()['detail'][0]['loc']


@pytest.mark.parametrize('candidate_level', ['Junior', 'Middle', 'Senior'])
def test_review_assignment_candidate_levels(candidate_level: str) -> None:
    """Test for checking work with different levels of cadidates"""
    payload: dict[str, str] = {
        'assignment_description': 'Test assignment',
        'github_repo_url': 'https://github.com/octocat/Hello-World',
        'candidate_level': candidate_level,
    }

    response: Response = client.post('/review-assignment', json=payload)

    assert response.status_code == 200
    data = response.json()
    assert data['conclusion']
