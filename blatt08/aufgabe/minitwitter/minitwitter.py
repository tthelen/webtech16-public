'''
Created on 10.05.2013

@author: Tobias
'''

from server.webserver import Webserver, App, StopProcessing
from server.apps.static import StaticApp
from server.apps.usermanagement import UsermanagementApp
from server.apps.static import StaticApp
from server.middlewares.session import SessionMiddleware
from server.middlewares.auth import AuthMiddleware
from server.log import log

import sqlite3 as sqlite
import os
from urllib.parse import quote, unquote


class MiniTwitterApp(App):
    """Create and display status messages"""

    def __init__(self, datadir='data'):
        self.datadir = datadir
        super().__init__()

    def register_routes(self):
        self.server.add_route(r"/?$", self.show)
        self.server.add_route(r"/logout$", self.logout)
        self.server.add_route(r"/login$", self.login)

    def show(self, request, response, pathmatch):
        """Process all requests. Dispatch POST to save method. Show tweets on GET requests."""

        if request.method.lower() == 'post':
            return self.save(request, response, pathmatch)

        m = [] # list of tweets
        try:
            f = open(self.datadir+'/minitwitter.data','r', encoding='utf-8')
            lines = f.readlines()
            f.close()
        except IOError:
            # no tweets, yet
            lines=[]

        try:
            message = request.params['message']
        except KeyError:
            message = ""

        for line in lines:
            try:
                (date,tweet) = line.strip().split("#")
            except ValueError:
                # ignore corrupt lines
                continue
            # tweet = unquote(tweet)
            m.append({'date': date, 'tweet': tweet})
        if not m:
            m.append({'date': 'No news', 'tweet': 'Create some.'})
        m.reverse()

        d = {'tweets': m, 'message': message, 'user': request.user }

        response.send_template('minitwitter.tmpl', d)

    def save(self, request, response, pathmatch):
        """Process post request to save new tweet."""

        request.require_login()

        import datetime
        now = datetime.datetime.utcnow().strftime("%d.%m.%Y %H:%M:%S")
        try:
            status = request.params['status']
        except KeyError:
            raise StopProcessing(500, "No status given.")
        try:
            f=open(self.datadir+'/minitwitter.data','a', encoding='utf-8')
            f.write(now + "#" + status + "\n")
            f.close()
        except IOError:
            raise StopProcessing(500, "Unable to connect to data file.")
        
        response.send_redirect("/?message={}".format(quote("Great! Now the world knows...")))

    def logout(self, request, response, pathmatch):
        if request.session:
            request.session.destroy()
        response.send_redirect("/")

    def login(self, request, response, pathmatch):
        request.require_login()
        response.send_redirect("/")


if __name__ == '__main__':

    db = sqlite.connect('minitwitter.sqlite')
    db.row_factory = sqlite.Row

    s = Webserver()
    s.set_templating("pystache")
    s.set_templating_path("templates.mustache")

    s.add_middleware(SessionMiddleware())
    s.add_middleware(AuthMiddleware(login_template='login.tmpl', db_connection=db))

    s.add_app(UsermanagementApp(db_connection=db))
    s.add_app(StaticApp(prefix='static', path='static'))

    s.add_app(MiniTwitterApp('data'))

    log(0, "Server running.")
    s.serve()
