import requests
import re
from bs4 import BeautifulSoup
import time
from random import randint
import pandas as pd
import datetime as dt


def stock_buyers(stock, starting_flag, ending_flag):  #scrape for director buy sells
    # try:
    url ='https://www.marketbeat.com/stocks/ASX/'+str(stock)+'/insider-trades/'
    page = requests.get(url)
    content = page.content
    soup = BeautifulSoup(content, 'html.parser')
    tb = soup.find_all('tr')
    time.sleep(randint(1,3))

    listed = []
    for t in tb:
        if '$' in t.text:
            listed+=[t.text]

    # print('***** ', listed)
    serieslist = pd.Series(listed)
    pattern=r'^(?P<date>[\d+/]+).*\b(?P<Name>\w+)Insider(?P<trade>\D+)(?P<shares>[\d,]+)A\$(?P<price>[\d\.]+)A\$(?P<value>[\d,\.]+)'
    if listed:
        directorbuysell = serieslist.str.extract(pattern)

        directorbuysell.replace(',','', regex=True, inplace=True)
        directorbuysell = directorbuysell.astype({'shares': 'float64', 'price': 'float64', 'value':'float64', 'date':'datetime64[ns]'})
        directorlistdated = directorbuysell[(directorbuysell['date']>starting_flag)&(directorbuysell['date']<ending_flag)]
        directorlistdated['date'] = directorlistdated['date'].dt.strftime('%d-%B')
        directorlistdated.drop('shares', axis=1, inplace=True)
        # directorlistdated['date'].astype('object', copy=False)

        return directorlistdated.values.tolist(), url
    else:
        return listed, url

# stock = 'FEL'
# starting_flag = "2021-01-04"
# ending_flag = "2021-07-18"

# dlist, url = stock_buyers(stock, starting_flag, ending_flag)
