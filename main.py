from Commodities_Future_Pricing_Lib import getConvenienceYield_XMoContract, stockForwardPrice, generateDivPayments, \
    simpleStockForwardPrice, generateCouponMonthPayments, bondForwardPrice

# To test the library and assert the correct values

# Commodity Example
F = 77.40
interest_rate = 8
annual_storage_cost = 3
annual_insurance_cost = 0.6

conv_yield = getConvenienceYield_XMoContract(3, F, interest_rate, annual_storage_cost, annual_insurance_cost, 76.25)

assert(conv_yield == 1.25)
print(f"Convenience Yield: {conv_yield} \n")


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
print(f"Forward stock price: {forwardPriceStock} \n")

simpleForwardPriceStock = simpleStockForwardPrice(stock_Price, interest_rate_stock, time_to_maturity, semiannual_div_payment, time_to_next_div_payment)
print(f"Simple forward stock price: {simpleForwardPriceStock} \n")


# Bond Example

bond_Price = 109.76
# 10 months
time_to_maturity_bond = 10
# 8%
interest_rate_bond = 8
# 5.25%
semiannual_coupon_payment = 5.25
# 2 months
time_to_next_coupon_payment = 2
# Assumed coupon rates
coupon_bond_rates = [8.2, 8.5]
# Semi-annual coupon payments
coupons_exp_prior = [5.25, 5.25]
coupon_times = generateCouponMonthPayments(time_to_maturity_bond, time_to_next_coupon_payment)

# time_rem_after_coupon_list,
simpleBondForwardBondPrice = bondForwardPrice(bond_Price, time_to_maturity_bond, interest_rate_bond, coupons_exp_prior,
                                              coupon_times, coupon_bond_rates)

assert(106.2159 <= simpleBondForwardBondPrice <= 106.216)
print(f"Forward bond price: {simpleBondForwardBondPrice} \n")
