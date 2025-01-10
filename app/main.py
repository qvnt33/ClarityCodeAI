import json
import logging
import logging.config

from fastapi import FastAPI
from pydantic import BaseModel, Field

from app.utils.chatgpt_client import get_chatgpt_response

# Logger configuration
with open('logging.conf') as file:
    logging_config = json.load(file)
logging.config.dictConfig(logging_config)

# Create logger
logger: logging.Logger = logging.getLogger(__name__)

app = FastAPI()


class AssignmentRequest(BaseModel):
    assignment_description: str = Field(description='Description of the coding assignment')
    github_repo_url: str = Field(description='URL of the GitHub repository to review')
    candidate_level: str = Field(description='Junior, Middle or Senior')


# Rout for processing POST request
@app.post('/review-assignment')
async def review_assignment(request: AssignmentRequest) -> str:
    assignment_description = request.assignment_description
    github_repo_url = request.github_repo_url
    candidate_level = request. candidate_level

    result = await get_chatgpt_response('як тебе звати?')

    return result
