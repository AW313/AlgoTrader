
import dataframe_image as dfi
from fpdf import FPDF
from datetime import datetime, timedelta, date
import os
import time
from time import sleep
from random import randint
import pandas as pd
import numpy as np
import datetime as dt
from matplotlib import pyplot as plt
import yfinance as yf
import requests
import re
from bs4 import BeautifulSoup
from asxoverviewtable import stockfacts, numby
pd.options.display.float_format = "{:,.2f}".format
plt.rcParams.update({'figure.max_open_warning': 0})
from scrape_directors import stock_buyers

WIDTH = 210
HEIGHT = 297

dater=date.today()


def save_df_as_image(df, path='/home/ajw/Documents/VSstudio/ASX Scaper/Stockscrappy2/dfbuy.png'):
    dfi.export(df, path)

def numt(n):
    x=0
    
    if n:
        if n<0:
            x=1
            n=abs(n)
        if n/1000000000>=1:
            nn = '${:,.2f} B'.format(n/1000000000)
        elif n/1000000>=1:
            nn = '${:,.2f} M'.format(n/1000000)
        elif n/1000>=1:
            nn = '${:,.0f} k'.format(n/1000)
        else: 
            nn = '{:.2f}'.format(n)
    else:
        nn = 'N/A'
    if x:
        nn = '-'+nn
    return nn

def title_format(date, pdf):
  # Unicode is not yet supported in the py3k version; use windows-1252 standard font
  pdf.set_font('Courier', '', 24)  
  pdf.ln(60)
  pdf.write(5, f"Muddystocks Weekly Review")
  pdf.ln(10)
  pdf.set_font('Courier', '', 16)
  pdf.write(4, f'{date}')
  pdf.ln(5)

def create_VOLfigure(df, stock, dated):
    
    try:
        x=4
        dated = datetime.strptime(str(dated), '%Y-%m-%d')
        dateplot = dated - timedelta(weeks=24)
        dx = df#[df.index>dateplot]
        covidmark = ['2020-03-15', dx['volume'].max()*0.8]
        s=int(len(df)/10)
        tickers = [d for d in dx.index[::s]]
        plt.subplots (figsize=(10, 4))
        plt.set_cmap('rainbow_r')
        plt.plot (dx[['volume', 'VOLSMA_100', 'BUY']])
        plt.ylim (dx['volume'].min(),dx['volume'].max())
        plt.xlim (dx.index.min(),dx.index.max())
        plt.scatter(covidmark[0], covidmark[1], marker='o')
        plt.annotate('COVID', (covidmark[0], covidmark[1]), )
        plt.ylabel('Volume', {'fontsize':x*3})
        plt.xticks (ticks=tickers, rotation=30, fontsize=x*2)
        plt.yticks(rotation=0, fontsize=x*2)
        plt.xlabel('Daily Volume', {'fontsize':x*2})
        plt.xlabel('Date', {'fontsize':x*2})
        plt.title(str(stock)+ ' Volume', {'fontsize':x*5})
        
        plt.legend(['Volume', 'VolAv', 'Buy'], fontsize=x*3, loc='upper left')
        volfile_local = '/home/ajw/Documents/VSstudio/ASX Scaper/Stockscrappy2/temp/'+str(stock)+'_vol'+str(dated)+'.jpg'
        plt.savefig(volfile_local, dpi=80)
        return volfile_local
    except ValueError:
        pass

def create_Barcashfigure(stock='BHP'):
    try:
        plt.clf()
        msft = yf.Ticker(stock)
        y = msft.balance_sheet.T/1000000
        plt.subplots (figsize=(6, 5))
        plt.bar(y.index, y['Cash'], align='edge', width=-80)
        plt.bar(y.index, y['Net Tangible Assets'], align='edge', width=80)
        # plt.bar(y.index, y['Total Operating Expenses'], align='center', width=60)
        plt.ticklabel_format(axis='y', style='plain', useLocale=True)
        plt.xticks(ticks=y.index, labels=list(y.index.strftime('%Y')), rotation=0)
        plt.legend(['Cash', 'Net Tangible Assets'], fontsize=10, loc='upper left')
        plt.axhline(y = 0, color = 'black', linestyle = '-')
        plt.ylabel('$ MM')
        plt.grid(axis='y') #, which='major', linewidth=2
        plt.title('Cash Etc FY $MM')

        barcashfile_local = '/home/ajw/Documents/VSstudio/ASX Scaper/Stockscrappy2/temp/'+str(stock)+'_barcash'+'.jpg'
        plt.savefig(barcashfile_local, dpi=80)
        return barcashfile_local
    except:
        print('barcash fail')
        pass

def create_BarPfigure(stock='BHP'):
    try:
        plt.clf()
        msft = yf.Ticker(stock)
        y = msft.financials.T/1000000
        plt.subplots (figsize=(6, 5))
        plt.bar(y.index, y['Net Income'], align='edge', width=-80)
        plt.bar(y.index, y['Total Revenue'], align='edge', width=80)
        plt.bar(y.index, y['Total Operating Expenses'], align='center', width=60)
        plt.ticklabel_format(axis='y', style='plain', useLocale=True)
        plt.xticks(ticks=y.index, labels=list(y.index.strftime('%Y')), rotation=0)
        plt.legend(['Net Income', 'Total Revenue', 'Total Operating Expenses'], fontsize=10, loc='upper left')
        plt.axhline(y = 0, color = 'black', linestyle = '-')
        plt.ylabel('$ MM')
        plt.grid(axis='y') #, which='major', linewidth=2
        plt.title('Profits FY $MM')

        barfile_local = '/home/ajw/Documents/VSstudio/ASX Scaper/Stockscrappy2/temp/'+str(stock)+'_barp'+'.jpg'
        plt.savefig(barfile_local, dpi=80)
        return barfile_local
    except:
        print('barP fail')
        pass


def create_pricefigure(df, stock, dated):
    
    try:
        x=4
        dated = datetime.strptime(str(dated), '%Y-%m-%d')
        dateplot = dated - timedelta(weeks=24)
        s=int(len(df)/10)
        tickers = [d for d in df.index[::s]]
        plt.locator_params(axis='x', nbins=5)
        dx = df#[df.index>dateplot]
        covidmark = ['2020-03-15', df['price'].mean()*1.2]
        
        plt.subplots (figsize=(10, 5))
        plt.plot (dx[['price', 'EWM', 'flag']])
        plt.scatter(covidmark[0], covidmark[1], marker='o')
        plt.annotate('COVID', (covidmark[0], covidmark[1]), )
        plt.ylim (dx['price'].min(),dx['price'].max())
        plt.xlim (dx.index.min(),dx.index.max())
        plt.xticks (ticks=tickers, rotation=30, fontsize=x*2)
        plt.yticks(rotation=0, fontsize=x*2)
        plt.xlabel('Date', {'fontsize':x*2})
        plt.ylabel('Price $', {'fontsize':x*3})
        plt.legend(['price', 'EWM', 'flag'], fontsize=x*3, loc='upper left')

        plt.title(str(stock)+ ' Price', {'fontsize':x*5})
        pricefile_local = '/home/ajw/Documents/VSstudio/ASX Scaper/Stockscrappy2/temp/'+str(stock)+'_price'+str(dated)+'.jpg'
        plt.savefig(pricefile_local, dpi=80)
        return pricefile_local
    except ValueError:
        pass
                
def create_pdf_title(sdate, edate,  volmultiple, valuetraded):
    pdf = FPDF() # A4 (210 by 297 mm)
    pdf.add_page()
    dated = date.today().strftime('%d of %B, %Y')
    sdate = datetime.strptime(sdate, "%Y-%m-%d").strftime('%d-%B')
    edate = datetime.strptime(edate, "%Y-%m-%d").strftime('%d-%B, %Y')
    # pdf.image("./resources/letterhead_cropped.png", 0, 0, WIDTH)
    title_format(dated, pdf)
    vt = numt(valuetraded)
    pdf.set_font('Courier')
    pdf.set_font_size(12)
    pdf.write(8, f"""\n\n\n Automated report on all ASX stocks flagged between a search range. \n
     Report range: {sdate} - {edate}\n
     First attempt 'BUY FLAG' stocks have the following requirements: 
     Share price has a rolling average with an increasing rate of change 
     AND a daily volume traded of over {volmultiple} Xs the rolling Average volume traded 
     AND daily trade value over {vt}M
     AND all flags fall within the date search range""")
    
    
    return pdf
     # dfimagelocal = str(stock)+'_df.png'
    # save_df_as_image(df, dfimagelocal)
    # pdf.image(dfimagelocal, 20, 100, w=160)#WIDTH-15)

def unikode(txt):
    tt=''
    # value = str(txt.encode("ascii", errors="replace"))
    for t in txt.split():
        t = t.encode("utf-8", errors='replace')
        try:
            tt += t.decode('ascii')+' '
        except:
            pass
    return tt

# def create_body_stock_report(df, stock, dated, pdf):
    dd = datetime.strptime(dated, '%Y-%m-%d')
    if stock != "%5EAXJO":
        stock += ".AX"
    msft = yf.Ticker(stock)
    
    sd = msft.get_info()
    #---------- dict text
    if stock != 'VTS.AX':
        try:
            mc = numt(sd['marketCap'])
        except:
            mc='N/A'
        try:
            tr = numt(sd['totalRevenue'])
        except:
            tr = 'N/A'
        try:
            rg = str(numt(sd['revenueGrowth']))+'%'
        except:
            rg = 'N/A'
        try:
            oc = numt(sd['operatingCashflow'])
        except:
            oc = 'N/A'
        try:
            pi = str(numt(sd['heldPercentInstitutions']*100))+'%'
        except:
            pi='N/A'
        try:
            eq = numt(sd['earningsQuarterlyGrowth'])
        except:
            eq = 'N/A'
        try:
            pe = numt(sd['trailingPE'])
        except:
            pe = 'N/A'
        try:
            tc = numt(sd['totalCash'])
        except:
            tc = 'N/A'
        try:
            bv = '$'+str(numt(sd['bookValue']))
        except:
            bv = 'N/A'
        try:
            td = numt(sd['totalDebt'])
        except:
            td = 'N/A'
        try:
            io = str(numt(sd['heldPercentInsiders']*100))+'%'
        except:
            io = 'N/A'
        try:
            dy = str(numt(sd['dividendYield']))+'%'
        except:
            dy='N/A'
        try:
            so = numt(sd['sharesOutstanding'])
        except:
            so='N/A'

        txt = unikode(sd['longBusinessSummary'])
        pdf.add_page()
        pdf.set_font('Courier', 'B')
        pdf.set_font_size(12)
        pdf.write(8, f"{stock[:3]} - {sd['longName']} \n")

        pdf.set_font('Courier')
        pdf.set_font_size(10)
        pdf.write(6, f"Operates in {unikode(sd['sector'])}, {unikode(sd['industry'])}.     Flag date {dd.strftime('%d of %B, %Y')}\n\n")

        pdf.set_font('Courier')
        pdf.set_font_size(8)
        pdf.write(5, f"""BIO:  {txt[:480]}
                     ----------------------------------------------------------------

        SHEET INFO
        Market cap:     {mc}          Revenue Growth:   {rg}     %Institutions: {pi}
        Total Revenue :  {tr}                                        %Insiders:  {io}
        Total Cash:      {tc}           Dividend Yeild {dy}
        Total Debt:      {td}           Price Earn Ratio: {pe} 
        Operating Cashflow: {oc}
        Qtrly Earn Growth: {eq}              
                                                SharesOn offer  {so}
                                    Book Value (mrq)-base price:   {bv}
                            
        
        mrq- most recent quarter / yoy- Year on Year
        """)
    try:
        pricefile_local = create_pricefigure(df, stock, dated)
        pdf.image(pricefile_local, 3, 120, w=140)#WIDTH-15)

        volfile_local = create_VOLfigure(df, stock, dated)
        pdf.image(volfile_local, 3, 210, w=140)#WIDTH-15)
    except:
        pass
    
def create_figsheet(df, stock, dated, pdf):
    pdf.add_page()
    pdf.set_font('Courier', 'B')
    pdf.set_font_size(12)
    pdf.write(8, f"{stock} ")
    try:
        pricefile_local = create_pricefigure(df, stock, dated)
        pdf.image(pricefile_local, 3, 120, w=140)#WIDTH-15)

        volfile_local = create_VOLfigure(df, stock, dated)
        pdf.image(volfile_local, 3, 210, w=140)#WIDTH-15)
    except:
        pass

def create_body_stock_report(df, stock, dated, pdf, buyp, starting_flag, ending_flag):
    dead=0
    dirlist, url = stock_buyers(stock, starting_flag, ending_flag)

    dd = datetime.strptime(dated, '%Y-%m-%d')
    if stock != "%5EAXJO":
        stock += ".AX"
    msft = yf.Ticker(stock)
    sd = msft.get_info()
    if stock != 'VTS.AX':
        try:
            time.sleep(randint(1,3))
            spobv, ebm, fpe, feps, fepss, tepss, teps, Eqs, cEQv, cEntv, po, isv, evb, eb, ev, sx, mc, tr, rg, oc, pi, eq, tpe, tc, bv, td, io, dy, so, mp = stockfacts(stock)
        except:
            print(stock, ' timed out..', end='')
            time.sleep(randint(20,50))
            spobv, ebm, fpe, feps, fepss, tepss, teps, Eqs, cEQv, cEntv, po, isv, evb, eb, ev, sx, mc, tr, rg, oc, pi, eq, tpe, tc, bv, td, io, dy, so, mp = stockfacts(stock)
        
            
        try:
            
            valt = df.loc[dated, 'valuetraded']
            volx = df.loc[dated, 'VolX']

        except:
            print('not flagged as a BUY')
            buyp=0
            valt=[0.0]
            volx=[0,0]
        if isinstance(valt, pd.Series):
            buyp=0
            valt=[0.0]
            volx=[0,0]
        try:
            txt = unikode(sd['longBusinessSummary'])
        
            k_eb, k_by, k_sl, k_bv, k_io, k_so = kolor(eb=ebm, sbv=spobv, kio=io, so=so)
            

            #---------------------------PAGE SETUP------------------------
            
            pdf.add_page()
            pdf.set_font('Courier', 'B')
            pdf.set_font_size(12)
            pdf.write(8, f"{stock[:3]} - {sd['longName']} \n")

            pdf.set_font('Courier')
            pdf.set_font_size(10)
            pdf.write(6, f"Operates in {unikode(sd['sector'])}, {unikode(sd['industry'])}.     Flag date {dd.strftime('%d of %B, %Y')}")
            pdf.ln(8)
            pdf.set_font('Courier')
            pdf.set_font_size(8)
            pdf.write(5, f"""BIO:  {txt[:480]}
                        ----------------------------------------------------------------\n""")
            
            pdf.cell(0,0,'SHEET INFO $MM')
            pdf.link(50, 80, 30, 8, "https://github.com/PyFPDF/fpdf2")
            pdf.ln(3)

            pdf.cell(50,8, f'Market Cap ${numby(mc)}',  align='L')
            pdf.cell(50,8, f'Current Share Price ${round(mp, ndigits=3)}',  align='R')
            pdf.cell(50,8, f'Under {round(po, ndigits=3)}%', align='R')

            pdf.ln(8)
            pdf.cell(50,8, f'Total Revenue ${numby(tr)}',  align='L')
            pdf.cell(50,8, f'CALC Intrinsic ShareValue ${round(isv, ndigits=3)}',align='R')
            pdf.set_fill_color(k_bv[0], k_bv[1], k_bv[2])
            pdf.cell(50,8, f'Book Value ${round(spobv, ndigits=3)}',  align='R', fill=True)

            pdf.ln(8)
            pdf.cell(50,8, f'Total Cash ${numby(tc)}',  align='L')
            pdf.cell(50,8, f'CALC Enterprise Value ${numby(cEntv)}',  align='R')
            pdf.cell(50,8, f'T_PE {round(tpe, ndigits=3)} F_PE {round(fpe, ndigits=3)}',  align='R')

            pdf.ln(8)
            pdf.cell(50,8, f'Total Debt ${numby(td)}', align='L')
            pdf.cell(50,8, f'CALC Equity Value ${numby(cEQv)}',  align='R')
            pdf.cell(50,8, f'T_EPS {teps}, F_EPS {feps}',  align='R')

            pdf.ln(8)
            pdf.cell(50,8, f'Operating Cashflow ${numby(oc)}', align='L')
            pdf.cell(50,8, f'CALC Equity Shares ${round(Eqs, ndigits=3)}',  align='R')
            pdf.cell(50,8, f'FLAGGED',  border = 'B', align='R')

            pdf.ln(8)
            pdf.cell(50,8, f'Enterprise Value ${numby(ev)}', align='L')
            pdf.set_fill_color(k_io[0], k_io[1], k_io[2])
            pdf.cell(50,8, f'Insiders Own % {round(io, ndigits=2)}',  align='R', fill=True)
            pdf.cell(50,8, f' BUY Date {dated}',  align='R')
            
            pdf.ln(8)
            pdf.set_fill_color(k_eb[0], k_eb[1], k_eb[2])
            pdf.cell(50,8, f'EBITDA Margin {round(ebm, ndigits=3)}%', align='L', fill=True)
            pdf.cell(50,8, f'Institutions Own {round(pi, ndigits=2)}%',  align='R')
            pdf.cell(50,8, f' BUY price $ {round(buyp, ndigits=2)}',  align='R')

            pdf.ln(8)  
            pdf.set_fill_color(k_so[0], k_so[1], k_so[2])
            pdf.cell(50,8, f'Shares On Offer {so}', align='L', fill=True)
            pdf.cell(50,8, f'', align='R')
            pdf.cell(50,8, f' Volume Over Av. {round(volx[0], ndigits=1)} Xs', align='R')

            pdf.ln(8)
            # pdf.set_fill_color(k_by[0], k_by[1], k_by[2])
            # pdf.cell(50,8, f'Insider buyers ${inside_Tot_buyers}', align='L', border = 'T', fill=True)
            # pdf.set_fill_color(k_sl[0], k_sl[1], k_sl[2])
            # pdf.cell(50,8, f'Insider Sellers ${inside_Tot_sellers}', align='C', border = 'T', fill=True)
            
            # pdf.set_fill_color(160, 255, 0)
            pdf.cell(50,8, f' Value Traded $MM {numby(valt[0])}', align='R')
            
            pdf.ln(8)
            pdf.cell(150,8, f' {dirlist}', align='L')
            # pdf.ln(8)
            # pdf.cell(150,8, f'SELLS {sellerslist}', align='L')

            pdf.ln(8)
            pdf.write(url)
        except:
            print('broke', end='')
            pass

    try:
        
        pricefile_local = create_pricefigure(df, stock, dated)
        pdf.image(pricefile_local, 3, 150, w=140)#WIDTH-15)

        volfile_local = create_VOLfigure(df, stock, dated)
        pdf.image(volfile_local, 3, 220, w=140)#WIDTH-15)
        
        barfile_local = create_BarPfigure(stock)
        pdf.image(barfile_local, 140, 155, w=65)#WIDTH-15)

        barcashfile_local = create_Barcashfigure(stock)
        pdf.image(barcashfile_local, 140, 220, w=65)#WIDTH-15)

    except:
        pass

def lastpage(pdf):


    pdf.add_page()
    pdf.set_font('Courier')
    pdf.set_font_size(8)
    pdf.write(5, """
    Revenue $MM:  recent full year revenue figures. Revenue from sales and services. Investment income not usually included

    Year on Year Revenue Growth %: growth profit is usually a better indicator. Companies can increase revenue by all kinds of means, including cutting profit margins or aquiring other companies. 
    This is of little use unless combined with other improving ratios. Uses latest full year figures

    EBIT Margin %: (>0, can be small ie.wesfarmers) Company earnings before interest and tax, shown as % of annual sales. Sometimes regarded as a better measure of its profitability. HAs little relevance for banks
    YoY EBIT Growth %: Measure of a comapnies efficiency. company is succesfully cutting costs

    EPS %: (>0) YoY Earnings Per Share. look for growth in EPS, ie greater than 0.

    Return on Equity %: (>10) company assets - debts. After tax profit as a %. Important gauge on how well a company is doing
    If ROE is growing each year ,  a real growth stock

    Debt 2 Equity Ratio %: (<70). be wary of a nubmer thats too high. unless its a slow growth stock . if 0, no debt. 

    Current Ratio : company assets (cash or quick assets) / Liabilities. the company ability to pay back quick debt. higher = better

    PER : Price Earnings Ratio. high = good. low = poor. current shareprice / earnings per share

    p NTA ratio: Price to NTA per share ratio. Assets - liabilities and tangible assets. value of 1 means its evaluated according to its assets

    Johans;
    Intrinsic Value: (EV + total cash - total debt) / no. shares
    Enterprise Value (EV): (market cap + debt) - total cash
    Equity Value:  ( EV + cash) - debt
    Equity Shares: EV / no. shares

    To identify trends, MPT analysts employ the Brooks ratio, which divides total insider sales of a company by total insider 
    trades (purchases and sales) and then averages this ratio for thousands of stocks. If the average Brooks ratio is less than
     40%, the market outlook is bullish; above 60% signals a bearish outlook.


    """)

def kolor(eb=0.1, by=2000, sl=-50, sbv=0.5, kio=23, so=300):
    
    red = [255,80,80]
    pink = [255, 140,150]
    orange = [255,130,0]
    yellow = [255,250,80]
    green = [130, 255, 0]
    blue = [15,15,255]
    white = [255,255,255]
    try:
        if -2<eb<=0:
            k_eb = pink
        elif eb<=-2:
            k_eb = red
        elif 0<eb<=3:
            k_eb = orange
        else:
            k_eb = green

        if by>2000000:
            k_by = blue
        elif by>200000:
            k_by = green
        elif by>1:
            k_by = yellow
        else:
            k_by=white

        if sl>1000000:
            k_sl = red
        elif sl>200000:
            k_sl = pink
        elif sl>1:
            k_sl = orange
        else:
            k_sl=white

        if sbv>=0.5:
            k_bv = blue
        elif sbv>0:
            k_bv = green
        elif sbv>-0.5:
            k_bv = yellow
        elif sbv>-1:
            k_bv = orange
        elif sbv>-1.5:
            k_bv = pink
        else:
            k_bv = red

        if kio>75:
            k_io = red
        elif kio>50:
            k_io = orange
        elif kio<10:
            k_io = red
        else:
            k_io = green

        if so > 2000000000:
            k_so = red
        elif so > 1500000000:
            k_so = orange
        else:
            k_so = white
    except:
        print('kolor bust')
        k_eb, k_by, k_sl, k_bv, k_io, k_so = white, white, white, white, white, white
    return k_eb, k_by, k_sl, k_bv, k_io, k_so
