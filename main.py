from gov_changelog_action.src.get_github_data import (
    get_inputs,
)
from gov_changelog_action.src.create_changelog import (
    make_changelog,
)
from github import Github
import yaml


def main():
    with open("changelog-config.yml") as f:
        config = yaml.load(f, Loader=yaml.FullLoader)

    access_token = get_inputs("ACCESS_TOKEN")
    branch = get_inputs("BRANCH")
    path = get_inputs("PATH")
    commit_message = get_inputs("COMMIT_MESSAGE")
    num_releases = get_inputs("RELEASE_COUNT")
    include_unreleased = get_inputs("UNRELEASED_COMMITS")

    g = Github(access_token)
    repo = g.get_repo("joshlynchONS/gov-changelog-action")

    make_changelog(
        repo, config, branch, path, commit_message, num_releases, include_unreleased
    )


if __name__ == "__main__":
    main()
