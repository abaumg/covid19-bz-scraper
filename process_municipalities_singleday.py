import pandas as pd
import datetime
import sys

## filename for csv file containing all dates
alldatesmunicST_csv = 'covid19_bz_municipalities.csv'

# hard coded filename to local file
#xlsx_file = r'1062210_Positiv27-03-2020.xlsx'
# sample URL to xls file
#xlsx_file = 'http://www.provinz.bz.it/news/de/news.asp?news_action=300&news_image_id=1062388'
# take file name or URL from command line
xlsx_file = sys.argv[1]

# read xls file to dataframe, excluding header lines (2), only read cols A, B, E
df = pd.read_excel(xlsx_file, header=2, usecols="A,B,E", dtype={'a': int, 'b': str})

# drop empty rows containing NaN values
df.dropna(inplace=True)

# only keep rows containing total numbers for municipalities
df_totale = df[df['Comune di residenza'].str.contains('Total')]

# convert ZIP codes back to integer numbers
df_totale.iloc[:, 0] = df_totale.iloc[:, 0].astype('int32')

# remove 'totale' from municipality name
df_totale.iloc[:,1] = df_totale.iloc[:,1].map(lambda x: x.rstrip(' Totale').upper())

# extract date from xls file
filedate = df.columns[2].strip('Totali al ')
# convert to datetime object
date = datetime.datetime.strptime(filedate, '%d-%m-%Y').strftime('%Y_%m_%d')

# add date column
df_totale['datum'] = date


## file name generation from current system date derived
#csv_file = '{date:%Y-%m-%d}_ST_communal_covid19pos.txt'.format(date=datetime.datetime.now())
##file name derived from column heading
#csv_file = '{date}_ST_communal_covid19pos.txt'.format(date=df.columns[2].strip('Totali al '))
# file name with date format YYYY_mm_dd
singledatemunicST_csv = 'covid19_bz_municipalities_{date}.csv'.format(date=date)

# rename columns
df_totale.columns = ['ISTAT_code', 'name_IT', 'totals', 'datum']
# re-order columns
df_totale = df_totale[['datum', 'ISTAT_code', 'name_IT', 'totals']]


# write to csv file
df_totale.to_csv(singledatemunicST_csv, sep=',', header=True, index=False)

## append to csv file containing all dates
df_totale.to_csv(alldatesmunicST_csv, sep=',', mode = 'a', header=False, index=False)
