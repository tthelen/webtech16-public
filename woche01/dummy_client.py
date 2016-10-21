# Web-Technologien 2016
#
# dummy_client.py
# Very simple web client.
#
# Tobias Thelen, 2016
# tobias.thelen@uni-osnabrueck.de
# Licence: Public Domain/CC-0 (https://creativecommons.org/publicdomain/zero/1.0/)
#
import socket

# Host, port and path as global variables
host = "www.informatik.uni-osnabrueck.de"
port = 80
path = "/institut_fuer_informatik.html"

c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # create TCP socket

c.connect((host, port))  # try to connect to remote host/port
f = c.makefile(mode='rw', buffering=1)  # create file-like access to connection

f.write("GET {} HTTP/1.1\n".format(path))  # send request line
f.write("Host: {}\n".format(host))  # send request headers
f.write("Connection: Close\n")
f.write("\n")

while 1:  # read entire response and print it line for line
    resp = f.readline()  # readline will return empty string on end of file
    if resp=="": break
    print(resp[:-1])  # omit \n (print adds own \n)

c.close()  # done
print("\nDone.")
