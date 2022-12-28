import tornado.web
import tornado.ioloop
import tornado.httpserver
from src.static_file import *
from src.config import *
from src.page_loader import *
from src.pages import *
from src.shell import *
from src.direct import direct


def render(self, template_name, **kwargs):
    # just to make my life easier
    with static_files(STATIC_HTML)as static_htmls:
        self.write(static_htmls.__get_file__(template_name))


tornado.web.RequestHandler.render = render


def main():
    application = tornado.web.Application(direct)
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(PORT)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == '__main__':
    main()
