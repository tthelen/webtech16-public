# Web-Technologien 2016
#
# dummy_server.py
# Very simple web server. Always serves the same response, regardless what request says.
#
# Tobias Thelen, 2016
# tobias.thelen@uni-osnabrueck.de
# Licence: Public Domain/CC-0 (https://creativecommons.org/publicdomain/zero/1.0/)
#
import socket
c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # prepare TCP socket
c.bind(('localhost', 8080))  # bind to port 8080
c.listen(1)  # listen for incoming requests

while 1:
    csock, caddr = c.accept()  # accept connection (csock is socket object, caddr is client address)
    conn = csock.makefile(mode='rw', buffering=1, errors='ignore')  # create file-like access

    # Read request
    request_line = conn.readline().strip()
    method, resource, protocol = request_line.split(" ")
    print("Request: %s %s %s" % (method, resource, protocol))  # log output to console
    while True:  # read, check and ignore headers
        header_line = conn.readline().strip()
        if not header_line:
            break
        (headerfield, headervalue) = header_line.split(":", 1)
        print("Header: %s: %s" % (headerfield.strip(), headervalue.strip()))

    # Write response
    conn.write("HTTP/1.1 200 OK\n")
    import datetime
    conn.write("Date: %s\n" % datetime.datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT"))  # rfc1123 compatible time representation
    conn.write("Content-Type: text/html\n")
    conn.write("Connection: close\n")
    conn.write("\n")  # extra leerzeile schliesst header ab

    conn.write("""
        <html>
            <head>
            <title>Dummy Webserver Info</title>
            </head>
        <body>
            <h1>Dummy Webserver Info</h1>
            <p>Der Webserver l&auml;uft auf Host %s und Port %s.</p>
        </body>
    """ % ('localhost', 8080))

    conn.close()
    csock.close()
