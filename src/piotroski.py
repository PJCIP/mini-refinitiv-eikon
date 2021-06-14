from numpy import nan
import yahoo_fin.stock_info as yf
import pandas as pd
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
    balance_sheet = yf.get_balance_sheet(ticker)
    cash_flow = yf.get_cash_flow(ticker)
    income_statement = yf.get_income_statement(ticker)
    years = balance_sheet.columns
def profitability():
    '''Finding profitablity following pitorski F score'''
    #Score1 Return on Asset = netincome/avg asset - chart
    netincome = income_statement[years[0]]['netIncome']
    avg_asset =(balance_sheet[years[0]]['totalAssets']+balance_sheet[years[1]]['totalAssets'])/2
    
    ROA = netincome/avg_asset
    ROA_score = 1 if ROA > 1 else 0 
    #Score 2 Operating cash flow
    ocf = cash_flow[years[0]]['totalCashFromOperatingActivities'] 
    ocf_score = 1 if ocf > 0 else 0
    #Score 3 Change in ROA = ROA(current) - ROA(previous)
    netincome_py = income_statement[years[1]]['netIncome']
    avg_asset_py =(balance_sheet[years[1]]['totalAssets']+balance_sheet[years[2]]['totalAssets'])/2
    ROA_py = netincome_py/avg_asset_py
    change_in_ROA = ROA - ROA_py
    change_in_ROA_score = 1 if change_in_ROA > 1 else 0  
    #Score 4 Accrual(ocf/totalassets - ROA > 0)
    accrual = ocf/balance_sheet[years[0]]['totalAssets'] - ROA
    accrual_score = 1 if accrual > 0 else 0
    #Score 5 Net income score
    net_income_score = 1 if netincome > 0 and netincome > netincome_py else 0
    profitablitiy_score = ROA_score+ocf_score+change_in_ROA_score+accrual_score+net_income_score
    return profitablitiy_score

def leverage():

#     Leverage, Liquidity and Source of Funds - Plan to have a chart for this
    # Score  6 - long term debt ratio
    try:
        long_term_debt = balance_sheet[years[0]]['longTermDebt']
        total_asset = balance_sheet[years[0]]['totalAssets']
        debt_ratio = long_term_debt/total_asset
        debt_ratio_score = 1 if debt_ratio < .4 else 0
    except:
        debt_ratio_score = 1

    #Score 7 - Current_ratio_score
    current_assets = balance_sheet[years[0]]['totalCurrentAssets']
    current_liab = balance_sheet[years[0]]['totalCurrentLiabilities']
    current_ratio = current_assets/current_liab
    current_ratio_score = 1 if current_ratio > 1 else 0

    leverage_score = debt_ratio_score+current_ratio_score
    return leverage_score

def operating_efficiency():
    #Plan to have chart for this
    #operating efficiency
    #Score 8- Gross margin
    gross_profit = income_statement[years[0]]['grossProfit']
    revenue = income_statement[years[0]]['totalRevenue']
    gross_profit_py = income_statement[years[1]]['grossProfit']
    revenue_py = income_statement[years[1]]['totalRevenue']
    gross_margin = gross_profit/revenue
    gross_margin_py = gross_profit_py/revenue_py
    gross_margin_score = 1 if gross_margin>gross_margin_py else 0

    #Score 9- Asset turnover
    avg_asset =(balance_sheet[years[0]]['totalAssets']+balance_sheet[years[1]]['totalAssets'])/2
    avg_asset_py =(balance_sheet[years[1]]['totalAssets']+balance_sheet[years[2]]['totalAssets'])/2
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
    try:
        get_data(ticker)
        profitablitiy_score = profitability()
        leverage_score = leverage()
        operating_efficiency_score = operating_efficiency()
        pe_ratio = pe(ticker)
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
        new_row ={'Ticker':ticker,'PE ratio':nan,'Profitability(/5)':nan,"Leverage(/2)":nan,'Operating efficiency(/2)':nan,'Piotroski F-score(/9)':nan,"Strength":"-"}
        summary = summary.append(new_row,ignore_index=True)
        print("Coudnt fetch the reports for {}".format(ticker))
        # break

    return summary

# tickers = yf.tickers_nifty50()
# # print(len(tickers))
# for ticker in tickers[20:30]:
#      result = piotroski(ticker)
