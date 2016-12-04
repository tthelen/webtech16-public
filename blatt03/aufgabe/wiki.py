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

    def read_page(self, pagename):
        """Read wiki page from data directory or raise NoSuchPageError."""

        try:
            with open("data/"+pagename, "r", encoding="utf-8") as f:
                x=f.read()
                print(x)
                return x
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

    def show(self, request, response, pathmatch=None):
        """Evaluate request and construct response."""

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
        response.send_template('templates/wiki/show.html',
                                   {'text': self.markup(text),
                                   'pagename': pagename})

    def edit(self, request, response, pathmatch=None):
        """Display wiki page for editing."""

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
        response.send_template('templates/wiki/edit.html',
                                   {'text': text,
                                   'pagename': pagename})

    def save(self, request, response, pathmatch=None):
        """Evaluate request and construct response."""

        try:
            pagename = pathmatch.group('pagename')
        except IndexError:
            # no pagename given: error
            response.send_template("templates/wiki/wikierror.html",
                               {'error':'No pagename given.',
                                'text':'save action needs pagename'}, code=500)
            return

        try:
            wikitext = request.params['wikitext']
        except KeyError:
            # no text given: error
            response.send_template("templates/wiki/wikierror.html",
                               {'error':'No wikitext given.',
                                'text':'save action needs wikitext'}, code=500)
            return

        # ok, save text
        f = open("data/" + pagename, "w", encoding='utf-8')
        f.write(wikitext)
        f.close()

        response.send_redirect("/show/"+pagename)


if __name__ == '__main__':
    s = webserver.Webserver()
    s.add_app(WikiApp())
    s.add_app(StaticApp(prefix='static', path='static'))
    s.serve()
