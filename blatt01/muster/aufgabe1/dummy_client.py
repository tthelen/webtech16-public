import socket
import base64

host = "httpbin.org"
port = 80
path = "/basic-auth/user/passwd"
#host="localhost"
#port=8080
#path="/secret"
username = "user"
password = "passwd"


def send_request(host, port, path, auth=None):
    """Send a request to connection file object f using path, host and authorization (if given)."""

    # Set up a TCP/IP socket
    c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect as client to a selected server
    # on a specified port
    c.connect((host, port))
    f = c.makefile(mode='rw', buffering=1)

    f.write("GET {} HTTP/1.1\n".format(path))
    f.write("Host: {}\n".format(host))
    f.write("Connection: Close\n")
    if auth:  # include Authorization header if auth is provided (must be ready-formatted Authorization-String
        f.write("Authorization: {}\n".format(auth))
        print("Authorization: {}".format(auth))
    f.write("\n")

    protocol, statuscode, reason = f.readline().split(" ", 2)

    # read headers
    headers = {}
    while True:
        try:
            (key, value) = f.readline().strip().split(":", 1)
            headers[key] = value
        except ValueError:
            break  # end of headers

    # read body
    body = f.read()

    f.close()
    c.close()
    return statuscode, headers, body


(statuscode1, headers1, body1) = send_request(host, port, path)

if statuscode1 == "401" and 'WWW-Authenticate' in headers1 and 'Basic' in headers1['WWW-Authenticate']:
    print("First attempt failed. Try again.")
    auth = "Basic " + base64.b64encode(bytes("%s:%s" % (username, password), 'utf-8')).decode('utf-8')
    print("Auth={}".format(auth))
    (statuscode2, headers2, body2) = send_request(host, port, path, auth)

    if statuscode2 != "200":  # second try did not work: abort
        print("Authorization failed!")
        print("Statuscode: {}".format(statuscode2))
        print("Headers: {}".format(headers2))
        print("Body: {}".format(body2))
        exit(1)

print("Success!")
print("Statuscode: {}".format(statuscode2))
print("Headers: {}".format(headers2))
print("Body: {}".format(body2))

# Close the connection when completed
print("\ndone")