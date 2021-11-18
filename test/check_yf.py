import yfinance as yf
import datetime
msft = yf.Ticker("AAPL")

# get stock info
# print(msft.info)
stock_info = msft.info
print(stock_info['beta'])
# get historical market data
start = datetime.datetime.now() - datetime.timedelta(days=1*365)
start = start.strftime('%Y-%m-%d')
print(start)
print(type(start))
#   start = datetime.datetime(2019, 7, 10)
end= datetime.datetime.today().strftime('%Y-%m-%d')

hist = msft.history(start=start,end=end)


# print(hist)
# # show actions (dividends, splits)
# print(msft.actions)

# # # show dividends
# print(msft.dividends)

# # show splits
# msft.splits

# # show financials
# print(msft.financials)
# print(msft.balance_sheet)
# print(msft.cashflow)
# msft.quarterly_financials

# # show major holders
# msft.major_holders

# # show institutional holders
# msft.institutional_holders

# # show balance sheet
# msft.balance_sheet
# msft.quarterly_balance_sheet

# # show cashflow
# msft.cashflow
# msft.quarterly_cashflow

# # show earnings
# msft.earnings
# msft.quarterly_earnings

# # show sustainability
# msft.sustainability

# # show analysts recommendations
# msft.recommendations

# # show next event (earnings, etc)
# msft.calendar

# # show ISIN code - *experimental*
# # ISIN = International Securities Identification Number
# msft.isin

# # show options expirations
# msft.options

# # show news
# msft.news

import requests

company = 'MSFT'
demo = '5df285c077779f8519c2bc667ae30191'

# beta = requests.get(f'https://financialmodelingprep.com/api/v3/company/profile/{company}?apikey={demo}')
# beta = beta.json()
# beta = float(beta['profile']['beta'])

# FR = requests.get(f'https://financialmodelingprep.com/api/v3/ratios/{company}?apikey={demo}').json()
# ETR = FR[0]['effectiveTaxRate']

metrics = requests.get(f'https://financialmodelingprep.com/api/v3/company-key-metrics/{company}?apikey={demo}')
metrics = metrics.json()
# print(metrics['metrics'])
# print(metrics)

# Key Metrics plot:
date = metrics['metrics'][0]['date']
ROE = float(metrics['metrics'][0]['ROE'])
payout_ratio = float(metrics['metrics'][0]['Payout Ratio'])

sustgrwothrate = ROE*(1-payout_ratio)
print(date,ROE,payout_ratio,sustgrwothrate)
# print(ETR)
print(metrics['metrics'][30]['date'])

period = len(metrics['metrics']) 
print(period)
key_metrics = list(metrics['metrics'][0].keys())[1:]
# for i in range(period):
#     print(type(i))
#     print(i)
#     print(metrics['metrics'])
# cnt = [int(i) for i in len(metrics['metrics'])]
# print(cnt)

dates = [metrics['metrics'][i]['date'] for i in range(len(metrics['metrics']))]
import pandas as pd
#  # metrics = metrics.remove('date')
# print(dates)
# print(key_metrics)
# Key for plotting the key metrics under fundamental analysis
a = 3
if a == 3:
    print(dates[:3])
    print(metrics['metrics'][:3])
    print(pd.DataFrame(metrics['metrics'][:3]))
    