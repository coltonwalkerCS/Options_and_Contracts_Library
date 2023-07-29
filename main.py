from Commodities_Future_Pricing_Lib import getConvenienceYield_XMoContract, stockForwardPrice, generateDivPayments, \
    simpleStockForwardPrice, generateCouponMonthPayments, bondForwardPrice
from PricingModels import call_option_expected_value, get_theoretical_value_of_contract, put_option_expected_value, \
    get_scaled_volatility, black_scholes_model_option_price, calc_theta_for_atm_option
from dynamic_hedging import delta_neutrality_stock
from option_class import greeks, option
# To test the library and assert the correct values


def test_commodities_futures():
    # Commodity Example
    F = 77.40
    interest_rate = 8
    annual_storage_cost = 3
    annual_insurance_cost = 0.6

    conv_yield = getConvenienceYield_XMoContract(3, F, interest_rate, annual_storage_cost, annual_insurance_cost, 76.25)

    assert (conv_yield == 1.25)
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
    assert (forwardPriceStock >= 69.006)
    print(f"Forward stock price: {forwardPriceStock} \n")

    simpleForwardPriceStock = simpleStockForwardPrice(stock_Price, interest_rate_stock, time_to_maturity,
                                                      semiannual_div_payment, time_to_next_div_payment)
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
    simpleBondForwardBondPrice = bondForwardPrice(bond_Price, time_to_maturity_bond, interest_rate_bond,
                                                  coupons_exp_prior,
                                                  coupon_times, coupon_bond_rates)

    assert (106.2159 <= simpleBondForwardBondPrice <= 106.216)
    print(f"Forward bond price: {simpleBondForwardBondPrice} \n")


def test_pricing_models():
    # Test call expected value
    print('Call & Put example 1: ')
    underlying_prices_list = [80, 90, 100, 110, 120]
    probs_associated_list = [0.2, 0.2, 0.2, 0.2, 0.2]

    exp_val_call = call_option_expected_value(underlying_prices_list, probs_associated_list, 100)
    assert (exp_val_call == 6)
    print(f'Expected value of a call contract: {exp_val_call}')

    exp_val_put = put_option_expected_value(underlying_prices_list, probs_associated_list, 100)
    assert (exp_val_put == 6)
    print(f'Expected value of a put contract: {exp_val_put}')

    # Test theoretical value func
    # Assuming 12% interest rate
    int_rate, num_mo = 0.12, 2
    theo_value = get_theoretical_value_of_contract(exp_val_call, int_rate, num_mo)
    assert (theo_value == 5.88)
    print(f'Theoretical value of a call contract: {theo_value}\n')

    # Test using more realistic probability distributions
    print('Call example | more realistic probs: ')
    underlying_prices_list_2 = [80, 90, 100, 110, 120]
    probs_associated_list_2 = [0.1, 0.2, 0.4, 0.2, 0.1]

    exp_val_call_2 = call_option_expected_value(underlying_prices_list_2, probs_associated_list_2, 100)
    assert (exp_val_call_2 == 4)
    print(f'Expected value of a call contract: {exp_val_call_2}')

    # & theo value
    theo_value_2 = get_theoretical_value_of_contract(exp_val_call_2, int_rate, num_mo)
    assert (theo_value_2 == 3.92)
    print(f'Theoretical value of a call contract: {theo_value_2}\n')

    # New example
    print('Example assuming forward price is $102')
    # Assume current stock is $100, the 2mo forward price = $100 * [1 * (0.12 * (2/12))] = $102
    # If $102 is the expected value of the stock, instead of assigning the prob around $100 lets try $102
    underlying_prices_example = [82, 92, 102, 112, 122]
    probs_associated_example = [0.1, 0.2, 0.4, 0.2, 0.1]
    exp_val_call_3 = call_option_expected_value(underlying_prices_example, probs_associated_example, 100)
    assert (exp_val_call_3 == 5.40)
    print(f'Expected value of a call contract: {exp_val_call_2}')

    # & theo value | assume same int rate & number of months
    theo_value_3 = get_theoretical_value_of_contract(exp_val_call_3, int_rate, num_mo)
    assert (theo_value_3 == 5.29)
    print(f'Theoretical value of a call contract: {theo_value_3}\n')

    # Test scaled volatility function

    annual_volatility = 20  # 20% (i.e. 1 standard deviation)
    gen_time_day = '1d'
    scaled_vol_day = get_scaled_volatility(annual_volatility, gen_time_day)
    assert (scaled_vol_day == 1.25)
    print(f'Scaled vol at {annual_volatility} given {gen_time_day} is {scaled_vol_day}%')

    gen_time_week = '1w'
    scaled_vol_week = get_scaled_volatility(annual_volatility, gen_time_week)
    assert(scaled_vol_week == 2.77)
    print(f'Scaled vol at {annual_volatility} given {gen_time_week} is {scaled_vol_week}% \n')

    # Test black-scholes model

    S = 100  # Current stock price
    K = 105  # Strike price
    T = 0.5  # Time to expiration in years
    r = 0.05  # Risk-free interest rate (5%)
    sigma = 0.2  # Volatility (20%)
    option_type_call = 'call'
    option_type_put = 'put'

    option_price_bsm_call = black_scholes_model_option_price(S, K, T, r, sigma, option_type_call)
    option_price_bsm_put = black_scholes_model_option_price(S, K, T, r, sigma, option_type_put)
    assert(option_price_bsm_call == 4.58)
    assert(option_price_bsm_put == 6.99)
    print(f"Theoretical option price for call: {option_price_bsm_call:.2f}")
    print(f"Theoretical option price for call: {option_price_bsm_put:.2f} \n")

    # Test atm theta calc function

    atm_option_theo_val = 2.50
    # days
    time_to_exp = 30

    theta_atm_op = calc_theta_for_atm_option(atm_option_theo_val, time_to_exp)
    assert(theta_atm_op == 0.042)
    print(f"Theta for atm option given {atm_option_theo_val} and {time_to_exp} days to exp is: {theta_atm_op} \n")


def test_dynamic_hedging():
    # Test delta neutrality
    test_greeks = greeks(0.5, 0.1, -0.06, 0.01, 0.01)
    test_option = option(1, 99.50, 5.00, test_greeks)
    number_of_contracts = 100

    equiv_stock = delta_neutrality_stock(test_option, number_of_contracts)
    assert(equiv_stock == -50.0)
    print(f'Equivalent stock: {equiv_stock}')


def run_test():
    print("----------------------------")
    print("RUN Commodities Futures Test")
    print("----------------------------")
    test_commodities_futures()
    print("----------------------------")
    print("END Commodities Futures Test")
    print("----------------------------")

    print("----------------------------")
    print("RUN Pricing Models Test")
    print("----------------------------")
    test_pricing_models()
    print("----------------------------")
    print("END Pricing Models Test")
    print("----------------------------")

    print("----------------------------")
    print("RUN Dynamic Hedging Test")
    print("----------------------------")
    test_dynamic_hedging()
    print("----------------------------")
    print("END Dynamic Hedging Test")
    print("----------------------------")


run_test()
