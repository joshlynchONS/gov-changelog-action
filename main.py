from get_github_data import (
    get_inputs,
    get_commits,
    get_tags_sha_dict,
    get_releases,
)
from manip_data import (
    update_commits,
    update_release_prefixes,
    get_prefixes,
)
from create_changelog import (
    create_changelog_text,
    update_changelog,
)
from github import Github
import yaml

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

tags_sha = get_tags_sha_dict(repo)
commits = get_commits(repo, branch)
commits = update_commits(tags_sha, commits, include_unreleased)
prefixes = get_prefixes(config)
releases = get_releases(repo, num_releases, include_unreleased)
releases = update_release_prefixes(releases, commits, prefixes)
changelog_content = create_changelog_text(releases, commits)
update_changelog(repo, path, commit_message, changelog_content)
