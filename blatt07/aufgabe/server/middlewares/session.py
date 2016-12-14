from server.log import log
from server.webserver import Middleware, Cookie
from uuid import uuid4
import re
import pickle # serialize and deserialize python data structures


class SessionMiddleware(Middleware):
    """Add a session attribute to request."""

    def __init__(self, cookiename="_sessid"):
        self.session = None
        self.cookiename = cookiename
        super().__init__()

    def process_request(self, request, response):
        """Get session ID from request cookies and load session."""
        if self.cookiename in request.cookies: # try to recover old session
            self.session = Session(request.cookies[self.cookiename], cookiename=self.cookiename)
            log(2,"Loaded from Session: %s" % self.session.data)
        else: # new session
            self.session = Session(cookiename=self.cookiename)
            log(2, "Created New Session")
        request.session = self.session # assignment does not copy objects!

    def process_response(self, response):
        """Add Session cookie to repsonse or delete session cookie if no session."""
        if self.session and self.session.sessid:
            self.session.save() # write session to data store
            response.add_cookie(self.session.make_cookie())
            log(2,"Added Session Cookie")
        else: # delete nonexistant or destroyed empty sessions
            response.add_cookie(self.session.make_delete_cookie())
            log(2, "Delete Session Cookie")


class InvalidSessionError(Exception):
    pass


class Session:
    def __init__(self, sessid='', cookiename='_sessid', path='/'):
        self.sessdatadir = 'sessions' # the data dir relative to current working directory (usually the place where the __main__ script is located
        self.sessid = sessid # the very secret session id (32-digit hex number)
        self.cookiename = cookiename # which name shall the cookie bear?
        self.path = path # for which path shall the cookie be valid?
        self.data = {} # the session content as dictionary
        
        if not self.sessid or not self.check_id():
            log(2, "Session constructor: Generate new Session")
            self.generate_id()
        else:
            try:
                log(2, "Session constructor: Try to load %s." % self.sessid)
                self.load()
            except InvalidSessionError:
                # silently fail and make fresh session if old one can't be loaded
                log(2, "Session Constructor: Failed to load, generate new Session.")
                self.generate_id()

    def generate_id(self):
        # generate new random session id for new session
        # cf. rfc4122
        self.sessid=uuid4().hex

    def check_id(self):
        return re.match(r"^[0-9a-f]{32}$", self.sessid)
    
    def load(self):
        """Load session data from file. 
           Raises InvalidSessionError if session does not exist."""
    
        if not self.check_id():
            raise InvalidSessionError()
        
        try:
            f = open(self.sessdatadir+'/'+self.sessid, 'rb')
        except IOError:
            raise InvalidSessionError()
            
        self.data = pickle.load(f)
        return self.data 
    
    def save(self):
        """Write session to data store. Contents will be pickled, so python objects can be stored/restored."""
        if not self.check_id():
            return False

        try:
            f = open(self.sessdatadir+'/'+self.sessid, 'wb')
        except IOError:
            raise
            return False
        
        pickle.dump(self.data, f)
        return True
    
    def destroy(self):
        """Destroys session."""
        
        if not self.check_id():
            return False

        try:
            import os
            os.unlink(self.sessdatadir+'/'+self.sessid)
        except IOError:
            return False
        
        self.data = {}
        self.sessid = ''
        
        return True

    def renew(self):
        """Destroy session and generate new id, i.e. make a new fresh session from the same session object."""
        self.destroy()
        self.generate_id()

    def __getitem__(self, key):
        """Direct access to Session data."""
        return self.data.__getitem__(key)

    def __setitem__(self, key, value):
        """Direct access to Session data."""
        return self.data.__setitem__(key, value)

    def make_cookie(self):
        """Returns Cookie object for session id"""
        return Cookie(self.cookiename, self.sessid, path='/')
    
    def make_delete_cookie(self):
        """Returns Cookie object to delete cookie"""
        return Cookie(self.cookiename, '', path='/', expires=Cookie.expiry_date(-1))

              
