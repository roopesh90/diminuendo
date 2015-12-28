import json
import tornado.web
import tornado.options

import logging as logger

class BaseHandler(tornado.web.RequestHandler):
    """A class to collect common handler methods - all other handlers should
    subclass this one.
    """

    def set_default_headers(self):
        """Default set of headers for the application.
        """
        self.set_header('Server', tornado.options.options.SERVER)
        self.set_header("Content-Type", "application/json")
        logger.debug("Default headers set")
    
    def prepare(self):
        """Incorporate request JSON into arguments dictionary.
        """
        if self.request.body:
            try:
                json_data = json.loads(self.request.body)
                self.request.arguments.update(json_data)
            except ValueError:
                message = 'Unable to parse JSON.'
                self.send_error(400, message=message) # Bad Request

        # Set up response dictionary.
        self.response = dict()    
    
    def write_error(self, status_code, **kwargs):
        if 'message' not in kwargs:
            if status_code == 405:
                kwargs['message'] = 'Invalid HTTP method.'
            else:
                kwargs['message'] = 'Unknown error.'

        self.response = kwargs
        self.write_json()

    def write_json(self):
        output = json.dumps(self.response)
        self.write(output)
        
