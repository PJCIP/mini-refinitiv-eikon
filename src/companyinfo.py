import yfinance as yfs
import yahoo_fin.stock_info as yf
from yahoo_fin import news
import pandas as pd

def esg(ticker):
    firm_data = yfs.Ticker(ticker)
    esg_data = pd.DataFrame(firm_data.sustainability)
       
    return esg_data
def statements(ticker):
    cmp = yfs.Ticker(ticker)
    balance_sheet = cmp.balance_sheet
    cash_flow = cmp.cashflow
    income_statement = cmp.financials
    # years = balance_sheet.columns
    return balance_sheet,cash_flow,income_statement

def info(ticker):
    c_info = yfs.Ticker(ticker).info
    longName =c_info['longName']
    symbol = c_info['symbol']
    logo = c_info['logo_url']
    industry = c_info['industry']
    phone =c_info['phone']
    website = c_info[ 'website']
    summary = c_info['longBusinessSummary']
    return longName,symbol,logo,industry,phone,website,summary

def stock_holders(ticker):
    major = yfs.Ticker(ticker).major_holders
    institutional_holders  =  yfs.Ticker(ticker).institutional_holders
    # print(stockholders)
    major_dict = major.to_dict('split')
    # print(major_dict)
    # direct_holders = stockholders['Direct Holders (Forms 3 and 4)']
    # institutional_holders = stockholders['Top Institutional Holders']
    return major_dict,major,institutional_holders

def fetch_news(ticker):
    news_data = news.get_yf_rss(ticker)
    return news_data

def analyst_info(ticker):
    analyst_data = yf.get_analysts_info(ticker)
    return analyst_data
    

