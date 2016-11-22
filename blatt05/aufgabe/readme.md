Uni Osnabrück, Web-Technologien 2016

Übungsblatt 5
=============

Abgabefrist: bis Sonntag, 4.12.2016, 24 Uhr


Aufgabe 1 Erweiterung des Icon-Editors (14 Punkte):
---------------------------------------------------

Erweitern Sie den Icon-Editor um folgende Funktionen:

- Malen: Statt nur mit einzelnen Clicks auf Einzelzellen soll auch gemalt werden
  können, indem Sie mit gedrückter Maustaste über die Tabelle fahren und dabei
  alle berührten Zellen färben. (5 Punkte)
- Pinselbreite: Führen Sie die Eigenschaft "Pinselbreite" ein, die regelt, wie groß die
  gesetzten Punkte (derzeit immer 1x1 Zellen/Pixel) sind. Mit einem Schieberegler (Tipp: <input type="range">)
  soll es möglich sein, für die Pinselbreite einen Wert zwischen 1 und 10 einzustellen, der dann dergestalt
  berücksichtigt wird, dass ein Klick anschließend n x n Zellen/Pixel große Punkte erzeugt, wobei der Klickpunkt
  links oben im entstehenden Quadrat ist. (5 Punkte)
- Icons laden: Es soll rein clientseitig möglich sein, eines der unter "vorhandene Icons" angezeigten Icons
  per Klick in den Editor zu übernehmen, um es zu bearbeiten und unter gleichem oder neuem Namen zu speichern.
  (Sie müssen dazu ein Image-Objekt erstellen, das mit der Data-URL als Quelle versehen wird und nach dem Laden
  dieser Quelle auf den Canvas-Kontext angezeigt wird. Anschließend können Sie die Pixel per getImageData auslesen)
  (4 Punkte)

Hinweise:

- Benutzen Sie KEINE Javascript-Bibliotheken, auch kein jQuery
- Alle Erweiterungen kommen ohne Veränderung des Server-Codes aus. Sie können den Server-Code aber ändern,
  wenn dadurch Teilaufgabe 3 für Sie einfacher wird.
- In der Courseware gibt es zur Aufgabe ein Video, das die Musterlösung demonstriert.


Aufgabe 2: Psychotest (6 Punkte)
---------------------------

Entwickeln Sie eine reine Javascript-Anwendung, die alle vorhandenen Tests auflistet, einen Test daraus auswählbar
macht und dann nacheinander Fragen aus einer gegebenen Javascript-Datenstruktur darstellt. Der Nutzer klickt je Frage
eine Antwort an und bekommt dann die nächste Frage präsentiert. Jede Frage trägt in unterschiedlichem Maße zu einer
oder mehrerer der für diesen Test abgelegten Kategorien bei. Die Ergebnisse werden während des Tests ausgewertet und
am Ende eine Auswertung präsentiert, die der Kategorie mit den meisten Punkten entspricht. Haben mehrere Kategorien
die gleiche Punktzahl wird die Auswertung für "default" verwendet.

Features:
- Auswahl des Tests aus einer Liste (immer sichtbar oder beim Start bzw. nach Beendigung eines Tests) (1 Punkt)
- Präsentation der Fragen nacheinander und Möglichkeit, genau eine Antwort auszuwählen (3 Punkte)
- Aufsammeln der Ergebnisse und Präsentation der Auswertung am Ende eines Tests (2 Punkte)

Hinweise:
- Sie müssen nichts zwischenspeichern, wird die Seite neu geladen oder ein anderer Test gewählt, muss neu begonnen werden.
- Sie dürfen die Fragen gerne verändern, erweitern, korrigieren etc.
- In der Courseware gibt es zur Aufgabe ein Video, das die Musterlösung demonstriert.