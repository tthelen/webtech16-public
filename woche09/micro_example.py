from server.micro import MicroApp

app = MicroApp()


@app.get('')
def index(request, response, pathmatch):
    response.send(body="""<!DOCTYPE html><html><body>
           Ahoi!
           <form action='greet' method='POST'>
           <input type=text name=name>
           </form></body></html>""")


@app.post('greet')
def greet(request, response, pathmatch):
    response.send(body="""
       <!DOCTYPE html><html><body>
           Ahoi {}!
         </body></html>""".format(request.params['name']))


app.serve()