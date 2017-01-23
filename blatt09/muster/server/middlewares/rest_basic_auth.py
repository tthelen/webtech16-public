from server.webserver import Middleware, StopProcessing
from server.log import log
import base64, json

users = {'admin': 'admin',  # usernames and passwords stored in an extremely ugly way
        'user1': 'user1',
        'user2': 'user2'}


class RestBasicAuthMiddleware(Middleware):
    """Handle authorization."""

    def __init__(self, server):
        self.server = server
        super().__init__()

    def process_request(self, request, response):
        """Check is request is login attempt or already authenticated."""
        self.request = request  # we'll need it later in the authenticate method
        self.response = response  # dito

        if 'Authorization' in request.headers:
            log(2,"Authorization header present")
            authtype, credentials = request.headers['Authorization'].split(' ')
            if authtype=='RestBasic':  # Our own Auth Mechanism
                username, password = base64.b64decode(credentials.encode('utf-8')).decode('utf-8').split(':')
                if username in users and password == users[username]:
                    log(2,"Credentials OK, user is "+username)
                    request.user = username
                else:
                    log(2,"Credentials not OK")
        else:
            request.user = False

        request.authenticate = self.authenticate

    def authenticate(self):
        """Check if user is authenticated. If not, send 401."""
        log(2,"Checking for authentication")
        if self.request.user:#
            log(2,"Authentication OK")
            return True
        else:
            log(2,"Authentication not OK, send 401")
            self.response.add_header("WWW-Authenticate", 'RestBasic realm="We need your password."')
            self.response.add_header('Content-Type', 'application/json')
            raise StopProcessing(401,json.dumps({"error":"Authentiction required."}))
