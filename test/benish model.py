from numpy import nan
from numpy.core.fromnumeric import repeat
from yahoo_fin import news
import yahoo_fin.stock_info as yf

import yfinance as yfs
# import yfinance as yf

# msft = yf.Ticker("MSFT")

# company_name = msft.info['longName']
import pandas as pd
balance_sheet = []
income_statement = []
cash_flow = []
years = []
summary = pd.DataFrame(columns=['Ticker','PE ratio','Profitability(/5)',"Leverage(/2)",'Operating efficiency(/2)','Piotroski F-score(/9)',"Strength"])

def get_data(ticker):
    global balance_sheet
    global cash_flow
    global income_statement
    global years
    balance_sheet = yf.get_balance_sheet(ticker)
    cash_flow = yf.get_cash_flow(ticker)
    income_statement = yf.get_income_statement(ticker)
    years = balance_sheet.columns
    # # print("b")
    # print(balance_sheet)
    # # print("c")
    # print(cash_flow)
    # # print("i")
    # print(income_statement)

def ratios():
   #Days Sales in Receivables Index(DSRI)
    net_rec = balance_sheet[years[0]]['netReceivables']
    net_rec_py = balance_sheet[years[1]]['netReceivables']
    sales = income_statement[years[0]]['totalRevenue']
    sales_py = income_statement[years[1]]['totalRevenue']
    DSRI = (net_rec/sales)/(net_rec_py/sales_py)
    #Gross Margin Index(GMI)
    cogs = income_statement[years[0]]['costOfRevenue']
    cogs_py = income_statement[years[1]]['costOfRevenue']
    GMI = ((sales_py - cogs_py)/sales_py)/((sales-cogs)/sales)
    #Asset Quality Index(AQI)
    current_asset = balance_sheet[years[0]]['totalCurrentAssets']
    ppe = balance_sheet[years[0]]['propertyPlantEquipment']
    securities =balance_sheet[years[0]]['commonStock']+balance_sheet[years[0]]['shortTermInvestments']
    total_asset =balance_sheet[years[0]]['totalAssets']
    current_asset_py = balance_sheet[years[1]]['totalCurrentAssets']
    ppe_py = balance_sheet[years[1]]['propertyPlantEquipment']
    securities_py =balance_sheet[years[1]]['commonStock']+balance_sheet[years[1]]['shortTermInvestments']
    total_asset_py =balance_sheet[years[1]]['totalAssets']
    AQI =(1-(current_asset+ppe+securities)/total_asset)/(1-(current_asset_py+ppe_py+securities_py)/total_asset_py)
    #Sales growth index
    SGI = sales/sales_py
    #Depreciation index
    Depr = cash_flow[years[0]]['depreciation']
    Depr_py =cash_flow[years[1]]['depreciation']
    DEPI = (Depr_py/(ppe_py+Depr_py))/(Depr/(ppe+Depr))
    #Sales General and Administrative Expenses Index
    sga = income_statement[years[0]]['sellingGeneralAdministrative']
    sga_py = income_statement[years[1]]['sellingGeneralAdministrative']
    SGAI = (sga/sales)/(sga_py/sales_py)
    #Leverage Index
    current_liab = balance_sheet[years[0]]['totalCurrentLiabilities']
    long_term_debt =balance_sheet[years[0]]['longTermDebt']
    current_liab_py =balance_sheet[years[1]]['totalCurrentLiabilities']
    long_term_debt_py =balance_sheet[years[1]]['longTermDebt']
    LVGI = ((current_liab+long_term_debt)/total_asset)/(current_liab_py+long_term_debt_py)/total_asset_py
    #Total accural to total asset
    incomefromcontops = income_statement[years[0]]['netIncomeFromContinuingOps']
    cashfromops = cash_flow[years[0]]['totalCashFromOperatingActivities']
    TATA = (incomefromcontops-cashfromops)/total_asset
    mscore = -4.84 +(.92*DSRI)+(.528*GMI)+(.404*AQI)+(.892*SGI)+(.115*DEPI)-(.172*SGAI)+(4.679*TATA)-(.327*LVGI)
    return mscore
    # mscore = −4.84 + 0.92 × DSRI + 0.528 × GMI + 0.404 × AQI + 0.892 × SGI + 0.115 × DEPI −0.172 × SGAI + 4.679 × TATA − 0.327 × LVGI

def benish_m_score(ticker):

    get_data(ticker)
    score = ratios()
    if score < -1.78:
        print("The benish M-score is {}.The company {} is unlikely to be a manipulator".format(score,ticker))
    else:
        print("The benish M-score is {}.The company {} is likely to be a manipulator".format(score,ticker))

ticker = 'AAPL'
msft = yfs.Ticker(ticker).info['longName']
print(msft)
benish_m_score(ticker)
print(yf.get_holders(ticker))