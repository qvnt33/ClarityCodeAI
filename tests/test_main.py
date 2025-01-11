from fastapi.testclient import TestClient
from httpx import Response

from app.main import app

client = TestClient(app)


def test_review_assignment_large_repo(mocker) -> None:
    """Test for checking work with big repositories (100+ files) API"""
    mocker.patch(
        'app.main.get_github_files',
        return_value=[{'name': f'file{i}.py', 'path': f'file{i}.py', 'content': 'print("Hello")'} for i in range(100)],
    )

    payload: dict[str, str] = {
        'assignment_description': 'Test assignment for large repo',
        'github_repo_url': 'https://github.com/octocat/Large-Repo',
        'candidate_level': 'Senior',
    }

    response: Response = client.post('/review-assignment', json=payload)
    assert response.status_code == 200
    assert len(response.json()['file_list'].split('\n')) == 100
