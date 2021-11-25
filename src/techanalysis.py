# TEchnical analysis
import pandas as pd
import yfinance as yfs


# Simple Moving Average
def SMA(data,period= 30,column = 'Close'):
    return data[column].rolling(window=period).mean()

# Exponential Moving Average
def EMA(data,period= 20,column = 'Close'):
    return data[column].ewm(span=period, adjust = False).mean()

# Moving Average Convergence/Divergence
def MACD(data, period_long=26,period_short=12,period_signal=9,column='Close'):
    ShortEMA = EMA(data,period_short,column=column)
    LongEMA = EMA(data,period_long,column=column)
    data['MACD'] = ShortEMA - LongEMA 
    data['Signal_Line'] = EMA(data,period_signal,column = 'MACD')

    return data

# Relative Strength Index

def RSI(data,period = 14,column ='Close'):
    delta = data[column].diff(1)
    delta = delta[1:]
    up = delta.copy()
    down = delta.copy()
    up[up<0] = 0
    down[down>0] = 0
    data['up'] = up
    data['down'] = down
    AVG_Gain = SMA(data,period,column='up')
    AVG_Loss = abs(SMA(data,period,column='down'))
    RS = AVG_Gain /AVG_Loss
    RSI = 100 - (100/(1+RS))
    data['RSI'] = RSI
    return data

def technical_analysis(data):
    # data = yfs.download(tickers = symbol)
    data = MACD(data)
    data = RSI(data)
    data['SMA'] = SMA(data)
    data['EMA'] = EMA(data)
    # print(data.columns)
    # print(data)
    return data

# symbol = 'MSFT'
# # data = yfs.download(tickers = symbol, period = period_dict[speriod], interval = interval_dict[sinterval])
# data = technical_analysis
