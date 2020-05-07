import csv
from datetime import datetime
import pandas as pd
import requests
import re

def bereinigen(input):
    input = input.replace('null', '0')
    input = input.replace('],', ']')
    return eval(input)

# Checken, ob wir die heutigen Daten schon haben
today = datetime.today().date()
df = pd.read_csv('data/covid19_bz.csv')
last_row = df.tail(1)
last_scraped_date = datetime.strptime(last_row['datum'].values[0], '%Y-%m-%d').date()
if not last_scraped_date < today:
    quit()


# HTTP-Request absetzen
request = requests.get('https://afbs.provinz.bz.it/upload/coronavirus/chartDE.js')

# Antwort lesen und durch Regex schicken
matches = re.search(
    r"(columns:\[\s)([\[[\d',\[\] .a-zA-Zäöü\r\n]*]*)]",
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


with open('data/covid19_bz.csv', mode='w') as datei:
    # CSV-Parameter setzen
    writer = csv.writer(datei, delimiter=',', quoting=csv.QUOTE_ALL)
    writer.writerow(['datum','positiv_gesamt','positiv_delta','positiv_aktuell_gesamt','positiv_aktuell_delta','geheilt_gesamt','geheilt_delta','tot_gesamt','tot_delta'])
    
    # Tage durchloopen
    for i in range(1, len(x1)):
        datum = '{}.2020'.format(x1[i]) # Jahreszahl ergänzen, da sie im Original fehlt
        datum = datetime.strptime(datum, '%d.%m.%Y').date()

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
