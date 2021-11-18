import pandas_datareader.data as web
import yfinance as yf
import datetime
def costofequity(symbol):
    RF = 0.063640

# Beta 
    msft = yf.Ticker(symbol)

    # get stock info
    # print(msft.info)
    stock_info = msft.info
    beta = stock_info['beta']

#Market Return
  
    start = datetime.datetime.now() - datetime.timedelta(days=1*365)
    start = start.strftime('%Y-%m-%d')
    #   start = datetime.datetime(2019, 7, 10)
    end= datetime.datetime.today().strftime('%Y-%m-%d')

    SP500 = web.DataReader(['sp500'], 'fred', start, end)
    #       #Drop all Not a number values using drop method.
    SP500.dropna(inplace = True)
    # print(SP500)
    SP500yearlyreturn = (SP500['sp500'].iloc[-1]/ SP500['sp500'].iloc[-252])-1
    print(SP500yearlyreturn)
# CAPM/ CoE
    cost_of_equity = RF+(beta*(SP500yearlyreturn - RF))
    print(cost_of_equity)
    #   return cost_of_equity

symbol = "MSFT"
print(costofequity(symbol))
