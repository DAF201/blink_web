import tornado.web
from src.config import *
from tornado_http_auth import DigestAuthMixin, auth_required
import hashlib
import time


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
