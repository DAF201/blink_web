import tornado.web
from src.config import STATIC_JS, STATIC_CSS, STATIC_FILE, FAVICON
from src.static_file import *


class script_loader(tornado.web.RequestHandler):
    def get(self, *keys):
        script = self.get_argument('script')
        with static_files(STATIC_JS)as static_scripts:
            self.write(static_scripts.__get_file__(script))


class style_sheet_loader(tornado.web.RequestHandler):
    def get(self, *keys):
        css = self.get_argument('css')
        with static_files(STATIC_CSS)as static_style_sheet:
            self.write(static_style_sheet.__get_file__(css))


class favicon(tornado.web.RequestHandler):
    def get(self):
        with static_files(STATIC_FILE)as static_file:
            self.write(static_file.__get_file__(FAVICON))

    def post(self):
        self.write('invaild method')
