import tornado.web
from tornado_http_auth import DigestAuthMixin, auth_required
import hashlib
import time
import random
from src.config import *
from src.static_file import *
from src.github_upload import *


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
            new_cookie = hashlib.sha256(
                bytes(int(time.time()))+b'shio').hexdigest()
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
                random.Random(time.time())
                music_title = random.choice(
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
                random.Random(time.time())
                music_title = random.choice(
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
    def post(self):
        # this is a list
        print(self.request.files.get('file')[0]['body'])
        print(self.request.arguments)

        pass
