__author__ = 'Tobias Thelen'

from server import webserver
from server.webserver import StopProcessing
from server.apps.static import StaticApp
from server.log import log


import os, re

class IconEditorApp(webserver.App):

    def register_routes(self):
        self.add_route("$", self.show)
        self.add_route("save$", self.save)


    def show(self, request, response, pathmatch):
        """Show the editor. Provide list of saved icons."""

        icon_list = os.listdir("data")
        icons_html = "<ul>"
        for icon_title in icon_list:
            with open("data/"+icon_title, "r") as f:
                icons_html += "<li class=icon-list-item><img src='%s' title='%s'></li>" % (f.read(), icon_title)
        icons_html += "</ul>"
        response.send_template("templates/iconeditor.tmpl", {'icons': icons_html})


    def save(self, request, response, pathmatch):
        """Save base64-encoded representation of icon pixels to a file."""

        if 'title' not in request.params or \
            not re.match(r"^[a-zA-Z0-9]+$", request.params['title']) or \
            'icon' not in request.params or \
            not request.params['icon'].startswith('data:'):
            raise StopProcessing(500, "Invalid parameters")
        else:
            with open("data/"+request.params['title'], "w") as f:
                f.write(request.params['icon'])
        response.send_redirect('/')


if __name__ == '__main__':
    s = webserver.Webserver()
    s.add_app(IconEditorApp())
    s.add_app(StaticApp(prefix='static', path='static'))
    s.serve()