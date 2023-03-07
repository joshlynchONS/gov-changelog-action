import semantic_version
from gov_changelog_action.src.get_github_data import (
    get_releases,
    get_commits,
    get_tags_sha_dict,
)


def create_tag(repo, branch):
    print("CURRENT TAGS")
    releases = get_releases(repo, "false")
    recent_tag = releases[0].tag
    tags_sha_dict = get_tags_sha_dict(repo)
    print(tags_sha_dict)
    version = semantic_version.Version(recent_tag)
    version_bump, unreleased_sha = find_version_bump(repo, branch, tags_sha_dict)
    new_version = increase_version(version, version_bump)
    repo.create_git_tag(new_version, new_version, type="commit", object=unreleased_sha)
    print("before")
    repo.create_git_ref(str(version), unreleased_sha)
    print("CREATED TAG {}".format(new_version))
    print(get_tags_sha_dict(repo))


def find_version_bump(repo, branch, tags_sha_dict):
    inv_tags_sha_dict = {}
    for k, v in tags_sha_dict.items():
        inv_tags_sha_dict[v] = k

    commits = get_commits(repo, branch)
    current_bump = "none"

    for commit in commits:
        if commit.sha not in inv_tags_sha_dict:
            message = commit.commit.message.split("\n\n")[0]
            if "[" in message and "]" in message:
                split_message = message.split("[")[1]
                version_increase = split_message.split("]")[0]
                current_bump = return_max_version_bump(current_bump, version_increase)
                unreleased_sha = commit.sha

    if current_bump == "none":
        raise RuntimeError(
            "No new version bump was detected in any of the unreleased commits"
        )
    else:
        return current_bump, unreleased_sha


def return_max_version_bump(old_max, current_bump):
    new_max = old_max
    if current_bump in ["patch", "minor", "major"]:
        if old_max == "none" or old_max == "patch":
            new_max = current_bump
        elif old_max == "minor" and current_bump == "major":
            new_max = current_bump

    return new_max


def increase_version(current_version, version_bump):
    if version_bump == "patch":
        new_version = current_version.next_patch()
    elif version_bump == "minor":
        new_version = current_version.next_minor()
    elif version_bump == "major":
        new_version = current_version.next_major()
    else:
        raise ValueError(
            "The version bump specified does not match the "
            "correct semantic version specifications"
        )
    return str(new_version)
