from server.webserver import Middleware


class LoggingMiddleware(Middleware):
    """Add a session attribute to request."""

    def __init__(self, logfile="logs/access_log"):
        self.logfile = logfile
        self.request = None
        super().__init__()

    def process_request(self, request, response):
        self.request = request  # we'll need it in processing the response

    def process_response(self, response):
        """Write log file entry."""

        import datetime
        now = str(datetime.datetime.now()).split('.')[0]  # standard string representation of current date and time
        if response.body:
            length=len(response.body)
        else:
            length=0

        with open(self.logfile, "a") as file:
            file.write(self.request.caddr[0]+" ")  # address
            file.write("-" + " ")  # stays empty
            if self.request.user:
                file.write(self.request.user+" ")
            else:
                file.write("-" + " ")  # authenticated user # TODO aufgabe 4
            file.write("[{}] ".format(now))  # now
            file.write('"{} {} {}" '.format(self.request.method, self.request.resource, self.request.protocol))  # request line
            file.write(str(response.code)+" ")   # response code
            file.write(str(length)+"\n")  # response body length
