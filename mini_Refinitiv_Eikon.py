import streamlit as st
import spacy_streamlit
import pandas as pd
from streamlit.proto import DataFrame_pb2
import yfinance as yfs
import mplfinance as mpf
from matplotlib import pyplot as plt
import mplfinance as mpf
import plotly.express as px
import yahoo_fin.stock_info as yf
import requests
import urllib
from src import companyinfo
from src import piotroski_with_chart
from src import piotroski
from src import benish
from src import sentimentanalyzer
from src import index
from src import fundamental
from src import techanalysis
plt.style.use("ggplot")
category= []
company_name=[]
stock_indices = ["-","NIFTY50","DOW","FTSE100","NASDAQ","SP500"]
api_key = '5df285c077779f8519c2bc667ae30191'
def retrieve_companyname(data,fetch,tic):
    data = data.dropna()
    comp_name= list(data[fetch])
    ticker = list(data[tic])
    return comp_name,ticker

def linechart_format(data):
    new_date = data.columns
    df_list = data.values.tolist()
    if len(df_list) >1:
        calu = df_list[0]
        
        cal = calu.pop(0)
        new_cal = calu
        
    else:
        cal = df_list.pop(0)
        new_cal = df_list
    new_date =list(data[1:])[1:] 
    df = pd.DataFrame({
    'date': new_date,
    cal: new_cal
    })

    df = df.rename(columns={'date':'index'}).set_index('index')
    return df






st.title("Mini-Refinitiv Eikon")
st.sidebar.title("Mini- Refinitiv Eikon")
# Checking for internet connection
# while True:
#     strframe1 = st.empty()
#     try :
#         stri = "https://www.google.co.in"
#         data = urllib.urlopen(stri)
#         # print ("Connected")
#         # st.empty()
#         strframe1.success('Connected to Internet')
#     except:
#         # print ("not connected" ,e )
#         st.empty()
#         strframe1.info('Please Check your internet connection')
        # print("No internet connection.")
# st.title("News")
#sidebar - Starts
search = st.sidebar.radio("Choose one of the option: ",["Type the ticker","Search for ticker in stock index list"],index = 0)
if search == "Type the ticker":
    symbol = st.sidebar.text_input("Ticker of the company")
    try:
        # holder = yf.get_holders(symbol)
        comp_name = yfs.Ticker(symbol).info['longName']
        st.sidebar.write("You have a selected {} and the ticker is {}".format(comp_name,symbol))
        
        st.sidebar.success('Fetch the ticker')
    except:
        st.sidebar.error('Unable to fetch the ticker')
    
else:
    category = st.sidebar.selectbox("Select a stock index ",stock_indices)
    data = index.extract_tickers()
    # print(data)
    if category == "-":
        st.info('Please select one index from dropdown')
    if category == "NIFTY50":
        company_name = list(data["NIFTY50"].keys())
        # print(company_name)
        ticker = [data['NIFTY50'][cname]['Symbol']+'.NS' for cname in company_name]
        # print(company_name)
        # print(ticker)
    if category == "DOW":
        company_name = list(data["DOW"].keys())
        print(company_name)
        ticker = [data["DOW"][cname]['Symbol'] for cname in company_name]
        print(ticker)
    if category == "FTSE100":
        # data = yf.tickers_ftse100(True)
        # company_name,ticker = retrieve_companyname(data,'Company','EPIC')
        company_name = list(data["FTSE100"].keys())
        print(company_name)
        ticker = [data["FTSE100"][cname]['Symbol'] for cname in company_name]
        print(ticker)
    if category == "FTSE250":
        # data = yf.tickers_ftse250(True)
        # company_name,ticker = retrieve_companyname(data,'Company',"Ticker")
        company_name = list(data["FTSE250"].keys())
        print(company_name)
        ticker = [data["FTSE250"][cname]['Symbol'] for cname in company_name]
        print(ticker)
    if category == "NASDAQ":
        # data = yf.tickers_nasdaq(True)
        # company_name,ticker = retrieve_companyname(data,'Security Name',"Symbol")
        company_name = list(data["NASDAQ"].keys())
        print(company_name)
        ticker = [data["NASDAQ"][cname]['Symbol'] for cname in company_name]
        print(ticker)
    if category == "SP500":
        # data = yf.tickers_sp500(True)
        # company_name,ticker = retrieve_companyname(data,'Security',"Symbol")
        company_name = list(data["SP500"].keys())
        print(company_name)
        ticker = [data["SP500"][cname]['Symbol'] for cname in company_name]
        print(ticker)
    
    if len(company_name)==0:
        st.sidebar.info('Please wait fetching the details')
    else:
        st.sidebar.write("Total no. of companies : {}".format(len(company_name)))
        st.sidebar.success('Fetched all the details')
        company = st.sidebar.selectbox("Select a company",company_name)
        symbol = ticker[company_name.index(company)]
        if symbol:
            st.sidebar.write("You have a selected {} and the ticker is {}".format(company,symbol))
#Sidebar ends

my_expander = st.sidebar.beta_expander(label="Company's Profile")
with my_expander:
        menu = st.selectbox("Let's Explore",["-","Overview","Ownership","ESG","Financial Statments","piotroski F-score","Benish M-score","News"],index =0)


#Start of main page
if menu == 'Overview':
    try:
        st.title('Overview')
        longName,symbol,logo,industry,phone,website,summary = companyinfo.info(symbol)
        co_name = longName
        st.markdown('''
        # {} - {}'''.format(longName,symbol))
        st.image(logo)
        st.markdown('''
        ## Industry type: {}
        {}
        ## Contact details
        - phone no.- {}
        - website - {}
        '''.format(industry,summary,phone,website))
    except:
        st.info('Please select one symbol')
elif menu == 'Ownership':
    try:
        major_dict,major_holders,institutional_holders = companyinfo.stock_holders(symbol)
        print(major_dict)
        print(institutional_holders)
        st.title('Ownership')
        st.markdown('''
        
        ## Ownership details
        - {} - {}
        - {} - {}
        - {} - {}
        - {} - {}
        '''.format(major_dict['data'][0][1],major_dict['data'][0][0],major_dict['data'][1][1],major_dict['data'][1][0],major_dict['data'][2][1],major_dict['data'][2][0],major_dict['data'][3][1],major_dict['data'][3][0]))

        # st.subheader('Major holders information:')
        # st.dataframe(major_holders)
        
        st.subheader('Institutional holders information:')
        st.dataframe(institutional_holders)
    except :

        st.info('There some issue in loading in this page')
        
elif menu == "Analyst estimates":
    analyst_estimate = companyinfo.analyst_info(symbol)
    st.title('Analyst estimate (Currency in USD)')
    st.subheader('Earnings Estimate information:')
    st.dataframe(analyst_estimate['Earnings Estimate'])
    st.subheader('Revenue Estimate information:')
    st.dataframe(analyst_estimate['Revenue Estimate'])
    st.subheader('Earnings History information:')
    st.dataframe(analyst_estimate['Earnings History'])
    st.subheader('EPS Revisions information:')
    st.dataframe(analyst_estimate['EPS Revisions'])
    st.subheader('Growth Estimates information:')
    st.dataframe(analyst_estimate['Growth Estimates'])

elif menu == "piotroski F-score":
    st.title('Piotroski F-score')
    st.subheader("What is Piotroski F-score?")
    st.write("Piotroski F-score is a number between 0 and 9 which is used to assess strength of company's financial position. The score is used by financial investors in order to find the best value stocks")
    st.subheader("How it is calculated?")
    st.markdown('''
        Piotroski f score is calculated based on 9 criteria divided into 3 groups
        
        - profitability
        - liquidity and leverage
        - operational efficiency
        ''')
    name = yfs.Ticker(symbol).info['longName']
    st.subheader('Piotroski F-score for {}'.format(name))
    fscore,flag = piotroski.piotroski(symbol)
    if flag == 404:
        st.info("Unable to fetch the financial statements")
    elif flag == 500:
        st.info("Unable to calculate scores")
    elif flag == 200:
        print(fscore.get('Piotroski F-score(/9)')[0])
        print(type(fscore.get('Piotroski F-score(/9)')[0]))
        st.markdown(' The Piotroski F-score for ** {} ** is ** {} ** and the strength of the company is considered to be ** {} **'.format(name,fscore.get('Piotroski F-score(/9)')[0],fscore.get('Strength')[0]))
        fscore = fscore.head(1).transpose()
        fscore.columns = ['Piotroski Score of '+name]
        # fscore = fscore[1:]
        # piotro_fscore = fscore.head(1).transpose()
        st.dataframe(fscore)

elif menu == 'Charts':
    st.title("Charts of Piotroski - F Score")
    fscore,profitability_table,leverage_table,oe_table = piotroski_with_chart.piotroski(symbol)
    my_expander = st.beta_expander(label='Performance of the company')
    with my_expander:
            group = st.selectbox('Select a group',['-','Profitability','Leverage and liquidity','Operation efficiency'])
            if group == '-':
                st.info('Please select one of the group listed')
            if group == 'Profitability':
                criteria = st.selectbox('Select a criteria',['-','Return of Assets','Operating Cash Flow','Accruals','Net Income'])
                if criteria == '-':
                    st.info('Please select one of the criteria listed')
                elif criteria == 'Return of Assets':
                    data = profitability_table[profitability_table['calculation']=='Return of Assets']
                    print(data)
                    st.line_chart(linechart_format(data))
                elif criteria == 'Operating Cash Flow':
                    data = profitability_table[profitability_table['calculation']=='Operating Cash Flow']
                    print(data)
                    st.line_chart(linechart_format(data))
                elif criteria == 'Accruals':
                    data = profitability_table[profitability_table['calculation']=='Accruals']
                    st.line_chart(linechart_format(data))
                elif criteria == 'Net Income':
                    data = profitability_table[profitability_table['calculation']=='Net Income']
                    st.line_chart(linechart_format(data))
            if group == 'Leverage and liquidity':
                criteria = st.selectbox('Select a criteria',['-','long debt ratio','current ratio'])
                if criteria == '-':
                    st.info('Please select one of the criteria listed')
                elif criteria == 'current ratio':
                    data = leverage_table[leverage_table['calculation']=='current ratio']
                    st.line_chart(linechart_format(data))

                elif criteria == 'long debt ratio':
                    data = leverage_table[leverage_table['calculation']=='long debt ratio']
                    st.line_chart(linechart_format(data))
            
            if group == 'Operation efficiency':
                criteria = st.selectbox('Select a criteria',['-','gross margin'])
                if criteria == '-':
                    st.info('Please select one of the criteria listed')
                elif criteria == 'gross margin':
                    data = oe_table[oe_table['calculation']=='gross margin']
                    st.line_chart(linechart_format(data))
                
elif menu == "Benish M-score":
    name = yfs.Ticker(symbol).info['longName']
    st.title('Benish M-score')
    st.subheader("What is Benish M-score?")
    st.write("The Beneish model is a statistical model that uses financial ratios calculated with accounting data of a specific company in order to check if it is likely (high probability) that the reported earnings of the company have been manipulated.")
    st.subheader("How it is calculated?")
    st.markdown('''
        The Beneish M-score is calculated using 8 variables (financial ratios):
        
        - Days Sales in Receivables Index
        - Gross Margin Index
        - Asset Quality Index
        - Sales Growth Index
        - Depreciation Index
        - Sales General and Administrative Expenses Index 
        - Leverage Index
        - Total Accruals to Total Assets

        ''')
    st.subheader('Benish M-score  for {}'.format(name))
    mscore = benish.benish_m_score(symbol)
    if mscore < -1.78:
        st.markdown(''' The benish M-score is ** {:.3f} **.The company ** {} ** is unlikely to be a manipulator'''.format(mscore,name))
    else:
        st.markdown(''' The benish M-score is ** {:.3f} **.The company ** {} ** is likely to be a manipulator'''.format(mscore,name))
    
    st.warning('Beneish M-score is a probabilistic model, so it cannot detect companies that manipulate their earnings with 100% accuracy.')
    st.warning('Financial institutions were excluded from the sample in Beneish paper when calculating M-score. It means that the M-score for fraud detection cannot be applied among financial firms (banks, insurance).')

elif menu =="News":
    newsdata = companyinfo.fetch_news(symbol)
    sent_score = []
    postive_news = 0
    negative_news = 0
    neutral_news = 0
    total_news = len(newsdata)
    
    st.title("News")
    my_expander = st.beta_expander(label='View News')
    with my_expander:
        for news in newsdata:
            summary = news['summary']
            link = news['link']
            title = news['title']
            date = news['published']
            docx,sentiment_score,sub_words,text_summary,key_entity = sentimentanalyzer.sentiment(summary)
            st.subheader(title)
            st.write('''published date: {}'''.format(date))
            if text_summary:
                st.markdown(text_summary)
            else:    
                st.write(summary)
            st.markdown('''*Key-entities - {} *'''.format(key_entity))
            sent_score.append(sentiment_score)
            if sentiment_score > 0: 
                postive_news+=1
                st.markdown('''<p style="color:green">Sentiment score = {:.3f}</p>
            '''.format(sentiment_score), unsafe_allow_html=True)
            elif sentiment_score == 0:
                neutral_news+=1
                st.markdown('''<p>Sentiment score = {:.3f}</p>
            '''.format(sentiment_score), unsafe_allow_html=True)

            else:
                negative_news+=1
                st.markdown('''<p style="color:red">Sentiment score = {:.3f}.</p>
            '''.format(sentiment_score), unsafe_allow_html=True)

            st.markdown('''[click here to read more]({})'''.format(link))

    avg_sentiment = sum(sent_score)/total_news
    st.markdown('''
        - Total no. of news = {}
        - No. of positive news = {}
        - No. of negative news = {}
        - No. of neutral news = {}
        '''.format(total_news,postive_news,negative_news,neutral_news))
    if avg_sentiment > 0 or avg_sentiment == 0:
        st.markdown('''
            - <p style="color:green"> Average sentiment score = {:.3f}</p>
            '''.format(avg_sentiment), unsafe_allow_html=True)
    else:
            st.markdown('''
            - <p style="color:red">Average sentiment score =  {:.3f}</p>
            '''.format(avg_sentiment), unsafe_allow_html=True)

elif menu == "Financial Statments":   
    balance_sheet,cash_flow,income_statement = companyinfo.statements(symbol)
    st.title('Financial Statements')
    st.subheader('Balance Sheet')
    st.dataframe(balance_sheet)
    st.subheader('Cash flow statement')
    st.dataframe(cash_flow)
    st.subheader('Income statement')
    st.dataframe(income_statement)

# What is the highest ESG score?

elif menu == "ESG":
    esg_table = companyinfo.esg(symbol)
    st.title('Environmental, Social and Governance')
    st.subheader("What is ESG?")
    st.write("Environmental, Social, and Corporate Governance (ESG) is an evaluation of a firm's collective conscientiousness for social and environmental factors. It is typically a score that is compiled from data collected surrounding specific metrics related to intangible assets within the enterprise.")
    period, interval, format,perf = st.beta_columns(4) 
    with period:
        # governanceScore
# socialScore
# environmentScore float(esg_table.loc['environmentScore'])
        st.subheader('Governance Score :{}'.format(float(esg_table.loc['governanceScore'])))

    with interval:
        st.subheader('Environmental Score :{}'.format(float(esg_table.loc['environmentScore'])))

    with format:
        st.subheader('Social Score :{}'.format(float(esg_table.loc['socialScore'])))
    
    with perf:
        st.subheader('ESG Performance :{}'.format(str(esg_table.loc['esgPerformance']['Value'])))
    
    st.subheader("How to interpret these scores?")
    st.write("The ESG Risk Ratings are categorized across five risk levels: negligible (0-10), low (10-20), medium (20-30), high (30-40) and severe (40+).")
    
    st.dataframe(esg_table)


fundamental_expander = st.sidebar.beta_expander(label="Fundamental Analysis")

with fundamental_expander:
    # Server type
    fund_menu = st.selectbox("Let's Explore",["-","Candle chart","Key Metrics","Ratios"],index =0)
    # Local host
    # fund_menu = st.selectbox("Let's Explore",["-","Candle chart","Understanding Market Return","DCF","Key Metrics","Ratios"],index =0)

if fund_menu == "Candle chart":
    st.title('Candle chart (Historical data)')
    period, interval, format = st.beta_columns(3) 
    # ,,,,,,,,,,
    period_dict = {'1 day':'1d','5 day':'5d','1 month':'1mo','3 months':'3mo','6 months':'6mo','1 year':'1y','2 years':'2y','5 years':'5y','10 years':'10y','year to date':'ytd','max':'max'}
    interval_dict ={'1 min':'1m','2 min':'2m','5 min':'5m','15 min':'15m','30 min':'30m','60 min':'60m','90 min':'90m','1 hr':'1h','1 day':'1d','5 day':'5d','1 week':'1wk','1 month':'1mo','3 month':'3mo'}
    with period:
        speriod = st.selectbox('Select the period',['1 day','5 day','1 month','3 months','6 months','1 year','2 years','5 years','10 years','year to date','max'])

    with interval:
        sinterval = st.selectbox('Select the interval',['1 min','2 min','5 min','15 min','30 min','60 min','90 min','1 hr','1 day','5 day','1 week','1 month','3 month'])

    with format:
        sformat = st.selectbox('Select a format',['Table','Chart'])

    data = yfs.download(tickers = symbol, period = period_dict[speriod], interval = interval_dict[sinterval])
    # fig, ax = mpf.plot(data,type='candle',mav=(3,6,9),volume=True,show_nontrading=True)
    # print(symbol)
    if sformat == "Table":
        st.dataframe(data)
    elif sformat == "Chart":
        fig, ax = mpf.plot(
                data,
                type="candle",
                style="yahoo",
                volume=True,
                returnfig=True,
                title=f"{yfs.Ticker(symbol).info['longName']}",
                figratio=(16, 7),
                figscale=1.2,
            )
        st.write(fig)

elif fund_menu == "Key Metrics":
    st.title('Company Key Metrics')
    metrics = requests.get(f'https://financialmodelingprep.com/api/v3/company-key-metrics/{symbol}?apikey={api_key}')
    metrics = metrics.json()
    k_metrics = st.multiselect('Select key metrics', list(metrics['metrics'][0].keys())[1:])
    period, format = st.beta_columns(2) 
    with period:
        speriod = st.selectbox('Select the period',['3 years','5 years','10 years','max'])
    with format:
        sformat = st.selectbox('Select a format',['Table','Chart'])
    if len(k_metrics) == 0:
        st.info('Please choose atleast one of key_metrics')
    else:
        if speriod != 'max':
            met = pd.DataFrame(metrics['metrics'][:int(speriod.split(' ')[0])])
            met = met[['date']+k_metrics]
        else:
            met = pd.DataFrame(metrics['metrics'])
            met = met[['date']+k_metrics]
        # met['date'] = pd.to_datetime(met['date'])
        met.index = met['date']
        met.index.name = 'date'
        met.drop(['date'], axis = 1,inplace=True)
        for metri in k_metrics:
            met[metri] = pd.to_numeric(met[metri], downcast="float")
        if sformat == 'Table':
            st.dataframe(met)
        else:
            rel = met.pct_change()
            cumret = (1+rel).cumprod() - 1
            cumret = cumret.fillna(0)
            st.line_chart(cumret)

elif fund_menu == "Ratios":
    st.title('Financial ratios')
    fr = requests.get(f"https://financialmodelingprep.com/api/v3/financial-ratios/{symbol}?apikey={api_key}")
    fr = fr.json()
    key_ratios = list(fr['ratios'][0].keys())[1:]
    period, ratios,format = st.beta_columns(3) 
    with period:
        speriod = st.selectbox('Select the period',['3 years','5 years','10 years','max'])
    with format:
        sformat = st.selectbox('Select a format',['Table','Chart'])
    with ratios:
        sratios = st.selectbox('Select a format',key_ratios)
    r_metrics = st.multiselect('Select key ratios', list(list(fr['ratios'][0][sratios].keys())))
    if len(r_metrics) == 0:
        st.info('Please choose atleast one of key_metrics')
    else:
        if speriod != 'max':
            met = pd.DataFrame(fr['ratios'][:int(speriod.split(' ')[0])])
            srat_met = pd.DataFrame(met[sratios])
            dates = [met['date'] for i in range(int(speriod.split(' ')[0]))]
            ratios = pd.DataFrame()
            for perd in range(int(speriod.split(' ')[0])):
                ratios = ratios.append([srat_met[sratios][perd]],ignore_index=True)
            ratios['date'] = dates[0]
            ratios = ratios[['date']+r_metrics]
            
            

        else:
            met = pd.DataFrame(fr['ratios'])
            srat_met = pd.DataFrame(met[sratios])
            dates = [met['date'] for i in range(len(met))]
            ratios = pd.DataFrame()
            for perd in range(len(met)):
                ratios = ratios.append([srat_met[sratios][perd]],ignore_index=True)
            ratios['date'] = dates[0]
            ratios = ratios[['date']+r_metrics]
        ratios.index = ratios['date']
        ratios.index.name = 'date'
        ratios.drop(['date'], axis = 1,inplace=True)
        for metri in r_metrics:
            ratios[metri] = pd.to_numeric(ratios[metri], downcast="float")
        if sformat == 'Table':
            st.dataframe(ratios)
        else:
            rel = ratios.pct_change()
            cumret = (1+rel).cumprod() - 1
            cumret = cumret.fillna(0)
            st.line_chart(cumret)
            
    

elif fund_menu == "DCF":
    st.title("Discounted Cash Flow")
    market,period = st.beta_columns(2)
    with market:
        smarket = st.selectbox('Select the market',['Global Market','Indian Market'])
        
    with period:
        speriod = st.selectbox('Select the period',['Before pandemic','Current'])

    
               
        # ke,kd,RF,ETR,LTGrowth,Terminal_value,Terminal_value_Discounted,target_equity_value,target_value,target_price_per_share,beta,credit_spread,npv,revenue_g,bs_forec,CF_forec=fundamental.dcf(ticker,smarket,speriod)
    
    ke,kd,RF,ETR,LTGrowth,Terminal_value,Terminal_value_Discounted,target_equity_value,target_value,target_price_per_share,beta,credit_spread,WACC,Debt_to,equity_to,npv,revenue_g,bs_forec,CF_forec,is_forec,yearlyreturn,currency=fundamental.dcf(symbol,smarket,speriod)
    title,header = st.beta_columns(2)
    with title:
        st.subheader('Revenue Growth rate: {:.4f}'.format(revenue_g))
    with header:
        st.subheader('Long Term Inflation Rate: {:.4f}'.format(LTGrowth))
    
    title,header = st.beta_columns(2)
    with title:
        st.subheader('Forecasted Statments:')
    with header:
        sstatement = st.selectbox('Select the Forecasted statement',['FCF','Balance Sheet','Income Statement'])
    if sstatement == 'FCF':
        st.dataframe(CF_forec)
    elif sstatement == 'Balance Sheet':
        st.dataframe(bs_forec)
    elif sstatement == 'Income Statement':
        st.dataframe(is_forec)
    
    wacc_expander = st.beta_expander(label='Weighted Average Cost of Capital: {:.4f}'.format(WACC))
    with wacc_expander:
        kcd,wd,we,t = st.beta_columns(4)
        with kcd:
            st.subheader('Cost of Debt: {:.4f}'.format(kd))
        with wd:
            st.subheader('Weight of Debt: {:.4f}'.format(Debt_to))
        with we:
            st.subheader('Weight of Equity: {:.4f}'.format(equity_to))
        with t:
            st.subheader('Effective Tax Rate: {:.4f}'.format(ETR))

    ke_expander = st.beta_expander(label='Cost of equity: {:.4f}'.format(ke))
    with ke_expander:
        mn,rf,b,yr = st.beta_columns(4)
        with mn:
            if smarket == 'Global Market':
                st.subheader(f"Market Name: S&P 500")

            elif smarket == 'Indian Market':
                st.subheader(f"Market Name: Nifty 50")
                        
        with rf:
            st.subheader('Risk Free Rate: {:.4f}'.format(RF))
        with b:
            st.subheader('Beta: {:.4f}'.format(beta))
        with yr:
            st.subheader('Market Yearly Return: {:.4f}'.format(yearlyreturn))

    

    
    tv,tvd = st.beta_columns(2)
    with tv:
        st.write('Terminal Value: {} {:,.4f}'.format(currency,Terminal_value))
    with tvd:
        st.write('Terminal value Discounted: {} {:,.4f}'.format(currency,Terminal_value_Discounted,))
    npvv,tev= st.beta_columns(2)
    with npvv:
        st.write('Net Present Value: {} {:,.4f}'.format(currency,npv))
    with tev:
        st.write('Target Equity Value: {} {:,.4f}'.format(currency,target_equity_value))
   
    st.subheader('Target price per shares: {} {:,.4f}'.format(currency,target_price_per_share))
        # new_title = '<p style="font-family:sans-serif; color:Gray; font-size: 22px;">Market name: </p><p style="font-family:sans-serif; color:Green; font-size: 12px;">S&P500</p>'
        # st.markdown(new_title, unsafe_allow_html=True)
    
        

        


elif fund_menu == "Understanding Market Return":
    st.title("Understanding Market Return")
    speriod = st.selectbox('Select the period',['Before pandemic','Current'])
    nfty50,SP500,nyearlyreturn,gyearlyreturn,gRF,iRF = fundamental.market(symbol,speriod)
    # gm,im = st.beta_columns(2)
    # with gm:
    st.header("Global market")
    st.subheader("Market name: S&P 500 (in USD)")
    rf,yr = st.beta_columns(2)
    with rf:
        st.subheader("Risk Free rate: {:.4f}".format(gRF))
    with yr:
        st.subheader("Yearly return: {:.4f}".format(gyearlyreturn))
    st.line_chart(SP500)
        # st.write('Terminal Value: {} {:,.4f}'.format(currency,Terminal_value))
    # with im:
        # ,''
    st.header("Indian market")
    st.subheader("Market name: Nifty 50 (in Rs)")
    
    rf,yr = st.beta_columns(2)
    with rf:
        st.subheader("Risk Free rate: {:.4f}".format(iRF))
    with yr:
        st.subheader("Yearly return: {:.4f}".format(nyearlyreturn))
    # print(SP500)
    # print(nfty50)
    # # print(nfty50[['Date','Close']])
    # print(nfty50.columns)
    st.line_chart(nfty50['Close'])

tech_expander = st.sidebar.beta_expander(label="Technical Analysis")
with tech_expander:
    group = st.selectbox('Select a group',['-','Technical Indicators','Technical Strategy'])

   
if group == 'Technical Indicators':

        st.title('Technical Indicators')
        period, interval, format = st.beta_columns(3) 
        # ,,,,,,,,,,
        period_dict = {'1 day':'1d','5 day':'5d','1 month':'1mo','3 months':'3mo','6 months':'6mo','1 year':'1y','2 years':'2y','5 years':'5y','10 years':'10y','year to date':'ytd','max':'max'}
        interval_dict ={'1 min':'1m','2 min':'2m','5 min':'5m','15 min':'15m','30 min':'30m','60 min':'60m','90 min':'90m','1 hr':'1h','1 day':'1d','5 day':'5d','1 week':'1wk','1 month':'1mo','3 month':'3mo'}
        with period:
                speriod = st.selectbox('Select the period',['1 day','5 day','1 month','3 months','6 months','1 year','2 years','5 years','10 years','year to date','max'])

        with interval:
            sinterval = st.selectbox('Select the interval',['1 min','2 min','5 min','15 min','30 min','60 min','90 min','1 hr','1 day','5 day','1 week','1 month','3 month'])

        with format:
            sformat = st.selectbox('Select a format',['Table','Chart'])
        r_metrics = st.multiselect('Select some parameters', ['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume', 'MACD',
        'Signal_Line', 'RSI', 'SMA', 'EMA'])
        if len(r_metrics) == 0:
            st.info('Please choose atleast one of key_metrics')
        else:
           

            data = yfs.download(tickers = symbol, period = period_dict[speriod], interval = interval_dict[sinterval])
            
            ta = techanalysis.technical_analysis(data)
            if sformat == "Table":
                st.dataframe(ta[r_metrics])
            elif sformat == "Chart":
                st.line_chart(ta[r_metrics])

if group == 'Technical Strategy':
    st.title('Technical Strategy')
    period, interval, format = st.beta_columns(3) 
    # ,,,,,,,,,,
    period_dict = {'1 day':'1d','5 day':'5d','1 month':'1mo','3 months':'3mo','6 months':'6mo','1 year':'1y','2 years':'2y','5 years':'5y','10 years':'10y','year to date':'ytd','max':'max'}
    interval_dict ={'1 min':'1m','2 min':'2m','5 min':'5m','15 min':'15m','30 min':'30m','60 min':'60m','90 min':'90m','1 hr':'1h','1 day':'1d','5 day':'5d','1 week':'1wk','1 month':'1mo','3 month':'3mo'}
    with period:
            speriod = st.selectbox('Select the period',['1 day','5 day','1 month','3 months','6 months','1 year','2 years','5 years','10 years','year to date','max'])

    with interval:
        sinterval = st.selectbox('Select the interval',['1 min','2 min','5 min','15 min','30 min','60 min','90 min','1 hr','1 day','5 day','1 week','1 month','3 month'])

    with format:
        sformat = st.selectbox('Select a format',['Table','Chart'])

    data = yfs.download(tickers = symbol, period = period_dict[speriod], interval = interval_dict[sinterval])
    df = techanalysis.technical_analysis(data)
    if sformat == "Table":
        st.dataframe(df)
    elif sformat == "Chart":
                # st.line_chart(ta[r_metrics])
        fig,ax = plt.subplots(figsize=(12.2,4.5))
        ax.plot(df.index,df['Adj Close'])
        ax.set_title('Adj. Close Price History')
        # ax.legend(df.columns.values,loc = 'upper left')
        st.pyplot(fig)

        fig,ax = plt.subplots(figsize=(12.2,4.5))
        ax.set_title('RSI Plot')
        ax.plot(df.index,df['RSI'])
        ax.axhline(0,linestyle='--', alpha = 0.5, color ='gray')
        ax.axhline(10,linestyle='--', alpha = 0.5, color ='orange')
        ax.axhline(20,linestyle='--', alpha = 0.5, color ='green')
        ax.axhline(30,linestyle='--', alpha = 0.5, color ='red')
        ax.axhline(70,linestyle='--', alpha = 0.5, color ='red')
        ax.axhline(80,linestyle='--', alpha = 0.5, color ='green')
        ax.axhline(90,linestyle='--', alpha = 0.5, color ='orange')
        ax.axhline(100,linestyle='--', alpha = 0.5, color ='gray')
        st.pyplot(fig)



            

