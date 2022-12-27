import os
import json

credentials = {'admin': 'admin'}


STATIC_HTML = os.getcwd()+'\\static_htmls\\'
STATIC_FILE = os.getcwd()+'\\static_files\\'
STATIC_JS = os.getcwd()+'\\static_js\\'
STATIC_CSS = os.getcwd()+'\\static_css\\'
COOKIE_DATA_BASE = os.getcwd()+"\\db\\cookie.json"


with open(COOKIE_DATA_BASE)as cookie_db:
    cookie_data = json.load(cookie_db)


PORT = 80

FAVICON = 'favicon.ico'
HOME_PAGE = 'home.html'
LOGIN_PAGE = 'login.html'

GITHUB_TOKEN = ''
GITHUB_REPO_ADDRESS = ''
