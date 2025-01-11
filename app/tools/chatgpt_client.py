import hashlib
import json
import logging
import re
from typing import Any

import redis
from fastapi import HTTPException
from openai import AsyncOpenAI
from openai.types.chat.chat_completion import ChatCompletion

from app.config import OPENAI_API_KEY, PROMPT_FOR_ANALYZE_CODE, REDIS_HOST, REDIS_PORT

logger: logging.Logger = logging.getLogger(__name__)

client = AsyncOpenAI(
    api_key=OPENAI_API_KEY,
)

redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0)


async def analyze_code_with_gpt(combined_code: str,
                                candidate_level: str,
                                assignment_description: str) -> dict[str, str] | Any:
    """Analyzes code using OpenAI GPT API.
    :param combined_code: Combined code from all GitHub files.
    :param candidate_level: Level of candidate (Junior, Middle, Senior)
    :param assignment_description
    :return: Result of analyze in format dictionary {'downsides': ..., 'rating': ..., 'conclusion': ...}
    """
    # Generate unique key for redis-cache
    cache_key: str = hashlib.sha256(f'{combined_code}_{candidate_level}_{assignment_description}'.encode()).hexdigest()

    # Check data in redis-cache
    cached_result = await redis_client.get(cache_key)
    if cached_result:
        return json.loads(cached_result)

    prompt: str = PROMPT_FOR_ANALYZE_CODE.format(
        combined_code=combined_code,
        candidate_level=candidate_level,
        assignment_description=assignment_description,
        )

    try:
        completion: ChatCompletion = await client.chat.completions.create(
        model='gpt-4o',
        messages=[
            {'role': 'system', 'content': 'You are an expert code reviewer.'},
            {'role': 'user', 'content': prompt},
            ],
        )

        review: str | None = completion.choices[0].message.content  # All code review from ChatGPT
        logger.info(f'GPT response: {review}')

        result: dict[str, str] = formatting_review_result(review)

        # Save result in redis-cache on 1 hour
        redis_client.set(cache_key, json.dumps(result), ex=3600)
        return result
    except Exception as e:
        logger.error(f'ChatGPT API error: {e}')
        raise HTTPException(status_code=500, detail=f'ChatGPT API error: {e}') from e


def formatting_review_result(review: str | None) -> dict[str, str]:
    """Formats review result from string format to dictionary with key and value when received by OpenAI API.
    :param review: Analyze by OpenAI API.
    :return: Formatted structured data.
    """
    return {
        'downsides_comments': divides_review_result(review, 'Downsides/Comments'),
        'rating': divides_review_result(review, 'Rating'),
        'conclusion': divides_review_result(review, 'Conclusion'),
    }


def divides_review_result(text: str | None, section_name: str) -> str:
    """Divides review result by ChatGPT into section content. Use regular functions.
    :param text: Full review result by ChatGPT.
    :param section_name: Name section to find.
    :return: Sections content.
    """
    if text is None:
        text = ''
    try:
        # Template for divide section
        pattern: str = rf'### {re.escape(section_name)}:\s*(.*?)(?=###|$)'
        match: re.Match[str] | None = re.search(pattern, text, re.DOTALL)
        if match:
            return match.group(1).strip()
        return 'Section not found'
    except Exception as e:
        logger.error(f'Error extracting section "{section_name}": {e}')
        return f'Section "{section_name}" not found.'
