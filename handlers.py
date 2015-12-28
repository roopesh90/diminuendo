import tornado.ioloop
import tornado.web

from base import BaseHandler
import string
import random

class MainHandler(BaseHandler):
    def get(self):
        self.response["message"] = "Yo"
        self.write_json()


class URLshrinkHandler(BaseHandler):
    def post(self):
        url = self.get_json_argument('u')
        print(self.request.body)
        print(a)
        # self.response['hash'] = self.create_hash()
        self.create_hash()
        self.write_json()

    def create_hash(self):
        _hash = ''.join(random.choice(string.ascii_lowercase +string.ascii_uppercase + string.digits) for _ in range(5))
        print(_hash)
        return _hash
