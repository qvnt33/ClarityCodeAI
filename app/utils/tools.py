def combines_github_files(github_files: list[dict]) -> str:
    """Returns combined list of files from GitHub API.
    :param github_files: GitHub files with their contents.
    :return: List of files in format string.
    """
    file_list: list[str] = [f'- {file.get("path", "Unknown path")}' for file in github_files]
    return '\n'.join(file_list)


def prepare_code_for_analysis(files: list[dict]) -> str:
    """Combines code from all GitHub files in one text for handling to OpenAI API.
    :param files: List of files with their contents ({'name': str, 'path': str, 'content': str})
    :return: Combined code for analysis.
    """
    lst_combined_files = []

    for file in files:
        file_name: str = f'# File: {file.get('name', '')}'
        file_content: str | None = file.get('content', '')
        lst_combined_files.append('\n'.join([file_name, file_content]))

    return '\n\n'.join(lst_combined_files)
