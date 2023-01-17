from get_github_data import get_inputs, get_commits, separate_commits
from github import Github

access_token = get_inputs("ACCESS_TOKEN")
branch = "first_action"
path = "CHANGELOG.md"
commit_message = "docs(CHANGELOG): update release notes"

g = Github(access_token)
repo = g.get_repo("joshlynchONS/gov-changelog-action")
releases = repo.get_releases()
tags = repo.get_tags()
tags_sha = {}
commits = get_commits(repo, branch)


for tag in tags:
    tags_sha[tag.name] = tag.commit.sha

for commit in commits:
    print(commit)
    message = commit.commit.message.split("\n\n")
    print(message)

commits_dict = separate_commits(tags_sha, commits)
print(commits_dict)

releases = repo.get_releases()
regenerate_releases = [r.tag_name for r in releases]
