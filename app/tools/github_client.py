import json
import logging
<<<<<<< HEAD
from typing import Any, Awaitable
=======
from typing import Any
>>>>>>> develop

import httpx
import redis

from app.config import GITHUB_TOKEN, REDIS_HOST, REDIS_PORT

logger: logging.Logger = logging.getLogger(__name__)

redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0)


async def get_github_files(repo_url: str, path: str = '') -> list[dict[str, str]] | Any:
    """Returns a list of files with their contents from a GitHub repository, including subdirectories.
    :param repo_url: URL repository.
    :param path: Path ot folder in repository.
    :return: List of files with their contents (name, path to file from main, content)
    """
    # Generate unique key for redis-cache
    cache_key: str = f'github_files:{repo_url}:{path}'

    # Check data in redis-cache
    cached_data = await redis_client.get(cache_key)
    if cached_data:
        logger.info(f'Cache hit for {cache_key}')
        return json.loads(cached_data)

    # Якщо даних немає в кеші, робимо запит до GitHub API
    logger.info(f'Cache miss for {cache_key}')
    url_parts: list[str] = repo_url.rstrip('/').split('/')
    owner, repo = url_parts[-2], url_parts[-1]

    api_url: str = f'https://api.github.com/repos/{owner}/{repo}/contents/{path}'
    headers: dict[str, str] = {'Authorization': f'Bearer {GITHUB_TOKEN}'}

    async with httpx.AsyncClient() as client:
        response: httpx.Response = await client.get(api_url,
                                                    headers=headers)
        if response.status_code != 200:
            logger.warning(f'Get incorrect answer from GitHub API: {response.status_code}')
            raise Exception(f'GitHub API error: {response.status_code} {response.text}')

        files = response.json()
        file_data: list[dict[str, str]] = []

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
                logger.info(f'Entering directory: {file["path"]}')
                folder_files: list[dict[str, str]] | Any = await get_github_files(repo_url, file['path'])
                file_data.extend(folder_files)

        # Save result in redis-cache on 1 hour
        redis_client.set(cache_key, json.dumps(file_data), ex=3600)

        return file_data
