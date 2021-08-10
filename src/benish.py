from numpy import nan
from numpy.core.fromnumeric import repeat
from yahoo_fin import news
import yahoo_fin.stock_info as yf
import yfinance as yfs
import pandas as pd

balance_sheet = []
income_statement = []
cash_flow = []
years = []

def get_data(ticker):
    global balance_sheet
    global cash_flow
    global income_statement
    global years
    cmp = yfs.Ticker(ticker)
    balance_sheet = cmp.balance_sheet
    cash_flow = cmp.cashflow
    income_statement = cmp.financials
    years = balance_sheet.columns

def ratios():
   #Days Sales in Receivables Index(DSRI)
    net_rec = balance_sheet[years[0]]['Net Receivables']
    net_rec_py = balance_sheet[years[1]]['Net Receivables']
    sales = income_statement[years[0]]['Total Revenue']
    sales_py = income_statement[years[1]]['Total Revenue']
    DSRI = (net_rec/sales)/(net_rec_py/sales_py)
    #Gross Margin Index(GMI)
    cogs = income_statement[years[0]]['Cost Of Revenue']
    cogs_py = income_statement[years[1]]['Cost Of Revenue']
    GMI = ((sales_py - cogs_py)/sales_py)/((sales-cogs)/sales)
    #Asset Quality Index(AQI)
    current_asset = balance_sheet[years[0]]['Total Current Assets']
    ppe = balance_sheet[years[0]]['Property Plant Equipment']
    securities =balance_sheet[years[0]]['Common Stock']+balance_sheet[years[0]]['Short Term Investments']
    total_asset =balance_sheet[years[0]]['Total Assets']
    current_asset_py = balance_sheet[years[1]]['Total Current Assets']
    ppe_py = balance_sheet[years[1]]['Property Plant Equipment']
    securities_py =balance_sheet[years[1]]['Common Stock']+balance_sheet[years[1]]['Short Term Investments']
    total_asset_py =balance_sheet[years[1]]['Total Assets']
    AQI =(1-(current_asset+ppe+securities)/total_asset)/(1-(current_asset_py+ppe_py+securities_py)/total_asset_py)
    #Sales growth index
    SGI = sales/sales_py
    #Depreciation index
    Depr = cash_flow[years[0]]['Depreciation']
    Depr_py =cash_flow[years[1]]['Depreciation']
    DEPI = (Depr_py/(ppe_py+Depr_py))/(Depr/(ppe+Depr))
    #Sales General and Administrative Expenses Index
    sga = income_statement[years[0]]['Selling General Administrative']
    sga_py = income_statement[years[1]]['Selling General Administrative']
    SGAI = (sga/sales)/(sga_py/sales_py)
    #Leverage Index
    current_liab = balance_sheet[years[0]]['Total Current Liabilities']
    long_term_debt =balance_sheet[years[0]]['Long Term Debt']
    current_liab_py =balance_sheet[years[1]]['Total Current Liabilities']
    long_term_debt_py =balance_sheet[years[1]]['Long Term Debt']
    LVGI = ((current_liab+long_term_debt)/total_asset)/(current_liab_py+long_term_debt_py)/total_asset_py
    #Total accural to total asset
    incomefromcontops = income_statement[years[0]]['Net Income From Continuing Ops']
    cashfromops = cash_flow[years[0]]['Total Cash From Operating Activities']
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
    
    return score

# ticker = 'AAPL'
# msft = yfs.Ticker(ticker).info['longName']
# print(msft)
# benish_m_score(ticker)
# print(yf.get_holders(ticker))