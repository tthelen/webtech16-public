Uni Osnabrück, Web-Technologien 2016

Übungsblatt 7
=============

Abgabefrist: bis Mittwoch, 04.01.2017, 24 Uhr


Aufgabe 1: Orientierung (0 Punkte)
----------------------------------------

Starten Sie das hier enthaltene Personen- und Teamlisten-Programm über das Skript teamlist.py.
Im Auslieferungszustand ist das Programm mit einer vorgefüllten SQLite-Datenbank ausgestattet.
Wenn Sie MongoDB nutzen möchten ändern Sie Zeile 4 in:

    from model_mongodb import Person, Team

Testen Sie zunächst die Anwendung, betrachten Sie Personen- und Teamlisten und finden Sie heraus,
wo sich AJAX-Aktionen verbergen. Orientieren Sie sich anschließend im Code und identifizieren Sie zunächst die Controller, anschließend
die Views und zuletzt die Models (der Code ist schon bekannt).

Für die folgenden Aufgaben können Sie selbst entscheiden, ob Sie SQLite oder MondoDB verwenden. 
Achten Sie bei der Umsetzung auf eine Einhaltung des Model-View-Controller-Schemas. Sie dürfen
alle Code-Teile verändern oder erweitern.
 
Stellen Sie Fragen im Forum.


Aufgabe 2: Anlegen von Nutzern und Teams (14 Punkte)
----------------------------------------------------

Ermöglichen Sie es, neue Nutzer und Teams anzulegen.  Dazu gehört auch die Eingabe mehrerer Hobbies und die
Zuordnung von Personen zu Teams und andersrum. All diese Operationen müssen über AJAX-Requests realisiert werden
und Listen sollen sofort nach Neuanlegen aktualisiert werden.

Diese Aufgabe lässt Ihnen viel Gestaltungsspielraum. Sie erhalten die volle Punktzahl, wenn Ihre Lösung
die Anforderungen den Buchstaben nach (sie muss also nicht hübsch oder elegant sein) erfüllt.

Aufgabe 3: Löschen (6 Punkte)
---------------------------------

Ermöglichen Sie es, dass durch Klick auf rote x-Symbole, die neben den Elementen angebracht sind, folgende
 Elemente mittels AJAX-Requests gelöscht werden können:
 
 * Zuordnungen von Personen zu Teams und Teams zu Personen
 * Einzelne Hobbies
 * Ganze Teams
 * Personen
 
Diese Aufgabe lässt Ihnen viel Gestaltungsspielraum. Sie erhalten die volle Punktzahl, wenn Ihre Lösung
die Anforderungen den Buchstaben nach (sie muss also nicht hübsch oder elegant sein) erfüllt.
