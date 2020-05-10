#!/usr/bin/env python
""" Script to pull municipal data for positive tested COVID-19 cases for province of South Tyrol from excel file
    and write/append to csv
    Usage:
        %(scriptName)s [URL]
    Parameters:
        URL (str): optional URL to xls sheet containing municipal covid-19 data for South Tyrol
                e.g. http://www.provinz.bz.it/news/de/news.asp?news_action=300&news_image_id=1062388,
                if not specified, static URL https://afbs.provinz.bz.it/upload/coronavirus/CoronavirusPositivi.xlsx
                will be used
    Output:
        creates new .csv file for specific day and appends data to (existing) .csv file containing previous days
"""

import sys
from datetime import datetime
import os.path
import pandas as pd
pd.options.mode.chained_assignment = None

# display help to console  if command line argument not provided
if len(sys.argv) > 1 and sys.argv[1] in ['-h', '--help']:
    print(__doc__ % {'scriptName' : sys.argv[0].split("/")[-1]})
    sys.exit(0)


#####################
# define output folder
outdir = r'data/'

## filename for csv file containing all dates
alldatesmunicST_csv = 'covid19_bz_municipalities.csv'

# check if today's data already exists
today = datetime.today().date()
df = pd.read_csv(outdir + alldatesmunicST_csv)
last_row = df.tail(1)
last_scraped_date = datetime.strptime(last_row['datum'].values[0], '%Y-%m-%d').date()
if not last_scraped_date < today:
    quit()


# hard coded filename to local file
#xlsx_file = r'1062210_Positiv27-03-2020.xlsx'

# take URL from command line or use static URL
if len(sys.argv) > 1:
    xlsx_file = sys.argv[1]
else:
    xlsx_file = 'https://afbs.provinz.bz.it/upload/coronavirus/CoronavirusPositivi.xlsx'

# read xls file to dataframe, excluding header lines (2), only read cols A, B, E
df = pd.read_excel(xlsx_file, header=2, usecols="A,B,E", dtype={'a': int, 'b': str})

# drop empty rows containing NaN values
df.dropna(inplace=True)

# only keep rows containing total numbers for municipalities
df_totale = df[df['Comune di residenza'].str.contains('Total')]

# convert ZIP codes back to integer numbers
df_totale.iloc[:, 0] = df_totale.iloc[:, 0].astype('int32')

# remove 'totale' from municipality name
df_totale.iloc[:, 1] = df_totale.iloc[:,1].map(lambda x: x.rstrip(' Totale').upper())

# extract date from xls file
filedate = df.columns[2].strip('Totali al ')
# convert to datetime object
date = datetime.strptime(filedate, '%d-%m-%Y').strftime('%Y-%m-%d')

# add date column
df_totale['datum'] = date

# file name with date format YYYY_mm_dd
singledatemunicST_csv = 'covid19_bz_municipalities_{date}.csv'.format(date=date.replace('-', '_'))

# rename columns
df_totale.columns = ['ISTAT_code', 'name_IT', 'totals', 'datum']
# re-order columns
df_totale = df_totale[['datum', 'ISTAT_code', 'name_IT', 'totals']]
# sort by date and istat code
df_totale = df_totale.sort_values(by=['datum', 'ISTAT_code'])

# write to csv file
df_totale.to_csv(outdir+singledatemunicST_csv, sep=',', header=True, index=False)

## append to csv file containing all dates
# check if file already exists, if true skip header, else write header
if os.path.exists(outdir+alldatesmunicST_csv):
    df_totale.to_csv(outdir + alldatesmunicST_csv, sep=',', mode='a', header=False, index=False)
else:
    df_totale.to_csv(outdir + alldatesmunicST_csv, sep=',', mode='a', header=True, index=False)



