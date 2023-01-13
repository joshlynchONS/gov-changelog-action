from get_github_data import (
    get_inputs,
    get_commits,
    separate_commits,
    create_changelog,
)
from github import Github

access_token = get_inputs("ACCESS_TOKEN")
branch = "main"

g = Github(access_token)
repo = g.get_repo("joshlynchONS/gov-changelog-action")
releases = repo.get_releases()
tags = repo.get_tags()
tags_sha = {}
for tag in tags:
    tags_sha[tag.name] = tag.commit.sha

releases = repo.get_releases()
regenerate_releases = [r.tag_name for r in releases]
commits = get_commits(repo, branch)
path = "CHANGELOG.md"
commit_message = "docs: create changelog"

print(releases)
print(regenerate_releases)
print(tags)
print(tags_sha)
for commit in commits:
    print(commit)
    message = commit.commit.message.split("\n\n")
    print(message)

commits_dict = separate_commits(tags_sha, commits)
print(commits_dict)

create_changelog(repo, path, commit_message, branch)
