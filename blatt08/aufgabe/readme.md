Uni Osnabrück, Web-Technologien 2016

Übungsblatt 8
=============

Abgabefrist: bis Mittwoch, 11.01.2017, 24 Uhr

Aufgabe 1 (15 Punkte): Sicherheitslücken in "Buggy MiniTwitter"
---------------------------------------------------------------

Im Aufgabenordner befindet sich eine Anwendung namens "MiniTwitter", die es Nutzern erlaubt, 
kurze Nachrichten abzusenden, die dann allen Nutzern angezeigt werden. 

Es gibt folgende Features:
- Nur angemeldete Nutzer dürfen Nachrichten schreiben. 
- Das Login erfolgt "lazy", d.h. erst, wenn eine Aktion es nötig macht.
- Es gibt normale Nutzer und Admins.
- Admins haben zusätzlich Zugriff auf eine Usermanagement-App.
- In der Usermanagement-App werden alle Nutzer angezeigt. Sie können gelöscht 
  und neue Nutzer angelegt werden.
- Die Nutzerdaten sind in einer SQL-Datenbank abgelegt. Die Passwörter werden ungehasht 
  und ohne Salt gespeichert, diesen Fehler müssen Sie nicht melden oder beheben. Vielleicht
  finden Sie aber einen Weg, ihn auszunutzen?
- Die Minitwitter-Daten sind in einer Datei abgelegt.

Untersuchen Sie die MiniTwitter-Anwendung auf die in der Vorlesung vorgestellten (und ggf. weitere) 
Sicherheitslücken. Gesucht werden dabei lediglich Sicherheitslücken, die in der Anwendung bzw. dem 
Servercode selbst liegen. Allgemeinere Probleme wie der Schutz gegen Denial-of-Service-Angriffe etc. 
sind nicht gemeint. 

Finden Sie (mindestens) 5 Sicherheitsprobleme, die Sie in der Datei bugs.txt dokumentieren und jeweils wie folgt angehen:

1. Bennung und Kurzbeschreibung der Sicherheitslücke anhand der in der Vorlesung vorgestellten Kategorien
2. Demonstration der Lücke, entweder durch Selenium-Tests oder Screenshots. Eine bloße Beschreibung, welche Eingabe zu Probleme führt, reicht nicht aus.
3. Beseitigung der Lücke. CSRF-Lücken werden durch Aufgabe 2 beseitigt.

Aufgabe 2 (5 Punkte): CSRF-Middleware
-------------------------------------

Implementieren Sie eine CSRF-Middleware zur systematischen Schließung von CSRF-Lücken. Der Schutz soll mithilfe
 von CSRF-Token funktionieren, die bei der Entgegennahme jedes POST-Requests geprüft werden. 
 
Um vor CSRF-Lücken geschützt zu sein, muss eine Anwendung folgendes tun:

1. Die CSRF-Middleware aktivieren.
2. In jedes POST-Formular ein gültiges CSRF-Token einfügen.

Ihre gesamte Implementation gehört in eine gesonderte Datei `server/middlewares/csrf.py`, Sie sollten den Code des
sonstigen Webservers nicht verändern. Eine Ausnahme ist die Art und Weise, wie die Template-Engine Zugriff auf die 
CSRF-Token bekommt. Sie können entweder an jeder Stelle in nutzenden Apps das Token mit übergeben, oder (empfohlen!)
in der Methode `response#send_template` das Dictionary vor Übergabe an die Templating-Engine erweitern. Diese 
Erweiterung soll aber allgemeingültig sein und nicht speziell auf die CSRF-Middleware zugeschnitten sein, d.h.
Sie könnten z.B. das server-, request-, session- oder response-Objekt immer in das Template-Dictionary aufnehmen. 

