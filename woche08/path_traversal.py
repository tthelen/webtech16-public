from server.webserver import Webserver, App, StopProcessing


class PathTraversalApp(App):
    """App vulnerable to path traversal attacks.

    Should deliver files from the data directory but can easily be
    abused to deliver any file that current process can read."""

    def register_routes(self):
        self.add_route("", self.show_form)
        self.add_route("data", self.show_data)

    def show_form(self, request, response, pathmatch):
        response.send(body="""
        <!DOCTYPE html>
        <html>
          <body>
            <form action='/data' method=get>
              <input type=text name=data>
            </form>
          </body>
        </html>""")

    def show_data(self, request, response, pathmatch):
        filename = request.params['data']

        import re
        if not re.match(r"[a-zA-Z0-9_-]+", filename):
            raise StopProcessing(400, "Invalid data parameter.")

        import os.path
        datapath = os.path.abspath("data")
        path = os.path.abspath("data/"+filename)
        if not path.startswith(datapath):
            raise StopProcessing(400, "Directory Traversal attack.")

        with open(path, "r") as f:
            response.send(body=f.read())

if __name__=='__main__':
    s = Webserver()
    s.add_app(PathTraversalApp())
    s.serve()