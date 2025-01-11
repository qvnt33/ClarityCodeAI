import json
import logging
import logging.config

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from app.tools.chatgpt_client import analyze_code_with_gpt
from app.tools.github_client import get_github_files
from app.tools.tools import combines_github_files, prepare_code_for_analysis

# Logger configuration
with open('logging.conf') as file:
    logging_config = json.load(file)
logging.config.dictConfig(logging_config)

# Create logger
logger: logging.Logger = logging.getLogger(__name__)

app = FastAPI()


class AssignmentRequest(BaseModel):
    assignment_description: str = Field(description='Description of the coding assignment.')
    github_repo_url: str = Field(description='URL of the GitHub repository to review.')
    candidate_level: str = Field(description='Junior, Middle or Senior.')


class ReviewResponse(BaseModel):
    downsides_comments: str = Field(description='All downsides comments from ChatGPT.')
    rating: str = Field(description='Score of code from ChatGPT. Format: Score/10.')
    conclusion: str = Field(description='Final conclusion of project from ChatGPT.')
    file_list: str = Field(description='Joined list of files from GitHub API.')


@app.post('/review-assignment', response_model=ReviewResponse)
async def review_assignment(request: AssignmentRequest) -> dict[str, str]:
    """Rout for processing POST request"""
    try:
        assignment_description: str = request.assignment_description
        github_repo_url: str = request.github_repo_url
        candidate_level: str = request.candidate_level

        logger.info(f'Received assignment: {assignment_description}, '
                    f'Repo URL: {github_repo_url}, '
                    f'Level: {candidate_level}')

        github_files: list[dict[str, str]] = await get_github_files(github_repo_url)  # GitHub files with their contents
        combined_code: str = prepare_code_for_analysis(github_files)  # Combined code

        # GPT code analysis
        try:
            result: dict[str, str] = await analyze_code_with_gpt(
                combined_code=combined_code,
                candidate_level=candidate_level,
                assignment_description=assignment_description,
            )
            logger.info('ChatGPT response received successfully.')
        except Exception as e:
            logger.error(f'GPT API error: {e}')
            raise HTTPException(status_code=500, detail=f'GPT API error: {str(e)}') from e

        # Add list of files to result
        file_list: str = combines_github_files(github_files)  # String of joined GitHub files
        result['file_list'] = file_list

        return result
    except Exception as e:
        logger.error(f'review-assignment error: {e}')
        raise HTTPException(status_code=500, detail=f'review-assignment error: {e}') from e
