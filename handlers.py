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
import inspect

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
                        set title = '%s', updated_at = '%s' where id = %d ''' % (title, updated_at, row)
            _execute(query)
    except Exception as e:
        msg = "something went wrong: %s" % e
        logger.info(msg)

def check_url_existence(url=None, url_hash=None):
    """To if url hash already generated
    """
    try:
        if url!=None:
            query = '''select * from urlsbase WHERE url like '%s' ''' % (url)
        elif url_hash!=None:
            query = '''select * from urlsbase WHERE shrink like '%s' ''' % (url_hash)
        else:
            return None
            
        row = _execute(query, False)
        if row!= None:
            return row
    except Exception as e:
        msg = "something went wrong: %s" % e
        logger.info(msg)
        return None

def update_url_hit(row=None,url=None,url_hash=None):
    """To update hit count on url
    """
    try:
        lasthit_at = datetime.datetime.now()
        if row!=None:
            query = ''' update urlsbase
                        set hits = hits+1, lasthit_at = '%s' where id = %d ''' % (lasthit_at, row)
        elif url!=None:
            query = ''' update urlsbase
                        set hits = hits+1, lasthit_at = '%s' where url = %s ''' % (lasthit_at, url)
        elif url_hash!=None:
            query = query = ''' update urlsbase
                        set hits = hits+1, lasthit_at = '%s' where shrink = %d ''' % (lasthit_at, url_hash)
        else:
            return None
            
        row = _execute(query, False)
        if row!= None:
            return True
    except Exception as e:
        msg = "something went wrong: %s" % e
        logger.info(msg)
        return None
    pass

def timestamp_parser(timestamp_str=None):
    """DB timestamp to datetime
    """
    if timestamp_str!=None:
        
        return datetime.datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S.%f")
    else:
        return None

def timestamp_to_hooman(timestamp_str=None):
    """DB timestamp to human readable
    """
    if timestamp_str!=None:
        date_time = timestamp_parser(timestamp_str)
        return date_time.strftime("%A ,%d %b %Y, %I:%M:%S %p")
    else:
        return None

##Handlers below
class MainHandler(BaseHandler):
    """List of all urls and handler descriptions
    """
    def get(self):
        app_handlers = [(handler.regex.pattern, handler.handler_class) for handler in self.application.handlers[0][1]]
        self.response = []
        for handler in app_handlers:
            temp_dict={}
            temp_dict['url'] = handler[0]
            temp_dict['description'] = inspect.getdoc(handler[1])
            self.response.append(temp_dict)
        self.write_json()
        
class RedirectHandler(BaseHandler):
    """Redirect to url and asynchronously updated hit count
    """
    @tornado.web.asynchronous
    def get(self, url_hash):
        if url_hash==None:
            self.redirect("/")
        else:
            row = check_url_existence(None,url_hash)
            if row==None:
                self.send_error(404, message="Requested url not found") # Bad Request
            else:
                self.redirect(row[1])
                update_url_hit(row[0])
        return
            
    
class URLshrinkHandler(BaseHandler):
    """Checks url existence, creates short url and updated title to db entry of url asynchronously
    """
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
                            ('%s', '%s', '%s', '%s', '%s') ''' % (url, url_hash, created_at, updated_at, lasthit_at)
                _execute(query)
            else:
                
                url_hash = row[3]
                url = row[1]
                created_at = row[5]
                updated_at = row[6]
                lasthit_at = row[7]
            
            self.response['url'] = url
            self.response['short_url'] = self.get_short_url(url_hash)
            self.response['created_at'] = str(created_at)
            self.response['updated_at'] = str(updated_at)
            self.response['lasthit_at'] = str(lasthit_at)
            self.write_json()
            self.finish()
            
            if row == None:
                #get title and update row
                query = '''select id from urlsbase WHERE shrink = '%s' ''' % (url_hash)
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
        _hash = ''.join(random.choice(string.ascii_lowercase +string.ascii_uppercase + string.digits) for _ in range(7))
        query = '''select id from urlsbase WHERE shrink = '%s' ''' % (_hash)
        rows = _execute(query)
        if len(rows)== 0:
            return _hash
        else:
            return self.create_path()

class TitleSearchHandler(BaseHandler):
    """
    Search url using page title
    """
    def post(self):
        try:
            escape_char = '%'
            search_query = self.get_json_argument('q')
            query = '''select * from urlsbase WHERE title like '%c%s%c' ''' % (escape_char, search_query, escape_char)
            rows = _execute(query)
            self.response = []
            # collate results as json list
            for entries in rows:
                temp_dict = {}
                temp_dict['title'] = entries[2]
                temp_dict['url'] = entries[1]
                temp_dict['short_url'] = self.get_short_url(entries[3])
                self.response.append(temp_dict)
            self.write_json()
            
        except Exception as e:
            msg = "something went wrong: %s" % e
            logger.info(msg)
            if not self._finished:
                #if the connection is closed, it won't call this function
                self.send_error(400, message="something went wrong") # Bad Request
            else:
                pass


class URLMetaListHandler(BaseHandler):
    """Lists all meta urls for links
    """
    def get(self):
        try:
            query = '''select * from urlsbase''' 
            rows = _execute(query)
            self.response = []
            # collate results as json list
            for entries in rows:
                temp_dict = {}
                temp_dict['meta_url'] = self.get_short_url("meta/%s" % (entries[3]))
                self.response.append(temp_dict)
            self.write_json()
            
        except Exception as e:
            msg = "something went wrong: %s" % e
            logger.info(msg)
            if not self._finished:
                #if the connection is closed, it won't call this function
                self.send_error(400, message="something went wrong") # Bad Request
            else:
                pass

class URLMetaHandler(BaseHandler):
    """Return meta details of short url
    """
    def get(self, url_hash):
        try:
            if url_hash!=None:
                print(url_hash)
                row = check_url_existence(None, url_hash)
                # collate required fields
                if row!=None:
                    
                    self.response['url'] = row[1]
                    self.response['title'] = row[2]
                    self.response['short_url'] = self.get_short_url(row[3])
                    self.response['no_hits'] = row[4]
                    self.response['created_at'] = timestamp_to_hooman(row[5])
                    self.response['updated_at'] = timestamp_to_hooman(row[6])
                    self.response['last_hit_at'] = timestamp_to_hooman(row[7])
                self.write_json()
            else:
                self.send_error(400, message="Short url doesnt exist")
            
            
        except Exception as e:
            msg = "something went wrong: %s" % e
            logger.info(msg)
            if not self._finished:
                #if the connection is closed, it won't call this function
                self.send_error(400, message="something went wrong") # Bad Request
            else:
                pass
