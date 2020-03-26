import csv
import datetime
import requests
import re

def bereinigen(input):
    input = input.replace('null', '0')
    input = input.replace('],', ']')
    return eval(input)

# HTTP-Request absetzen
request = requests.get('http://www.provinz.bz.it/sicherheit-zivilschutz/zivilschutz/aktuelle-daten-zum-coronavirus.asp')

# Antwort lesen und durch Regex schicken
matches = re.search(
    r"(columns:\[\s)([\[[\d',\[\] .a-zA-Z\r\n]*]*)]",
    request.text
    )

# Die eigentlichen Daten stecken in der zweiten Capturegroup
html = matches.group(2).strip()

zeilen = list(map(bereinigen, html.split('\n')))

# Zuordnung der einzelnen Zeilen
x1 = zeilen[0]
x2 = zeilen[1]
x3 = zeilen[2]
x4 = zeilen[3]
positive = zeilen[4]
aktuell_positive = zeilen[5]
geheilt = zeilen[6]
tot = zeilen[7]


with open('/tmp/covid19_bz.csv', mode='w') as datei:
    # CSV-Parameter setzen
    writer = csv.writer(datei, delimiter=';', quoting=csv.QUOTE_ALL)
    writer.writerow(['datum','positiv_gesamt','positiv_delta','positiv_aktuell_gesamt','positiv_aktuell_delta','geheilt_gesamt','geheilt_delta','tot_gesamt','tot_delta'])
    
    # Tage durchloopen
    for i in range(1, len(x1)):
        datum = '{}.2020'.format(x1[i]) # Jahreszahl ergänzen, da sie im Original fehlt
        datum = datetime.datetime.strptime(datum, '%d.%m.%Y').date()

        # tägliche Gesamtzahlen
        p = positive[i]
        ap = aktuell_positive[i]
        g = geheilt[i]
        t = tot[i]

        # tägliche Deltas berechnen
        diff_p = (positive[i] - positive[i-1]) if type(positive[i-1]) == int else positive[i]
        diff_ap = (aktuell_positive[i] - aktuell_positive[i-1]) if type(aktuell_positive[i-1]) == int else aktuell_positive[i]
        diff_g = (geheilt[i] - geheilt[i-1]) if type(geheilt[i-1]) == int else geheilt[i]
        diff_t = (tot[i] - tot[i-1]) if type(tot[i-1]) == int else tot[i]

        # CSV-File schreiben
        writer.writerow([datum, p, diff_p, ap, diff_ap, g, diff_g, t, diff_t])
