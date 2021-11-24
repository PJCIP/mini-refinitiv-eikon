# Requires fcf.py to be in same directory for working of this file
from src import companyinfo
import pandas_datareader.data as web
import yfinance as yf
import datetime
from src import fcf 
from nsepy import get_history
import numpy as np
import pandas as pd
import urllib.request
import pandas as pd
from pprint import pprint
from html_table_parser.parser import HTMLTableParser
import ssl
ssl._create_default_https_context = ssl._create_unverified_context


def url_get_contents(url):
    """ Opens a website and read its binary contents (HTTP Response Body) """
    req = urllib.request.Request(url=url)
    f = urllib.request.urlopen(req)
    return f.read()

def extract_table(url):
    xhtml = url_get_contents(url).decode('utf-8')
    p = HTMLTableParser()
    p.feed(xhtml)
    table = p.tables
    return table


def base(ticker,market,period):
  balance_sheet,cash_flow,income_statement = companyinfo.statements(ticker)
  years = balance_sheet.columns

  # Calculating Effective Tax Rate
  EBIT = income_statement[years[0]]['Ebit']
  IE = income_statement[years[0]]['Interest Expense']
  TE = income_statement[years[0]]['Income Tax Expense']
  EBT = EBIT - IE
  ETR = TE/EBT

  Debt_to = balance_sheet[years[0]]['Total Liab'] / (balance_sheet[years[0]]['Total Liab'] + balance_sheet[years[0]]['Total Stockholder Equity'])
  equity_to = balance_sheet[years[0]]['Total Stockholder Equity'] / (balance_sheet[years[0]]['Total Liab'] + balance_sheet[years[0]]['Total Stockholder Equity'])

  # Calculate interest coverage ratio which inturn used for finding the credit spread

  interest_coverage_ratio = abs(EBIT/IE)
  # print("EBIT:{}")
  # interest_coverage_ratio=15.99367088607595


  # RF of india from RBI perspective
  # RF = 0.063640
  if market == 'Global Market':

    if period == "Current":    
      start = datetime.datetime.now() - datetime.timedelta(days=1*365)
      start = start.strftime('%Y-%m-%d')
              
      end= datetime.datetime.today().strftime('%Y-%m-%d')
      #end = datetime.datetime(2020, 7, 10)

      Treasury = web.DataReader(['TB1YR'], 'fred', start, end)
      RF = float(Treasury.iloc[-1])
      RF = RF/100

      SP500 = web.DataReader(['sp500'], 'fred', start, end)
      SP500.dropna(inplace = True)
      # print(SP500)
      rows = SP500.shape[0]
      # print(rows)
      yearlyreturn = (SP500['sp500'].iloc[-1]/ SP500['sp500'].iloc[-rows])-1

    elif period == "Before pandemic":
      start = datetime.datetime(2018, 4, 1)
      end= datetime.datetime(2019,4,1)
              
      # end= datetime.datetime.today().strftime('%Y-%m-%d')
      #end = datetime.datetime(2020, 7, 10)

      Treasury = web.DataReader(['TB1YR'], 'fred', start, end)
      RF = float(Treasury.iloc[-1])
      RF = RF/100
      SP500 = web.DataReader(['sp500'], 'fred', start, end)
      SP500.dropna(inplace = True)
      # print(SP500)
      rows = SP500.shape[0]
      # print(rows)
      yearlyreturn = (SP500['sp500'].iloc[-1]/ SP500['sp500'].iloc[-rows])-1

    elif period == "During pandemic":
      start = datetime.datetime(2020, 4, 1)
      end= datetime.datetime(2021,4,1)
      Treasury = web.DataReader(['TB1YR'], 'fred', start, end)
      RF = float(Treasury.iloc[-1])
      RF = RF/100
      SP500 = web.DataReader(['sp500'], 'fred', start, end)
      SP500.dropna(inplace = True)
      # print(SP500)
      rows = SP500.shape[0]
      # print(rows)
      yearlyreturn = (SP500['sp500'].iloc[-1]/ SP500['sp500'].iloc[-rows])-1

    
  elif market == "Indian Market":
    crp_url = 'https://pages.stern.nyu.edu/~adamodar/New_Home_Page/datafile/ctryprem.html'
    crp = extract_table(crp_url)[0]
    df = pd.DataFrame(crp,columns=crp[0])
    df.drop(index=df.index[0], 
        axis=0, 
        inplace=True)
    crp = str(df[(df.Country == "India")]['Country Risk Premium']).split('%')[0].split(' ')
    crp_list = list(filter(None, crp))
    crp = float(crp_list[1])/100
    RF = 0.063640 - crp
    if period == "Current":    
      start = datetime.datetime.now() - datetime.timedelta(days=1*365)
      # start = start.strftime('%Y-%m-%d')
      end= datetime.datetime.today()
      nfty50 = get_history(symbol='NIFTY 50', start=start, end=end, index = True)
      nfty50 = pd.DataFrame(nfty50)
      nfty50['Index_Name'] = 'NIFTY 50'
      rows = nfty50.shape[0]
      yearlyreturn = (nfty50['Close'].iloc[-1]/ nfty50['Close'].iloc[-rows])-1


    elif period == "Before pandemic":
      start = datetime.datetime(2018, 4, 1)
      end= datetime.datetime(2019,4,1)
      
      nfty50 = get_history(symbol='NIFTY 50', start=start, end=end, index = True)
      nfty50 = pd.DataFrame(nfty50)
      nfty50['Index_Name'] = 'NIFTY 50'
      rows = nfty50.shape[0]
      yearlyreturn = (nfty50['Close'].iloc[-1]/ nfty50['Close'].iloc[-rows])-1


    elif period == "During pandemic":
      start = datetime.datetime(2020, 4, 1)
      end= datetime.datetime(2021,4,1)
      
      nfty50 = get_history(symbol='NIFTY 50', start=start, end=end, index = True)
      nfty50 = pd.DataFrame(nfty50)
      nfty50['Index_Name'] = 'NIFTY 50'
      rows = nfty50.shape[0]
      yearlyreturn = (nfty50['Close'].iloc[-1]/ nfty50['Close'].iloc[-rows])-1


  return RF,interest_coverage_ratio,Debt_to,equity_to,ETR,yearlyreturn

def market(ticker,period):
  
  if period == "Current":    
    start = datetime.datetime.now() - datetime.timedelta(days=1*365)
    # start = start.strftime('%Y-%m-%d')
            
    end= datetime.datetime.today()
    #end = datetime.datetime(2020, 7, 10)

    Treasury = web.DataReader(['TB1YR'], 'fred', start, end)
    RF = float(Treasury.iloc[-1])
    gRF = RF/100

    SP500 = web.DataReader(['sp500'], 'fred', start, end)
    SP500.dropna(inplace = True)
    # print(SP500)
    rows = SP500.shape[0]
    print("sp 500 current")
    print(rows)
    gyearlyreturn = (SP500['sp500'].iloc[-1]/ SP500['sp500'].iloc[-rows])-1


  elif period == "Before pandemic":
    start = datetime.datetime(2018, 4, 1)
    end= datetime.datetime(2019,4,1)
            
    # end= datetime.datetime.today().strftime('%Y-%m-%d')
    #end = datetime.datetime(2020, 7, 10)

    Treasury = web.DataReader(['TB1YR'], 'fred', start, end)
    RF = float(Treasury.iloc[-1])
    gRF = RF/100
    SP500 = web.DataReader(['sp500'], 'fred', start, end)
    SP500.dropna(inplace = True)
    # print(SP500)
    rows = SP500.shape[0]
    print("sp 500 BP")
    print(rows)
    gyearlyreturn = (SP500['sp500'].iloc[-1]/ SP500['sp500'].iloc[-rows])-1

  elif period == "During pandemic":
    start = datetime.datetime(2020, 4, 1)
    end= datetime.datetime(2021,4,1)
    Treasury = web.DataReader(['TB1YR'], 'fred', start, end)
    RF = float(Treasury.iloc[-1])
    gRF = RF/100
    SP500 = web.DataReader(['sp500'], 'fred', start, end)
    SP500.dropna(inplace = True)
    # print(SP500)
    rows = SP500.shape[0]
    print("sp 500 DP")
    print(rows)
    gyearlyreturn = (SP500['sp500'].iloc[-1]/ SP500['sp500'].iloc[-rows])-1

  
  crp_url = 'https://pages.stern.nyu.edu/~adamodar/New_Home_Page/datafile/ctryprem.html'
  crp = extract_table(crp_url)[0]
  df = pd.DataFrame(crp,columns=crp[0])
  df.drop(index=df.index[0], 
      axis=0, 
      inplace=True)
  crp = str(df[(df.Country == "India")]['Country Risk Premium']).split('%')[0].split(' ')
  crp_list = list(filter(None, crp))
  crp = float(crp_list[1])/100
  iRF = 0.063640 - crp

  if period == "Current":    
    start = datetime.datetime.now() - datetime.timedelta(days=1*365)
    # start = start.strftime('%Y-%m-%d')
    end= datetime.datetime.today()
    nfty50 = get_history(symbol='NIFTY 50', start=start, end=end, index = True)
    nfty50 = pd.DataFrame(nfty50)
    nfty50['Index_Name'] = 'NIFTY 50'
    rows = nfty50.shape[0]
    print("n50 current")
    print(rows)
    nyearlyreturn = (nfty50['Close'].iloc[-1]/ nfty50['Close'].iloc[-rows])-1


  elif period == "Before pandemic":
    start = datetime.datetime(2018, 4, 1)
    end= datetime.datetime(2019,4,1)
    nfty50 = get_history(symbol='NIFTY 50', start=start, end=end, index = True)
    nfty50 = pd.DataFrame(nfty50)
    nfty50['Index_Name'] = 'NIFTY 50'
    rows = nfty50.shape[0]
    print("n50 bp")
    print(rows)
    nyearlyreturn = (nfty50['Close'].iloc[-1]/ nfty50['Close'].iloc[-rows])-1


  elif period == "During pandemic":
    start = datetime.datetime(2020, 4, 1)
    end= datetime.datetime(2021,4,1)
    nfty50 = get_history(symbol='NIFTY 50', start=start, end=end, index = True)
    nfty50 = pd.DataFrame(nfty50)
    nfty50['Index_Name'] = 'NIFTY 50'
    rows = nfty50.shape[0]
    print("n50 dp")
    print(rows)
    nyearlyreturn = (nfty50['Close'].iloc[-1]/ nfty50['Close'].iloc[-rows])-1


  return nfty50,SP500,nyearlyreturn,gyearlyreturn,gRF,iRF


# print(RF, interest_coverage_ratio)

def cost_of_debt(RF,interest_coverage_ratio):
  if interest_coverage_ratio > 8.5:
    #Rating is AAA
    credit_spread = 0.0063
  if (interest_coverage_ratio > 6.5) & (interest_coverage_ratio <= 8.5):
    #Rating is AA
    credit_spread = 0.0078
  if (interest_coverage_ratio > 5.5) & (interest_coverage_ratio <=  6.5):
    #Rating is A+
    credit_spread = 0.0098
  if (interest_coverage_ratio > 4.25) & (interest_coverage_ratio <=  5.49):
    #Rating is A
    credit_spread = 0.0108
  if (interest_coverage_ratio > 3) & (interest_coverage_ratio <=  4.25):
    #Rating is A-
    credit_spread = 0.0122
  if (interest_coverage_ratio > 2.5) & (interest_coverage_ratio <=  3):
    #Rating is BBB
    credit_spread = 0.0156
  if (interest_coverage_ratio > 2.25) & (interest_coverage_ratio <=  2.5):
    #Rating is BB+
    credit_spread = 0.02
  if (interest_coverage_ratio > 2) & (interest_coverage_ratio <=  2.25):
    #Rating is BB
    credit_spread = 0.0240
  if (interest_coverage_ratio > 1.75) & (interest_coverage_ratio <=  2):
    #Rating is B+
    credit_spread = 0.0351
  if (interest_coverage_ratio > 1.5) & (interest_coverage_ratio <=  1.75):
    #Rating is B
    credit_spread = 0.0421
  if (interest_coverage_ratio > 1.25) & (interest_coverage_ratio <=  1.5):
    #Rating is B-
    credit_spread = 0.0515
  if (interest_coverage_ratio > 0.8) & (interest_coverage_ratio <=  1.25):
    #Rating is CCC
    credit_spread = 0.0820
  if (interest_coverage_ratio > 0.65) & (interest_coverage_ratio <=  0.8):
    #Rating is CC
    credit_spread = 0.0864
  if (interest_coverage_ratio > 0.2) & (interest_coverage_ratio <=  0.65):
    #Rating is C
    credit_spread = 0.1134
  if interest_coverage_ratio <=  0.2:
    #Rating is D
    credit_spread = 0.1512
  

  cost_of_debt = RF + credit_spread
  # print("kd:{},RF:{},credit_spread:{},icr:{}".format(cost_of_debt,RF,credit_spread,interest_coverage_ratio))
  return cost_of_debt,credit_spread



#Calculating the Cost_of_equity
def costofequity(RF,symbol,yearlyreturn):
    # RF = 0.063640
    # msft.quarterly_balance_sheet

# Beta 
    cmp = yf.Ticker(symbol)

    # get stock info
    # print(msft.info)
    stock_info = cmp.info
    beta = stock_info['beta']
    # print("Beta {}".format(beta))
#Market Return
    # During pandamic 
      # start = datetime.datetime(2019, 7, 10)
      # end= datetime.datetime(2020,7,10)

    # SP500 = web.DataReader(['sp500'], 'fred', start, end)
    #     #Drop all Not a number values using drop method.
    # SP500.dropna(inplace = True)

    # SP500yearlyreturn = (SP500['sp500'].iloc[-1]/ SP500['sp500'].iloc[-252])-1
    # print(start,end)
    # print("web sp500yearlyreturn")
    # print(SP500yearlyreturn)

    # Need to find an alternative to sp500
    # start = datetime.datetime.now() - datetime.timedelta(days=1*365)
    # start = start.strftime('%Y-%m-%d')
    # end= datetime.datetime.today().strftime('%Y-%m-%d')

    # SP500 = web.DataReader(['sp500'], 'fred', start, end)
    # SP500.dropna(inplace = True)
    # # print(SP500)
    # rows = SP500.shape[0]
    # # print(rows)
    # SP500yearlyreturn = (SP500['sp500'].iloc[-1]/ SP500['sp500'].iloc[-rows])-1
    # print(start,end)
    # print("Current sp500yearly return")
    # print(SP500yearlyreturn)
# CAPM/ CoE
    cost_of_equity = RF+(beta*(yearlyreturn - RF))
    # print(cost_of_equity)
    #   return cost_of_equity
    return cost_of_equity,beta

def dcf(ticker,type,period):
  RF,interest_coverage_ratio,Debt_to,equity_to,ETR,yearlyreturn = base(ticker,type,period)
  kd,credit_spread = cost_of_debt(RF,interest_coverage_ratio)
  ke,beta = costofequity(RF,ticker,yearlyreturn)
  # ke = 0.07
  # Calculating the WACC
  WACC = (kd*(1-ETR)*Debt_to) + (ke*equity_to)
  # print("WACC {},equity_to{},Debt_to{}".format(WACC,equity_to,Debt_to))
  # print("ETR{}".format(ETR))
  # print("ke{},kd{}".format(ke,kd))
  # # WACC = 0.04
  # #FCF
  revenue_g,bs_forec,is_forec,CF_forec = fcf.forecast(RF,ticker)
  # print(bs_forec)
  # print(is_forec)
  # print(cf_forec)

  # NPV
  FCF_List = CF_forec.iloc[-1].values.tolist()
  npv = np.npv(WACC,FCF_List)
  # print(npv)
  #Terminal value
  LTGrowth = 0.02

  Terminal_value = (CF_forec['next_5_year']['FCF'] * (1+ LTGrowth)) /(WACC - LTGrowth)
  # print(Terminal_value)
  Terminal_value_Discounted = Terminal_value/(1+WACC)**4
  # print(Terminal_value_Discounted)

  #Calculating the DCF
  # print(bs_forec)

  target_equity_value = Terminal_value_Discounted + npv

  debt = bs_forec['current_year']['Total Liab']

  target_value = target_equity_value - debt
  # print("TvD:{},npv:{},tev:{},debt:{},tv:{}".format(Terminal_value_Discounted,npv,target_equity_value,debt,target_value))
  cmp = yf.Ticker(ticker)
  stock_info = cmp.info
  numbre_of_shares = stock_info['sharesOutstanding']
  # print("Total No. of share holders is {}".format(numbre_of_shares))
  currency = stock_info['currency']


  target_price_per_share = target_value/numbre_of_shares
  # print(ticker + ' forecasted price per stock is ' +str(currency)+' '+str(target_price_per_share) )
  # print('the forecast is based on the following assumptions: '+ 'revenue growth: ' + str(revenue_g) + ' Cost of Capital: ' + str(WACC) )
  # print('perpetuity growth: ' + str(LTGrowth)  )
  return ke,kd,RF,ETR,LTGrowth,Terminal_value,Terminal_value_Discounted,target_equity_value,target_value,target_price_per_share,beta,credit_spread,WACC,Debt_to,equity_to,npv,revenue_g,bs_forec,CF_forec,is_forec,yearlyreturn,currency

# ticker = 'MSFT'
# type = "Indian"
# period = "before"
# dcf(ticker,type,period)
# print(ticker + ' forecasted price per stock is ' +str(currency)+' '+str(target_price_per_share) )
# print('the forecast is based on the following assumptions: '+ 'revenue growth: ' + str(revenue_g) + ' Cost of Capital: ' + str(WACC) )
# print('perpetuity growth: ' + str(LTGrowth)  )

#Key inference: An Exponential growth in sp500 -> Result in high Ke -> Result in high WACC -> Result in less DCF Value

#Calculating the SGR
#ROE and PAyout Ratio
# metrics = requests.get(f'https://financialmodelingprep.com/api/v3/company-key-metrics/{quote}?apikey=your_api_key')
# metrics = metrics.json()
# print(metrics['metrics'])
# ROE = float(metrics['metrics'][0]['ROE'])
# payout_ratio = float(metrics['metrics'][0]['Payout Ratio'])

# sustgrwothrate = ROE*(1-payout_ratio)
# print(sustgrwothrate)

# Reference
# https://codingandfun.com/calculating-weighted-average-cost-of-capital-wacc-with-python/
# https://www.rbi.org.in/ ---> RF is taken from RBI Dataset --> 2031 GS
# http://pages.stern.nyu.edu/~adamodar/New_Home_Page/datafile/ratings.htm ---> credit spread from interest coverage ratio


