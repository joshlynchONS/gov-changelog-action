import github

g = github.Github("${{secrets.GITHUB_TOKEN}}")
print("got g")
user = g.get_user()
print(user.name)
