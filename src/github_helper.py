from github import Github, GithubException
from json import load
from hashlib import md5
from src.tools import blink_in_decode
from requests import get

with open('./static_files/token.json', 'r')as github_config:
    github_config = load(github_config)
github = Github(login_or_token=github_config['token'])
github_user = github.get_user()
github_repo = github_user.get_repo(github_config['repo'])


class github_helper():
    def __init__(self):
        self.this = Github(login_or_token=github_config['token'])
        self.github_user = github.get_user()
        self.github_repo = github_user.get_repo(github_config['repo'])

    def upload(self,  file_data):
        try:
            res = github_repo.create_file(md5(
                file_data).hexdigest()+'.png', 'upload file', file_data, 'main')
            return res
        except GithubException as exception:
            if r"Invalid request.\n\n\"sha\" wasn't supplied." in str(exception):
                return {'message': 'file already exists'}
            else:
                return {'message': str(exception)}

    def download(self, file_name):
        try:
            url = github_repo.get_contents(file_name).raw_data['download_url']
            raw_data = get(url=url).content
            return blink_in_decode(raw_data)
        except GithubException as exception:
            if '"message": "Not Found"' in str(exception):
                return {'message': 'file does not exist'}
            return {'message': 'file exists'}


git_helper = github_helper()
