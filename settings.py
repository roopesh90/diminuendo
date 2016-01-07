"""
    Settings for the app
"""
import logging as logger
import os

import tornado
import tornado.log
from tornado.options import define, options

# Make filepaths relative to settings.
PATH = lambda root, *a: os.path.join(root, *a)
ROOT = os.path.dirname(os.path.abspath(__file__))

##Port Details will be provided by commandline parameters using supervisor
__PORT = int(os.environ.get("PORT", 8888))
define("port", default=__PORT, help="run on the given port", type=int)
options.parse_command_line()

SETTINGS = {}

define("SERVER", default="diminuendo")
DEPLOYMENT = "development"
#enabled debug, auto reload and trace back
SETTINGS['debug'] = True
SETTINGS['serve_traceback'] = True
SETTINGS['logging'] = "debug"

#SQLite db path
DBNAME = "db/diminuendo.db"
SETTINGS['DBPATH'] = PATH(ROOT, DBNAME)

# Curret configuration details displayed
logger.info("\n\n\tDiminuendo - URL shortener API")
logger.info("Spinning up @ port "+ str(options.port) + "\n")
logger.info("INITIAL SETTINGS: \n")
logger.info("Deployment type:     "+DEPLOYMENT)
logger.info("HTTP server name:    "+tornado.options.options.SERVER)
logger.info("SQLite DB path:      "+SETTINGS['DBPATH']+"\n")
