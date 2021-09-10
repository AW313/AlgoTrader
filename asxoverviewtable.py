from numpy import ndarray
import numpy as np
import pandas as pd
from historytester import Stocks2Call
# from makemypdf import *
import time
from time import sleep
from random import randint
import yfinance as yf
import requests
from bs4 import BeautifulSoup
from datetime import date, datetime

pd.set_option("display.max_rows", 280)
pd.set_option("display.max_columns", 25)
pd.set_option("display.width", 1000)
pd.options.display.float_format = "{:,.2f}".format

def stockfacts(code='MIN.AX'):
    
    sleep(randint(1,3))
    msft = yf.Ticker(code)
    info = msft.info

    try:
        mc = info['marketCap']
    except KeyError:
        mc=np.nan
    try:
        tr = info['totalRevenue']
    except:
        tr=np.nan
    
    try:
        rg = info['revenueGrowth']
    except:
        rg=np.nan
    try:
        oc = info['operatingCashflow']
    except:
        oc=np.nan
    try:
        pi = info['heldPercentInstitutions']*100
        if not pi:
            pi=np.nan
    except:
        pi = np.nan
    try:
        eq = info['earningsQuarterlyGrowth']
        if not eq:
            eq=np.nan
    except:
        eq=np.nan
    try:
        tpe = info['trailingPE']
        
        if tpe=='Infinity':
            tpe = 0
        elif not tpe:
            tpe=np.nan
        
    except:
        tpe = np.nan
    try:
        fpe = info['forwardPE']
        if not fpe:
            fpe = np.nan
    except:
        fpe = np.nan
    try:
        tc = info['totalCash']
        if not tc:
            tc=np.nan
    except:
        tc=np.nan
    try:
        bv = info['bookValue']
        if not bv:
            bv=np.nan
    except:
        bv=np.nan
    
    try:
        td = info['totalDebt']
        if not td:
            td=np.nan
    except:
        td=np.nan
    try:
        io = info['heldPercentInsiders']*100
        if not io:
            io=np.nan
    except:
        io = np.nan
    try:
        dy = info['dividendYield']
    except:
        dy=np.nan
    try:
        so = info['sharesOutstanding']
    except:
        so=np.nan
    try:
        mp = info['regularMarketPrice']
    except:
        mp=np.nan
    try:
        sx = info['sector']
    except:
        sx=np.nan
    try:
        ev = info['enterpriseValue']
    except:
        ev=np.nan
    try:
        eb = info['ebitda']
    except:
        eb=np.nan
    try:
        teps = info['trailingEps']
    except:
        teps=np.nan
    
    try:
        feps = info['forwardEps']
        if not feps:
            feps=np.nan
    except:
        feps = np.nan
    try:
        evb = ev/eb  # Calc Enterprise value / EBITDA
    except TypeError:
        evb = np.nan
    try:
        isv = (ev + tc - td) / so  #Calc intrinsic share value
        po = (isv / mp-1)*100 # Calc percentage under
    except TypeError:
        isv = np.nan
        po = np.nan
    try:
        cEntv = (mc+td)-tc  # calc Enterprise value
    except:
        cEntv = np.nan
    try:
        cEQv = (ev+tc)-td # Calc Equity value
        if not cEQv:
            cEQv=np.nan
    except TypeError:
        cEQv = np.nan
    try:    
        Eqs = cEQv / so  # Calc equity shares
        if not Eqs:
            Eqs=np.nan
    except:
        Eqs = np.nan

    try:
        tepss = teps * tpe  # calc trailing shareprice
        if not tepss:
            tepss=np.nan
    except TypeError:
        tepss = np.nan

    try:
        fepss = feps * fpe  # calc Fwd shareprice
        if not fepss:
            fepss=np.nan
    except TypeError:
        fepss = np.nan
    try:
        ebm = tr / eb # EBITDA MARGIN %
        if not ebm:
            ebm=np.nan
    except:
        ebm = np.nan

    try:
        spobv = 1-mp/bv  #share price over book value
        if not spobv:
            spobv=np.nan
    except:
        spobv = np.nan

    return spobv, ebm, fpe, feps, fepss, tepss, teps, Eqs, cEQv, cEntv, po, isv, evb, eb, ev, sx, mc, tr, rg, oc, pi, eq, tpe, tc, bv, td, io, dy, so, mp

def numby(n):
    if n:
        nn = n/1000000
    else:
        nn = np.nan
    return round(nn, ndigits=2)

def johansle(stocks):
    JHstocks = pd.DataFrame()
    for stock in stocks:
        try:
            print(stock, end=' ')
            try:
                
                spobv, ebm, fpe, feps, fepss, tepss, teps, Eqs, cEQv, cEntv, po, isv, evb, eb, ev, sx, mc, tr, rg, oc, pi, eq, tpe, tc, bv, td, io, dy, so, mp = stockfacts(str(stock)+'.AX')
            except:
                print(stock, ' timed out..')
                
                sleep(randint(25,40))
                spobv, ebm, fpe, feps, fepss, tepss, teps, Eqs, cEQv, cEntv, po, isv, evb, eb, ev, sx, mc, tr, rg, oc, pi, eq, tpe, tc, bv, td, io, dy, so, mp = stockfacts(str(stock)+'.AX')
        
            inside_Tot_buyers, inside_Tot_sellers = stock_insider(stock)

            # print(bv, '****', type(bv))

            JHstocks = JHstocks.append(pd.DataFrame(
                            {
                                "Sector": [sx],
                                "Stock": [stock],
                                "MarketCap $MM": [numby(mc)],
                                "Total Cash $MM": [numby(tc)],
                                "Total Debt $MM": [numby(td)],
                                "OpCashflow $MM": [numby(oc)],
                                "TotRevenue $MM": [numby(tr)],
                                "Enterprise Value $MM": [numby(ev)],
                                "EBITDA $MM": [numby(eb)],
                                "CALC EV/EBITDA %": [round(evb, ndigits=3)],
                                "EBITDA Margin %": [round(ebm, ndigits=3)],
                                "Shares Outstanding": [so],
                                "Current SharePrice": [round(mp, ndigits=3)],
                                
                                "CALC Intrinsic Share Value": [round(isv, ndigits=3)],
                                "CALC Percentage Under %": [round(po, ndigits=3)],
                                "CALC Enterprise Value": [numby(cEntv)],
                                "CALC Equity Value": [numby(cEQv)],
                                "CALC Equity Shares": [round(Eqs, ndigits=3)],
                                "CALC Trailing EPS*PE Shareprice": [round(tepss, ndigits=3)],
                                "CALC Fwd EPS*PE Shareprice": [round(fepss, ndigits = 3)],
                                "Trailing Earnings Per Share": [teps],
                                "Fwd Earnings Per Share": [feps],
                                "BookValue": [round(bv, ndigits=2)],
                                "Shareprice/Bookvalue %": [round(spobv, ndigits=3)],
                                "Trailing PE": [round(tpe, ndigits=3)],
                                "Forward PE": [round(fpe, ndigits=3)],
                                "Qtrly Earnings Growth": [eq],
                                "Insiders%": [round(io, ndigits=2)],
                                "Institutions%": [round(pi, ndigits=2)],
                                "InsidersBUYLast12months": [inside_Tot_buyers],
                                "InsidersSELLast12months": [inside_Tot_sellers*-1],
                                "count": 1

                            }),ignore_index=True,)

        except:
            pass
    
    JHstocks = JHstocks.sort_values('CALC Percentage Under %', ascending=False)
    
    
    print('DONE')
    return JHstocks

def stock_insider(stock='LRK'):
    inside_Tot_buyers = -999
    inside_Tot_sellers = -999
    # try:
    #     url ='https://www.marketbeat.com/stocks/ASX/'+str(stock)+'/insider-trades/'
    #     page = requests.get(url)
    #     content = page.content
    #     soup = BeautifulSoup(content, 'html.parser')
    #     tb = soup.find_all('tr')
    #     time.sleep(randint(1,3))
    #     # tb is all the rows in the insider buyers table. the first two are total buy / sell. then the last n amount are individaul purchases and date of purchase
    #     inside_Tot_buyers = int(tb[0].text.split('$')[-1].split('.')[0].replace(',',''))
    #     inside_Tot_sellers = int(tb[1].text.split('$')[-1].split('.')[0].replace(',',''))
    # except:
    #     inside_Tot_buyers=np.nan
    #     inside_Tot_sellers=np.nan
        
    return inside_Tot_buyers, inside_Tot_sellers
#----------------------------
#---------------------------

dfAllData = pd.DataFrame()

stocks = ['ACL', 'ADO', 'AIS', 'BBN', 'BKT', 'BLD', 'BSA', 'BWX', 'CAP', 'CDA', 'DEG', 'EGH', 
'EL8', 'GNM', 'GRV', 'HLX', 'IDX', 'IVR', 'JHC', 'LCD', 'MIN', 'ONX', 'ORN', 'TLM', 'BPT', 'CAA', 'REG', 
'8EC', 'BPT', 'OOK', 'RIO', 'MIN', 'CVW', 'GDI', 'DXS', 'ENN', 'NMT', 'EBO', 'RMD', 'COG']
# # stocks = ['AHK', 'AHI']
# stocks = ['BPT', 'OOK', 'RIO', 'MIN', 'CVW', 'GDI', 'DXS', 'ENN', 'NMT', 'EBO', 'RMD', 'COG', 'TIN']
# stocks = ['NMT', 'EBO', 'RMD', 'COG', 'TIN', 'CVW', 'GDI']
stocks = ['LSF', 'BHP', 'LCL']


# stocks = Stocks2Call('ASX_Listed_Companies_19-07-2021_08-08-24_AEST.csv')

# for stock in stocklists:
# print(datetime.now())
# df = johansle(stocks)
# tday = str(date.today())
# df.to_csv('lsf.csv')
# print(datetime.now())