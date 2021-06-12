# import typing
import pandas as pd
import numpy as np
import datetime as dt
from yahoo_fin.stock_info import get_data

# functions are important
def stocks2call(file='thursdays.csv') -> list:  # creates list of stock codes

    filepath='/home/ajw/Documents/VSstudio/ASX Scaper/raw data'
    codedf=pd.read_csv(filepath+'/'+file)   # newASXdata
    codedf.rename(columns={'stock': 'code'}, inplace=True)
    codedf.sort_values(['code','date'], ascending=[True,False], axis=0, inplace=True)
    rawstock=codedf.code.unique()
    codedf['date']=pd.to_datetime(codedf['date'], format='%Y %m %d')
    stocks=[s for s in rawstock if len(s) ==3]
    stocks=['BHP']
    return stocks

def load_data(stock, startdate='15/01/2018', enddate='19/10/2020') -> pd.DataFrame: # choose data extent to load from yahoofin. API
    # read from csv or internet
    df=pd.DataFrame()
    #stocks=['VGB', 'LYL', 'SKC', 'PME']     
    try:
        yf_data=get_data(stock+'.AX', start_date=startdate, end_date=enddate, index_as_date=False, interval="1d")
        for c in yf_data['ticker']:
            yf_data['ticker']=c[:3]
        df=df.append(pd.DataFrame(yf_data[['close', 'date', 'volume', 'ticker']]))
    except:
        pass


    df['date']=pd.to_datetime(df['date'], format='%Y %m %d')
    df=df.rename(columns={'close':'price', 'ticker':'code'})
    df.sort_values(['date'], ascending=False, axis=0, inplace=True)
    df.drop_duplicates(subset=['date'], inplace=True)
    print(df)
    return df

def algoAverages(df):  # create averages
    df['price'].mask(df['price']==0.000,np.nan, inplace=True)
    df['price'].fillna(method='bfill', inplace=True)   
    df['xewm'] = df['price'].ewm(span=22, adjust=False).mean()
    df['EWM']=df['xewm'].rolling(int(2), center=True, closed=None).mean()  #smooth out ewm
    df['EWM'].fillna(method='backfill', inplace=True)
    
    df['VOLSMA_100'] = df.volume.rolling(window=45).mean()
    df['VOLSMA_100'].fillna(method='backfill', inplace=True)

    df.drop('xewm', axis=1, inplace=True)
    
    return df

def algoRateofchange(df):  #define rate of changes
    
    
    #dfcode=df[df['code']==code]
    #dfcode.reset_index(inplace=True)
    for i in df.index:
        b=i-1
        c=i+2
        try:
            if df.loc[b,'EWM']!=0:
                
                df.loc[i,'dvdtEWM'] = df.loc[b,'EWM'] - df.loc[i,'EWM']
            if df.loc[i,'dvdtEWM']==0:
                df.loc[i,'dvdtEWM']=df.loc[c,'dvdtEWM']       
    
        except:
            pass
        
        try:
            df['dvdtEWM'][0:2]=df['dvdtEWM'][2]
        except:
            pass


        if df.loc[i,'dvdtEWM']>0.00005: 
            df.loc[i,'flag']=df['price'].mean()
        else:
            df.loc[i,'flag']=0

    
        try:
            if df.loc[i,'dvdtEWM']<0 and (df.loc[i,'VOLSMA_100']*4 <= df.loc[i, 'volume']):  # changed this
                df.loc[i,'SELL']=(df['price'].max()*0.9)
            else:
                df.loc[i,'SELL']=0
        except:
            pass

        try:
            df['flag'][0:2]=df['flag'][2]
        except:
            pass

        if df.loc[i,'VOLSMA_100']*4 <= df.loc[i,'volume'] and df.loc[i,'flag']>0:
            df.loc[i,'BUY']=df['volume'].max()
        else:
            df.loc[i,'BUY']=0

    return df

def filter_date(df, start_date: dt.date, end_time: dt.date, df_to_filter: pd.DataFrame) -> pd.DataFrame:
    pass

def buysellflags(df, start_flag='15/01/2018', end_flag='15/02/2018'): # define flags and create new df of flagged info
    df['valuetraded']=df['price']*df['volume']
    print('Y')
    threshold=0.000011
    dfbuy=pd.DataFrame()
    dB=df[(df.BUY>threshold) & (df.valuetraded>1000000)]
    dS=df[(df.SELL>threshold) & (df.valuetraded>300000)]
    
    timeflag = pd.Interval(pd.Timestamp(end_flag),pd.Timestamp(str(pd.to_datetime(start_flag))), closed='left')
    

    for d in dB['date']:
        if pd.Timestamp(d) in timeflag:
            print('.', end='')
            
            BB.append(stock)
            
            currp=float(df['price'][0])
            dailyVols=humanize.intword(int(df[ df['date']==str(d)[:10] ]['volume']))
            avVols=humanize.intword(int(df[ df['date']==str(d)[:10] ]['VOLSMA_100']))
            f3=d + pd.DateOffset(months=3)
            f6=d + pd.DateOffset(months=6)
            try:
                f9=d + pd.DateOffset(months=9)
                f12=d + pd.DateOffset(months=12)
            except:
                pass

            try:
                
                bindex=df[ df['date']==str(d)[:10] ].index.values-4
                f3index=bindex-60
                f6index=bindex-120
                try:
                    f9index=bindex-180
                    f12index=bindex-235
                except:
                    pass
                #print('T ', bindex)
                buyp=float(df['price'][bindex])
                valtraded=float(df['valuetraded'][bindex])
                d10chan="{:.1f}".format((float(df['price'][bindex+4])-float(df['price'][bindex+14]))/float(df['price'][bindex+4])*100)
                
                f3p=float(df['price'][f3index])
                f6p=float(df['price'][f6index])
                try:
                    f9p=df['price'].astype(np.float64)[f9index]
                    f12p=float(df['price'][f12index])
                except:
                    pass
                prof="{:.1f}".format((float(df['price'][0])-buyp)/buyp*100)
                dfbuy=dfbuy.append(pd.DataFrame({'stock':stock, 'buy':'BUY', 'date': str(d)[:10] , 'buyprice': buyp , 'currentprice': currp, 'profit%': prof, '10daychange%': d10chan, 'avVOL': avVols, 'DailyVol': dailyVols, '3month$': f3p, '6month$': f6p, '9month$': f9p, '12month$': f12p, 'ValueTraded': valtraded}, index=[0]), ignore_index=True)

            except:
                try:
                    bindex=df[ df['date']==str(d)[:10] ].index.values
                    #print('J ', bindex)
                    buyp=float(df['price'][bindex])
                    valtraded=float(df['valuetraded'][bindex])
                    d10chan="{:.1f}".format((float(df['price'][bindex])-float(df['price'][bindex+10]))/float(df['price'][bindex])*100)
                    PERIOD = 20

                    f3index=bindex-PERIOD*3
                    f6index=bindex-PERIOD*6
                    try:
                        f9index=bindex-PERIOD*9
                        f12index=bindex-PERIOD*12
                    except:
                        pass

                    prof="{:.1f}".format((float(df['price'][0])-buyp)/buyp*100)
                    dfbuy=dfbuy.append(pd.DataFrame({'stock':stock, 'buy':'BUY', 'date': str(d)[:10] , 'buyprice': buyp , 'currentprice': currp, 'profit%': prof, '10daychange%':d10chan, 'avVOL': avVols, 'DailyVol': dailyVols, '3month$': f3p, '6month$': f6p, '9month$': f9p, '12month$': f12p, 'ValueTraded': valtraded}, index=[0]), ignore_index=True)



                except:
                    pass
                pass              

    for s in dS['date']:
        if pd.Timestamp(s) in timeflag:
            
            SS.append(stock)
            try:
                Sindex=df[ df['date']==str(s)[:10] ].index.values-4
                
                d10chan="{:.1f}".format((float(df['price'][Sindex+4])-float(df['price'][Sindex+14]))/float(df['price'][Sindex+4])*100)
                Sellp=float(df['price'][Sindex])
                
                dfbuy=dfbuy.append(pd.DataFrame({'stock':stock, 'buy':'SELL', 'date': str(s)[:10] , 'buyprice': Sellp , 'currentprice': 0, 'profit%': 0, '10daychange%':d10chan}, index=[0]), ignore_index=True)
            except:
                try:
                    Sindex=df[ df['date']==str(s)[:10] ].index.values
                    d10chan="{:.1f}".format((float(df['price'][Sindex])-float(df['price'][Sindex+10]))/float(df['price'][Sindex])*100)
                    Sellp=float(df['price'][Sindex])
                    #prof="{:.1f}".format((float(dp['price'][0])-buyp)/buyp*100)
                    dfbuy=dfbuy.append(pd.DataFrame({'stock':stock, 'buy':'SELL', 'date': str(s)[:10] , 'buyprice': Sellp , 'currentprice': 0, 'profit%': 0, '10daychange%':d10chan}, index=[0]), ignore_index=True)
                except :

                    pass
            
            pass              

        else:
            pass
    return dfbuy

def cleanup(dfbuy):
    try:
        dfbuy['10daychange%']=dfbuy['10daychange%'].astype('float32')

        dfbuy['3m%']=(dfbuy['3month$']-dfbuy['buyprice'])*100/dfbuy['buyprice']
        dfbuy['6m%']=(dfbuy['6month$']-dfbuy['buyprice'])*100/dfbuy['buyprice']
        dfbuy['9m%']=(dfbuy['9month$']-dfbuy['buyprice'])*100/dfbuy['buyprice']
        dfbuy['12m%']=(dfbuy['12month$']-dfbuy['buyprice'])*100/dfbuy['buyprice']
    except:
        pass
    return dfbuy
    #-------------------------------------------------------------
#__________________________________________________
# def benchmark(stock='XAO', **kwargs):
#     load_data(stock, **kwargs)
#     pass
    
def startstopcheck(df,sdate='01/01/2018', edate='19/03/2021'):
    priceatstart=df.loc['date'==sdate,'price']
    priceatend=df.loc['date'==edate,'price']
    
    pass


#STOCKS FROM 2018 BOOK
stocks=['ONT', 'ABC', 'AGL', 'ALQ', 'ALU', 'AMA', 'ANN', 'ARB', 'ALL', 'AUB', 'ANZ', 'BOQ', 'BPT', 'BHP', 'BKL', 'BLA', 'BRG', 'BTT', 'CTX', 'CAR', 'CWP', 'CCL', 'COH', 'CDA', 'CKF', 'CBA', 'CTD', 'CSR', 'DTL', 'DMP', 'DWS', 'EVT', 'EVN', 'FLT', 'FMG', 'GEM', 'GBT', 'GNG', 'GWA', 'HSN', 'HVN', 'IFM', 'IAG', 'IRI', 'IRE', 'JBH', 'LLC', 'MLD', 'MQG', 'MFG', 'MIN', 'MNF', 'MND', 'MNY', 'MOC', 'MYS', 'NAB', 'NHF', 'NCK', 'NST', 'OCL', 'ORI', 'PEA', 'PGC', 'PPT', 'PTM', 'PME', 'RCG', 'REA', 'REH', 'RFG', 'RIO', 'SEK', 'SRV', 'SIG', 'SRX', 'SHL', 'SXL', 'SDG', 'SUL', 'TGR', 'TNE', 'TPG', 'VTG', 'WEB', 'WLL', 'WES', 'WBC', 'WOW']

stocks=['BHP']
for asxcode in stocks:
    # df=load_data(stock, startdate='01/01/2018', enddate='19/03/2021')

# for asxcode in stocks2call():
    data=load_data(asxcode, startdate='01/01/2018', enddate='19/10/2020')
    avdata=algoAverages(data)
    print(asxcode, '  averages done ', end=' ')
    rocdata=algoRateofchange(avdata)
    print(rocdata, 'done ROC ', end=' ')
    dfbuy=buysellflags(rocdata, start_flag='15/02/2018', end_flag='01/03/2018')
    print(dfbuy, 'done cleanup ', end=' ')
    cleanup(dfbuy)
    print(' done flags ', end=' ')
    print(dfbuy)
# all_data = load_data()
# filtered_data = filter_date(dt.date(2020, 1, 1), dt.date(2020, 3, 1), all_data)
# print(df)
# th is is the sunday test...
#master
# feature branch
# master b

