from jinja2 import Environment, FileSystemLoader


def create_changelog_text(releases, commits):
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
