#!/usr/bin/env python

import feedparser
import requests

from bs4 import BeautifulSoup
from time import mktime


def get_pressrelease_url():
    """ Parse the provincial RSS feed and returns the URL of the latest press release which includes updated numbers
        Output:
            URL to press release containing latest covid-19 data for South Tyrol. If nothing was found, return None
    """

    feed = feedparser.parse('http://www.provinz.bz.it/news/de/news.asp?news_action=201')

    for item in feed.entries:
        pubdate_hour = item.published_parsed.tm_hour
        # Press releases are always published around 10am
        if 8 < pubdate_hour < 13:
            text_to_search = '{} {}'.format(
                item.title,
                item.description
            ).lower()

            # Search for common used words
            words = ['daten', 'gesamtzahl', 'zahlen', 'anzahl', 'aktualisiert', 'aktuell']
            if any(x in text_to_search for x in words):
                # Potential hit! Fetch the content to be sure
                request = requests.get(item.link)
                if 'Zahlen in K' in request.text:
                    # Bingo!
                    return item.link
    return None


def get_numbers_from_pressrelease(url):
    """ Pull latest covid-19 data from daily press release.
        Parameters:
            URL (str): URL to press release
        Output:
            Data (dict): Dict containing the parsed data
    """

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
            if 'Zahlen in Kürze' in p.text:
                zik = True
    for datapoint in p_list:
        print(datapoint.split(':'))


"""
print(get_pressrelease_url())
get_numbers_from_pressrelease('http://www.provinz.bz.it/news/de/news.asp?news_action=4&news_article_id=637159') # 31.03.
get_numbers_from_pressrelease('http://www.provinz.bz.it/news/de/news.asp?news_action=4&news_article_id=637096') # 30.03.
get_numbers_from_pressrelease('http://www.provinz.bz.it/news/de/news.asp?news_action=4&news_article_id=637083') # 29.03.
get_numbers_from_pressrelease('http://www.provinz.bz.it/news/de/news.asp?news_action=4&news_article_id=637069') # 28.03.
get_numbers_from_pressrelease('http://www.provinz.bz.it/news/de/news.asp?news_action=4&news_article_id=636998') # 27.03.
get_numbers_from_pressrelease('http://www.provinz.bz.it/news/de/news.asp?news_action=4&news_article_id=636946') # 26.03.
"""