import os
import tornado.web
from handlers import MainHandler, URLshrinkHandler, RedirectHandler

PATH = lambda root, *a: os.path.join(root, *a)
ROOT = os.path.dirname(os.path.abspath(__file__))

URL_PATTERNS = [
    (r"/shrink/", URLshrinkHandler),
    (r"/", MainHandler),
    (r"/([a-zA-Z0-9\/]+)*", RedirectHandler),
]
