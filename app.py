import tornado.ioloop
import tornado.web
import tornado.httpserver
from tornado.options import options

from settings import SETTINGS
from urls import URL_PATTERNS
import sqlite3
import logging as logger

class DiminuendoApp(tornado.web.Application):
    def __init__(self):
        tornado.web.Application.__init__(self, URL_PATTERNS, **SETTINGS)

def dbSeeder():
    """Db seeder and verifier
    """
    logger.info("Db seeder initiated")
    connection = sqlite3.connect(SETTINGS['DBPATH'])
    cursorobj = connection.cursor()
    basetbl="urlsbase"
    try:
        cursorobj.execute('SELECT * FROM %s' %(basetbl))
        logger.info("Table \'%s\' exists, table verified" %(basetbl))
        print('')
    except:
        logger.info("Creating table \'%s\'" %(basetbl))
        cursorobj.execute('CREATE TABLE %s (\
            id INTEGER PRIMARY KEY   AUTOINCREMENT,\
            url TEXT,\
            title TEXT  DEFAULT "",\
            shrink TEXT,\
            hits INTEGER  DEFAULT 0,\
            created_at TIMESTAMP,\
            updated_at TIMESTAMP,\
            lasthit_at TIMESTAMP)' %(basetbl) )
        logger.info("Successfully created table \'%s\'" %(basetbl))
    connection.commit()
    connection.close()
    logger.info("Seeder completed")
    
def main():
    # Verify the database exists and has the correct layout
    dbSeeder()
    
    app = DiminuendoApp()
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()
