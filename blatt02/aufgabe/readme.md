Uni Osnabrück, Web-Technologien 2016

Übungsblatt 2
=============

Abgabefrist: bis Sonntag, 13.11.2016, 24 Uhr

_**Hinweis:** Sie sollten für die drei Aufgaben keine gesonderten Verzeichnisse 
oder Kopien von Dateien anlegen. Alle drei Aufgaben sollen parallel im
vorhandenen Code erledigt werden. Verwenden Sie dabei unbedingt die angegebenen 
Dateinamen._

Aufgabe 1 (8 Punkte): Info-App
----------------------

Implementieren Sie eine Info-App, die für den Entwickler wichtige
Informationen über den Server ausgibt. Die App soll folgende 
Informationen ausgeben:
* Liste der registrierten Apps mit kurzer Beschreibung (die Beschreibung könnte z.B. dem Doc-String einer 
App-Klasse entnommen werden. Sie dürfen die vorhandenen App-Klassen auch ändern.)
* Liste der registrierten Routen mit hilfreichen Informationen (selbst überlegen!)

Der Prefix-Mechanismus soll wie in den Beispielen funktionieren. 

Erstellen Sie ein starbares Programm `info.py`, dass folgendes URL-Schema implementiert:
* / - Allgemeine Begrüßungsseite (beliebigen begrüßenden Inhalts)
* /static - Statische Dateien
* /info - Zugriff auf die Info-App

Aufgabe 2: Caching für den File-Server (8 Punkte)
------------------------

Caching ist eine der wichtigsten Maßnahmen zur Beschleunigung von Webseiten. 
Für effektives Caching müssen häufig Webserver und -client zusammenspielen.
Eine der einfachsten Caching-Varianten ist "if-modified-since".

Dazu liefert zunächst der Server bei ausgelieferten Ressourcen, die gecached 
werden können sollen, den Response-Header:

    Last-Modified: Tue, 01 Nov 2016 12:45:26 GMT

mit. Die Zeitangabe gibt an, zu welchem Zeitpunkt die ausgelieferte Ressource
zuletzt modifiziert wurde und erfolgt im RFC-1123-Format.

Der Browser entscheidet nun selbst, ob die Ressource (= Body der Response) 
gechached werden soll. Falls ja, sendet er bei allen zukünftigen Anfrage
nach der gleichen Ressource folgenden Request-Header mit.

    If-Modified-Since: Tue, 01 Nov 2016 12:45:26 GMT
    
Der Zeitstempel ist identisch mit dem Last-Modified-Header-Wert, der 
vom Server für die gecachete Version der Ressource übermittelt wurde.

Der Server prüft nun durch Vergleich mit dem If-Modified-Since-Wert, 
ob eine jüngere Version der angefragten Ressource vorliegt. 

Falls ja, liefert er die Ressource vollständig aus und setzt dabei einen 
aktualisierten Last-Modified-Wert.

Falls nein, wird der Code

    304 Not Modified
    
zusammen mit allen Header-Zeilen generiert. Der Body wird in diesem Fall nicht
mitgesandt und der Browser verwendet die gecachete Version der Ressource. Requests,
die zu einem anderen Code als 200 führen würden (z.B. 404) werden wie gewohnt
ausgeliefert.

**Aufgabe:** Verändern Sie die File-Server-App `server/apps/static.py` so, dass sie If-Modified-Since-Caching unterstützt. 
Berücksichtigen Sie dabei:
* Als Modifikationsdatum soll das Modifikationsdatum der auszuliefernden Datei 
im Dateisystem verwendet werden (os.path.getmtime(path)).
* Fertigen Sie Screenshots an, die belegen, dass das Browser-Caching mit Ihrer #
modifizierten App funktioniert. Verwenden Sie zum Testen 
z.B. das Programm `fileserver.py`.

Aufgabe 3: Fahrenheit->Celsius (4 Punkte)
-------------------------

Erweitern Sie die Celsius-App in `celsius.py`um die Möglichkeit, 
auch in die entgegengesetzte Richtung zu konvertieren, also von Grad Fahrenheit 
in Grad Celisus. Die so entstehende App soll beide Möglichkeiten bieten.
Wie Sie das Interface realisieren, bleibt Ihnen überlassen (kein Javascript!).


