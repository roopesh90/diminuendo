import os
import tornado.web
from handlers import MainHandler

PATH = lambda root, *a: os.path.join(root, *a)
ROOT = os.path.dirname(os.path.abspath(__file__))

URL_PATTERNS = [
    (r"/", MainHandler),
]
