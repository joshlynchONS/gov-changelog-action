import os


class Release:
    def __init__(self, tag, date):
        self.tag = tag
        self.date = date
        self.prefixes = []

    def update_prefixes(self, commit_prefix):
        if commit_prefix not in self.prefixes:
            self.prefixes.append(commit_prefix)


def get_inputs(input_name: str, prefix="INPUT") -> str:
    """Get a Github action's input by name

    Parameters
    ----------
    input_name : str
        Input name from workflow file.
    prefix : str, optional
        prefix of the input_name. Defaults to 'INPUT'

    Returns
    -------
    str
        The user input response
    """
    return os.getenv(prefix + "_{}".format(input_name).upper())


def get_commits(repo, branch):
    """Get all commits from the repository

    Parameters
    ----------
    repo : Github.repo
        The GitHub repository
    branch : str
        The repository branch

    Returns
    -------
    List[Github.commit]
        List of all github commits
    """
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
        Dictionary containing the repository tags with it's respective
        sha string
    """
    tags = repo.get_tags()
    tags_sha = {}
    for tag in tags:
        tags_sha[tag.name] = tag.commit.sha
    return tags_sha


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

    if unreleased_bool == "true":
        temp_release = Release("Unreleased", "")
        updated_releases.append(temp_release)

    for release_num in range(int(number_releases)):
        tag = releases[release_num].tag_name
        date = releases[release_num].created_at
        date = date.strftime("%Y-%m-%d")
        temp_release = Release(tag, date)
        updated_releases.append(temp_release)

    return updated_releases
