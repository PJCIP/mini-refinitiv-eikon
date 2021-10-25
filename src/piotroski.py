from numpy import nan
import yahoo_fin.stock_info as yf
import pandas as pd
import yfinance as yfs
balance_sheet = []
income_statement = []
cash_flow = []
years = []
summary = pd.DataFrame(columns=['Ticker','PE ratio','Profitability(/5)',"Leverage(/2)",'Operating efficiency(/2)','Piotroski F-score(/9)',"Strength"])

def get_data(ticker):
    global balance_sheet
    global cash_flow
    global income_statement
    global years
    # balance_sheet = yf.get_balance_sheet(ticker)
    # cash_flow = yf.get_cash_flow(ticker)
    # income_statement = yf.get_income_statement(ticker)
    cmp = yfs.Ticker(ticker)
    balance_sheet = cmp.balance_sheet
    cash_flow = cmp.cashflow
    income_statement = cmp.financials
    years = balance_sheet.columns
    print(cmp,balance_sheet,cash_flow,income_statement,years)

def profitability():
    '''Finding profitablity following pitorski F score'''
    #Score1 Return on Asset = netincome/avg asset - chart
    netincome = income_statement[years[0]]['Net Income']
    avg_asset =(balance_sheet[years[0]]['Total Assets']+balance_sheet[years[1]]['Total Assets'])/2
    
    ROA = netincome/avg_asset
    ROA_score = 1 if ROA > 1 else 0 
    #Score 2 Operating cash flow
    ocf = cash_flow[years[0]]['Total Cash From Operating Activities'] 
    ocf_score = 1 if ocf > 0 else 0
    #Score 3 Change in ROA = ROA(current) - ROA(previous)
    netincome_py = income_statement[years[1]]['Net Income']
    avg_asset_py =(balance_sheet[years[1]]['Total Assets']+balance_sheet[years[2]]['Total Assets'])/2
    ROA_py = netincome_py/avg_asset_py
    change_in_ROA = ROA - ROA_py
    change_in_ROA_score = 1 if change_in_ROA > 1 else 0  
    #Score 4 Accrual(ocf/totalassets - ROA > 0)
    accrual = ocf/balance_sheet[years[0]]['Total Assets'] - ROA
    accrual_score = 1 if accrual > 0 else 0
    #Score 5 Net income score
    net_income_score = 1 if netincome > 0 and netincome > netincome_py else 0
    profitablitiy_score = ROA_score+ocf_score+change_in_ROA_score+accrual_score+net_income_score
    return profitablitiy_score

def leverage():

#     Leverage, Liquidity and Source of Funds - Plan to have a chart for this
    # Score  6 - long term debt ratio
    try:
        long_term_debt = balance_sheet[years[0]]['Long Term Debt']
        total_asset = balance_sheet[years[0]]['Total Assets']
        debt_ratio = long_term_debt/total_asset
        debt_ratio_score = 1 if debt_ratio < .4 else 0
    except:
        debt_ratio_score = 1

    #Score 7 - Current_ratio_score
    current_assets = balance_sheet[years[0]]['Total Current Assets']
    current_liab = balance_sheet[years[0]]['Total Current Liabilities']
    current_ratio = current_assets/current_liab
    current_ratio_score = 1 if current_ratio > 1 else 0

    leverage_score = debt_ratio_score+current_ratio_score
    return leverage_score

def operating_efficiency():
    #Plan to have chart for this
    #operating efficiency
    #Score 8- Gross margin
    gross_profit = income_statement[years[0]]['Gross Profit']
    revenue = income_statement[years[0]]['Total Revenue']
    gross_profit_py = income_statement[years[1]]['Gross Profit']
    revenue_py = income_statement[years[1]]['Total Revenue']
    gross_margin = gross_profit/revenue
    gross_margin_py = gross_profit_py/revenue_py
    gross_margin_score = 1 if gross_margin>gross_margin_py else 0

    #Score 9- Asset turnover
    avg_asset =(balance_sheet[years[0]]['Total Assets']+balance_sheet[years[1]]['Total Assets'])/2
    avg_asset_py =(balance_sheet[years[1]]['Total Assets']+balance_sheet[years[2]]['Total Assets'])/2
    asset_turnover_ratio = revenue/avg_asset
    asset_turnover_ratio_py = revenue_py/avg_asset_py
    asset_turnover_Score = 1 if asset_turnover_ratio > asset_turnover_ratio_py else 0
    operating_efficiency_Score = gross_margin_score+asset_turnover_Score
    return operating_efficiency_Score

def pe(ticker):
    pe_data = yf.get_quote_table(ticker)
    pe_ratio = pe_data['PE Ratio (TTM)']
    if pe_ratio != pe_ratio:
        pe_ratio = 0
    return pe_ratio

def piotroski(ticker):
    global summary
    flag = 200
    try:
        get_data(ticker)
    except:
        flag = 404
        print("Coudnt fetch the reports for {}".format(ticker))
        return summary,flag
        
    try:
        profitablitiy_score = profitability()
        leverage_score = leverage()
        operating_efficiency_score = operating_efficiency()
        # print(profitablitiy_score,leverage_score,operating_efficiency_score)
        pe_ratio = 0
        if(profitablitiy_score!=profitablitiy_score or leverage_score!=leverage_score or operating_efficiency_score!=operating_efficiency_score):
            PiotroskiFscore = nan
        else:
            PiotroskiFscore = profitablitiy_score+leverage_score+operating_efficiency_score
            if PiotroskiFscore>7:
                strength = "Strong"
            elif PiotroskiFscore <3:
                strength = "Weak"
            else:
                strength="Medium"     
        new_row ={'Ticker':ticker,'PE ratio':pe_ratio,'Profitability(/5)':profitablitiy_score,"Leverage(/2)":leverage_score,'Operating efficiency(/2)':operating_efficiency_score,'Piotroski F-score(/9)':PiotroskiFscore,"Strength":strength}
        summary = summary.append(new_row,ignore_index=True)
        print("Ticker {} is added to the summary".format(ticker))
    except:
        flag = 500
        print("Unable to calculate the scores {}".format(ticker))
        return summary,flag
        # pe_ratio = pe(ticker)
    # finally:
        
        
    # except:
    #     new_row ={'Ticker':ticker,'PE ratio':nan,'Profitability(/5)':nan,"Leverage(/2)":nan,'Operating efficiency(/2)':nan,'Piotroski F-score(/9)':nan,"Strength":"-"}
    #     summary = summary.append(new_row,ignore_index=True)
        
        # break

    return summary,flag

# ticker = 'AAPL'
# msft = yfs.Ticker(ticker).info['longName']
# print(msft)
# piotroski(ticker)
# print(yf.get_holders(ticker))
