#!/usr/local/bin/python
# coding: utf-8

"""
aufgabe-00-02.py

Musterlösung zu Aufgabe 1, Blatt 0

@author: Tobias Thelen
@contact: tobias.thelen@uni-osnabrueck.de
@licence: public domain
@status: completed
@version: 1 (04/2015)
"""

# Dictionary, das die zu zählenden Ressouren beinhaltet
resources = {}
ips = {}
codes = {}

# with-Statement vereinfacht Exception-Handling mit Dateien etc. und sorgt
# dafür, dass sie auf jeden Fall korrekt geschlossen werden
with open("data.txt", "r") as f:
    # for-Schleife über geöffnete Datei iteriert zeilenweise
    for entry in f:
        try:
            (ip, code, resource) = entry.strip().split(":")
        except ValueError:  # not enough or too much values to unpack (malformed entries)
            continue
        if resource in resources:
            resources[resource] += 1
        else:
            resources[resource] = 1

        if code in codes:
            codes[code] += 1
        else:
            codes[code] = 1

        if ip in ips:
            ips[ip] += 1
        else:
            ips[ip] = 1

print("Resources:\n")
for (k, v) in resources.items():
    print("%3d: %s" % (v, k))
print("Codes:\n")
for (k, v) in codes.items():
    print("%3d: %s" % (v, k))
print("IPs:\n")
for (k, v) in ips.items():
    print("%3d: %s" % (v, k))
