import tornado.ioloop
import tornado.web
import tornado.httpserver
from tornado.options import options

from settings import SETTINGS
from urls import URL_PATTERNS

class DiminuendoApp(tornado.web.Application):
    def __init__(self):
        tornado.web.Application.__init__(self, URL_PATTERNS, **SETTINGS)

def main():
    app = DiminuendoApp()
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()
