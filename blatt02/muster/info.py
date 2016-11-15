__author__ = 'Tobias Thelen'

from server import webserver
from server.apps.info import InfoApp
from server.apps.static import StaticApp


class WelcomeApp(webserver.App):
    """Says hello."""

    def register_routes(self):
        self.add_route("", self.welcome)

    def welcome(self, request, response, pathmatch):
        """Redirects to /static/welcome.html."""
        response.send_redirect('/static/welcome.html')

    def __str__(self):
        return "WelcomeApp"


if __name__ == '__main__':
    s = webserver.Webserver()
    s.add_app(WelcomeApp())
    s.add_app(InfoApp(prefix='info'))
    s.add_app(StaticApp(prefix='static', path='static'))
    s.serve()
