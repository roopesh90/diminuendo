import tornado.ioloop
import tornado.web

from base import BaseHandler
import string
import random
import sqlite3

from settings import SETTINGS as dummySettings
import logging as logger
import tornado.httpclient as httpclient
from bs4 import BeautifulSoup
import datetime

print(dummySettings['DBPATH'])

def _execute(query, fetchall=True):
    """Single method to execute all sql queries
    """
    connection = sqlite3.connect(dummySettings['DBPATH'])
    cursorobj = connection.cursor()
    try:
        cursorobj.execute(query)
        if fetchall==True:
            result = cursorobj.fetchall()
        else:
            result = cursorobj.fetchone()
        connection.commit()
    except Exception:
        raise
    connection.close()
    return result

def get_url_title(url):
    """To fetch title of page
    """
    http_client = httpclient.HTTPClient()
    try:
        response = http_client.fetch(url)
        soup = BeautifulSoup(response.body, 'html.parser')
        title = soup.title.string
    except httpclient.HTTPError as e:
        # HTTPError is raised for non-200 responses; the response
        # can be found in e.response.
        msg = "something went wrong: %s" % str(e)
        logger.info(msg)
        title = 0
    except Exception as e:
        # Other errors are possible, such as IOError.
        msg = "something went wrong: %s" % str(e)
        logger.info(msg)
        title = 0
    http_client.close()
    return title

def update_url_title(url=None,row=None):
    """To update title of page in db
    """
    try:
        if row==None or url==None:
            msg = "row to update title is not existant"
            logger.info(msg) 
        else:
            title = get_url_title(url)
            updated_at = datetime.datetime.now()
            query = ''' update urlsbase
                        set title = '%s', updated_at = '%s' where id = %d ''' % (title, updated_at, row);
            _execute(query)
    except Exception as e:
        msg = "something went wrong: %s" % e
        logger.info(msg)

def check_url_existence(url=None, url_hash=None):
    """To if url hash already generated
    """
    try:
        if url!=None:
            query = '''select * from urlsbase WHERE url like '%s' ''' % (url);
        elif url_hash!=None:
            query = '''select * from urlsbase WHERE shrink like '%s' ''' % (url_hash);
        else:
            return None
            
        row = _execute(query, False)
        if row!= None:
            return row
    except Exception as e:
        msg = "something went wrong: %s" % e
        logger.info(msg)
        return None

def update_url_hit(row=None):
    """To update hit count on url
    """
    pass

class MainHandler(BaseHandler):
    def get(self):
        self.response["message"] = "Yo, short url needed"
        self.write_json()

class RedirectHandler(BaseHandler):
    @tornado.web.asynchronous
    def get(self, url_hash):
        """Redirect to url
        """
        if url_hash==None:
            self.redirect("/")
        else:
            row = check_url_existence(None,url_hash)
            self.redirect(row[1])
        return
            
    
class URLshrinkHandler(BaseHandler):
    @tornado.web.asynchronous
    def post(self):
        try:
            url = self.get_json_argument('u')
            row = check_url_existence(url)
            #check url existence and generate hash and insert to db
            if row == None:
                url_hash = self.create_hash()
                created_at = datetime.datetime.now()
                updated_at = datetime.datetime.now()
                lasthit_at = datetime.datetime.now()
                # marks = int(self.get_argument("marks"))
                # name = self.get_argument("name")
                query = ''' insert into urlsbase
                            (url, shrink, created_at, updated_at, lasthit_at) values 
                            ('%s', '%s', '%s', '%s', '%s') ''' % (url, url_hash, created_at, updated_at, lasthit_at);
                _execute(query)
            else:
                
                url_hash = row[3]
                url = row[1]
                created_at = row[5]
                updated_at = row[6]
                lasthit_at = row[7]
            
            print(vars(self.request))
            short_url =("%s://%s/%s" %           (self.request.protocol, self.request.host,url_hash)) 
            self.response['url'] = url
            self.response['short_url'] = short_url
            self.response['created_at'] = str(created_at)
            self.response['updated_at'] = str(updated_at)
            self.response['lasthit_at'] = str(lasthit_at)
            self.write_json()
            self.finish()
            
            if row == None:
                #get title and update row
                query = '''select id from urlsbase WHERE shrink = '%s' ''' % (url_hash);
                row = _execute(query, False)
                if row!= None:
                    update_url_title(url,row[0])
            
        except Exception as e:
            msg = "something went wrong: %s" % e
            logger.info(msg)
            if not self._finished:
                #if the connection is closed, it won't call this function
                self.send_error(400, message="something went wrong") # Bad Request
            else:
                pass

    def create_hash(self):
        _hash = ''.join(random.choice(string.ascii_lowercase +string.ascii_uppercase + string.digits) for _ in range(5))
        print(_hash)
        return _hash