from src.tools import *
from github import Github
import base64
import requests

# with open("test.py", 'rb')as test_file:
#     test_file = test_file.read()
# re = requests.post("http://127.0.0.1/APIs/blink_in",
#                    files={'file': test_file})
# print(re.text)

re = requests.get("http://127.0.0.1/APIs/blink_in",
                  params={'file': '49e7d58783980862ae84bcd1580aa02a.png'})
print(re.content)

# git = Github(login_or_token='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')
# user = git.get_user()
# repo = user.get_repo('blink_in_inventory')
# data = base64.b64decode(repo.get_contents(
#     '49e7d58783980862ae84bcd1580aa02a.png').raw_data['content'])
# print(data)
# with open('test.txt', 'wb')as test:
#     test.write(blink_in_decode(data))
