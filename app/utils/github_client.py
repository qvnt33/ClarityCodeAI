import httpx
from config import GITHUB_TOKEN


async def get_github_files(repo_url: str, path: str = '') -> list:
    """Returns a list of files with their contents from a GitHub repository, including subdirectories.

    Args:
        repo_url (str): URL repository
        path (str): Path to folder in repository

    Returns:
        list[dict]: List of files with their contents (name, path to file from main, content)
    """
    url_parts: list[str] = repo_url.rstrip('/').split('/')
    owner, repo = url_parts[-2], url_parts[-1]

    api_url: str = f'https://api.github.com/repos/{owner}/{repo}/contents/{path}'
    headers: dict[str, str] = {'Authorization': f'Bearer {GITHUB_TOKEN}'}

    async with httpx.AsyncClient() as client:
        response: httpx.Response = await client.get(api_url,
                                                    headers=headers)
        if response.status_code != 200:
            raise Exception(f'GitHub API error: {response.status_code} {response.text}')

        files = response.json()
        file_data: list = []

        for file in files:
            if file['type'] == 'file':
                file_response: httpx.Response = await client.get(file['download_url'])  # File code
                if file_response.status_code == 200:
                    file_data.append({
                        'name': file['name'],
                        'path': file['path'],
                        'content': file_response.text,
                    })
            elif file['type'] == 'dir':
                # Repeat recursively
                folder_files: list = await get_github_files(repo_url, file['path'])
                file_data.extend(folder_files)
        return file_data
