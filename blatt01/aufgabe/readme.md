Uni Osnabrück, Web-Technologien 2016

Übungsblatt 1
=============

Abgabefrist: bis Sonntag, 06.11.2016, 24 Uhr


Aufgabe 1 (18 Punkte): http Basic-Authentifizierung
----------------------

Bei der http Basic-Authentifizierung schützt ein Webserver eine Ressource und erlaubt den Zugriff erst nach Übermittlung eines korrekten Paares von Benutzername und Passwort. Diese einfache und weit verbreitete Authentifizierungsmethode ist daran zu erkennen, dass der Browser den Nutzer mit einem eigenen Fenster nach Benutzername und Passwort fragt und das Eingabefeld nicht Bestandteil der Webseite ist.

In dieser Aufgabe sollen Sie:

* den Webserver (file_server.py) so modifizieren, dass alle Ressourcen mit http Basic Auth geschützt sind (12 Punkte)
* den Webclient (dummy_client.py) so modifizieren, dass er per http Basic Auth geschützte Ressourcen erkennen und dann abrufen kann (6 Punkte)

Die Authentifizierung besteht aus 4 Schritten:

1. Der Client fordert eine Ressource an (hier: test.html):

    `GET /test.html HTTP/1.1`

2. Der Server teilt mit, dass die Ressource geschützt ist:

    `HTTP/1.1 401 Not Authorized`
    
    `WWW-Authenticate: Basic realm="Ein Hinweis, was der Nutzer tun soll"`

    `...der folgende Content wird angezeigt, wenn Authentifizierung fehlschlägt und Nutzer im Browser abbricht...`

    Das Header-Feld muss `WWW-Authenticate` heißen und zwei durch Leerzeichen getrennte Angaben enthalten:

    1. `Basic` (Bezeichnet das Authentifizierungsverfahren)
    2. `realm="...irgendein Text..."` (Text, der vom Browser als Hinweis angezeigt wird)

3. Der Client erkennt den 401-Code und wiederholt seine Anfrage, ergänzt um ein Authorization-Header-Feld:

    `GET /test.html HTTP/1.1`
    
    `Authorization: Basic YmVudXR6ZXI6cGFzc3dvcnQ=`

    Das Header-Feld muss `Authorization` heißen und zwei durch Leerzeichen getrennte Angaben enthalten:

    1. `Basic` (Bezeichnet das Authentifizierungsverfahren)
    2. Base64-codierte Angabe von Nutzername und Passwort, die in Python wie folgt gebildet wird: `base64.b64encode(username+":"+password)`

4. Der Server liefert die Ressource aus oder wiederholt Schritt 2
    * Sind die übergebenen Authentifizierungsinformationen korrekt (`base64.b64decode()` dekodiert die Angabe wieder), wird die Ressource wie gewohnt mit Code `200 OK` und ohne `WWW-Authenticate-Feld` ausgeliefert.
    * Sind die übergebenen Authentifizierungsinformationen nicht korrekt, wird die Ausgabe von Schritt 2 wiederholt. Es gibt kein definiertes Ende dieser Schleife.

Hinweise:

* Die angegebenen Request- und Response-Beispiele sind nicht vollständig (Date-Feld, Host-Feld usw. fehlen)
* Sie können Benutzername und Passwort im Server hart kodieren (keine Passwort-Datei o.ä.)
* Der Client soll Code 401 und den WWW-Authenticate-Header erkennen und erst daraufhin die Authentifizierungsinformationen senden (statt einfach immer den Authenticate-Header mitzusenden)
* Der Prozess soll auch funktionieren, wenn Schritt 2 übersprungen wird (Browser merken sich z.B. für die laufende Session die eingegebenen Authentifizierungsinformationen und liefern sie nach der Ersteingabe automatisch mit)
* Testen Sie den Server mit einem Browser und dem modifizierten Client
* Testen Sie den Client mit dem modifizierten Server und einer fremden geschützten Ressource, z.B. http://httpbin.org/basic-auth/user/passwd (user und password können durch beliebige Benutzernamen/Passwort ersetzt werden, s. http://httpbin.org)

Zur Abgabe müssen Sie die Aufgabe nicht absenden, es zählt der Stand des Repositories am 06.11.2016, 24 Uhr.

Aufgabe 2: Simple Crawler (2 Punkte)
------------------------

**Achtung!** Die Aufgabe ist schwierig. Es gibt nur zwei Punkte, weil sie als Zusatzaufgabe für diejenigen gedacht ist, die sich mit Aufgabe 1 langweilen.

Modifizieren Sie den Client (dummy_client.py) so, dass er eine Website (d.h. eine zusammenhängende Menge von Webseiten unter einer Domäne) rekursiv nach einem Suchbegriff durchsucht.

Vorgehen:
* Setzte Host, Port und Suchbegriff
* Initialisiere die Queue noch zu besuchender Pfade mit dem Startpfad
* Solange Queue nicht leer:
    * Lese Response auf Get-Request an (Host,Port,Startpfad)
    * Wenn Weiterleitung (Code 301,302,303) und `Location`-Header-Feld zeigt auf gleichen Host:
        * Füge Pfad-Wert des `Location`-Feldes an Queue an (`urllib.parse.urlparse` kann genutzt werden, um URIs zu parsen).
    * Sonst, wenn Code=`200 OK`:
        * Wenn Suchbegriff in Body enthalten (Body der Response ist die gesamte HTML-Seite, zum Durchsuchen alle HTML-Tags löschen): Gebe Treffer-Nachricht und URL aus
        * Suche alle Links (Muster: &lt;a href="LINK"&gt;) auf der Seite
        * Für alle Links:
            * Wenn Link auf gleichen Host/Port zeigt und Link mit .html endet und Link noch nicht besucht und noch nicht in Queue:
                * Füge Pfad des Links an Queue an.
    * Sonst: Ignoriere Ergebnis
* Gebe Zusammenfassung aus: Anzahl gescannter Seiten und Anzahl der Treffer.

Tipps:
* Lesen Sie die Response als Byte-Strom und verwenden Sie dann `f.read().decode('utf8', 'ignore')` um den gelesenen Text als UTF-8 zu codieren und evtl. Fehler dabei zu ignorieren. Das ist zwar unsauber (z.B. können Sie dann Umlaute auf Latin-1-codierten Seiten nicht finden), ein vollständiges Handling der Seitencodierung ist aber sehr aufwendig.
* Benutzen Sie `re.findall` mit einem geeigneten regulären Ausdruck zum Suchen der Links
* Sie müssen zwischen absoluten und relativen Links unterscheiden. `os.path.dirname` liefert Ihnen den Verzeichnis einer Pfadangabe.
* Zum Testen können Sie mit der Startseite `http://tools.moocip.de/crawl/index.html` nach dem String `Mond` suchen. Sie sollten insgesamt 6 Seiten durchsucht haben und 3 Treffer finden.

Zur Abgabe müssen Sie die Aufgabe nicht absenden, es zählt der Stand des Repositories am 06.11.2016, 24 Uhr.
