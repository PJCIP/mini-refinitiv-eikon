import urllib.request
import pandas as pd
from pprint import pprint
from html_table_parser.parser import HTMLTableParser


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
# print(len(table))

def extract_tickers():
    # S&P 500
    sp_500_url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    sp500 = extract_table(sp_500_url)[0]
    df = pd.DataFrame(sp500,columns=sp500[0])
    df.drop(index=df.index[0], 
            axis=0, 
            inplace=True)
    df.rename(columns={"Security": "Company"},inplace=True)
    df.set_index("Company", inplace = True)
    sp500_ticker = df.to_dict('index')
    # print(sp500_ticker.keys())  #For getting the company name
    # sp500_ticker['Symbol']

    #Dow-Jones Ticker
    dj_url = 'https://en.wikipedia.org/wiki/Dow_Jones_Industrial_Average'
    dj = extract_table(dj_url)[1]
    df = pd.DataFrame(dj,columns=dj[0])
    df.drop(index=df.index[0], 
            axis=0, 
            inplace=True)
    # print(df)
    df.set_index("Company", inplace = True)
    dj_ticker = df.to_dict('index')
    # print(dj_ticker)
    # print(dj_ticker.keys())  #For getting the company name
    # dj_ticker['Symbol']
     

    #FTSE100 Ticker
    ftse100_url = 'https://en.wikipedia.org/wiki/FTSE_100_Index'
    ftse100 = extract_table(ftse100_url)[3]
    df = pd.DataFrame(ftse100,columns=ftse100[0])
    df.drop(index=df.index[0], 
            axis=0, 
            inplace=True)
    df.rename(columns={"EPIC": "Symbol"},inplace=True)
    df.set_index("Company", inplace = True)
    ftse100_ticker = df.to_dict('index')
    # print(ftse100_ticker)
    # ftse100_ticker = list(df['EPIC'])
    # print(dj_ticker.keys())  #For getting the company name
    # dj_ticker['Symbol']


    # FTSE250
    ftse250_url = 'https://en.wikipedia.org/wiki/FTSE_250_Index'
    ftse250 = extract_table(ftse250_url)[1]
    df = pd.DataFrame(ftse250,columns=ftse250[0])
    df.drop(index=df.index[0], 
            axis=0, 
            inplace=True)
    # print(df)
    df.rename(columns={"Ticker 4": "Symbol"},inplace=True)
    df.set_index("Company", inplace = True)
    ftse250_ticker = df.to_dict('index')
    # print(ftse250_ticker)
    # ftse250_ticker = list(df['Ticker 4'])

    # NIFTY50
    nf50_url = 'https://en.wikipedia.org/wiki/NIFTY_50'
    nf50 = extract_table(nf50_url)[1]
    df = pd.DataFrame(nf50,columns=nf50[0])
    df.drop(index=df.index[0], 
            axis=0, 
            inplace=True)
    # print(df)
    df.rename(columns={"Company Name": "Company"},inplace=True)
    df.set_index("Company", inplace = True)
    nf50_ticker = df.to_dict('index')
    # nf50_ticker = list(df['Symbol'])
    # print(nf50_ticker)

    # NASDAQ - 100
    nasdaq_url = 'https://en.wikipedia.org/wiki/Nasdaq-100'
    # pprint(extract_table(nasdaq_url))
    nasdaq100 = extract_table(nasdaq_url)[3]
    df = pd.DataFrame(nasdaq100,columns=nasdaq100[0])
    df.drop(index=df.index[0], 
            axis=0, 
            inplace=True)
    # print(df)
    df.rename(columns={"Ticker": "Symbol"},inplace=True)
    df.set_index("Company", inplace = True)
    nasdaq100_ticker = df.to_dict('index')
    
    tickers ={"SP500":sp500_ticker,"NASDAQ":nasdaq100_ticker,"NIFTY50":nf50_ticker,"FTSE250":ftse250_ticker,"FTSE100":ftse100_ticker,"DOW":dj_ticker}
    return tickers





