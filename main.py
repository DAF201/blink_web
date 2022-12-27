import tornado.web
import tornado.ioloop
import tornado.httpserver
from src.static_file import *
from src.config import *
from src.page_loader import *
from src.pages import *
from src.shell import *


def render(self, template_name, **kwargs):
    # just to make my life easier
    with static_files(STATIC_HTML)as static_htmls:
        self.write(static_htmls.__get_file__(template_name))


tornado.web.RequestHandler.render = render


class home_page(tornado.web.RequestHandler):
    def get(self):
        self.render(HOME_PAGE)

    def post(self):
        self.write('Nothing here to post!')


def main():
    application = tornado.web.Application([
        (r'/', home_page),
        (r'/favico', favicon),
        (r'/scripts(.*)', script_loader),
        (r'/css(.*)', style_sheet_loader),
        (r'/login', login_page),
        (r'/shell(.*)', shell)
    ])
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(PORT)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == '__main__':
    main()
