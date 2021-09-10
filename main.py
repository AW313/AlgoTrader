
from historytester import LoadYFinanceData, Stocks2Call, AlgoAverages, AlgoRateOfChange, tempclean, LoadDateRange, CurrentBuy_flag
from makemypdf import *
from datetime import date
import yfinance as yf

# -----------------------------------------------#
# #CHOOSE  DATE RANGE TO INVESTIGATE + FLAG LIMITS

starting_flag = "2021-08-01"
ending_flag = "2021-08-31"
volmultiple = 5
valuetraded = 2000000
benchmark_stock = "%5EAXJO"
# -----------------------------------------------#
#  LOAD DATA AND RANGE FROM CSV..

filepath = "/home/ajw/Documents/VSstudio/ASX Scaper/Stockscrappy2/ASX_Listed_Companies_22-06-2021_02-13-18_AEST.csv"
# df=HistoricalCsvLoad(filepath)
sdate, edate = LoadDateRange(starting_flag, ending_flag)
dfbuy = pd.DataFrame()

def stocklists():
    stocks = ['']
    stocks = ['ADI', 'ADO', 'AIS', 'BBN', 'BKT', 'BLD', 'BSA', 'BWX', 'CAP', 'CDA', 'DEG', 'EGH',
     'EL8', 'GNM', 'GRV', 'HLX', 'IDX', 'IVR', 'JHC', 'LCD', 'MIN', 'NXS', 'ONX', 'ORN', 'TLM']  #AW 'ACL', 
    
    # stocks=['MEL', 'VG8', 'CDM', 'MTM', 'LSF', 'STX', 'CSR', 'R3D', 'FEX']
    # stocks = ['MIN', 'BPT', 'RIO', 'MAH', 'CIM']
    # stocks = ['FEL', 'SFR', 'SVY', 'SLZ', 'SKY', 'RIO', 'MIN'] #coppAer
    # stocks = ['RAC', 'AZS', 'FAU', 'EX1', 'NYR', 'FEL']

    stocks=['AVA', 'AXP', 'HCH', 'IEQ']
    # stocks=['88E', 'BTC-AUD']

    return stocks
# ----------------------------------------------#
#  RUN SCRIPT to test HISTORIC PRICES
def historyrun():
    # for code in Stocks2Call():
    for code in stocks:
        print(code, end=" ")

        df_historic = LoadYFinanceData(code, sdate, edate)
        # df_historic=HistoricalCallByDate(code, df, sdate, edate)

        if len(df_historic) != 0:
            df_HistoricAverages = AlgoAverages(df_historic)
            df_ROC_flags = AlgoRateOfChange(df_HistoricAverages, volmultiple)
            dfbuy = HistoricBuyFlagToDF(
                df_ROC_flags, dfbuy, code, starting_flag, ending_flag, valuetraded
            )

        else:
            print("^", end="")
            pass

    dfbuy = BenchmarkASX(dfbuy, starting_flag, sdate, edate, benchmark_stock)
    dfbuy = CleanupPercentages(dfbuy)
    dfbuy.drop_duplicates("stock", inplace=True)
    print("\n\n\n\n", dfbuy)


    # print(dfbuy.describe())
    dfbuy.to_csv("testerJuly.csv", sep=",")
# historyrun(dfbuy)
#----------------------------------------------------------
# RUN SCRIPT CURRUNT DAY FLAGS
print('START', datetime.now())

def currentdayrun(dfbuy):
    print('stocks to process, ', end='')
    pdf = create_pdf_title(starting_flag, ending_flag, volmultiple, valuetraded)
    
    buyl=''
    # for code in Stocks2Call():
    stocks = stocklists()
    # stocks=['BIN']
    
    for code in stocks:
        print(code, end=" ")
        df_current = LoadYFinanceData(code, sdate, edate)
        # df_historic=HistoricalCallByDate(code, df, sdate, edate)
        if len(df_current) != 0:
            df_currentAverages = AlgoAverages(df_current)
            df_ROC_flags = AlgoRateOfChange(df_currentAverages, volmultiple)
            
            dated, buy, dfbuy, buyp = CurrentBuy_flag(df_ROC_flags, dfbuy, code, starting_flag, ending_flag, valuetraded)
        else:
            print("^", end="")
            pass

        buy=1  #  RUN THEM ALL
        if buy == True:# and yf.Ticker(code).info['marketCap'] is not None:
            buyl+=code+', '
            create_body_stock_report(df_ROC_flags, code, dated, pdf, buyp, starting_flag, ending_flag)
        else:
            print('', end='')
            pass
    

    dfbuy.drop_duplicates("stock", inplace=True)
    print("\n\n\n\n", dfbuy)

    print('buylist is  \n', buyl)
    save_df_as_image(dfbuy)
    pdf.add_page()
    pdf.write(25, 'BUY Overview \n\n')
    pdf.image('dfbuy.png', 8, 60, w=160)#WIDTH-15)
    lastpage(pdf)

    tday = str(date.today())
    pdf.output('JTs.pdf', 'F')
    # pdf.output('BUYLIST'+tday+'.pdf', 'F')    
    # dfbuy.to_csv('BUYRUN'+tday+'.csv', sep=",")
    
# print(stocks)
currentdayrun(dfbuy)
print('********* END', datetime.now())

tempclean()