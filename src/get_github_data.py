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
