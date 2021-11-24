import pandas as pd
#!pip install nsepy
from nsepy import get_history
import datetime
import pandas_datareader.data as web
# Extract Index Data
# symbol = ['NIFTY SMLCAP 100','NIFTY SMLCAP 250','NIFTY SMLCAP 50','NIFTY MIDCAP 150','NIFTY 50','NIFTY NEXT 50','NIFTY FMCG']
# start = datetime.datetime.now() - datetime.timedelta(days=1*365)
# # start = start.strftime('%Y-%m-%d')
# end= datetime.datetime.today()

start = datetime.datetime(2018, 4, 1)
end= datetime.datetime(2019,4,1)
nfty50 = get_history(symbol='NIFTY 50', start=start, end=end, index = True)
nfty50 = pd.DataFrame(nfty50)
nfty50['Index_Name'] = 'NIFTY 50'
# data1 = pd.concat([data1,data])?
# print(nfty50)
print(nfty50.shape)
rows = nfty50.shape[0]
# print(rows)
nfty50yearlyreturn = (nfty50['Close'].iloc[-1]/ nfty50['Close'].iloc[-rows])-1
print(start,end)
print("Current nfty50yearly return")
print(nfty50yearlyreturn)

# DCF 
# Before covid(2018-2019), during covid(2019-2020)and after covid(2020-2021)

# from lxml import html
# import requests
  
# # Request the page
# page = requests.get('https://www.rbi.org.in/')
  
# # Parsing the page
# # (We need to use page.content rather than 
# # page.text because html.fromstring implicitly
# # expects bytes as input.)
# rbi = html.fromstring(page.content)  
  
# # Get element using XPath //*[@id="wrapper"]/div[10]/table/tbody/tr[5]/td[2] /html/body/form/div[7]/div/section[1]/div/div[1]/div[10]/table/tbody/tr[5]/td[2]
# RF = rbi.xpath('//*[@id="wrapper"]/div[10]/table/tbody/tr[5]/td[1]')
# print(RF)
# print(type(RF))

period = "during"

if period == "current":    
      start = datetime.datetime.now() - datetime.timedelta(days=1*365)
      start = start.strftime('%Y-%m-%d')
              
      end= datetime.datetime.today().strftime('%Y-%m-%d')
      #end = datetime.datetime(2020, 7, 10)

      Treasury = web.DataReader(['TB1YR'], 'fred', start, end)
      RF = float(Treasury.iloc[-1])
      RF = RF/100
      print(RF)
      
elif period == "before":
    start = datetime.datetime(2018, 4, 1)
    end= datetime.datetime(2019,4,1)
            
    # end= datetime.datetime.today().strftime('%Y-%m-%d')
    #end = datetime.datetime(2020, 7, 10)

    Treasury = web.DataReader(['TB1YR'], 'fred', start, end)
    RF = float(Treasury.iloc[-1])
    RF = RF/100
    print(RF)

elif period == "during":
    start = datetime.datetime(2020, 4, 1)
    end= datetime.datetime(2021,4,1)
            
    # end= datetime.datetime.today().strftime('%Y-%m-%d')
    #end = datetime.datetime(2020, 7, 10)

    Treasury = web.DataReader(['TB1YR'], 'fred', start, end)
    RF = float(Treasury.iloc[-1])
    RF = RF/100
    print(RF)

# Extracting the country risk premium --> https://pages.stern.nyu.edu/~adamodar/New_Home_Page/datafile/ctryprem.html 


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

crp_url = 'https://pages.stern.nyu.edu/~adamodar/New_Home_Page/datafile/ctryprem.html'
crp = extract_table(crp_url)[0]
df = pd.DataFrame(crp,columns=crp[0])
df.drop(index=df.index[0], 
    axis=0, 
    inplace=True)
# df.rename(columns={"Security": "Company"},inplace=True)
# df.set_index("Country", inplace = True)

# print(df)
crp = str(df[(df.Country == "India")]['Country Risk Premium']).split('%')[0].split(' ')
# print(crp)
crp_list = list(filter(None, crp))
# print(str_list)
# print(type(crp))
crp = float(crp_list[1])/100
print(crp)
# print(float(crp))

