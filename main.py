from gov_changelog_action.src.get_github_data import (
    get_inputs,
)
from gov_changelog_action.src.create_changelog import (
    make_changelog,
)
from github import Github
import yaml
import os


def main():
    print(os.path.dirname(os.path.realpath(__file__)))
    with open("/changelog-config.yml") as f:
        config = yaml.load(f, Loader=yaml.FullLoader)

    access_token = get_inputs("ACCESS_TOKEN")
    branch = get_inputs("BRANCH")
    path = get_inputs("PATH")
    commit_message = get_inputs("COMMIT_MESSAGE")
    include_unreleased = get_inputs("UNRELEASED_COMMITS")
    repo_name = get_inputs("REPO_NAME")

    if repo_name == "":
        repo_name = get_inputs("REPOSITORY", "GITHUB")

    g = Github(access_token)
    repo = g.get_repo(repo_name)

    make_changelog(repo, config, branch, path, commit_message, include_unreleased)


if __name__ == "__main__":
    main()
