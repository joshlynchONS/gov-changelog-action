from github import Github
import os


def get_inputs(input_name: str, prefix="INPUT") -> str:
    """
    Get a Github actions input by name

    Args:
        input_name (str): input_name in workflow file.
        prefix (str, optional): prefix of input variable. Defaults to 'INPUT'.

    Returns:
        str: action_input

    References
    ----------
    [1] https://help.github.com/en/actions/automating-your-workflow-with-github-
    actions/metadata-syntax-for-github-actions#example
    """
    return os.getenv(prefix + "_{}".format(input_name).upper())


access_token = get_inputs("ACCESS_TOKEN")
branch = "main"

g = Github(access_token)
print("got g")
repo = g.get_repo("joshlynchONS/gov-changelog-action")
print(repo)
releases = repo.get_releases()
print(releases)
tags = repo.get_tags()
print(tags)
commits = repo.get_commits(sha=branch)
for commit in commits:
    message = commit.commit.message.split("\n\n")
    print(message)
