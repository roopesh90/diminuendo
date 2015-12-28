import tornado.ioloop
import tornado.web
import tornado.httpserver
from tornado.options import options

from settings import SETTINGS
from urls import URL_PATTERNS
import sqlite3

class DiminuendoApp(tornado.web.Application):
    def __init__(self):
        tornado.web.Application.__init__(self, URL_PATTERNS, **SETTINGS)

def dbSeeder():
    """Db seeder and verifier
    """
    connection = sqlite3.connect(SETTINGS['DBPATH'])
    cursorobj = connection.cursor()
    try:
        cursorobj.execute('SELECT * FROM urlsbase')
        print('Table already exists')
    except:
        print('Creating table \'urlsbase\'')
        cursorobj.execute('CREATE TABLE urlsbase (\
            id INTEGER PRIMARY KEY   AUTOINCREMENT,\
            url TEXT,\
            title TEXT  DEFAULT "",\
            shrink TEXT,\
            hits INTEGER  DEFAULT 0,\
            created_at TIMESTAMP,\
            updated_at TIMESTAMP,\
            lasthit_at TIMESTAMP)')
        print('Successfully created table \'urlsbase\'')
    connection.commit()
    connection.close()
    
def main():
    # Verify the database exists and has the correct layout
    dbSeeder()
    
    app = DiminuendoApp()
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()
