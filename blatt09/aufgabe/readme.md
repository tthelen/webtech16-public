Uni Osnabrück, Web-Technologien 2016

Übungsblatt 9
=============

Abgabefrist: bis Mittwoch, 18.01.2017, 24 Uhr

Aufgabe 1 (15 Punkte): Dateien neu anlegen, editieren und löschen
------------------------------------------------------------------

Vervollständigen Sie die im Client-Interface bereits angelegten Funktionen
zum Anlegen, Bearbeiten und Löschen von Dateien. Die Anwendung soll weiterhin
als Single-Page-App funktionieren. Fehlende REST-Routen im Server sind ggf. zu 
ergänzen. Die Bearbeitung des Dateiinhaltes soll in einer Textarea geschehen.


Aufgabe 2 (5 Punkte): Authentifizierung
---------------------------------------

Versehen Sie das gesamte REST-Interface (alle Routen) mit einer 
http-Basic-Authentifizierung, die den Nutzer einmalig nach Zugangsdaten 
fragt. Sie dürfen dabei Code aus Vorwochen verwenden.

Sie benötigen folgendes:
1. Auf Server-Seite eine Datenbank (Datei) mit Benutzernamen und Passwörtern.
2. Auf Client-Seite eine Abfrage von Benutzername und Passwort
3. Auf Client-Seite eine Codierung der Zugangsdaten und Übergabe den die AJAX-Requests, 
   z.B. per setRequestHeader)
4. Auf Server-Seite eine Überprüfung der Zugangsdaten (wie bereits umgesetzt).