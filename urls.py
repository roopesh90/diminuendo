import os
from handlers import MainHandler, URLshrinkHandler, RedirectHandler, TitleSearchHandler, URLMetaListHandler, URLMetaHandler

PATH = lambda root, *a: os.path.join(root, *a)
ROOT = os.path.dirname(os.path.abspath(__file__))

URL_PATTERNS = [
    (r"/shrink/", URLshrinkHandler),
    (r"/s/", TitleSearchHandler),
    (r"/meta/", URLMetaListHandler),
    (r"/meta/([a-zA-Z0-9\/]+)*", URLMetaHandler),
    (r"/", MainHandler),
    (r"/([a-zA-Z0-9\/]+)*", RedirectHandler),
]
