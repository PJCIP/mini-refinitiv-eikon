# from src import companyinfo - for src version
# from re import I
import cinfo_revised as companyinfo
ticker = 'AAPL'
balance_sheet,cash_flow,income_statement = companyinfo.statements(ticker)
years = balance_sheet.columns
print(income_statement)
# Calculating Effective Tax Rate
# ETR = Tax Expense(Income Tax Expense) / EBT
# EBT = EBIT(Ebit) - Interest Expense(Interest Expense)

EBIT = income_statement[years[0]]['Ebit']
IE = income_statement[years[0]]['Interest Expense']
TE = income_statement[years[0]]['Income Tax Expense']
EBT = EBIT - IE
ETR = TE/EBT

print(ETR)
# Calculate interest coverage ratio which inturn used for finding the credit spread

interest_coverage_ratio = EBIT/IE
print(interest_coverage_ratio)
# RF of india from RBI perspective
RF = 0.063640

def cost_of_debt(RF,interest_coverage_ratio):
  if interest_coverage_ratio > 8.5:
    #Rating is AAA
    credit_spread = 0.0063
  if (interest_coverage_ratio > 6.5) & (interest_coverage_ratio <= 8.5):
    #Rating is AA
    credit_spread = 0.0078
  if (interest_coverage_ratio > 5.5) & (interest_coverage_ratio <=  6.5):
    #Rating is A+
    credit_spread = 0.0098
  if (interest_coverage_ratio > 4.25) & (interest_coverage_ratio <=  5.49):
    #Rating is A
    credit_spread = 0.0108
  if (interest_coverage_ratio > 3) & (interest_coverage_ratio <=  4.25):
    #Rating is A-
    credit_spread = 0.0122
  if (interest_coverage_ratio > 2.5) & (interest_coverage_ratio <=  3):
    #Rating is BBB
    credit_spread = 0.0156
  if (interest_coverage_ratio > 2.25) & (interest_coverage_ratio <=  2.5):
    #Rating is BB+
    credit_spread = 0.02
  if (interest_coverage_ratio > 2) & (interest_coverage_ratio <=  2.25):
    #Rating is BB
    credit_spread = 0.0240
  if (interest_coverage_ratio > 1.75) & (interest_coverage_ratio <=  2):
    #Rating is B+
    credit_spread = 0.0351
  if (interest_coverage_ratio > 1.5) & (interest_coverage_ratio <=  1.75):
    #Rating is B
    credit_spread = 0.0421
  if (interest_coverage_ratio > 1.25) & (interest_coverage_ratio <=  1.5):
    #Rating is B-
    credit_spread = 0.0515
  if (interest_coverage_ratio > 0.8) & (interest_coverage_ratio <=  1.25):
    #Rating is CCC
    credit_spread = 0.0820
  if (interest_coverage_ratio > 0.65) & (interest_coverage_ratio <=  0.8):
    #Rating is CC
    credit_spread = 0.0864
  if (interest_coverage_ratio > 0.2) & (interest_coverage_ratio <=  0.65):
    #Rating is C
    credit_spread = 0.1134
  if interest_coverage_ratio <=  0.2:
    #Rating is D
    credit_spread = 0.1512
  
  cost_of_debt = RF + credit_spread
  print(cost_of_debt)
  return cost_of_debt

print(cost_of_debt(RF,interest_coverage_ratio))

#Calculating the Cost_of_equity
# ke = RF+(beta*(niftyyearlyreturn - RF))
#  SP500yearlyreturn = (SP500['sp500'].iloc[-1]/ SP500['sp500'].iloc[0])-1

# Calculating the WACC

#Calculating the SGR

#Calculating the DDM



# Reference
# https://codingandfun.com/calculating-weighted-average-cost-of-capital-wacc-with-python/
# https://www.rbi.org.in/ ---> RF is taken from RBI Dataset --> 2031 GS
# http://pages.stern.nyu.edu/~adamodar/New_Home_Page/datafile/ratings.htm ---> credit spread from interest coverage ratio


