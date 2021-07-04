# import typing
import pandas as pd
import numpy as np
import datetime as dt
from datetime import date, timedelta
from pandas.io.pytables import incompatibility_doc
from yahoo_fin.stock_info import get_data

# import warnings
# warnings.simplefilter(action='ignore')
pd.set_option('display.max_rows', 280)
pd.set_option('display.max_columns', 25)
pd.set_option('display.width', 1000)
pd.options.display.float_format = '{:,.2f}'.format

def Stocks2Call(file='ASX_Listed_Companies_22-06-2021_02-13-18_AEST.csv') -> list:  # creates list of stock codes
    filepath='/home/ajw/Documents/VSstudio/ASX Scaper/Stockscrappy2/'
    # filepath='/home/ajw/Documents/VSstudio/ASX Scaper/raw data'
    codedf=pd.read_csv(filepath+file)   # newASXdata
    codedf.rename(columns={'ASX code': 'code'}, inplace=True)
    codedf.sort_values(['code'], ascending=True, axis=0, inplace=True)
    rawstock=codedf.code.unique()
    # codedf['date']=pd.to_datetime(codedf['date'], format='%Y %m %d')
    stocks=[s for s in rawstock if len(s) ==3]
    print(len(stocks))
    return stocks

def LoadYahooFinanceData(stock, startdate='15/01/2018', enddate='19/10/2020') -> pd.DataFrame: # choose data extent to load from yahoofin. API
    # read from csv or internet
    df=pd.DataFrame()
    #stocks=['VGB', 'LYL', 'SKC', 'PME']
    if stock!='%5EAXJO':
        stock+='.AX'
    try:
        yf_data=get_data(stock, start_date=startdate, end_date=enddate, index_as_date=False, interval="1d")
        if stock!='%5EAXJO':
            
            for c in yf_data['ticker']:
                yf_data['ticker']=c[:3]
        
        df=df.append(pd.DataFrame(yf_data[['close', 'date', 'volume', 'ticker']]))
       

        df['date']=pd.to_datetime(df['date'], format='%Y %m %d')
        df=df.rename(columns={'close':'price', 'ticker':'code'})
        df.sort_values(['date'], ascending=False, axis=0, inplace=True)
        df.drop_duplicates(subset=['date'], inplace=True)
        df.set_index('date', inplace=True)
        return df

    except: #stock doesnt exsist in the Yahoo API.
        print('_f', end='' )
        return df
        
def LoadYahootoCSV():
    pass

def HistoricalCsvLoad(file):
    df=pd.read_csv(file)
    df.set_index('date', inplace=True)
    df.drop('Unnamed: 0', axis=1, inplace=True)
    return df

def HistoricalCallByDate(code, df, sdate='2021-03-01', edate='2021-03-12'):
    df=df[df['code']==code]
    df=df.loc[edate:sdate]
    return df    

def AlgoAverages(df):  # create averages
    df['price'].mask(df['price']==0.000,np.nan, inplace=True)
    df['price'].fillna(method='bfill', inplace=True)   
    df['xewm'] = df['price'].ewm(span=22, adjust=False).mean()
    df['EWM']=df['xewm'].rolling(int(2), center=True, closed=None).mean()  #smooth out ewm
    df['EWM'].fillna(method='backfill', inplace=True)
    
    df['VOLSMA_100'] = df.volume.rolling(window=45).mean()
    df['VOLSMA_100'].fillna(method='backfill', inplace=True)

    df.drop('xewm', axis=1, inplace=True)
    
    return df

def AlgoRateOfChange(df, volmultiple=4):  #define rate of change of the averages and set a value to the base flags
    
    df.reset_index(inplace=True)
    
    for i in df.index:
        b=i+1
        c=i+2

        try:
            df.loc[i,'dvdtEWM'] = df.loc[c,'EWM'] - df.loc[i,'EWM']

            if df.loc[i,'dvdtEWM']>0.00005: 
                df.loc[i,'flag']=df['price'].mean()
            else:
                df.loc[i,'flag']=0

        
        
            if df.loc[i,'dvdtEWM']<0 and (df.loc[i,'VOLSMA_100']*volmultiple <= df.loc[i, 'volume']):  # changed this
                df.loc[i,'SELL']=(df['price'].max()*0.9)
            else:
                df.loc[i,'SELL']=0

            if df.loc[i,'VOLSMA_100']*volmultiple <= df.loc[i,'volume'] and df.loc[i,'flag']>0:
                df.loc[i,'BUY']=df['volume'].max()
            else:
                df.loc[i,'BUY']=0

        except KeyError:
            pass
    return df

def FutureDatePrice(df, date):
    

    if isinstance(date, dt.datetime):
        pass
        
    else:
        date=dt.datetime.strptime(date, "%Y-%m-%d")

    for i in range(4,10):
        try:
            
            daysafter=(date + timedelta(days=i)).strftime("%Y-%m-%d")

            buyp=df.loc[daysafter, 'price']
            if isinstance(buyp, pd.Series):
                buyp=buyp[0]
            
                
            break

        except:
            buyp=0
            pass

    for i in range(90,100):
        try:
            
            f3after=(date + timedelta(days=i)).strftime("%Y-%m-%d")
            f3p=df.loc[f3after, 'price']
            if isinstance(f3p, pd.Series):
                f3p=f3p[0]

            break

        except:
            f3p=-999
            pass

    for i in range(180,190):
        try:
            f6after=(date + timedelta(days=i)).strftime("%Y-%m-%d")
            f6p=df.loc[f6after, 'price']
            if isinstance(f6p, pd.Series):
                f6p=f6p[0]

            break

        except:
            f6p=-999
            pass
    
    for i in range(270,280):
        try:
            f9after=(date + timedelta(days=i)).strftime("%Y-%m-%d")
            f9p=df.loc[f9after, 'price']
            if isinstance(f9p, pd.Series):
                f9p=f9p[0]
            break

        except:
            f9p=-999
            pass

    
    for i in range(350,360):
        try:
            f12after=(date + timedelta(days=i)).strftime("%Y-%m-%d")
            f12p=df.loc[f12after, 'price']
            if isinstance(f12p, pd.Series):
                f12p=f12p[0]
            break
        except:
            f12p=-999
            pass

    return buyp, f3p, f6p, f9p, f12p

def HistoricBuyFlagToDF(df,dfbuy, asxcode, start_flag='', end_flag='', valuetraded=1000000): # define flags and create new df of flagged info
    
    df['valuetraded']=df['price']*df['volume']
    dBd=pd.DataFrame()
    dSd=pd.DataFrame()
    threshold=0.000011
    df.set_index('date', inplace=True)
    
    try:
        dB=df[(df.BUY>threshold) & (df.valuetraded>valuetraded)]
        dBd=dB.loc[end_flag:start_flag]
    except:
        
        pass

    try:
        dS=df[(df.SELL>threshold) & (df.valuetraded>valuetraded/3)]
        dSd=dS.loc[end_flag:start_flag]
    except:
        pass
    
    if len(dBd)!=0:
        for d in dBd.index:
            
            print('.', end='')
            
            # BB.append(stock)
            # d=dt.datetime.strptime(d, "%Y-%m-%d")
            d=str(d.strftime("%Y-%m-%d"))
            dailyVols=df.loc[d, 'volume'][0]
            avVols=df.loc[d, 'VOLSMA_100'][0]
            
            
            flagdate=d
            
            buyp, f3p, f6p, f9p, f12p = FutureDatePrice(df, d)
            valtraded=buyp * dailyVols
           
            dfbuy=dfbuy.append(pd.DataFrame({'stock':asxcode, 'buy':'BUY', 'flagdate': flagdate ,
             'buyprice': [buyp] , 'avVOL': [avVols], 'DailyVol': [dailyVols], '3month$': [f3p], '6month$': [f6p], '9month$': [f9p], 
             '12month$': [f12p], 'ValueTraded': [valtraded]}), ignore_index=True)  #'profit%': prof,# '10daychange%': d10chan, 
        
    else:
        pass
        
    # if len(dSd)!=0:
    #     for s in dSd.index:
            
                
    #         # SS.append(stock)
    #         for i in range(4,10):
    #             try:
    #                 selldaysafter=(s- timedelta(days=i)).strftime("%Y-%m-%d")
                    
    #                 Sellp=df.loc[selldaysafter, 'price']
    #                 valtraded=df.loc[selldaysafter, 'valuetraded']
    #                 # indexdate=df.loc[daysafter, 'date']
    #                 print(Sellp)
                    
    #                 break
    #             except:
    #                 pass
            
            
    #         dfbuy=dfbuy.append(pd.DataFrame({'stock':asxcode, 'buy':'SELL', 'date': s , 'buyprice': Sellp , 
    #         'currentprice': 0, 'profit%': 0, '10daychange%':d10chan}), ignore_index=True)
            
    # else:
    #     pass
    
    
    return dfbuy

def CleanupPercentages(dfbuy):
    dfbuy['3m%']=(dfbuy['3month$']-dfbuy['buyprice'])*100/dfbuy['buyprice']
    dfbuy['6m%']=(dfbuy['6month$']-dfbuy['buyprice'])*100/dfbuy['buyprice']
    dfbuy['9m%']=(dfbuy['9month$']-dfbuy['buyprice'])*100/dfbuy['buyprice']
    dfbuy['12m%']=(dfbuy['12month$']-dfbuy['buyprice'])*100/dfbuy['buyprice']
    dfbuy.mask(dfbuy[['3m%','6m%','9m%','12m%']]<-1000, np.nan, inplace=True)
    return dfbuy
    #-------------------------------------------------------------

def BenchmarkASX(dfbuy, starting_flag, sdate, edate, stock='%5EAXJO'):
    benchmark_data=LoadYahooFinanceData(stock, sdate, edate)
    buyp, f3p, f6p, f9p, f12p = FutureDatePrice(benchmark_data, starting_flag)
    
    dfbuy=dfbuy.append(pd.DataFrame({'stock':'Benchmark', 'flagdate': starting_flag, 'buyprice': [buyp], '3month$': [f3p], '6month$': [f6p], '9month$': [f9p], 
             '12month$': [f12p] }), ignore_index=True) 
    return dfbuy

def LoadDateRange(starting_flag='2020-05-01', ending_flag='2020-08-01'):    

    strpd_start=dt.datetime.strptime(starting_flag, "%Y-%m-%d")
    load_start=strpd_start-dt.timedelta(weeks=100)
    sdate=load_start.strftime("%Y-%m-%d")

    strpd_end=dt.datetime.strptime(ending_flag, "%Y-%m-%d")
    load_end=strpd_end+dt.timedelta(weeks=58)
    edate=load_end.strftime("%Y-%m-%d")

    return sdate, edate

#-----------------------------------------------#
# #CHOOSE  DATE RANGE TO INVESTIGATE + FLAG LIMITS

starting_flag='2019-02-01'
ending_flag= '2019-05-01'
volmultiple=7
valuetraded=10000000
benchmark_stock='%5EAXJO'
#-----------------------------------------------#
#  LOAD DATA AND RANGE FROM CSV..

filepath='/home/ajw/Documents/VSstudio/ASX Scaper/Stockscrappy2/ASX_Listed_Companies_22-06-2021_02-13-18_AEST.csv'
# df=HistoricalCsvLoad(filepath)
sdate, edate=LoadDateRange(starting_flag, ending_flag)
dfbuy=pd.DataFrame()

stocks=['AMI', 'MWY', 'CLW']

#----------------------------------------------#
#  RUN SCRIPT
# for code in Stocks2Call():
for code in stocks:
    print(code, end=' ')
    
    df_historic=LoadYahooFinanceData(code, sdate, edate)
    # df_historic=HistoricalCallByDate(code, df, sdate, edate)

    if len(df_historic)!=0:
        df_HistoricAverages=AlgoAverages(df_historic)
        df_ROC_flags=AlgoRateOfChange(df_HistoricAverages, volmultiple)
        dfbuy=HistoricBuyFlagToDF(df_ROC_flags, dfbuy, code,  starting_flag, ending_flag, valuetraded )
        
    else:
        print('^', end='')
        pass

dfbuy=BenchmarkASX(dfbuy, starting_flag, sdate, edate, benchmark_stock)
dfbuy=CleanupPercentages(dfbuy)
dfbuy.drop_duplicates('stock', inplace=True)
print('\n\n\n\n', dfbuy)


# print(dfbuy.describe())
# dfbuy.to_csv('tsety22.csv', sep=',')