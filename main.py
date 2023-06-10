from Commodities_Future_Pricing_Lib import getConvenienceYield_XMoContract, stockForwardPrice, generateDivPayments, \
    simpleStockForwardPrice

# Commodity Example
F = 77.40
interest_rate = 8
annual_storage_cost = 3
annual_insurance_cost = 0.6

conv_yield = getConvenienceYield_XMoContract(3, F, interest_rate, annual_storage_cost, annual_insurance_cost, 76.25)

assert(conv_yield == 1.25)
print(f"Convenience Yield: {conv_yield}")

# Stock example
stock_Price = 67
time_to_maturity = 8
interest_rate_stock = 6
semiannual_div_payment = 0.33
time_to_next_div_payment = 1
applicable_interest_rate = [6.2, 6.5]

divTimes, divPayments = generateDivPayments(time_to_maturity, semiannual_div_payment, 1)

forwardPriceStock = stockForwardPrice(stock_Price, time_to_maturity, interest_rate_stock, divPayments, divTimes,
                                      applicable_interest_rate)
assert(forwardPriceStock >= 69.006)
print(f"Forward stock price: {forwardPriceStock}")

simpleForwardPriceStock = simpleStockForwardPrice(stock_Price, interest_rate_stock, time_to_maturity, semiannual_div_payment, time_to_next_div_payment)
print(f"Simple forward stock price: {simpleForwardPriceStock}")
