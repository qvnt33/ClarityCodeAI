from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()


class AssignmentRequest(BaseModel):
    assignment_description: str = Field(description='Description of the coding assignment')
    github_repo_url: str = Field(description='URL of the GitHub repository to review')
    candidate_level: str = Field(description='Junior, Middle or Senior')


# Rout for processing POST request
@app.post('/review-assignment')
async def review_assignment(request: AssignmentRequest) -> list:
    assignment_description = request.assignment_description
    github_repo_url = request.github_repo_url
    candidate_level = request. candidate_level

    result = [assignment_description, github_repo_url, candidate_level]

    return result
