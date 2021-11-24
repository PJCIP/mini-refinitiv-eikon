import pandas_datareader.data as web
import yfinance as yf
import datetime
from src import companyinfo
import pandas as pd
def forecast(RF,symbol):
    # RF = 0.063640
    
# Forecasting the fcf
    BS,cf,i_s = companyinfo.statements(symbol)
    # print(income_statement)
    years = BS.columns
    # print(balance_sheet.columns)
    # print(income_statement.columns)
    revenue_g = (i_s[years[0]]['Total Revenue'] - i_s[years[1]]['Total Revenue'])/i_s[years[1]]['Total Revenue']
    income_statement = pd.DataFrame(i_s[years[0]])
    income_statement.dropna(inplace=True)
    income_statement.columns = ['current_year']
    income_statement['as_%_of_revenue'] = income_statement / income_statement['current_year']['Total Revenue']


    #forecasting 5 next years income statement
    income_statement['next_year'] =  (income_statement['current_year']['Total Revenue'] * (1+revenue_g)) * income_statement['as_%_of_revenue'] 
    income_statement['next_2_year'] =  (income_statement['next_year']['Total Revenue'] * (1+revenue_g)) * income_statement['as_%_of_revenue'] 
    income_statement['next_3_year'] =  (income_statement['next_2_year']['Total Revenue'] * (1+revenue_g)) * income_statement['as_%_of_revenue'] 
    income_statement['next_4_year'] =  (income_statement['next_3_year']['Total Revenue'] * (1+revenue_g)) * income_statement['as_%_of_revenue'] 
    income_statement['next_5_year'] =  (income_statement['next_4_year']['Total Revenue'] * (1+revenue_g)) * income_statement['as_%_of_revenue'] 

    # print(income_statement)


    #Get Balance sheet as a percentage of revenue
    balance_sheet = pd.DataFrame(BS[years[0]])
    balance_sheet.dropna(inplace=True)
    balance_sheet.columns = ['current_year']
    balance_sheet['as_%_of_revenue'] = balance_sheet / income_statement['current_year']['Total Revenue']
    

    #forecasting the next 5 years Balance Sheet.
    balance_sheet['next_year'] =  income_statement['next_year'] ['Total Revenue'] * balance_sheet['as_%_of_revenue']
    balance_sheet['next_2_year'] =  income_statement['next_2_year'] ['Total Revenue'] * balance_sheet['as_%_of_revenue']
    balance_sheet['next_3_year'] =  income_statement['next_3_year']['Total Revenue'] * balance_sheet['as_%_of_revenue'] 
    balance_sheet['next_4_year'] =  income_statement['next_4_year']['Total Revenue']  * balance_sheet['as_%_of_revenue'] 
    balance_sheet['next_5_year'] =  income_statement['next_5_year']['Total Revenue'] * balance_sheet['as_%_of_revenue']
    # print(balance_sheet)

    #Get Cashflow as a percentage of revenue
    cashflow = pd.DataFrame(cf[years[0]])
    cashflow.dropna(inplace=True)
    cashflow.columns = ['current_year']
    cashflow['as_%_of_revenue'] = cashflow / income_statement['current_year']['Total Revenue']

    #forecasting the next 5 years Cashflow.
    cashflow['next_year'] =  income_statement['next_year'] ['Total Revenue'] * cashflow['as_%_of_revenue']
    cashflow['next_2_year'] =  income_statement['next_2_year'] ['Total Revenue'] * cashflow['as_%_of_revenue']
    cashflow['next_3_year'] =  income_statement['next_3_year']['Total Revenue'] * cashflow['as_%_of_revenue'] 
    cashflow['next_4_year'] =  income_statement['next_4_year']['Total Revenue']  * cashflow['as_%_of_revenue'] 
    cashflow['next_5_year'] =  income_statement['next_5_year']['Total Revenue'] * cashflow['as_%_of_revenue']
    # print(cashflow)

    CF_forecast = {}
    CF_forecast['next_year'] = {}
    CF_forecast['next_year']['netIncome'] = income_statement['next_year']['Net Income']
    CF_forecast['next_year']['inc_depreciation'] = cashflow['next_year']['Depreciation']
    CF_forecast['next_year']['inc_receivables'] = balance_sheet['next_year']['Net Receivables'] - balance_sheet['current_year']['Net Receivables']
    CF_forecast['next_year']['inc_inventory'] = balance_sheet['next_year']['Inventory'] - balance_sheet['current_year']['Inventory']
    CF_forecast['next_year']['inc_payables'] = balance_sheet['next_year']['Accounts Payable'] - balance_sheet['current_year']['Accounts Payable']
    CF_forecast['next_year']['CF_operations'] = CF_forecast['next_year']['netIncome'] + CF_forecast['next_year']['inc_depreciation'] + (CF_forecast['next_year']['inc_receivables'] * -1) + (CF_forecast['next_year']['inc_inventory'] *-1) + CF_forecast['next_year']['inc_payables']
    CF_forecast['next_year']['CAPEX'] = balance_sheet['next_year']['Property Plant Equipment'] - balance_sheet['current_year']['Property Plant Equipment'] + cashflow['next_year']['Depreciation']

    CF_forecast['next_year']['FCF'] = CF_forecast['next_year']['CAPEX'] + CF_forecast['next_year']['CF_operations']

    CF_forecast['next_2_year'] = {}
    CF_forecast['next_2_year']['netIncome'] = income_statement['next_2_year']['Net Income']
    CF_forecast['next_2_year']['inc_depreciation'] = cashflow['next_2_year']['Depreciation']
    CF_forecast['next_2_year']['inc_receivables'] = balance_sheet['next_2_year']['Net Receivables'] - balance_sheet['next_year']['Net Receivables']
    CF_forecast['next_2_year']['inc_inventory'] = balance_sheet['next_2_year']['Inventory'] - balance_sheet['next_year']['Inventory']
    CF_forecast['next_2_year']['inc_payables'] = balance_sheet['next_2_year']['Accounts Payable'] - balance_sheet['next_year']['Accounts Payable']
    CF_forecast['next_2_year']['CF_operations'] = CF_forecast['next_2_year']['netIncome'] + CF_forecast['next_2_year']['inc_depreciation'] + (CF_forecast['next_2_year']['inc_receivables'] * -1) + (CF_forecast['next_2_year']['inc_inventory'] *-1) + CF_forecast['next_2_year']['inc_payables']
    CF_forecast['next_2_year']['CAPEX'] = balance_sheet['next_2_year']['Property Plant Equipment'] - balance_sheet['next_year']['Property Plant Equipment'] + cashflow['next_2_year']['Depreciation']
    CF_forecast['next_2_year']['FCF'] = CF_forecast['next_2_year']['CAPEX'] + CF_forecast['next_2_year']['CF_operations']
   

    CF_forecast['next_3_year'] = {}
    CF_forecast['next_3_year']['netIncome'] = income_statement['next_3_year']['Net Income']

    CF_forecast['next_3_year']['inc_depreciation'] = cashflow['next_3_year']['Depreciation'] 
    CF_forecast['next_3_year']['inc_receivables'] = balance_sheet['next_3_year']['Net Receivables'] - balance_sheet['next_2_year']['Net Receivables']
    CF_forecast['next_3_year']['inc_inventory'] = balance_sheet['next_3_year']['Inventory'] - balance_sheet['next_2_year']['Inventory']
    CF_forecast['next_3_year']['inc_payables'] = balance_sheet['next_3_year']['Accounts Payable'] - balance_sheet['next_2_year']['Accounts Payable']
    CF_forecast['next_3_year']['CF_operations'] = CF_forecast['next_3_year']['netIncome'] + CF_forecast['next_3_year']['inc_depreciation'] + (CF_forecast['next_3_year']['inc_receivables'] * -1) + (CF_forecast['next_3_year']['inc_inventory'] *-1) + CF_forecast['next_3_year']['inc_payables']
    CF_forecast['next_3_year']['CAPEX'] = balance_sheet['next_3_year']['Property Plant Equipment'] - balance_sheet['next_2_year']['Property Plant Equipment'] + cashflow['next_3_year']['Depreciation'] 
    CF_forecast['next_3_year']['FCF'] = CF_forecast['next_3_year']['CAPEX'] + CF_forecast['next_3_year']['CF_operations']
    
    CF_forecast['next_4_year'] = {}
    CF_forecast['next_4_year']['netIncome'] = income_statement['next_4_year']['Net Income']

    CF_forecast['next_4_year']['inc_depreciation'] = cashflow['next_4_year']['Depreciation'] 
    CF_forecast['next_4_year']['inc_receivables'] = balance_sheet['next_4_year']['Net Receivables'] - balance_sheet['next_3_year']['Net Receivables']
    CF_forecast['next_4_year']['inc_inventory'] = balance_sheet['next_4_year']['Inventory'] - balance_sheet['next_3_year']['Inventory']
    CF_forecast['next_4_year']['inc_payables'] = balance_sheet['next_4_year']['Accounts Payable'] - balance_sheet['next_3_year']['Accounts Payable']
    CF_forecast['next_4_year']['CF_operations'] = CF_forecast['next_4_year']['netIncome'] + CF_forecast['next_4_year']['inc_depreciation'] + (CF_forecast['next_4_year']['inc_receivables'] * -1) + (CF_forecast['next_4_year']['inc_inventory'] *-1) + CF_forecast['next_4_year']['inc_payables']
    CF_forecast['next_4_year']['CAPEX'] = balance_sheet['next_4_year']['Property Plant Equipment'] - balance_sheet['next_3_year']['Property Plant Equipment'] + cashflow['next_4_year']['Depreciation'] 
    CF_forecast['next_4_year']['FCF'] = CF_forecast['next_4_year']['CAPEX'] + CF_forecast['next_4_year']['CF_operations']
    
    CF_forecast['next_5_year'] = {}
    CF_forecast['next_5_year']['netIncome'] = income_statement['next_5_year']['Net Income']

    CF_forecast['next_5_year']['inc_depreciation'] = cashflow['next_5_year']['Depreciation'] 
    CF_forecast['next_5_year']['inc_receivables'] = balance_sheet['next_5_year']['Net Receivables'] - balance_sheet['next_4_year']['Net Receivables']
    CF_forecast['next_5_year']['inc_inventory'] = balance_sheet['next_5_year']['Inventory'] - balance_sheet['next_4_year']['Inventory']
    CF_forecast['next_5_year']['inc_payables'] = balance_sheet['next_5_year']['Accounts Payable'] - balance_sheet['next_4_year']['Accounts Payable']
    CF_forecast['next_5_year']['CF_operations'] = CF_forecast['next_5_year']['netIncome'] + CF_forecast['next_5_year']['inc_depreciation'] + (CF_forecast['next_5_year']['inc_receivables'] * -1) + (CF_forecast['next_5_year']['inc_inventory'] *-1) + CF_forecast['next_5_year']['inc_payables']
    CF_forecast['next_5_year']['CAPEX'] = balance_sheet['next_5_year']['Property Plant Equipment'] - balance_sheet['next_4_year']['Property Plant Equipment'] + cashflow['next_5_year']['Depreciation'] 
    CF_forecast['next_5_year']['FCF'] = CF_forecast['next_5_year']['CAPEX'] + CF_forecast['next_5_year']['CF_operations']

    #Cashflow forecast in dataframe
    CF_forec = pd.DataFrame.from_dict(CF_forecast,orient='columns')
    pd.options.display.float_format = '{:,.0f}'.format
    print(CF_forec)
    # print(CF_forecast)
    return revenue_g,balance_sheet,income_statement,CF_forec
# forecast('GOOG')
