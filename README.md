# covid19-bz-scraper

This repository contains a set of scripts to pull/scrape data for COVID-19 cases in South Tyrol from provinz.bz.it pages. This repo exists because the Autonomus Province of South Tyrol is unable to provide the data as Open Data on it's Open Data Portal.

The scraped data is provided in the [data/](https://github.com/abaumg/covid19-bz-scraper/tree/master/data) subfolder as well:
- [covid19_bz.csv](https://github.com/abaumg/covid19-bz-scraper/blob/master/data/covid19_bz.csv): basic data (positive, recovered, deceased)
- [covid19_bz_detailed.csv](https://github.com/abaumg/covid19-bz-scraper/blob/master/data/covid19_bz_detailed.csv): detailed data (tested, positive, hospitalized, isolated, recovered, deceased)
- [covid19_bz_municipalities.csv](https://github.com/abaumg/covid19-bz-scraper/blob/master/data/covid19_bz_municipalities.csv) and covid19_bz_municipalities_YYYY_MM_DD.csv: data by municipalities

----

## process_municipalities_singleday.py

Pull municipal data for positive tested COVID-19 cases for province of South Tyrol from excel file
and write/append to csv

### Usage:
python process_municipalities_singleday.py [URL]
### Parameters:
URL (string): URL to xls sheet containing municipal covid-19 data for South Tyrol 
e.g. http://www.provinz.bz.it/news/de/news.asp?news_action=300&news_image_id=1062388
### Output:
Creates new `data/covid19_bz_municipalities_YYYY-MM-DD.csv` file for specific day and appends data to (existing) `data/covid19_bz_municipalities.csv` file containing previous days

----

## scrape_pressreleases.py

Parse detailed covid-19 data from official press releases and write/append to csv

### Usage:
python scrape_pressreleases.py
### Parameters:
None
### Output:
Creates new `data/covid19_bz_detailed_YYYY-MM-DD.csv` file for specific day and appends data to (existing) `data/covid19_bz_detailed.csv` file containing previous days

----

## scrape_graphics.py

Parse basic covid-19 data from http://www.provinz.bz.it/sicherheit-zivilschutz/zivilschutz/aktuelle-daten-zum-coronavirus.asp.

### Usage:
python scrape_graphics.py
### Parameters:
None
### Output:
Appends data to `data/covid19_bz.csv`
