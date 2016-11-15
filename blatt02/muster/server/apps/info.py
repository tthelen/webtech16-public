from server.log import log
from server.webserver import App, StopProcessing

class InfoApp(App):
    """Print server info."""

    def register_routes(self):
        self.add_route("", self.info)

    def info(self, request, response, pathmatch):
        """List information on currently registered apps and routes."""
        body = ""
        body += "Info:\n\nRegistered Apps:\n\n"
        for a in self.server.apps:
            body += str(a) + " - " + a.__doc__+"\n"
        body+="\n"
        body += "Routes:\n\n"
        for r in self.server.routes:
            body+=r[0]+ " --> " + r[1].__doc__+"\n"
        response.set_content_type("text/plain")
        response.send(body=body)

    def __str__(self):
        return "InfoApp"