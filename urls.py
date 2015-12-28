import os
import tornado.web
from handlers import MainHandler, URLshrinkHandler, RedirectHandler, TitleSearchHandler

PATH = lambda root, *a: os.path.join(root, *a)
ROOT = os.path.dirname(os.path.abspath(__file__))

URL_PATTERNS = [
    (r"/shrink/", URLshrinkHandler),
    (r"/s/", TitleSearchHandler),
    (r"/", MainHandler),
    (r"/([a-zA-Z0-9\/]+)*", RedirectHandler),
]
