from github import Github, GithubException
import json
import hashlib
with open('./static_files/token.json', 'r')as github_config:
    github_config = json.load(github_config)
github = Github(login_or_token=github_config['token'])
github_user = github.get_user()
github_repo = github_user.get_repo(github_config['repo'])

# uploaded_files = []
# for x in github_repo.get_contents(""):
#     print((str(x).replace('ContentFile(path="', '').replace('")', '')))
#     uploaded_files.append(x)


# def github_upload(file_name, file_data):
#     try:
#         if file_name not in uploaded_files:
#             res = github_repo.create_file(
#                 file_name+".png", 'upload file', file_data, 'main')
#             return res
#         else:
#             raise
#     except:
#         try:
#             res = github_repo.create_file(
#                 file_name.split('.')[0]+hashlib.md5(file_data).hexdigest()[:10]+'.png', 'upload file', file_data, 'main')
#             return res
#         except GithubException as exception:
#             if r"Invalid request.\n\n\"sha\" wasn't supplied." in str(exception):
#                 return {"ERROR": "FILE EXISTED"}
#             else:
#                 return str(exception)


class github_uploader():
    def __init__(self):
        self.this = Github(login_or_token=github_config['token'])
        self.github_user = github.get_user()
        self.github_repo = github_user.get_repo(github_config['repo'])

    def upload(self, file_name, file_data):
        try:
            res = github_repo.create_file(
                file_name.split('.')[0]+hashlib.md5(file_data).hexdigest()[:4]+'.png', 'upload file', file_data, 'main')
            return res
        except GithubException as exception:
            if r"Invalid request.\n\n\"sha\" wasn't supplied." in str(exception):
                return {"message": "file exists"}
            else:
                return str(exception)


github_upload = github_uploader()
