import socket
import urllib.parse


def make_absolutepath(new_path, old_path):
    """Make an absolute pathname and handle relative paths.

    Examples:
        make_absolutepath('seite2.html','/index.html') = '/seite2.html'
        make_absolutepath('seite2.html','/somedir/index.html') = '/somedir/seite2.html'
        make_absolutepath('/seite2.html','/somedir/index.html') = '/seite2.html'
    """
    import os.path
    # new
    if not new_path or (new_path and new_path[0] != '/'):
        dir = os.path.dirname(old_path)
        return dir+'/'+new_path
    else:
        return new_path


def send_request(host, port, path):
    """Send a request to connection file object f using path, host and authorization (if given)."""

    # Set up a TCP/IP socket
    c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect as client to a selected server
    # on a specified port
    c.connect((host, port))
    f = c.makefile(mode='rwb', buffering=1)
    #print("Open {}:{}{}".format(host,port,path))
    f.write(bytes("GET {} HTTP/1.1\n".format(path), 'utf8'))
    f.write(bytes("Host: {}\n".format(host), 'utf8'))
    f.write(bytes("Connection: Close\n", 'utf8'))
    f.write(bytes("\n\n", 'utf8'))
    while 1:
        request_line = f.readline().decode('utf-8').strip()
        if request_line:
            break
    protocol, statuscode, reason = request_line.split(" ", 2)
    # read headers
    headers = {}
    while True:
        try:
            (key, value) = f.readline().decode('utf8').split(":", 1)
            headers[key.strip()] = value.strip()
        except ValueError:
            break  # end of headers

    # read body
    body = f.read().decode('utf8', 'ignore')
    f.close()
    c.close()
    return statuscode, headers, body


queue=[("tools.moocip.de", 80, "/crawl/index.html")]  # Page to start with (host, port, path)
visited = []  # List of already visited pages (neccessary for cycle check)
keyword = "Mond"  # Keyword to search for

while queue:  # as long as we still have pages to visit
    (host, port, path) = queue[0]  # extract first page from queue
    visited.append(queue[0])  # put it in "visited" list already (cycle check)
    (code, headers, body) = send_request(host, port, path)  # send request and fetch result, TODO: better error handling
    if code in ['301', '302', '303']:  # redirect
        url = urllib.parse.urlparse(headers['Location'])  # parse the Location header
        abspath = make_absolutepath(url.path, path)  # resolve relative URLs
        if url.netloc == host:  # only consider redirections to same host (TODO: discuss if that is the correct way)
            if not (url.netloc, port, abspath) in visited:  # cycle check
                queue.append((url.netloc, port, abspath))  # enqueue redirection
            # print("Redirect to {}".format(url.path))
        else:
            # print("Dead link: Redirect to {}:{} instead of {}:{}".format(url.hostname, url.port, host,port))
            pass
    elif code == '200':  # success
        import re

        # find search string
        clean_body = re.sub(r'<[^>]*>', '', body)  # remove any html tags
        if re.search(keyword, clean_body):
            print("HIT in {}".format(host+url.path))

        # find links to other pages
        links = re.findall(r'<a href="([^"]*)"', body)
        for link in links:
            url = urllib.parse.urlparse(link)
            if (not url.netloc or url.netloc != host) and '.html' in url.path:  # only html on same host
                abspath = make_absolutepath(url.path, path)
                if not (host, port, abspath) in visited and not (host, port, abspath) in queue:  # cycle check
                    queue.append((host, port, abspath))
                    # print("Append to queue (size: {}): ({},{},{})".format(len(queue), host,port,url.path))
    else:
        # print("Ignoring {}".format(code))
        pass
    queue = queue[1:]  # pop first item off queue

print("Done. {} pages scanned.".format(len(visited)))