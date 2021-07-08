import requests
from bs4 import BeautifulSoup
import time
import pandas as pd
from random import randint
import math
import datetime as dt
from datetime import timedelta
from datetime import date

def timeconvert(postdate):
    datedictionary = {'one':1, 'two':2, 'three':3, 'four':4, 'five':5, 'six':6, 'seven':7, 'eight':8, 'nine':9, 
    'ten':10, 'eleven':11, 'twelve':12, 'thirteen':13, 'fourteen':14, 'fifteen':15, 'eighteen':18  }
    
    if 'hours|minutes|now' in postdate:
        d=0
    elif 'twenty' in postdate:
        for word in postdate.split():
            if word in datedictionary:
                d = 20 + datedictionary[word]
            else:
                d=20
    elif 'thirty' in postdate:
        d=30
    else:
        for word in postdate.split():
            if word[:-4] in datedictionary:
                d=10 + datedictionary[word[:-4]]
                
            elif word in datedictionary:
                d = datedictionary[word]
                pass

    Dated = date.today()-timedelta(days=d)
    return str(Dated)
def renamd(df, column, dict):
     #replace dict values
    for k,v in dict.items():
        x = pd.Series(df[column])
        y = x.str.lower().str.findall(k)
        
        for i in range(len(y)):
            if y[i]!=[]:
                x[i]=v
            else:
                pass

    return df

def SeekScrape_Mining():
    joblistings = pd.read_csv('joblistings_Mining_Resource_Energy.csv')
    # joblistings = pd.DataFrame()
    no = 0

    # load up first page
    surl = 'https://www.seek.com.au/jobs-in-mining-resources-energy/mining-exploration-geoscience?sortmode=ListedDate'
    site = requests.get(surl)
    content = site.content
    soup = BeautifulSoup(content, 'html.parser')
    #pull job section
    posts = soup.find(class_='_1UfdD4q')

    # find total pages of job sections  20 jobs / page
    count = int(soup.find(id='SearchSummary').text[:3])
    pages = math.ceil(count/20)
    print(str(pages)+' pages to scrape')

    for i in range(pages+1):
        print(str(i)+'-'+str(pages), end=', ')
        try:
            
            surl = 'https://www.seek.com.au/jobs-in-mining-resources-energy/mining-exploration-geoscience?page='+str(i)+'&sortmode=ListedDate'
            site = requests.get(surl)
            content = site.content
            soup = BeautifulSoup(content, 'html.parser')
            posts = soup.find(class_='_1UfdD4q')
        except:
            #pass first page through.. 
            pass
        time.sleep(randint(20,30))
        
        for post in posts:
            no+=1
            title = post.find('h1').text
            co = post.find(class_='_3mgsa7- _15GBVuT _2Ryjovs').text[3:]
            postdate = post.find(class_='_2cFajGc').text
            if 'more' in postdate:
                break
            locale = post.find(class_='_7ZnNccT').text[9:]
            x = int(len(locale)/2)+1
            location = locale[:x]
            
            time.sleep(randint(5,13))
            if postdate != 'This is a featured job':
                joblistings = joblistings.append(
                        pd.DataFrame(
                            {
                                'count': [no],
                                "Company": [co],
                                "Job": [title],
                                "Date": timeconvert(postdate),
                                "Location": [location],
                            }
                        ))
            else:
                pass
    return joblistings

def Tchanges(joblistings):

    miningchanges={'eophys':'Geophysicist','exploration & geologist|geophys|geoscien':'Explorationist', 'eolog': 'Geologist', 
    'rill': 'Driller', 'eotech': 'Geotech', 'ass|tech': 'Assistant', 'anal': 'Analyst',
    'operat':'Operations', 'mech|labour|constr|studen|survey':'Other', 'engin':'Engineer'}


    joblistings.reset_index(inplace=True)
    joblistings.drop(['count', 'index'], axis=1, inplace=True)
    joblistings['Jobgroup']=joblistings['Job']
    renamd(joblistings,'Jobgroup',miningchanges)
    joblistings.drop_duplicates(inplace=True)
    return joblistings

#-----------------------------------------------------
#   Scrape data from SEEk - mining and exploration into a table and generalise job titles
joblistings = SeekScrape_Mining()
joblistings = Tchanges(joblistings)
joblistings.drop_duplicates(inplace=True)
joblistings.to_csv('joblistings_Mining_Resource_Energy.csv')
print('DONE')

# further work 
#   - Limit overwrite loading to only new dates
#   - scrape other industry key jobs??