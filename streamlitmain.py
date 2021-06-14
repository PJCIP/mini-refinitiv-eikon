import streamlit as st
import spacy_streamlit
import pandas as pd
import yfinance as yfs
from matplotlib import pyplot as plt
import yahoo_fin.stock_info as yf
from src import companyinfo
from src import piotroski_with_chart
from src import piotroski
from src import benish
from src import sentimentanalyzer
plt.style.use("ggplot")
category= []
company_name=[]
stock_indices = ["-","NIFTY50","DOW","FTSE100","FTSE250","IBOVESPA","NASDAQ","NIFTYBANK","SP500"]
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

menu = st.sidebar.selectbox("Menu",["Overview","Ownership","Financial Statments","Analyst estimates","piotroski F-score","Benish M-score","News","Charts"],index =0)

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
    if category == "-":
        st.info('Please select one index from dropdown')
    if category == "NIFTY50":
        data = yf.tickers_nifty50(True)
        company_name,ticker = retrieve_companyname(data,'Company Name','Symbol')
    if category == "DOW":
        data = yf.tickers_dow(True)
        company_name,ticker = retrieve_companyname(data,'Company','Symbol')
    if category == "FTSE100":
        data = yf.tickers_ftse100(True)
        company_name,ticker = retrieve_companyname(data,'Company','EPIC')
    if category == "FTSE250":
        data = yf.tickers_ftse250(True)
        company_name,ticker = retrieve_companyname(data,'Company',"Ticker")
        
    if category == "IBOVESPA":
        data = yf.tickers_ibovespa(True)
        company_name,ticker = retrieve_companyname(data,'Share',"Symbol")
        
    if category == "NASDAQ":
        data = yf.tickers_nasdaq(True)
        company_name,ticker = retrieve_companyname(data,'Security Name',"Symbol")
        
    if category == "NIFTYBANK":
        data = yf.tickers_niftybank()
        company_name = data
        ticker = data

    if category == "SP500":
        data = yf.tickers_sp500(True)
        company_name,ticker = retrieve_companyname(data,'Security',"Symbol")
    
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
        major_dict,direct_holders,institutional_holders = companyinfo.stock_holders(symbol)
        st.title('Ownership')
        st.markdown('''
        
        ## Ownership details
        - {} - {}
        - {} - {}
        - {} - {}
        - {} - {}
        '''.format(major_dict['data'][0][1],major_dict['data'][0][0],major_dict['data'][1][1],major_dict['data'][1][0],major_dict['data'][2][1],major_dict['data'][2][0],major_dict['data'][3][1],major_dict['data'][3][0]))

        st.subheader('Direct holders information:')
        st.dataframe(direct_holders)
        
        st.subheader('Institutional holders information:')
        st.dataframe(institutional_holders)
    except:
        st.info('Please select one symbol')

elif menu == "Analyst estimates":
    analyst_estimate = companyinfo.analyst_info(symbol)
    st.title('Analyst estimate')
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
    fscore = piotroski.piotroski(symbol)
    print(fscore.get('Piotroski F-score(/9)')[0])
    print(type(fscore.get('Piotroski F-score(/9)')[0]))
    st.markdown(' The Piotroski F-score for ** {} ** is ** {} ** and the strength of the company is considered to be ** {} **'.format(name,fscore.get('Piotroski F-score(/9)')[0],fscore.get('Strength')[0]))
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
            st.markdown('''Key-entities - {}'''.format(key_entity))
            sent_score.append(sentiment_score)
            if sentiment_score > 0 or sentiment_score == 0:
                postive_news+=1
                st.markdown('''<p style="color:green">Sentiment score = {:.3f}</p>
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
        '''.format(total_news,postive_news,negative_news))
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



