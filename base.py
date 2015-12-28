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
        # Set up response dictionary.
        self.response = dict()
        
    def load_json(self):
        """Load JSON from the request body and store them in
        self.request.arguments, like Tornado does by default for POSTed form
        parameters.
        
        If JSON cannot be decoded, raises an HTTPError with status 400.
        """
        logger.debug("load_json called")
        try:
            self.request.arguments = json.loads(self.request.body.decode('utf-8'))
        except (ValueError, TypeError):
            msg = "Could not decode JSON: %s" % self.request.body
            logger.debug(msg)
            self.send_error(400, message=msg) # Bad Request
            
    def get_json_argument(self, name, default=None):
        """Find and return the argument with key 'name' from JSON request data.
        Similar to Tornado's get_argument() method.
        """
        if default is None:
            default = self._ARG_DEFAULT
        if not self.request.arguments:
            self.load_json()
        if name not in self.request.arguments:
            if default is self._ARG_DEFAULT:
                msg = "Missing argument '%s'" % name
                logger.debug(msg)
                raise tornado.web.HTTPError(400, msg)
            logger.debug("Returning default argument %s, as we couldn't find '%s' in %s" % (default, name, self.request.arguments))
            return default
        arg = self.request.arguments[name]
        logger.debug("Found '%s': %s in JSON arguments" % (name, arg))
        return arg
    
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
        
