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

    if unreleased_bool == "true":
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


def update_release_prefixes(releases, commits, prefixes):
    """Creates a list of prefixes within the release class to be used
    within the template

    Parameters
    ----------
    releases : list[class Release]
        List of releases
    commits : list[class Commit]
        List of commits
    """
    prefix_dict = {prefix.prefix: prefix for prefix in prefixes}
    updated_releases = []
    for release in releases:
        for commit in commits:
            if (commit.release == release.tag) and (commit.prefix in prefix_dict):
                release.update_prefixes(prefix_dict[commit.prefix])
        updated_releases.append(release)

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
