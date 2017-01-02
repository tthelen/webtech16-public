"""
webserver.py

@author: Tobias Thelen
@contact: tobias.thelen@uni-osnabrueck.de
@licence: public domain
@status: completed
@version: 2 (04/2015)
"""

import socket, re, os
from server.log import log
from string import Template


class StopProcessing(Exception):
    """
    Exception: Immediately stop processing and issue an error response.
    """

    def __init__(self, code, reason):
        """
        Immediately stop processing and issue an error response.

        :param code: Error status code
        :param reason: Text to display
        """
        self.code = code
        self.reason = reason

    def __str__(self):
        """
        Representation for informational purposes.
        :return: Displayable string with code and reason
        """
        return "[%d] %s" % (self.code, self.reason)


class App:
    """An app wraps web applications or reusable components for
       web applications such as serving static files, providing
       statistical information on the server.

       An app registers it routes with the server and provides
       callbacks for these routes.
       """

    def __init__(self, **kwargs):
        """
        Initialises an app.

        The App base class recognizes these keywords:

        prefix - add a prefix to all routes the app registers.
                 The prefix must not have a leading or trailing slash.
                 Example: prefix=static

        :param kwargs: Keyword arguments
        """
        kwargs.setdefault('prefix', '')  # default: no prefix
        self.prefix = kwargs['prefix']  # set prefix

    def add_route(self, partial_route, handler):
        """
        Prefixes a route and adds it to server.

        :param partial_route: Partial route to match (may include named regex groups)
        :param handler: Function/Method to be called if route matches
        :return: Result of server.add_route
        """

        if self.prefix and partial_route and not partial_route.startswith('/'):
            partial_route = '/' + partial_route  # ensure / after prefix if there is a partial route without /
        prefixed_route = "^/" + self.prefix + partial_route
        if not prefixed_route.endswith('$'):  # add end anchor if necessary
            prefixed_route += '$'
        return self.server.add_route(prefixed_route, handler)

    def register_routes(self):
        pass


class Middleware:

    def __init__(self):
        pass

    def process_request(self, request, response):
        pass

    def process_response(self, response):
        pass


class Cookie:
    """Data for single Cookie."""

    def __init__(self, name, value, secure=False, httpOnly=False, **kwargs):
        """Construct Cookie from python data"""
        self.name = name
        self.value = value
        self.httpOnly = httpOnly
        self.secure = secure
        self.attrkeys = ['Comment', 'Domain', 'Max-Age', 'Path', 'Expires']
        self.attrs = {}
        for attr in self.attrkeys:
            pyattr = attr.replace('-','_').lower()
            self.attrs[attr] = kwargs[pyattr] if pyattr in kwargs else ''

    @classmethod
    def parse(cls, cookie):
        """Construct Cookie from HTTP Request Header data"""
        pairs = map(lambda x: x.strip(),cookie.split(";"))
        cookies = {}
        for p in pairs:
            [key, value] = p.split("=", 1)
            cookies[key] = value
        return cookies

    def get_header(self):
        """Build HTTP Response Header Representation."""
        h = "Set-Cookie: %s=%s" % (self.name, self.value)
        args = ";".join(["%s=%s" % (key, val) for (key, val) in self.attrs.items()])
        if args:
            h += ";" + args
        if self.secure:
            h += "; secure"
        if self.httpOnly:
            h += "; httpOnly"
        return h + "\n"

    @classmethod
    def expiry_date(cls, numdays):
        """ Returns a cookie expiry date in the required format."""
        from datetime import date, timedelta
        new = date.today() + timedelta(days = numdays)
        return new.strftime("%a, %d-%b-%Y 23:59:59 GMT")

    def __getitem__(self, key):
        """Direct access to Cookie data."""
        if key == 'name':
            return self.name
        elif key == 'value':
            return self.value
        else:
            return self.attrs.__getitem__(key)


class Request:
    """
    http request data.
    """

    def __init__(self):
        self.headers = {}
        self.method = None
        self.protocol = None
        self.resource = None
        self.path = None
        self.params = {}
        self.origin = None  # will be set from server

    def parse(self, conn):
        """Parses an http-Request and return a dictionary with process_request line values and headers."""
        self.headers = {}

        # read process_request line
        request_line = conn.readline().decode('utf-8').strip()
        log(1, "Request-Line: %s" % request_line)
        if not request_line:  # rfc says "server SHOULD ignore blank request lines"
            return None

        # parse process_request line
        try:
            self.method, self.resource, self.protocol = request_line.split(" ")
        except ValueError:
            raise StopProcessing(400, "Bad request-line: %s\n" % request_line)

        # parse resource to path and params
        # extract GET parameters
        from urllib.parse import urlparse, parse_qs # analyse urls and parse query strings
        requrl = urlparse(self.resource)
        self.path = requrl.path
        self.params.update(parse_qs(requrl.query))

        # read and parse Request-Headers
        while True:
            header_line = conn.readline().decode('utf-8').strip()
            if not header_line:
                break
            log(2, "Header-Line: " + header_line)
            (headerfield, headervalue) = header_line.split(":", 1)
            self.headers[headerfield.strip()] = headervalue.strip()

        # read cookies
        if 'Cookie' in self.headers:
            log(2, "Cookie ist: %s" % self.headers['Cookie'])
            self.cookies = Cookie.parse(self.headers['Cookie'])
        else:
            self.cookies = {}

        # parse POST parameters
        log(1,"Methode %s" % self.method)
        if self.method == 'POST' or self.method == 'post':
            postbody = conn.read(int(self.headers['Content-Length'])).decode('utf-8')
            self.params.update(parse_qs(postbody))

        # all parameter values are lists
        # replace lists by the only element if there is only one
        for key in self.params:
            if len(self.params[key])==1:
                self.params[key] = self.params[key][0]

        return self.headers


class Response:
    """
    http response data
    """

    def __init__(self, conn, server):
        self.conn = conn  # the connection to write to
        self.code = None  # status code
        self.headers = {}  # all the response headers
        self.cookies = []
        self.body = None  # response body
        self.server = server

    def add_header(self, key, value):
        """
        Adds or overwrites a given key-value pair to the http Headers.

        :param key: http-Header
        :param value: it's value
        """
        self.headers[key] = value

    def add_cookie(self, cookie):
        """Add cookie to send."""
        self.cookies.append(cookie)

    def set_content_type(self, content_type):
        """
        Sets or overwrite the response's content type.

        :param content_type:
        """
        self.headers['Content-Type'] = content_type

    def send(self, code=None, headers=None, body=""):

        # method parameters overwrite/add to instance variables
        if code:
            self.code = code
        if body:
            if self.body:
                self.body += body
            else:
                self.body = body
        if headers:
            self.headers.update(headers)

    def commit(self):

        def w(txt):
            """Decode as UTF-8 and write to client connection"""
            self.conn.write(bytes(txt, 'UTF-8'))

        # default values
        if not self.code:
            self.code = 200
        if 'Content-Type' not in self.headers:
            self.headers['Content-Type'] = "text/html; charset=UTF-8"

        from server.statuscodes import statuscode

        (phrase, explanation) = statuscode(self.code)
        w("HTTP/1.1 %d %s\n" % (self.code, phrase))
        log(1, "HTTP/1.1 %d %s (%s)\n" % (self.code, phrase, explanation))

        import datetime

        w("Date: %s\n" % datetime.datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S"))
        w("Connection: close\n")

        # send cookies
        for c in self.cookies:
            w(c.get_header())

        # send other headers
        for key, value in self.headers.items():
            w("%s: %s\n" % (key, value))
        w("\n")  # extra leerzeile schliesst header ab

        if self.body:
            if isinstance(self.body, str):  # UTF-8
                w(self.body)
            else:  # bytes, e.g. binary data
                self.conn.write(self.body)

    def send_template(self, template, dictionary={}, code=None, headers=None):
        """
        Reads a template file, substitutes placeholders and sends it.

        :param template: Template file name
        :param dictionary: Keys and values for template placeholders
        :param code: The status code (default: 200)
        :param headers: Additional headers (default: None)
        :return:
        """
        from importlib import import_module
        templating = import_module("server.templating.{}".format(self.server.templating))
        body = templating.Templating.render(self.server.templating_path, template, dictionary)
        self.send(code=code, headers=headers, body=body)  # Substitute with dictionary values/keys

    def send_redirect(self, url):
        self.send(302, {'Location': url})


class Webserver:
    """Implements a simple webserver.

    In this version it receives and parses requests
    but always returns the same static response.

    Usage:
    server = Webserver(post=8080)
    server.serve()
    """

    def __init__(self, port=8080):
        self.port = port
        self.apps = []  # registered apps (App classes)
        self.routes = []  # registered routes (regex, handler)
        self.middlewares = [] # registeres middlewares (handler)
        self.request = None
        self.response = None
        self.templating = "python_templates" # default template engine
        self.templating_path = "templates"
        self.templating_available = ["python_templates", "jinja2", "pystache"]

    def set_templating(self, templating):
        if templating in self.templating_available:
            self.templating = templating
        else:
            raise Exception("Invalid templating engine name: {}. Available are: {}.".format(templating, self.templating_available))

    def set_templating_path(self, path):
        self.templating_path = path

    def add_app(self, app):
        """
        Register an app.
        :param app: App class instance
        :return: nothin
        """
        app.server = self  # set app's server attribute
        app.register_routes()  # let app register its routes
        self.apps.append(app)  # fill list of apps

    def add_route(self, route, action):
        """
        Register a route for request processing.
        """
        self.routes.append((route, action))

    def add_middleware(self, middleware_handler):
        """
        Register a middleware for request preprocessing and response postprocessing.
        :param middleware_handler: Middleware Subclass
        """
        self.middlewares.append(middleware_handler)

    def serve(self):
        """
        Listen for http requests forever and trigger processing.
        """

        try:
            c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            c.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            c.bind(('localhost', self.port))
            c.listen(1)
        except socket.error as msg:
            log(0, msg)
            return

        log(0, "Server running on http://{}:{} .".format('localhost', self.port))

        while 1:
            csock, caddr = c.accept()
            conn = csock.makefile(mode='rwb', buffering=1)
            self.request = Request()
            self.response = Response(conn, self)

            if self.request.parse(conn):
                self.request.origin = caddr[0]
                try:
                    # preprocessing (middlewares)
                    for m in self.middlewares:
                        m.process_request(self.request, self.response)

                    # processing (check registered routes for actions)
                    processed = False
                    for route in self.routes:
                        log(2, "Matche %s gegen %s" % (route[0], self.request.path))
                        match = re.match(route[0], self.request.path)
                        if match:
                            log(2, "Route %s matcht Request %s" % (route[0], self.request.path))
                            route[1](self.request, self.response, match)
                            processed = True
                            break

                    if not processed:
                        raise StopProcessing(404, "No matching route.")

                except StopProcessing as spe:
                    self.response.send(code=spe.code, body=spe.reason)

                # preprocessing (middlewares)
                for m in self.middlewares:
                    m.process_response(self.response)

                # actually write response to server connection
                try:
                    self.response.commit()
                except (ConnectionAbortedError, BrokenPipeError):
                    pass

            conn.close()
            csock.close()
