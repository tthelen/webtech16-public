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

                # TT: support If-Modified-Since-Caching (Aufgabe 2)
                # 1. Get modification time and convert it to a python datetime object
                # 2. Always send a Last-Modified header
                # 3. If request contains If-Modified-Since header:
                #    3.1 Parse If-Modified-Since-Date to datetime object
                #    3.2 Compare datetime objects
                #    3.3 Stop processing and issue a 304 response if browser has current version
                # 4. else: deliver as usual
                import os.path, time, datetime
                mtime = os.path.getmtime(self.path + resource)  # unix timestamp (seconds since 1.1.1970)
                modification_time = datetime.datetime.fromtimestamp(mtime)  # convert to datetime object
                response.add_header('Last-Modified', modification_time.strftime("%a, %d %b %Y %H:%M:%S"))
                response.add_header('Cache-Control', "max-age=7200")
                log(2,"Modification time is {}".format(mtime))
                print(request.headers)
                if 'If-Modified-Since' in request.headers:
                    import email.utils
                    if_modified_since_time = time.mktime(email.utils.parsedate(request.headers['If-Modified-Since'])) # unix time stamp
                    log(2,"mtime={}, ims_time={}".format(mtime, if_modified_since_time))
                    if int(mtime) <= int(if_modified_since_time):  # compare datetimes
                        log(1,"Yeah!")
                        response.send(code=304)
                        return
                    else:
                        log(1,"Oh no hit.")

                response.send(body=f.read())  # read and dump whole file
        except IOError:
            raise StopProcessing(404, "File not found: %s" % resource)

    def __str__(self):
        return "StaticApp - liefert unter /{} statische Dateien aus {} aus".format(self.prefix, self.path)