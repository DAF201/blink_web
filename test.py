# from github import Github
# from json import load
# with open('./static_files/github_token.json', 'r')as github_config:
#     github_config = load(github_config)
# g = Github(login_or_token=github_config['token'])
# user = g.get_user()
# repo = user.get_repo(github_config['repo'])
# with open('test.png', 'rb')as test_File:
#     test_File = test_File.read()
# re = repo.create_file('test.png', 'test upload', test_File, "main")
# print(re)


import requests

with open("test.png", 'rb')as test_file:
    test_file = test_file.read()
re = requests.post("http://127.0.0.1/APIs/blink_in",
                   files={'file': test_file}, params={'file_name': 'test.png'})
