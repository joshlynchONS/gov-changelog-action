import os
from jinja2 import Environment, FileSystemLoader


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


def get_commits(repo, branch):
    # function because will add try and except in case of no commits
    commits = repo.get_commits(sha=branch)
    return commits


def separate_commits(tags_sha_dict, commits):
    release_commits_dict = {}
    inv_tags_sha_dict = {}
    for k, v in tags_sha_dict.items():
        inv_tags_sha_dict[v] = k
        release_commits_dict[k] = []

    for commit in commits:
        if commit.sha in inv_tags_sha_dict:
            tag = inv_tags_sha_dict[commit.sha]
            release_commits_dict[tag].append(commit)

    return release_commits_dict


def create_changelog(repo, path, commit_message, branch):
    environment = Environment(loader=FileSystemLoader("src/"))
    template = environment.get_template("template.txt")

    releases = ["v0.0.1"]
    commits = [{"prefix": "added", "message": "commit message test"}]

    content = template.render(releases=releases, prefixes=["added"], commits=commits)
    print(path)
    print(commit_message)
    print(content)
    repo.create_file(
        path,
        commit_message,
        content,
    )
