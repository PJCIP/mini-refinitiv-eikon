import yfinance as yfs
import yahoo_fin.stock_info as yf
from yahoo_fin import news
 


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
    stockholders =  yf.get_holders(ticker)
    major_dict = major.to_dict('split')
    direct_holders = stockholders['Direct Holders (Forms 3 and 4)']
    institutional_holders = stockholders['Top Institutional Holders']
    return major_dict,direct_holders,institutional_holders

def fetch_news(ticker):
    news_data = news.get_yf_rss(ticker)
    # print(news_data[0])
    print(len(news_data))
    news_data = news_data[0]
    summary = news_data['summary']
    link = news_data['link']
    title = news_data['title']
    date = news_data['published']
    print(title)
    print(summary)
    print(link)
    print(date)
fetch_news('AAPL')