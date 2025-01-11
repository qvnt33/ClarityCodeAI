# ruff: noqa: E501
import os

from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv(filename='.env'))

OPENAI_API_KEY: str | None = os.getenv('OPENAI_API_KEY')
GITHUB_TOKEN: str | None = os.getenv('GITHUB_TOKEN')

PROMPT_FOR_ANALYZE_CODE = """
Analyze the following code critically and provide constructive feedback. Be as honest and strict as possible in your evaluation, highlighting both strengths and weaknesses, even if they are significant. Adjust your evaluation based on the developer level (Junior, Middle, Senior) as follows:

- Junior: Focus on basic coding skills, such as syntax, organization, and simple functionality. Accept small mistakes but ensure the basics are solid.
- Middle: Expect intermediate-level knowledge, including modularity, error handling, and adherence to best practices. Highlight areas for improvement in maintainability and scalability.
- Senior: Require advanced skills, including scalability, optimization, and clean architecture. Highlight any gaps or areas where the code does not meet these high standards.

Use the following criteria to determine the rating:
- 1-4: Poor quality; major issues or missing key functionality.
- 5-7: Average quality; functional but needs significant improvement.
- 8-9: Good quality; meets most requirements with minor issues.
- 10: Excellent quality; exceeds expectations with no major flaws.

Provide feedback according to these points:

1. Downsides/Comments: List any potential issues, bugs, or bad practices in the code. Provide detailed feedback as a numbered list.

2. Rating: Provide the overall code quality as a single numerical value on a scale of 1 to 10, based on cleanliness, efficiency, readability, and alignment with the assignment. Respond with just the number (e.g., "8/10").

3. Conclusion: Summarize your overall impression of the code and its suitability for a {candidate_level} developer. Be critical and honest about whether the code meets the expected standard for this level. Provide this in one concise paragraph.

Respond strictly in the following structured format:

### Downsides/Comments:
<list of comments>

### Rating:
<number>/10

### Conclusion:
<summary paragraph>

Assignment Description: {assignment_description}

Here is the code:
{combined_code}
"""

REDIS_HOST = 'redis'
REDIS_PORT = 6379
