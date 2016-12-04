Uni Osnabrück, Web-Technologien 2016

Übungsblatt 6
=============

Abgabefrist: bis Sonntag, 11.12.2016, 24 Uhr

_**Hinweis:** Alle Aufgabenteile sind im gleichen Code zu erledigen._


Aufgabe 1: Logging-Middleware (4 Punkte)
----------------------------------------

Implementieren Sie eine neue Middleware-Klasse im Verzeichnis server/middlewares, die genutzt werden
kann, um Server-Anfragen zu protokollieren. Verwenden Sie zur Protokollierung das typische
Common Log Format: https://www.w3.org/Daemon/User/Config/Logging.html#common-logfile-format

Die Protokollierung geschieht in eine konfigurierbare Datei, Default ist access_log im Verzeichnis logs.

Das Feld rfc931 wird hier nicht verwendet, sondern durch ein Minus-Zeichen "-" repräsentiert.

Das Feld authuser ist per default ebenfalls ein "-", soll aber bei der Authentizierung in Aufgabe 3
gefüllt werden.

Beispiel: Nutzer tobias ruft von 127.0.0.1 die Editier-Ansicht für die Wiki-Seite main auf und bekommt 
eine Response mit Status-Code 200 und einen Response-Body mit 4899 Bytes Länge ausgeliefert:

127.0.0.1 - tobias [2016-12-04 12:00:01] "GET /edit/main HTTP/1.1" 200 4899

Die Logfiles können mit verschiedenen CLF-Analysetools ( besonders hübsch: http://logstalgia.io ) 
analysiert werden.


Aufgabe 2: Umstellung auf Template-Engine (4 Punkte)
----------------------------------------------------

Die im Code zur Aufgabe enthaltene Wiki-Anwendung soll auf eine echte Template-Engine umgestellt 
werden. Sie können selbst wählen, ob Sie Jinja2 oder Mustache (pystache) verwenden. 

Sie können auch eine andere Engine verwenden (falls z.B. schon in Blatt 3 verwendet), müssen dann 
aber selbst Adapter-Code im Verzeichnis server/templating bereitstellen.

Anforderungen an die Template-Lösung:
- Vermeiden Sie Redundanzen so weit wie möglich
- Der Server-Code darf geändert werden
- Das hier verwendete Layout sollte erhalten bleiben

Aufgabe 3: Nutzerauthentifizierung für das Wiki (10 Punkte)
---------------------------------

Die Aktionen edit, save und delete sollen nur noch nach erfolgreicher Authentifizierung möglich
sein. Implementieren Sie dazu eine HTML-Form-basierte Authentifizierung und nutzen Sie Session-Cookies
und in der abgelegte Informationen.

Die Anforderungen:
- edit, save und delete sollen nur für angemeldete Nutzer möglich sein
- Die Login-Aufforderung ist "lazy", d.h. die Abfrage von Benuterzname und Passwort erscheint erst,
  wenn sie tatsächlich nötig ist. Anschließend bleibt der Nutzer eingeloggt.
- Der Login-Status soll an geeigneter Stelle sichtbar sein, für eingeloggte Nutzer soll auch der
  Benutzername angezeigt werden. 
- Es muss einen Nutzer mit Benutzername admin und Passwort admin geben.

Gestalten Sie die Authentifizierung so generisch wie möglich. Prüfen Sie, ob Sie Teile davon als
Middleware und/oder separate App gestalten können.

Für die Aufgabe ist keine komplette Benutzerverwaltung zum Anlegen und Verwalren von Nutzern gefordert. 
Es reicht z.B. eine Datei, in der Nutzername und Passwort abgelegt sind. Die liest das Programm dann 
aus und vergleicht.

Selbstverständlich darf das Passwort nicht im Klartext gespeichert werden, sondern nur kryptographisch 
verschlüsselt. Außerdem muss es einen Salt beinhalten, damit das verschlüsselte Passwort nicht über 
vorberechnete Hash-Tabellen angreifbar wird.

Ein Eintrag in der der Nutzerverwaltung enthält also:
- Benutzername
- Salt (Ein zufallswert)
- Verschlüsseltes Passwort (SHA256(salt+passwort))

Beim Login wird dann das eingegebene Passwort ebenfalls mit den Salt gehasht und die Hashwerte 
verglichen. Für das Hashen, die Salt-Generierung und das Vergleichen hilft Ihnen die eingebaute 
Python-Bibliothek crypt ( https://docs.python.org/3/library/crypt.html ).


Aufgabe 4: Logout (2 Punkte)
----------------------------

Als Ergänzung zu Aufgabe 3 soll es eine Aktion logout samt zugehörigem Button geben, die den 
Nutzer auf sichere Weise aus der Anwendung ausloggt.
