import github

g = github.Github('${{secrets.GITHUB_TOKEN}}')
user = g.get_user()
print(user.name)
