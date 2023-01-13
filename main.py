from get_github_data import get_inputs
from github import Github

access_token = get_inputs("ACCESS_TOKEN")
branch = "main"

g = Github(access_token)
repo = g.get_repo("joshlynchONS/gov-changelog-action")
releases = repo.get_releases()
tags = repo.get_tags()

releases = repo.get_releases()
regenerate_releases = [r.tag_name for r in releases]

print(releases)
print(regenerate_releases)
