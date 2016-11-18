#!/usr/local/bin/python
# coding: utf-8

"""
celsius.py

@author: Tobias Thelen
@contact: tobias.thelen@uni-osnabrueck.de
@licence: public domain
@status: completed
@version: 2 (04/2015)
"""

from server import webserver
from server.apps.static import StaticApp
from server.log import log

import os

class CelsiusApp(webserver.App):

    def register_routes(self):
        self.add_route(r"", self.celsius)


    def celsius(self, request, response, pathmatch=None):

        msg = ""
        if 'celsius' in request.params:
            try:
                fahrenheit = float(request.params['celsius']) * 9 / 5 + 32
                msg = "%s° Celsius sind %4.2f° Fahrenheit" % (request.params['celsius'], fahrenheit)
            except (ValueError, TypeError):
                msg = "Bitte eine Zahl eingeben!"

        response.send_template("templates/celsius/celsius.tmpl", {'msg': msg})


if __name__ == '__main__':
    s = webserver.Webserver()
    s.add_app(CelsiusApp())
    s.add_app(StaticApp(prefix='static', path='static'))
    log(0, "Server running.")
    s.serve()