from server.webserver import Webserver, App, StopProcessing
from sql_injection_model_sql import Person, db_setup

class SQLInjectionApp(App):
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
        persons = Person.find(lastname=request.params['data'])
        response.send(body="<br>".join([p.__str__() for p in persons]))

if __name__=='__main__':
    db_setup()
    s = Webserver()
    s.add_app(SQLInjectionApp())
    s.serve()