from server.webserver import Webserver, App
from server.micro import MicroApp

data = {    # ugly: we provide some kind of quirky in-memory-database
    '1': { 'id': 1, 'title': 'TODOs erledigen', 'completed': False },
    '2': { 'id': 2, 'title': 'Neue TODOs eintragen', 'completed': False },
    '3': { 'id': 3, 'title': 'Sonne einschalten', 'completed': True}
}

# GET /todo  - Collection lesen
# GET /todo/123  - einen TODO-Eintrag lesen
# POST /todo - neuen Eintrag anlegen
# PUT /todo/123 - Eintrag updaten
# DELETE /todo/123 - Eintrag löschen
#
# Server kann jetzt JSON-Bodies verarbeiten
# request.jsondata - deserialisierte/geparste JSON

app = MicroApp()

@app.get('')
def index(request, response, pathmatch):
    """Show index page"""
    response.send_redirect('/static/index.html')


@app.get('todo')
def read_todos(request, response, pathmatch):
    """Read collection."""
    response.send_json(data=list(data.values()))


@app.post('todo')
def create_todo(request, response, pathmatch):
    """Create new todo."""
    print(data)
    nextid = int(sorted(data)[-1])+1
    todo = { 'id': nextid,
             'title': request.jsondata.get('title', 'No title yet'),
             'completed': request.jsondata.get('completed', False)}
    data["{}".format(nextid)] = todo
    response.send(code=200, body='')


@app.get('todo/(?P<id>[0-9]+)')
def read_todo(request, response, pathmatch):
    """Read single todo."""
    id = pathmatch.group('id')
    response.send_json(data=data[id])


@app.put('todo/(?P<id>[0-9]+)')
def update_todo(request, response, pathmatch):
    """Update todo."""
    id = pathmatch.group('id')
    todo = { 'id': id,
             'title': request.jsondata.get('title', data[id]['title']),
             'completed': request.jsondata.get('completed', data[id]['completed'])}
    print(todo)
    data[id] = todo
    response.send_json(data=data[id])


@app.delete('todo/(?P<id>[0-9]+)')
def delete_todo(request, response, pathmatch):
    """Delete todo."""
    id = pathmatch.group('id')
    del data[id]
    response.send(code=200, body='')

app.server.set_templating("pystache")
app.server.set_templating_path("templates.mustache")

app.serve()

