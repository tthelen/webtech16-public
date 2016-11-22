Uni Osnabrück, Web-Technologien 2016

Übungsblatt 4
=============

Abgabefrist: bis Sonntag, 27.11.2016, 24 Uhr


Aufgabe 1: Weiterleitungs-Countdown (12 Punkte)
---------------------------------------

Entwickeln Sie eine HTML-/Javscript-Anwendung (d.h. es ist kein aktiver Server-Code erforderlich), die einen Countdown
einblendet und nach Ablauf des Countdown auf eine andere Webseite weiterleitet.

Zunächst werden Datum und Uhrzeit sowie eine Weiterleitungsadresse (URL) eingegeben. Nach Absenden des Formulars
(Submit-Knopf) verschwindet das Formular und ein großer Countdown wird eingeblendet, der sekundenweise die Zeit bis
zum Erreichen des eingegebenen Zeitpunktes herunterzählt. Wenn diese Zeit erreicht oder schon verstrichen ist, wird
auf die eingegebene Adresse weitergeleitet oder, falls keine eingegeben wurde, auf eine von Ihnen bestimmte
Default-Adresse.

Hinweise:
- Sie können von Javascript aus auf eine andere Seite umleiten, indem Sie die location-Eigenschaft des windows-Objektes
  setzen.
- Mit windows.setInterval(callback, ms) können Sie eine Funktion (callback) registrieren, die anschließend
  alle ms Millisekunden aufgerufen wird.
- Für Zeit- und Datumsoperationen können Sie das Javascript-Date-Objekt verwenden.
- Benutzen Sie nur reines Javascript, keine Zusatzbibliotheken.
- Es gibt ein kurzes Demo-Video im Courseware-Abschnitt für Woche 4, das zeigt, wie die Lösung aussehen kann.


Aufgabe 2: Stud.IP-Bookmarklet (8 Punkte)
---------------------------------

Ein Bookmarklet ist ein Browser-Bookmark das Javascript-Code enthält. Dazu wird das Pseudo-Schema javascript: verwendet.

Wenn Sie folgendes in die Browser-Zeile eintippen, bekommen Sie ein Hinweisfenster mit der Meldung "42":

javascript:alert(42);

Eine solche Zeile lässt sich über die Bookmark-Verwaltung auch als Bookmark ablegen, allerdings sollte dort in der
Regel am Ende noch undefined; stehen, damit das Resultat des Ausdrucks "undefined" ist - in diesem Fall öffnet der
Browser keine neue Seite.

Erstellen Sie ein Bookmarklet, das bei geöffneter Stud.IP-Seite das Stud.IP-Logo oben rechts gegen Ihren Benutzernamen
austauscht. Der Benutzer- oder Loginname (z.B. tthelen) sollte weiß dargestellt werden und ungefär in der gleichen
Größe wie das Logo erscheinen.

Reichen Sie das Bookmarlet als Text-Datei ein und legen Sie einen Screenshot bei, der zeigt, wie das Resultat bei Ihnen
aussieht.

Hinweise:
- Zum Entwickeln und Testen können Sie auch die Javscript-Konsole in den Developer-Tools verwenden.
- Der Benutzername steht auf jeder Seite ganz links unten "Sie sind angemeldet als ...".
- Es gibt ein kurzes Demo-Video im Courseware-Abschnitt für Woche 4, das zeigt, wie die Lösung aussehen kann.

