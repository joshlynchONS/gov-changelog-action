from get_github_data import (
    get_inputs,
    get_commits,
    update_commits,
    get_tags_sha_dict,
    get_releases,
    get_prefixes,
    create_changelog_text,
    update_changelog,
)
from github import Github

access_token = get_inputs("ACCESS_TOKEN")
branch = "parse_commits"
path = "CHANGELOG.md"
commit_message = "docs(CHANGELOG): update release notes"

g = Github(access_token)
repo = g.get_repo("joshlynchONS/gov-changelog-action")

tags_sha = get_tags_sha_dict(repo)
commits = get_commits(repo, branch)
commits = update_commits(tags_sha, commits)
prefixes = get_prefixes(commits)
print(prefixes)
releases = get_releases(repo)
changelog_content = create_changelog_text(releases, prefixes, commits)
update_changelog(repo, path, commit_message, changelog_content)
