'''
Created on May 16, 2011

@author: tobias
'''

from server import webserver

class CookieTesterApp(webserver.App):

    def register_routes(self):
        self.server.add_route(r"", self.cookieTester)

    def cookieTester(self, request, response, pathmatch):

        try:
            n = request.cookies['name']
        except KeyError:
            n = "[kein Cookie gesetzt]"
        c = webserver.Cookie("name","tobias")
        response.add_cookie(c)
        response.send(body="Alter Zustand: %s" % n)
        
if __name__ == '__main__':
    print("Server running.")
    server = webserver.Webserver()
    server.add_app(CookieTesterApp())
    server.serve()
