from jinja2 import Environment, FileSystemLoader
from gov_changelog_action.src.get_github_data import (
    get_tags_sha_dict,
    get_commits,
    get_releases,
)
from gov_changelog_action.src.manip_data import (
    update_commits,
    get_prefixes,
    update_release_prefixes,
)


def create_changelog_text(releases, commits):
    """Create changelog content using a jinja2 template

    Parameters
    ----------
    releases : list[str]
        List of all unique releases
    commits : list[class Commit]
        List of all the commits

    Returns
    -------
    str
        The content of the changelog as a string
    """
    environment = Environment(loader=FileSystemLoader(""))
    template = environment.get_template("template.txt")
    content = template.render(releases=releases, commits=commits)
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
    repo.create_file(path, commit_message, content)
    print("CREATE CHANGELOG")


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


def make_changelog(
    repo, config, branch, path, commit_message, num_releases, include_unreleased
):
    """Create or update a changelog in the users repository

    Parameters
    ----------
    repo : Github.repo
        The github repository
    config : dict (json/yml format)
        A dictionary config containing all the prefixes
    branch : str
        The name of the branch to push the changelog
    path : str
        The file path to create/update the changelog
    commit_message : str
        The commit message for the github action
    num_releases : str
        An intereger number of releases to regenerate
    include_unreleased : str
        Boolean variable whether to include unreleased commits
    """
    tags_sha = get_tags_sha_dict(repo)
    commits = get_commits(repo, branch)
    commits = update_commits(tags_sha, commits, include_unreleased)
    prefixes = get_prefixes(config)
    releases = get_releases(repo, num_releases, include_unreleased)
    releases = update_release_prefixes(releases, commits, prefixes)
    changelog_content = create_changelog_text(releases, commits)

    update_changelog(repo, path, commit_message, changelog_content)
