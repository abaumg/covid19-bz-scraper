# covid19-bz-scraper

## process_municipalities_singleday.py

Script to pull municipal data for positive tested COVID-19 cases for province of South Tyrol from excel file
and write/append to csv

### Usage:
    python process_municipalities_singleday.py [URL]
### Parameters:
URL (string): URL to xls sheet containing municipal covid-19 data for South Tyrol 
e.g. http://www.provinz.bz.it/news/de/news.asp?news_action=300&news_image_id=1062388
### Output:
creates new `data/covid19_bz_municipalities_YYYY-MM-DD.csv` file for specific day and appends data to (existing) `data/covid19_bz_municipalities.csv` file containing previous days

## scrape_pressreleases.py

Script to parse detailed covid-19 data from official press releases and write/append to csv

### Usage:
    python scrape_pressreleases.py
### Parameters:
    None
### Output:
creates new `data/covid19_bz_detailed_YYYY-MM-DD.csv` file for specific day and appends data to (existing) `data/covid19_bz_detailed.csv` file containing previous days
