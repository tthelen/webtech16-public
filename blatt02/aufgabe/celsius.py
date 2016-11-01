from server import webserver


class CelsiusApp(webserver.App):
    """
    Webanwendung zum Konvertieren von Celisus-Grad in Fahrenheit-Grad.

    Diese sehr einfache Anwendung demonstriert die Verwendung des Server-Frameworks.
    Die Klasse Celsius-App benötigt zwei Methoden:
    1. Registrierung der Routen
    2. Definition eines Request-Handlers
    """

    def register_routes(self):
        self.add_route('', self.celsius)  # there is only one route for everything

    def celsius(self, request, response, pathmatch=None):
        msg = ""
        if 'celsius' in request.params:  # check if parameter is given
            try:  # calculate
                fahrenheit = float(request.params['celsius']) * 9 / 5 +32
                msg = "{}° Celsius sind {:4.2f}° Fahrenheit".format(request.params['celsius'], fahrenheit)
            except (ValueError, TypeError):
                msg = "Bitte eine Zahl eingeben."
        response.send_template('templates/celsius/celsius.tmpl', {'msg':msg})

if __name__ == '__main__':
    s = webserver.Webserver()
    s.add_app(CelsiusApp(prefix='celsius'))
    s.serve()