__author__ = 'Tobias Thelen'

from server import webserver
from server.apps.static import StaticApp


import os

if __name__ == '__main__':
    s = webserver.Webserver()
    s.add_app(StaticApp(path='static'))
    s.serve()