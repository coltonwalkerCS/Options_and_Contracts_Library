import math


# --- Physical commodities (Grains, Energy Products, Precious Metals, etc) ---


# Find the forward price for a physical commodity
def physicalCommodityForwardPrice(commodity_price, time_to_maturity, interest_rate, annual_storage_rate,
                                  annual_insurance_cost):
    forward_price = (commodity_price * (1 + interest_rate * time_to_maturity) + (annual_storage_rate * time_to_maturity)
                     + (annual_insurance_cost * time_to_maturity))
    return forward_price


def getConvenienceYield_XMoContract(numMonths, forward_price, interest_rate, annual_storage_cost, annual_insurance_cost,
                                    cash_price):
    commodity_price = forward_price - (annual_storage_cost + annual_insurance_cost) * (numMonths / 12)
    commodity_price /= (1 + (interest_rate / 100) * (numMonths / 12))
    return cash_price - commodity_price


# ---- STOCK ----

# Assumes semiannual payments
# Given the time to maturity, dividend payment and time to next dividend
# Return the list of each dividend and the corresponding time left for each dividend
def generateDivPayments(time_to_maturity, dividend_payment, time_to_next_div):
    time = time_to_maturity - time_to_next_div
    divTimes = [time]
    timeLeft = time - 6
    while timeLeft > 0:
        divTimes.append(timeLeft)
        timeLeft -= 6
    divPayments = [dividend_payment] * len(divTimes)
    return divTimes, divPayments


# Given the stock price, time to maturity, interest rate, and a list of the dividend payment, time remaining and
# applicable interest rate for each corresponding dividend
# Return the forward price
def stockForwardPrice(stock_price, time_to_maturity, interest_rate, each_dividend_payment,
                      time_remaining_after_each_div, applicable_interest_rate):
    forwardPrice = stock_price + (stock_price * (interest_rate / 100) * (time_to_maturity / 12))

    dividend_sum = 0
    for i in range(len(each_dividend_payment)):
        dividend_sum += each_dividend_payment[i] * (1 + (applicable_interest_rate[i] / 100) *
                                                    (time_remaining_after_each_div[i] / 12))

    forwardPrice -= dividend_sum

    return round(forwardPrice, 3)


def simpleStockForwardPrice(stock_price, interest_rate, time_to_maturity, dividend, time_to_next_div):
    numDividends = math.floor((time_to_maturity - time_to_next_div) / 6) + 1
    forwardPrice = stock_price * (1 + (interest_rate / 100) * time_to_maturity / 12) - (numDividends * dividend)
    return round(forwardPrice, 3)


# ---- BONDS ----

def bondForwardPrice(bond_price, time_to_maturity, rate_interest, each_coupon_prior_to_exp, time_rem_after_coupon_list,
                     applicable_interest_rate_from_each_coupon):
    sum_interest_coupons = 0

    for i in range(0, len(each_coupon_prior_to_exp)):
        sum_interest_coupons += (
                    each_coupon_prior_to_exp[i] * (1 + (applicable_interest_rate_from_each_coupon[i] / 100) *
                                                   (time_rem_after_coupon_list[i] / 12)))

    forwardPrice = (bond_price * (1 + (rate_interest / 100) * (time_to_maturity / 12)) - sum_interest_coupons)
    return round(forwardPrice, 3)


def generateCouponMonthPayments(time_to_maturity, next_coupon_payment):
    coupon_ind_time = time_to_maturity - next_coupon_payment
    coupon_times = [coupon_ind_time]
    coupon_ind_time -= 6
    while coupon_ind_time > 0:
        coupon_times.append(coupon_ind_time)
        coupon_ind_time -= 6
    return coupon_times
