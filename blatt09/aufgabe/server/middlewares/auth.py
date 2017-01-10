from server.webserver import Middleware, StopProcessing, AlreadyProcessed


class AuthMiddleware(Middleware):
    """Handle authorization."""

    def __init__(self, server, login_template="server/templates/login.mustache"):
        self.login_template = login_template
        self.server = server
        super().__init__()

    def process_request(self, request, response):
        """Check is request is login attempt or already authenticated."""
        self.request = request  # we'll need it later in the authenticate method
        self.response = response  # dito

        if '__do_login' in request.params and 'username' in request.params and \
                        'password' in request.params and request.method=='POST':
            # Login form submitted
            request.user = None
            if self.check_credentials(request.params['username'], request.params['password']):
                request.session['auth']={'user':request.params['username']}
            else:
                return self.authenticate("Wrong credentials. Try again.")

        elif '__do_logout' in request.params:
            # to logout, remove auth information from session
            try:
                del request.session.data['auth']
            except KeyError:
                pass
            request.user = None

        try:
            request.user = request.session['auth']['user']  # already authenticated
        except KeyError:
            request.user = None  # not authenticated

        request.authenticate = self.authenticate

    def authenticate(self, msg=""):
        """Check if user is authenticated. If not, display login form."""
        if self.request.user:
            return True
        else:
            templating = self.server.templating  # save current templating settings
            templating_path = self.server.templating_path
            self.server.set_templating("pystache")
            self.server.set_templating_path(".")
            params = {'hidden_fields': self.request.params}  # pass all parameters
            self.response.send_template(self.login_template, params)
            self.server.templating = templating  # restore templating settings
            self.server.templating_path = templating_path
            raise AlreadyProcessed()

    def check_credentials(self, username, password):
        with open("user.db", "r") as file:
            while 1:
                try:
                    line = file.readline().strip()  # read a line with username:salt:password
                    if not line:
                        break
                    (user, salt, pwd) = line.split(':')
                    if user == username:  # user found?
                        import hashlib
                        # check if sha256(salt+given password) == sha(salt+real password)
                        if hashlib.sha256(salt.encode('utf-8')+password.encode('utf-8')).hexdigest() == pwd:
                            return True
                except ValueError:
                    continue
        return False
