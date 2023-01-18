import os
from jinja2 import Environment, FileSystemLoader
from github import GithubObject


class Commit:
    def __init__(self, message, release):
        self.message = message
        self.prefix = "other"
        self.release = release
        self.find_prefix()

    def find_prefix(self):
        split_message = self.message.split(": ")
        if len(split_message) > 1:
            self.prefix = split_message[0]
            del split_message[0]
            self.message = "".join(split_message)


class Prefix:
    def __init__(self, prefix, heading, version_bump):
        self.prefix = prefix
        self.heading = heading
        self.version_bump = version_bump


class Release:
    def __init__(self, tag, date):
        self.tag = tag
        self.date = date


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
    commits = repo.get_commits(sha=branch)
    return commits


def get_tags_sha_dict(repo):
    """Creates a dictionary of tags with their respective sha str

    Parameters
    ----------
    repo : Github.repo
        Github repository

    Returns
    -------
    dict{tag -> str: sha -> str}
        _description_
    """
    tags = repo.get_tags()
    tags_sha = {}
    for tag in tags:
        tags_sha[tag.name] = tag.commit.sha
    return tags_sha


def update_commits(tags_sha_dict, commits, unreleased_bool):
    """Iterates through all commits and turns them into the updated class.
    The output is a list of the updated commits

    Parameters
    ----------
    tags_sha_dict : dict{tag -> str: sha -> str}
        dictionary of all tags with their respective sha string
    commits : list[Github.commit class]
        list of all GitHub commits
    unreleased_bool: bool
        boolean variable on whether to include unreleased commits

    Returns
    -------
    list[class Commit]
        list of the updated commits
    """
    updated_commits = []
    inv_tags_sha_dict = {}
    for k, v in tags_sha_dict.items():
        inv_tags_sha_dict[v] = k

    if unreleased_bool:
        current_release = "Unreleased"
    else:
        current_release = list(tags_sha_dict)[0]

    for commit in commits:
        if commit.sha in inv_tags_sha_dict:
            current_release = inv_tags_sha_dict[commit.sha]

        message = commit.commit.message.split("\n\n")[0]
        temp_commit = Commit(message, current_release)
        updated_commits.append(temp_commit)

    return updated_commits


def get_releases(repo, number_releases, unreleased_bool):
    """Get list of all releases within the repository

    Parameters
    ----------
    repo : Github.repo
        Github repository
    number_releases : int
        The number of releases to publish in the changelog
    unreleased_bool: bool
        boolean variable on whether to include unreleased commits

    Returns
    -------
    list[class Release]
        List of all releases from the github repository
    """
    releases = repo.get_releases()

    if int(number_releases) == -1:
        number_releases = releases.totalCount

    updated_releases = []

    if unreleased_bool:
        temp_release = Release("Unreleased", "")
        updated_releases.append(temp_release)

    for release_num in range(int(number_releases)):
        tag = releases[release_num].tag_name
        date = releases[release_num].created_at
        date = date.strftime("%Y-%m-%d")
        temp_release = Release(tag, date)
        updated_releases.append(temp_release)

    return updated_releases


def get_prefixes(config):
    """Get a list of unique prefixes and their respective changelog heading
    and version bump. This ignores any prefix that has the feature show set
    as false.

    Parameters
    ----------
    config : dict{prefix -> str: features -> dict}
        yaml config containing all the permitted prefixes and their features

    Returns
    -------
    list[class Prefix]
        List of all prefixes as a class
    """
    prefixes = config["prefixes"]
    unique_prefixes = []
    for prefix, features in prefixes.items():
        show = features["show"]
        if show:
            heading = features["heading"]
            version_bump = features["release"]
            temp_prefix = Prefix(prefix, heading, version_bump)
            unique_prefixes.append(temp_prefix)
    return unique_prefixes


def create_changelog_text(releases, prefixes, commits):
    """Create changelog content using a jinja2 template

    Parameters
    ----------
    releases : list[str]
        List of all unique releases
    prefixes : list[str]
        List of all unique prefixes
    commits : list[class Commit]
        List of all the commits

    Returns
    -------
    str
        The content of the changelog as a string
    """
    environment = Environment(loader=FileSystemLoader("src/"))
    template = environment.get_template("template.txt")
    content = template.render(releases=releases, prefixes=prefixes, commits=commits)
    return content


def create_changelog(repo, path, commit_message, content):
    """Creates a new changelog document in the users repository.
    To be used when no changelog exists

    Parameters
    ----------
    repo : Github.repo
        The GitHub repository
    path : str
        The desired path to the changelog
    commit_message : str
        The desired commit message for the workflow to use when creating the changelog
    content : str
        The contents of the changelog
    """
    repo.create_file(
        path, commit_message, content, GithubObject.NotSet, GithubObject.NotSet
    )


def update_changelog(repo, path, commit_message, content):
    """Updates an existing changelog document in the users repository
    To be used when a changelog exists

    Parameters
    ----------
    repo : Github.repo
        The GitHub repository
    path : str
        The desired path to the changelog
    commit_message : str
        The desired commit message for the workflow to use when creating the changelog
    content : str
        The contents of the changelog
    """
    current_changelog = repo.get_contents(path)
    sha = current_changelog.sha
    repo.update_file(path, commit_message, content, sha)
    print("UPDATE CHANGELOG")
