#!/usr/bin/env python
""" Script to parse daily covid-19 data from official press releases and write/append to csv

"""

import feedparser
import os
import pandas as pd
import re
import requests

from bs4 import BeautifulSoup
from datetime import date
from datetime import datetime



def get_pressrelease_url():
    """ Parse the provincial RSS feed and returns the URL of the latest press release which includes updated numbers
        Parameters:
            None
        Output:
            Date of press release in ISO format
            URL to press release containing latest covid-19 data for South Tyrol. If nothing was found, return None
    """

    feed = feedparser.parse('http://www.provinz.bz.it/news/de/news.asp?news_action=201&news_cate_id=750')

    for item in feed.entries:
        pubdate_hour = item.published_parsed.tm_hour
        # Press releases are always published around 10am
        today = date.today().isoformat()
        pubdate = '{}-{:0>2d}-{:0>2d}'.format(item.published_parsed.tm_year, item.published_parsed.tm_mon, item.published_parsed.tm_mday)
        # if item was published today between 8am and 1pm, it could be a press release
        if 7 < pubdate_hour < 18 and pubdate == today:
            text_to_search = '{} {}'.format(
                item.title,
                item.description
            ).lower()

            # Search for common used words
            words = ['daten', 'gesamtzahl', 'zahlen', 'anzahl', 'aktualisiert', 'aktuell', 'abstriche', 'geheilte', 'corona', 'coronavirus']
            if any(x in text_to_search for x in words):
                # Potential hit! Fetch the content to be sure
                request = requests.get(item.link)
                if 'Die Zahlen' in request.text:
                    # Bingo!
                    return pubdate, item.link
    return None


def get_numbers_from_pressrelease(url, date=datetime.today().strftime('%Y-%m-%d')):
    """ Pull latest covid-19 data from daily press release.
        Parameters:
            URL (str):  URL to press release (usually will be obtained by get_pressrelease_url())
            Date (str): optional date (format: YYYY-MM-DD) for which the obtained data will be saved to
        Currently supported fields:
            deceased_total              Verstorbene insgesamt
            hospitalized_icu            Covid-19 Patientinnen und Patienten in Intensivbetreuung
            hospitalized_normal         Auf Normalstationen und in Gossensaß untergebrachte Covid-19-Patienten/Patientinnen/Personen
            hospitalized_suspicious     Als Verdachtsfälle Aufgenommene
            isolated_current            Personen in Quarantäne/häuslicher Isolation
            isolated_released           Personen, die Quarantäne/häusliche Isolation beendet haben
            isolated_total              Personen betroffen von verordneter Quarantäne/häuslicher Isolation
            positive_delta              Positiv getestete neue Personen
            positive_familydoctors      Positiv getestete Basis- und Kinderbasisärzte
            positive_sabes_employees    Positiv getestete Mitarbeiter und Mitarbeiterinnen des Sanitätsbetriebes
            positive_total              Gesamtzahl mit neuartigem Coronavirus infizierte Personen
            recovered_total             Geheilte insgesamt
            swabs_delta                 Untersuchte Abstriche gestern
            swabs_total                 Gesamtzahl der untersuchten Abstriche
            tested_total                Gesamtzahl der getesteten Personen
        Output:
            None
    """

    fields = {
        'deceased_total' : None,
        'hospitalized_icu' : None,
        'hospitalized_normal' : None,
        'hospitalized_suspicious' : None,
        'isolated_current' : None,
        'isolated_released' : None,
        'isolated_total' : None,
        'positive_delta' : None,
        'positive_familydoctors' : None,
        'positive_sabes_employees' : None,
        'positive_total' : None,
        'recovered_total' : None,
        'swabs_delta' : None,
        'swabs_total' : None,
        'tested_total' : None,
    }

    # Get press release HTML code and parse it with BS4
    request = requests.get(url)
    html = request.text
    soup = BeautifulSoup(html, features='html.parser')

    # Find main text
    artikel = soup.find(id='artikel')

    # Find all <p> in main text and loop through them. We want every <p> after "Die Zahlen in Kürze"
    zik = False
    p_list = []
    for p in artikel.find_all('p'):
        if zik is True:
            p_list.append(p.text)
        else:
            if 'Die Zahlen i' in p.text:
                zik = True

    # Loop through <p> and try to scrape known fields
    for datapoint in p_list:
        fieldname = None
        try:
            key, value = datapoint.split(':', maxsplit=1)
            key = key.lower()
            value = value.strip()
            value = value.replace('\xa0', ' ')
            value = value.replace('.', '')
            value = re.sub('[\(\[].*?[\)\]]', '', value)
        except ValueError:
            continue

        if 'gesamtzahl der untersuchten abstriche' in key:
            fieldname = 'swabs_total'
            value = value
        elif 'abstriche gestern' in key:
            fieldname = 'swabs_delta'
            value = value
        elif 'getesteten personen' in key:
            fieldname = 'tested_total'
            value = value
        elif 'positiv getestet' in key and 'neu' in key:
            fieldname = 'positive_delta'
            value = value
        elif 'gesamtzahl' in key and 'infizierte personen' in key:
            fieldname = 'positive_total'
            value = value
        elif 'auf normalstationen' in key:
            fieldname = 'hospitalized_normal'
            value = value
        elif 'intensiv' in key and not 'ausland' in key:
            fieldname = 'hospitalized_icu'
            value = value 
        elif 'verdachtsf' in key:
            fieldname = 'hospitalized_suspicious'
            value = value
        elif 'verstorbene' in key and 'gesamt' in key:
            fieldname = 'deceased_total'
            value = value
        elif 'personen betroffen von' in key:
            fieldname = 'isolated_total'
            value = value
        elif 'personen in quarantäne' in key:
            fieldname = 'isolated_current'
            value = value
        elif 'isolation beendet' in key:
            fieldname = 'isolated_released'
            value = value
        elif 'geheilte' in key:
            fieldname = 'recovered_total'
            value = value
        elif 'positiv' in key and 'sanitätsbetrieb' in key:
            fieldname = 'positive_sabes_employees'
            value = value
        elif 'getestete' in key and 'ärzte' in key:
            fieldname = 'positive_familydoctors'
            value = value

        else:
            # Unknown field
            value = None

        if fieldname and key and value:
            try:
                value = value.replace(',', '')
                value = value.replace('.', '')
            except AttributeError:
                pass

            try:
                fields.update(
                    {
                        fieldname: int(value)
                    }
                )
            except ValueError:
                print('Couldn\'t parse value for field "{}"'.format(fieldname))

    fields.update({'pressrelease_url': url})

    # create DataFrame
    df = pd.DataFrame(data=fields, index=[date])

    # write total CSV
    filename = 'data/covid19_bz_detailed.csv'
    header = False if os.path.exists(filename) else True
    df.to_csv(filename, sep=',', mode='a', header=header, index=True)


try:
    date, url = get_pressrelease_url()
except TypeError:
    print('No press release for today was found')
    quit()

# Checken, ob wir die heutigen Daten schon haben
today = datetime.today().date()
df = pd.read_csv('data/covid19_bz_detailed.csv')
last_row = df.tail(1)
last_scraped_date = datetime.strptime(last_row['date'].values[0], '%Y-%m-%d').date()
if not last_scraped_date < today:
    quit()

get_numbers_from_pressrelease(url, date)