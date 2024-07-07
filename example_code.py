from Stock_Data import * 


company_prices = company_data_price("AAPL")
company_financial = company_financials("AAPL")

ema200 = company_financial.twohundred_ema()
ema50 = company_financial.fifty_ema()
revenue_per_share = company_financial.revenue_per_share()
fiscal_year_end = company_financial.find_fiscal_year_end()
profit_margin = company_financial.profit_margin()
operating_margin = company_financial.operating_margin()




price = company_prices.find_stock_price()
avg_volume = company_prices.find_avg_volume()
market_cap=company_prices.find_marketcap()


###!! There are more things in this library. I just got lazy to put them all in 

