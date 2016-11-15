import server.webserver

class DummyApp(App):
    """A very silly simple App."""
    def register_routes(self):
        self.add_route("", self.dummy)

    def dummy(self, request, response, pathmatch):
        response.send(200, body="Huhuh, ich bin ein dummy.")

server = Webserver(8080)  # Initialize webserver on port 8080
server.add_app(DummyApp())  # register DummyApp without prefix
server.serve()  # listen for connections and serve
