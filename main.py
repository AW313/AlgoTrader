from historytester import *

# -----------------------------------------------#
# #CHOOSE  DATE RANGE TO INVESTIGATE + FLAG LIMITS

starting_flag = "2021-05-30"
ending_flag = "2021-07-08"
volmultiple = 5
valuetraded = 2000000
benchmark_stock = "%5EAXJO"
# -----------------------------------------------#
#  LOAD DATA AND RANGE FROM CSV..

filepath = "/home/ajw/Documents/VSstudio/ASX Scaper/Stockscrappy2/ASX_Listed_Companies_22-06-2021_02-13-18_AEST.csv"
# df=HistoricalCsvLoad(filepath)
sdate, edate = LoadDateRange(starting_flag, ending_flag)
dfbuy = pd.DataFrame()

stocks = ["AMI", "MWY", "CLW"]


# ----------------------------------------------#
#  RUN SCRIPT to test HISTORIC PRICES
def historyrun():
    # for code in Stocks2Call():
    for code in stocks:
        print(code, end=" ")

        df_historic = LoadYahooFinanceData(code, sdate, edate)
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
def currentdayrun(dfbuy):
    # for code in Stocks2Call():
    for code in stocks:
        print(code, end=" ")

        df_current = LoadYahooFinanceData(code, sdate, edate)
        # df_historic=HistoricalCallByDate(code, df, sdate, edate)

        if len(df_current) != 0:
            df_currentAverages = AlgoAverages(df_current)
            df_ROC_flags = AlgoRateOfChange(df_currentAverages, volmultiple)
            dfbuy = HistoricBuyFlagToDF(
                df_ROC_flags, dfbuy, code, starting_flag, ending_flag, valuetraded
            )

        else:
            print("^", end="")
            pass

    dfbuy.drop_duplicates("stock", inplace=True)
    print("\n\n\n\n", dfbuy)


    # print(dfbuy.describe())
    dfbuy.to_csv("buyflagsJuly.csv", sep=",")

currentdayrun(dfbuy)