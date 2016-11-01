# coding: utf-8
# Uni Osnabrück, Web-Technologien 2016
# Übungsblatt 0, Aufgabe 2
#
# Hinweise:
# 1. Sie müssen keine Autorennamen in den Quellcode schreiben, die Zuordnung erfolgt
# über Ihr github-Projekt.
# 2. Sie müssen Ihre Lösung nicht einreichen, es zählt der Stand des Repositories zum
# Abgabezeitpunkt.
# 3. Wollen Sie Teillösungen etc. nicht gleich in das Github-Projekt übernehmen, können
# Sie das Projekt klonen und die Änderungen später zusammenführen.
#
# Aufgabenstellung:
#
# Erstellen Sie ein Python-Programm, das eine fiktive Log-Datei eines
# Web-Servers einliest und daraus einfache Statistiken erstellt.
#
# Das Programm soll:
# - die Datei data.txt einlesen und evtl. auftretende Exceptions abfangen
# - die Werte aller drei Felder (Remote IP, Status Code, Path) in Dictionaries
#   aufsammeln und die Vorkommen zählen,
# - sowie am Ende die aufgesammelten Werte auf die Konsole ausgeben (print)
#
# Zu implementierende Einzelschritte:
#
# 0. Dictionaries für remote_ips, status_codes, paths initialisieren
# 1. Datei öffnen
# 2. Datei zeilenweise einlesen
#    2.1. Jede Zeile parsen, Fehler abfangen
#    2.2. Wenn kein Fehler: Daten in Dictionaries ablegen
# 3. Datei schließen
# 4. Unterschiedliche Remote IPs mit jeweiliger Häufigkeit ausgeben
# 5. Unterschiedliche Status Codes mit jeweiliger Häufigkeit ausgeben
# 6. Unterschiedliche Pfade mit jeweiliger Häufigkeit ausgeben

