from numpy import nan
# import yahoo_fin.stock_info as yf
# import pandas as pd

# tickers = yf.tickers_nifty50()
# print(tickers)
import yfinance as yf
msft = yf.Ticker("MSFT")
print(msft.info)

print(msft.sustainability)
# print(msft.)