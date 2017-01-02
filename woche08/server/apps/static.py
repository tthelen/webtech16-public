__author__ = 'Tobias Thelen'

from server.log import log
from server.webserver import App, StopProcessing


class StaticApp(App):
    """Serve static files."""

    def __init__(self, **kwargs):
        """StaticApp constructor.

        :param:path File system path to server files from.
        :return: nothing
        """
        self.path = kwargs['path']
        if not self.path.endswith('/'):
            self.path += "/"
        super().__init__(**kwargs)

    def register_routes(self):
        self.add_route('(?P<file>.+)', self.sendfile)

    def sendfile(self, request, response, pathmatch=None):
        """Serve a static file from local filesystem."""

        # path might be urlencoded
        from urllib.parse import unquote

        resource = unquote(pathmatch.group('file'))

        # directory traversal protection
        # os function os.path.abspath calculates normalized absolute path
        # self.path must be a prefix of it
        from os.path import abspath

        log(2, "check for directory traversal attack: does %s start with %s ?" % (
            abspath(self.path + resource), abspath(self.path)))
        if not abspath(self.path + resource).startswith(abspath(self.path)):
            raise StopProcessing(500, "500 internal server error.\nDirectory traversal attack attempted.\n")

        # open, read and server file
        try:
            log(2, "Try to open %s" % resource)
            with open(self.path + resource, 'rb') as f:
                # guess type from extension
                import mimetypes

                (content_type, encoding) = mimetypes.guess_type(resource)
                response.set_content_type(content_type)
                response.send(body=f.read())  # read and dump whole file
        except IOError:
            raise StopProcessing(404, "File not found: %s" % resource)

    def __str__(self):
        return "StaticApp - liefert unter /{} statische Dateien aus {} aus".format(self.prefix, self.path)