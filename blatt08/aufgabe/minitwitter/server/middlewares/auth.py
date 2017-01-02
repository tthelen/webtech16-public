from server.log import log
from server.webserver import Middleware, StopProcessing
from urllib.parse import quote, unquote
import server.usermodel


class AuthMiddleware(Middleware):
    """Add a user object to every request."""

    def __init__(self, login_template='templates/login.tmpl', db_connection = None):
        self.user = None
        self.login_template = login_template
        self.users = server.usermodel.Users(db_connection)
        super().__init__()

    def process_request(self, request, response):
        """Fetch user from session or create a fresh anonymous user."""
        try:
            self.user = request.session["AuthMiddleware.user"]
            if not isinstance(self.user, server.usermodel.User):
                self.user = server.usermodel.AnonymousUser()
        except KeyError:
            self.user = server.usermodel.AnonymousUser()
        request.user = self.user  # store user in request object
        request.require_login = self.require_login  # attach require_login method to request object
        self.request = request  # remember for later user
        self.response = response

    def require_login(self, msg=""):
        """Only returns if an authenticated user session exists. Otherwise login page will be displayed."""

        log(1, "Require Login")
        if not self.request.user.is_authenticated:
            log(2, "No authenticated user found")
            if '_username' in self.request.params and '_password' in self.request.params:
                log(2, "Username and password found in Request")
                user = self.users.login(self.request.params['_username'], self.request.params['_password'])
                if user:
                    log(2, "Login succeeded.")
                    self.user = user
                    self.request.session['AuthMiddleware.user'] = self.user # save user to session
                    self.request.user = self.user # expose user object to request
                    return True
                else:
                    log(2, "Login failed")
                    if self.users.findByUsername(self.request.params['_username']):
                        msg += "\nDas Passwort ist falsch! Bitte versuchen Sie es nochmal."
                    else:
                        msg += "\nDer Benutzername existiert nicht! Bitte versuchen Sie es nochmal."

            log(2, "Present login form")
            self.login_form(msg) # never returns but raises StopProcessing
        else:
            log(2, "Authenticated user is present from session.")
            return True

    def login_form(self, msg=''):
        """Send a login form to the user and stop processing.

        The login form presents a post form that contains all original parameters (both get and post)
        and will be send to the same url. Parameters will be augmented by _username and _password parameters
        from the login form and next time, require_login can check these credentials.
        """

        d = dict()
        d['msg'] = msg
        d['action'] = self.request.resource # repeat complete url including get parameters
        if self.request.method.lower() == 'post':
            # construct a list of hidden input fields that contain all parameters
            # TODO: this also includes the get parameters which is superfluous
            d['post_parameters'] = ['<input type=hidden name="%s" value="%s">' %
                                    (quote(bytes(key, encoding='utf-8')), quote(bytes(value, encoding='utf-8')))
                                    for (key,value) in self.request.params.items()
                                    if key not in ['_username', '_password']]
        else:
            d['post_parameters'] = []
        self.response.send_template(self.login_template, d)

        raise StopProcessing(200,"OK") # don't return to calling code but finish the response

