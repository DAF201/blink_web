from github import Github
from json import load
from src.config import LOCAL_FILE_BUFFER


class github_uploader():
    def __init__(self):
        # I don't want to deal with super() things
        with open('./static_files/github_token.json', 'r')as github_config:
            self.github_config = load(github_config)
        self.this = Github(self.github_config['token'])
        self.user = self.this.get_user()
        self.repo = self.user.get_repo(self.github_config['repo'])

    def upload(self, local_file_name, message='upload file', branch='main'):
        try:
            with open(LOCAL_FILE_BUFFER+local_file_name, 'rb')as file_to_upload:
                return self.repo.create_file(local_file_name, message, file_to_upload.read(), branch)
        except Exception as e:
            return {"ERROR": e}
