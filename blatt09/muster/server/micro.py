from server.webserver import Webserver, App
from server.apps.static import StaticApp
from functools import wraps

class MicroApp(App):
    """Puts a micro framework (see flask, sinatra etc.) on top of the Webserver framework.

    Usage:
    app = MicroApp()

    @app.get('')
    def index(request, response, pathmatch):
        response.send(body="Hey!")

    @app.put('thing/(?P<thing_id>)')
    def update_thing(request, response, pathmatch):
        thing = model.find_thing(pathmatch.group('thing_id'))
        thing.foo = request.params['foo']
        thing.store()
        response.send_redirect('/')

    @app.route('info')
    def info(request, response, pathmatch):
        response.send(body="Just for info")

    @app.route('info', methods=['PUT', 'POST'])
    def info(request, response, pathmatch):
        response.send(body="Just for info")
    """

    def __init__(self, **kwargs):
        self.server = Webserver()
        super().__init__(**kwargs)

        # add middlewares and other apps here...
        self.server.add_app(StaticApp(prefix='static', path='static'))
        self.server.add_app(self)

    def get(self, url):
        """Decorator function for GET routes that maps to the route method."""
        return self.route(url, ['GET'])

    def post(self, url):
        """Decorator function for GET routes that maps to the route method."""
        return self.route(url, ['POST'])

    def put(self, url):
        """Decorator function for GET routes that maps to the route method."""
        return self.route(url, ['PUT'])

    def delete(self, url):
        """Decorator function for GET routes that maps to the route method."""
        return self.route(url, ['DELETE'])

    def route(self, url, methods=None):
        """Decorator function with arguments. Returns a decorator function that takes a function and wraps it or
           has some side effetcs (like registering the route)."""
        def wrap(f):
            self.add_route(url, f, methods=methods)
            return f
        return wrap

    def serve(self):
        self.server.serve()


