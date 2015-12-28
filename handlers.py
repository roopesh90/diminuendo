import tornado.ioloop
import tornado.web

from base import BaseHandler
import string
import random
import sqlite3
from settings import SETTINGS as dummySettings

def _execute(query):
    connection = sqlite.connect(dummySettings['DBPATH'])
    cursorobj = connection.cursor()
    try:
        cursorobj.execute(query)
        result = cursorobj.fetchall()
        connection.commit()
    except Exception:
        raise
    connection.close()
    return result

class MainHandler(BaseHandler):
    def get(self):
        self.response["message"] = "Yo"
        self.write_json()
    
class URLshrinkHandler(BaseHandler):
    def post(self):
        url = self.get_json_argument('u')
        print(self.request.body)
        print(url)
        self.create_hash()
        self.write_json()

    def create_hash(self):
        _hash = ''.join(random.choice(string.ascii_lowercase +string.ascii_uppercase + string.digits) for _ in range(5))
        print(_hash)
        return _hash
