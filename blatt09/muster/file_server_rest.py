from server.micro import MicroApp
from server.middlewares.rest_basic_auth import RestBasicAuthMiddleware  # Aufgabe 2
import os, uuid, json

app = MicroApp()
app.server.add_middleware(RestBasicAuthMiddleware(app.server))
datadir = 'data'
url_base = 'http://localhost:8080'


def construct_path(filename):
    """Prevent path traversal attacks: Is resulting path below desired datadir in file system?"""
    global datadir
    fn = os.path.abspath(datadir+'/'+filename)

    if fn.startswith(os.path.abspath(datadir)):
        return fn
    else:
        return None


def absurl(path, type=None):
    """Makes an absolute url from a path that may or may not start with /."""
    if not path.startswith('/'):
        path = '/' + path
    if type=='file':
        path = '/files' + path
    return url_base + path

@app.get('')
def index(request,response,pathmatch):
    """Produces a static list of available data types as urls.

    Currently:

    ['http://localhost:8080/files']

    """
    request.authenticate()
    response.send(code=200, body=json.dumps([absurl('files')]))


@app.get('files')
def index(request, response, pathmatch):
    """Produces a list of all files as hpyerlinks.

    Output:

    { files: [fileurl1, fileurl2, fileurl3] }

    """
    global datadir, url_base

    request.authenticate()

    files = os.listdir(datadir)
    response.send(code=200, body=json.dumps({'files':[absurl(f, type='file') for f in files]}))


@app.get('files/(?P<id>[0-9A-Za-z]+)')
def read(request, response, pathmatch):
    global url_base

    request.authenticate()

    filename = pathmatch.group('id')
    fn = construct_path(filename)
    if fn:
        with open(fn, "r", encoding='utf-8') as f:
            response.send(code=200, body=json.dumps({'id':filename,
                                                     'url': absurl(filename, type='file'),
                                                     'content': f.read()}))
    else:
        response.send(code=400, body=json.dumps({'error': 'Invalid filename'}))


@app.post('files')
def create(request, response, pathmatch):
    """Create new file. Filename is random uuid (hex)."""

    request.authenticate()

    if not request.jsondata or 'content' not in request.jsondata:
        response.send(code=400, body=json.dumps({'error':'Parameter content missing'}))
    else:
        filename = uuid.uuid4().hex
        fn = construct_path(filename)
        if fn:
            with open(fn, "w", encoding='utf-8') as f:
                f.write(request.jsondata['content'])
            response.send(code=200, body=json.dumps({'id':filename, 'url': absurl(filename, type='file')}))
        else:
            response.send(code=400, body=json.dumps({'error':'Invalid filename'}))


@app.put('files/(?P<id>[0-9A-Za-z]+)')
def create_or_update(request, response, pathmatch):
    """Create new file (if id does not exist so far) or update existing one."""

    request.authenticate()

    if not request.jsondata or 'content' not in request.jsondata or 'id' not in request.jsondata:
        response.send(code=400, body=json.dumps({'error':'Parameter content missing'}))
    else:
        filename = request.jsondata['id']
        fn = construct_path(filename)
        if fn:
            with open(fn, "w", encoding='utf-8') as f:
                f.write(request.jsondata['content'])
            response.send(code=200, body=json.dumps({'id':filename, 'url': absurl(filename, type='file')}))
        else:
            response.send(code=400, body=json.dumps({'error':'Invalid filename'}))


@app.delete('files/(?P<id>[0-9A-Za-z]+)')
def delete(request, response, pathmatch):

    request.authenticate()

    filename = pathmatch.group('id')
    try:
        os.unlink(construct_path(filename))
        response.send(code=200, body=json.dumps({'ok': True}))
    except OSError as error:
        response.send(code=500, body=json.dumps({'error': 'OS Error: {}'.format(error)}))


app.serve()
