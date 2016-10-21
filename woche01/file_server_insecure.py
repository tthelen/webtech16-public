# Web-Technologien 2016
#
# file_server_insecure.py
# Simple File-Server. Attention! Contains severe security vulnerability!
#
# Tobias Thelen, 2016
# tobias.thelen@uni-osnabrueck.de
# Licence: Public Domain/CC-0 (https://creativecommons.org/publicdomain/zero/1.0/)
#

import socket
c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # prepare TCP socket
c.bind(('localhost', 8080))  # bind to port 8080
c.listen(5)  # listen for incoming connections

while 1:
    csock, caddr = c.accept() # wait for a connection and accept it

    conn = csock.makefile(mode='rwb', buffering=1) # create file-like access

    # We have to write the data as bytes not as utf-8 because that would
    # break binary files. So we always have to convert Python Strings (UTF-8)
    # to bytes and vice versa.

    def w(txt):
        """Decode as UTF-8 and write to client connection"""
        conn.write(bytes(txt, 'UTF-8'))

    # Read request
    while 1:
        request_line = conn.readline().decode('utf-8').strip()
        if request_line.strip():
            break
    method, resource, protocol = request_line.split(" ")
    print("Request: %s %s %s" % (method, resource, protocol))
    while True:
        header_line = conn.readline().decode('utf-8').strip()
        if not header_line:
            break
        (headerfield, headervalue) = header_line.split(":", 1)

    from urllib.parse import unquote
    resource = unquote(resource) # Path may contain urlencoded parts

    # open file as byte stream and read from file system
    try:
        f = open('static' + resource, 'rb')
    except IOError:
        w("HTTP/1.1 404 File not found\n\n")
        w("404 File not found: %s\n" % resource)
        print("Response: 404 File not Found")
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
        w("Connection: close\n")  # our server can't handle connection reuse
        w("Content-Type: %s\n" % content_type)
        w("\n")
        print("Response: 200 OK, Content-Type: {}".format(content_type))
        conn.write(f.read())  # read and dump whole file

    conn.close()
    csock.close()

