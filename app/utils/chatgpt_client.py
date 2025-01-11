import logging
import re

from fastapi import HTTPException
from openai import AsyncOpenAI
from openai.types.chat.chat_completion import ChatCompletion

from app.config import OPENAI_API_KEY, PROMPT_FOR_ANALYZE_CODE

logger: logging.Logger = logging.getLogger(__name__)

client = AsyncOpenAI(
    api_key=OPENAI_API_KEY,
)


async def analyze_code_with_gpt(combined_code: str,
                                candidate_level: str,
                                assignment_description: str) -> dict[str, str]:
    """Analyzes code using OpenAI GPT API.
    :param combined_code: Combined code from all GitHub files.
    :param candidate_level: Level of candidate (Junior, Middle, Senior)
    :param assignment_description
    :return: Result of analyze in format dictionary {'downsides': ..., 'rating': ..., 'conclusion': ...}
    """
    prompt: str = PROMPT_FOR_ANALYZE_CODE.format(
        combined_code=combined_code,
        candidate_level=candidate_level,
        assignment_description=assignment_description,
        )
    try:
        completion: ChatCompletion = await client.chat.completions.create(
        model='gpt-3.5-turbo',
        messages=[
            {'role': 'system', 'content': 'You are an expert code reviewer.'},
            {'role': 'user', 'content': prompt},
            ],
        )

        review: str | None = completion.choices[0].message.content  # All code review from ChatGPT
        logger.info(f'GPT response: {review}')

        # print(review)
        # print(parse_review_result(review))
        return formatting_review_result(review)
    except Exception as e:
        logger.error(f'ChatGPT API error: {e}')
        raise HTTPException(status_code=500, detail=f'ChatGPT API error: {e}') from e


def formatting_review_result(review: str) -> dict[str, str]:
    """Formats review result from string format to dictionary with key and value when received by OpenAI API.
    :param review: Analyze by OpenAI API.
    :return: Formatted structured data.
    """
    return {
        'downsides_comments': divides_review_result(review, 'Downsides/Comments'),
        'rating': divides_review_result(review, 'Rating'),
        'conclusion': divides_review_result(review, 'Conclusion'),
    }


def divides_review_result(text: str, section_name: str) -> str:
    """Divides review result by ChatGPT into section content. Use regular functions.
    :param text: Full review result by ChatGPT.
    :param section_name: Name section to find.
    :return: Sections content.
    """
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
