import os
import json

# loging page username and password
credentials = {'daf201': 'having a good time?'}

# static files folder
STATIC_HTML = os.getcwd()+'\\static_htmls\\'
STATIC_FILE = os.getcwd()+'\\static_files\\'
STATIC_JS = os.getcwd()+'\\static_js\\'
STATIC_CSS = os.getcwd()+'\\static_css\\'
MUSIC_PLAYLIST = os.getcwd()+'\\music_playlist\\'
VIDEO_PLAYLIST = os.getcwd()+'\\video_playlist\\'
FAVICON = 'favicon.ico'
HOME_PAGE = 'home.html'
LOGIN_PAGE = 'login.html'

# cookie database
COOKIE_DATA_BASE = os.getcwd()+'\\db\\cookie.json'
try:
    with open(COOKIE_DATA_BASE)as cookie_db:
        cookie_data = json.load(cookie_db)
except:
    cookie_data = []
    with open(COOKIE_DATA_BASE, 'w')as cookie_db:
        json.dump(cookie_data, cookie_db)

# port
PORT = 443

# storage
GITHUB_TOKEN = ''
GITHUB_REPO_ADDRESS = ''

CERTFILE = r'C:\Certbot\live\www.blink-in.com\fullchain.pem'
PRIVATE_KEY = r'C:\Certbot\live\www.blink-in.com\privkey.pem'
