import tornado.web
from tornado_http_auth import DigestAuthMixin, auth_required
from hashlib import sha256
from time import time
from random import Random, choice
from src.config import *
from src.static_file import *
from src.github_helper import *
from src.tools import *


class home_page(tornado.web.RequestHandler):
    def get(self):
        self.render(HOME_PAGE)

    def post(self):
        self.write('Nothing here to post!')


class login_page(tornado.web.RequestHandler, DigestAuthMixin):
    @auth_required(realm='Protected', auth_func=credentials.get)
    def get(self):
        if not self.get_cookie('auth'):
            # 'shio' means salt
            new_cookie = sha256(
                bytes(int(time()))+b'shio').hexdigest()
            # I don't think it can last 10 years
            self.set_cookie('auth', new_cookie, expires_days=365*10)
            cookie_data.append(new_cookie)
            with open(COOKIE_DATA_BASE, 'w')as cookie_data_base:
                json.dump(cookie_data, cookie_data_base)
        else:
            if self.get_cookie('auth') not in cookie_data:
                return
        self.render(LOGIN_PAGE)


class music_playing(tornado.web.RequestHandler):
    def get(self, *keys):
        music = self.get_argument('music')
        if music == 'random':
            with static_files(MUSIC_PLAYLIST) as music_playlist:
                Random(time())
                music_title = choice(
                    list(music_playlist.__get_raw_list__().keys()))
                self.write(music_playlist.__get_file__(music_title))
            return
        if music == 'get_list':
            with static_files(MUSIC_PLAYLIST) as music_playlist:
                self.write(json.dumps(music_playlist.__get_list__()))
            return
        with static_files(MUSIC_PLAYLIST) as music_playlist:
            self.write(music_playlist.__get_file__(music))


class video_playing(tornado.web.RequestHandler):
    def get(self, *keys):
        video = self.get_argument('video')
        if video == 'random':
            with static_files(VIDEO_PLAYLIST) as video_playlist:
                Random(time())
                music_title = choice(
                    list(video_playlist.__get_raw_list__().keys()))
                self.write(video_playlist.__get_file__(music_title))
            return
        if video == 'get_list':
            with static_files(VIDEO_PLAYLIST) as video_playlist:
                self.write(json.dumps(video_playlist.__get_list__()))
            return
        with static_files(VIDEO_PLAYLIST) as video_playlist:
            self.write(video_playlist.__get_file__(video))


class blink_in(tornado.web.RequestHandler):
    def get(self):
        raw_data = git_helper.download(self.get_argument('file')+'.png')
        self.write(raw_data)

    def post(self):
        file_data = self.request.files.get('file')[0]['body']
        upload_res = git_helper.upload(blink_in_encode(file_data))
        self.write(str(upload_res))
