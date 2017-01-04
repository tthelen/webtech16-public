"""
wiki.py
A very very simple Wiki

@author: Tobias Thelen
@contact: tobias.thelen@uni-osnabrueck.de
@licence: public domain
@status: completed
@version: 3 (10/2016)
"""

from server import webserver
from server.middlewares.logging import LoggingMiddleware
from server.middlewares.session import SessionMiddleware
from server.middlewares.auth import AuthMiddleware
from server.apps.static import StaticApp
import re


class NoSuchPageError(Exception):
    """Raise if try to access non existant wiki page."""
    pass


class WikiApp(webserver.App):
    """
    Webanwendung zum kollaborativen Schreiben (wiki).

    Diese sehr einfache Anwendung demonstriert ein simples Wiki.
    """

    def register_routes(self):
        self.add_route("/?$", self.show)
        self.add_route("show(/(?P<pagename>\w+))?$", self.show)
        self.add_route("edit/(?P<pagename>\w+)$", self.edit)
        self.add_route("save/(?P<pagename>\w+)$", self.save)
        self.add_route("delete/(?P<pagename>\w+)$", self.delete)
        self.add_route("login", self.login)

    def read_page(self, pagename):
        """Read wiki page from data directory or raise NoSuchPageError."""

        try:
            with open("data/"+pagename, "r", encoding="utf-8") as f:
                x=f.read()
                return x
        except IOError:
            raise NoSuchPageError

    def delete_page(self, pagename):
        """Remove a page from page list. Cannot be undone."""
        import os
        try:
            os.unlink("data/"+pagename)
        except IOError:
            raise NoSuchPageError

    def markup(self, text):
        """Substitute wiki markup in text with html."""

        text = re.sub(r"<",
                      r"&lt;",
                      text)

        # substitute links: [[pagename]] -> <a href="/show/pagename">pagename</a>
        text = re.sub(r"\[\[([a-zA-Z0-9]+)\]\]",
                      r"<a href='/show/\1'>\1</a>",
                      text)

        # substitute headlines: !bang -> <h1>bang</h1>
        text = re.sub(r"^!(.*)$", r"<h1>\1</h1>", text, 0, re.MULTILINE)

        # replace two ends of line with <p>
        text = re.sub(r"\r?\n\r?\n", r"<p>", text)

        # replace one end of line with <br>
        text = re.sub(r"\r?\n\r?\n", r"<br>", text)

        return text

    def pagelist(self):
        """Read the list of pages from file system and return a list of pagenames."""

        from os import listdir
        # only include pages that match the pagename regex
        pages = [page for page in listdir("data") if re.match(r"^[a-zA-Z0-9]+$", page)]
        pages.sort()
        return pages  # We like them sorted

    def show(self, request, response, pathmatch=None):
        """Evaluate request and construct response."""

        # pagename can be given py request parameter or path. request parameter has higher priority
        if 'pagename' in request.params and re.match(r"[a-zA-Z0-9]+", request.params['pagename']):
            pagename = request.params['pagename']
        else:
            try:
                pagename = pathmatch.group('pagename') or "main"
            except IndexError:
                pagename = "main"  # default pagename

        try:
            text = self.read_page(pagename)
        except NoSuchPageError:
            # redirect to edit view if page does not exist
            response.send_redirect("/edit/" + pagename)
            return

        # show page
        response.send_template('show.mustache',
                                   {'text': self.markup(text),
                                    'user': request.user,
                                    'pagelist': self.pagelist(),
                                    'pagename': pagename})

    def edit(self, request, response, pathmatch=None):
        """Display wiki page for editing."""

        request.authenticate()

        try:
            pagename = pathmatch.group('pagename') or "main"
        except IndexError:
            pagename = "main"

        try:
            text = self.read_page(pagename)
        except NoSuchPageError:
            # use default text if page does not yet exist
            text = "This page is still empty. Fill it."

        # fill template and show
        response.send_template('edit.mustache',
                                   {'text': text,
                                    'user':request.user,
                                    'pagelist': self.pagelist(),
                                    'pagename': pagename})

    def delete(self, request, response, pathmatch=None):
        """Delete a wiki page."""

        request.authenticate()

        try:
            pagename = pathmatch.group('pagename') or "main"
            self.delete_page(pagename)
        except (IndexError, NoSuchPageError):
            pass

        response.send_redirect('/')

    def save(self, request, response, pathmatch=None):
        """Evaluate request and construct response."""

        request.authenticate()

        try:
            pagename = pathmatch.group('pagename')
        except IndexError:
            # no pagename given: error
            response.send_template("wikierror.mustache",
                               {'error':'No pagename given.',
                                'user': request.user,
                                'pagelist': self.pagelist(),
                                'text':'save action needs pagename'}, code=500)
            return

        try:
            wikitext = request.params['wikitext']
        except KeyError:
            # no text given: error
            response.send_template("wikierror.mustache",
                               {'error':'No wikitext given.',
                                'user': request.user,
                                'pagelist': self.pagelist(),
                                'text':'save action needs wikitext'}, code=500)
            return

        # ok, save text
        f = open("data/" + pagename, "wb")
        f.write(wikitext.encode("utf-8"))
        f.close()

        response.send_redirect("/show/"+pagename)

    def login(self, request, response, pathmatch):
        """Display login form or do nothing and redirect to start."""
        request.authenticate()
        response.send_redirect("/")


if __name__ == '__main__':
    s = webserver.Webserver()
    s.set_templating('pystache')
    s.set_templating_path('templates.mustache/wiki')
    s.add_middleware(LoggingMiddleware())
    s.add_middleware(SessionMiddleware())
    s.add_middleware(AuthMiddleware(s))
    s.add_app(WikiApp())
    s.add_app(StaticApp(prefix='static', path='static'))
    s.serve()
