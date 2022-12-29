from github import Github
with open('./static_files/github_token', 'r')as token:
    token = token.read()
g = Github(login_or_token=token)
user = g.get_user()
print(user)
login = user.login
print(user)
print(login)
