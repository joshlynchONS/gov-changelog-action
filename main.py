from gov_changelog_action.src.get_github_data import (
    get_inputs,
)
from gov_changelog_action.src.create_changelog import (
    make_changelog,
)
from gov_changelog_action.src.update_release import create_tag
from github import Github
import yaml


def main():
    print("STARTING PROCESS")

    with open("/changelog-config.yml") as f:
        config = yaml.load(f, Loader=yaml.FullLoader)

    access_token = get_inputs("ACCESS_TOKEN")
    branch = get_inputs("BRANCH")
    path = get_inputs("PATH")
    commit_message = get_inputs("COMMIT_MESSAGE")
    include_unreleased = get_inputs("UNRELEASED_COMMITS")
    repo_name = get_inputs("REPO_NAME")
    update_changelog = get_inputs("UPDATE_CHANGELOG")
    create_tag_bool = get_inputs("CREATE_TAG")

    if repo_name == "":
        repo_name = get_inputs("REPOSITORY", "GITHUB")

    g = Github(access_token)
    repo = g.get_repo(repo_name)

    print("BEFORE IF STATEMENTS")

    if update_changelog == "true".lower():
        print("Updating changelog")
        make_changelog(repo, config, branch, path, commit_message, include_unreleased)

    if create_tag_bool == "true".lower():
        print("creating a new tag")
        create_tag(repo, branch)

    print("AFTER IF STATEMENTS")


if __name__ == "__main__":
    main()
