import socket
import base64

c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # TCP socket vorbereiten
c.bind(('localhost', 8080))  # an Port 8080 binden
c.listen(1)  # auf hereinkommende Verbindungen lauschen

username = "user"
password = "passwd"

while 1:
    csock, caddr = c.accept()
    conn = csock.makefile(mode='rwb', buffering=1)

    def w(txt):
        """Decode as UTF-8 and write to client connection"""
        conn.write(bytes(txt, 'UTF-8'))

    # Read request
    request_line = conn.readline().decode('utf-8').strip()
    method, resource, protocol = request_line.split(" ")
    print("Request: %s %s %s" % (method, resource, protocol))
    headers={}
    while True:
        header_line = conn.readline().decode('utf-8').strip()
        if not header_line:
            break
        (headerfield, headervalue) = header_line.split(":", 1)
        headers[headerfield.strip()] = headervalue.strip()

    # check Authorization
    auth = False # not authorized
    if 'Authorization' in headers:
        try:
            (u, p) = base64.b64decode(headers['Authorization'].split(" ")[1]).decode('utf-8').split(":")
            if u == username and p == password:
                auth = True
        except ValueError:
            pass

    if not auth:
        w("HTTP/1.1 401 Authorization required\n")
        w('WWW-Authenticate: Basic realm="Provide correct credentials for webtech15"\n')
        w("\nDu darst nicht rein. Sag mir erst deinen Namen und dein Passwort.")
        conn.close()
        csock.close()
        continue

    # some protection from directory traversal attacks
    from urllib.parse import unquote
    resource = unquote(resource)
    if ".." in resource:
        w("HTTP/1.1 500 Internal Server Error\n\n")
        w("500 internal server error.\nDirectory traversal attack attempted.\n")
        conn.close()
        csock.close()
        continue

    try:
        f = open('static' + resource, 'rb')
    except IOError:
        w("HTTP/1.1 404 File not found\n\n")
        w("404 File not found: %s\n" % resource)
    else:
        # Write response
        w("HTTP/1.1 200 OK\n")
        import datetime
        w("Date: %s\n" % datetime.datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT"))

        # guess type from extension
        import mimetypes
        (content_type, encoding) = mimetypes.guess_type(resource)
        if not content_type:
            content_type = "text/plain"
        w("Connection: close\n")
        w("Content-Type: %s\n" % content_type)
        w("\n")
        conn.write(f.read())  # read and dump whole file

    conn.close()
    csock.close()

