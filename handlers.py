import tornado.ioloop
import tornado.web

from base import BaseHandler

class MainHandler(BaseHandler):
    def get(self):
        self.response["message"] = "Yo"
        self.write_json()
