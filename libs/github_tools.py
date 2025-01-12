from github import Github


class github_tool:
    g: Github
    u: any

    def __init__(self, path):
        with open(path, "r") as f:
            self.g = Github(f.read())
        self.u = self.g.get_user()

    @staticmethod
    def upload(file_data, repo, branch="main", file_name=""):
        r = github_tool.g.get_repo(repo)

    @staticmethod
    def download(repo, branch="main", file_name=""):
        r = github_tool.g.get_repo(repo)
