import unittest
import pandas as pd

from CommoditiesFuturePricing import getConvenienceYield_XMoContract, stockForwardPrice, generateDivPayments, \
    simpleStockForwardPrice, generateCouponMonthPayments, bondForwardPrice
from PricingModels import call_option_expected_value, get_theoretical_value_of_contract, put_option_expected_value, \
    get_scaled_volatility, black_scholes_model_option_price, calc_theta_for_atm_option
from DynamicHedging import delta_neutrality_stock
from PyOptionClasses.OptionsClass import greeks, option, option_data
from FindingSpreads import (getStraddleSpreads, getStrangleSpreads, getButterflySpreads, getCondorSpreads,
                            getIronCondorSpreads)


class CommoditiesFuturesTest(unittest.TestCase):

    def test_ConvenienceYield(self):
        # Commodity Example
        F = 77.40
        interest_rate = 8
        annual_storage_cost = 3
        annual_insurance_cost = 0.6

        conv_yield = getConvenienceYield_XMoContract(3, F, interest_rate, annual_storage_cost, annual_insurance_cost,
                                                     76.25)

        self.assertEqual(conv_yield, 1.25)
        # print(f"Convenience Yield: {conv_yield} \n")

    def test_stock_futures(self):
        stock_Price = 67
        time_to_maturity = 8
        interest_rate_stock = 6
        semiannual_div_payment = 0.33
        time_to_next_div_payment = 1
        applicable_interest_rate = [6.2, 6.5]

        divTimes, divPayments = generateDivPayments(time_to_maturity, semiannual_div_payment, 1)

        forwardPriceStock = stockForwardPrice(stock_Price, time_to_maturity, interest_rate_stock, divPayments, divTimes,
                                              applicable_interest_rate)

        self.assertEqual(forwardPriceStock, 69.006)
        # print(f"Forward stock price: {forwardPriceStock} \n")

        simpleForwardPriceStock = simpleStockForwardPrice(stock_Price, interest_rate_stock, time_to_maturity,
                                                          semiannual_div_payment, time_to_next_div_payment)

        self.assertEqual(simpleForwardPriceStock, 69.020)
        # print(f"Simple forward stock price: {simpleForwardPriceStock} \n")

    def test_bond_futures(self):
        # Bond Example
        bond_Price = 109.76
        # 10 months
        time_to_maturity_bond = 10
        # 8%
        interest_rate_bond = 8
        # 5.25%
        # semiannual_coupon_payment = 5.25
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

        self.assertEqual(simpleBondForwardBondPrice, 106.216)
        # print(f"Forward bond price: {simpleBondForwardBondPrice} \n")


class PricingModelsTest(unittest.TestCase):

    def test_options_expected_value_and_theo_value_1(self):
        # Test call expected value
        # print('Call & Put example 1: ')
        underlying_prices_list = [80, 90, 100, 110, 120]
        probs_associated_list = [0.2, 0.2, 0.2, 0.2, 0.2]

        exp_val_call = call_option_expected_value(underlying_prices_list, probs_associated_list, 100)
        self.assertEqual(exp_val_call, 6)
        # print(f'Expected value of a call contract: {exp_val_call}')

        exp_val_put = put_option_expected_value(underlying_prices_list, probs_associated_list, 100)
        self.assertEqual(exp_val_put, 6)
        # print(f'Expected value of a put contract: {exp_val_put}')

        # Test theoretical value func
        # Assuming 12% interest rate
        int_rate, num_mo = 0.12, 2
        theo_value = get_theoretical_value_of_contract(exp_val_call, int_rate, num_mo)
        self.assertEqual(theo_value, 5.88)
        # assert (theo_value == 5.88)
        # print(f'Theoretical value of a call contract: {theo_value}\n')

        # Test using more realistic probability distributions
        underlying_prices_list_2 = [80, 90, 100, 110, 120]
        probs_associated_list_2 = [0.1, 0.2, 0.4, 0.2, 0.1]

        exp_val_call_2 = call_option_expected_value(underlying_prices_list_2, probs_associated_list_2, 100)
        self.assertEqual(exp_val_call_2, 4)
        # assert (exp_val_call_2 == 4)
        # print(f'Expected value of a call contract: {exp_val_call_2}')

        # & theo value
        theo_value_2 = get_theoretical_value_of_contract(exp_val_call_2, int_rate, num_mo)
        self.assertEqual(theo_value_2, 3.92)

        # assert (theo_value_2 == 3.92)
        # print(f'Theoretical value of a call contract: {theo_value_2}\n')

    def test_options_expected_value_and_theo_value_2(self):
        # New example
        int_rate, num_mo = 0.12, 2
        # print('Example assuming forward price is $102')
        # Assume current stock is $100, the 2mo forward price = $100 * [1 * (0.12 * (2/12))] = $102
        # If $102 is the expected value of the stock, instead of assigning the prob around $100 lets try $102
        underlying_prices_example = [82, 92, 102, 112, 122]
        probs_associated_example = [0.1, 0.2, 0.4, 0.2, 0.1]
        exp_val_call_3 = call_option_expected_value(underlying_prices_example, probs_associated_example, 100)
        self.assertEqual(exp_val_call_3, 5.40)
        # print(f'Expected value of a call contract: {exp_val_call_2}')

        # & theo value | assume same int rate & number of months
        theo_value_3 = get_theoretical_value_of_contract(exp_val_call_3, int_rate, num_mo)
        self.assertEqual(theo_value_3, 5.29)
        # print(f'Theoretical value of a call contract: {theo_value_3}\n')

    def test_scaled_volatility(self):
        # Test scaled volatility function
        annual_volatility = 20  # 20% (i.e. 1 standard deviation)
        gen_time_day = '1d'
        scaled_vol_day = get_scaled_volatility(annual_volatility, gen_time_day)
        self.assertEqual(scaled_vol_day, 1.25)
        # print(f'Scaled vol at {annual_volatility} given {gen_time_day} is {scaled_vol_day}%')

        gen_time_week = '1w'
        scaled_vol_week = get_scaled_volatility(annual_volatility, gen_time_week)
        self.assertEqual(scaled_vol_week, 2.77)
        # print(f'Scaled vol at {annual_volatility} given {gen_time_week} is {scaled_vol_week}% \n')

    def test_black_scholes_model(self):
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
        self.assertEqual(option_price_bsm_call, 4.58)
        self.assertEqual(option_price_bsm_put, 6.99)
        # assert (option_price_bsm_call == 4.58)
        # assert (option_price_bsm_put == 6.99)
        # print(f"Theoretical option price for call: {option_price_bsm_call:.2f}")
        # print(f"Theoretical option price for call: {option_price_bsm_put:.2f} \n")

    def test_atm_theta_calculation(self):
        # Test atm theta calc function

        atm_option_theo_val = 2.50

        # days
        time_to_exp = 30

        theta_atm_op = calc_theta_for_atm_option(atm_option_theo_val, time_to_exp)
        self.assertEqual(theta_atm_op, 0.042)
        # assert (theta_atm_op == 0.042)
        # print(f"Theta for atm option given {atm_option_theo_val} and {time_to_exp} days to exp is: {theta_atm_op} \n")


class DynamicHedgingTest(unittest.TestCase):
    def test_delta_neutrality(self):
        # Test delta neutrality
        #  option_type, strike_price, cost, implied_volatility, curr_greeks, curr_stock_price, annual_time_to_exp,
        #                  curr_int_rate, curr_volatility):
        op_type = 'call'
        strike_price = 99.50
        cost = 5.00
        implied_volatility = 12
        curr_stock_price = 100
        annual_time_to_exp = 0.223
        curr_interest_rate = 0.01
        curr_volatility = 13
        test_greeks = greeks(0.5, 0.1, -0.06, 0.01, 0.01)
        test_option = option(op_type, strike_price, cost, implied_volatility, test_greeks, curr_stock_price,
                             annual_time_to_exp, curr_interest_rate, curr_volatility, 'Bought')
        number_of_contracts = 100

        equiv_stock = delta_neutrality_stock(test_option, number_of_contracts)
        self.assertEqual(equiv_stock, -50.0)
        # print(f'Equivalent stock: {equiv_stock}')


class FindingSpreadsTest(unittest.TestCase):

    def setUp(self):
        self.call_options_exp_may_15_data = {
            'Exercise Price': [44, 46, 48, 50, 52, 54],
            'Price': [4.59, 2.99, 1.75, 0.93, 0.47, 0.23],
            # 'Theoretical value': [10.5, 20.3, 15.7, 8.9, 12.1],
            'Delta': [0.92, 0.78, 0.56, 0.33, 0.16, 0.06],
            'Gamma': [0.045, 0.088, 0.116, 0.107, 0.072, 0.037],
            'Theta': [-0.0046, -0.0091, -0.0121, -0.0111, -0.0075, -0.0038],
            'Vega': [0.029, 0.057, 0.075, 0.069, 0.047, 0.024],
            'Implied Volatility': [19.83, 20.25, 20.48, 20.88, 21.63, 22.46]
        }
        self.put_options_exp_may_15_data = {
            'Exercise Price': [44, 46, 48, 50, 52, 54],
            'Price': [0.20, 0.58, 1.35, 2.53, 4.06, 5.84],
            # 'Theoretical value': [10.5, 20.3, 15.7, 8.9, 12.1],
            'Delta': [-0.08, -0.22, -0.44, -0.67, -0.84, -0.94],
            'Gamma': [0.045, 0.088, 0.116, 0.107, 0.072, 0.037],
            'Theta': [-0.0046, -0.0091, -0.0121, -0.0111, -0.0075, -0.0038],
            'Vega': [0.029, 0.057, 0.075, 0.069, 0.047, 0.024],
            'Implied Volatility': [20.12, 20.09, 20.48, 20.88, 21.45, 22.73]
        }

        self.call_options_exp_july_15_data = {
            'Exercise Price': [44, 46, 48, 50, 52, 54],
            'Price': [4.96, 3.52, 2.38, 1.55, 0.97, 0.60],
            # 'Theoretical value': [10.5, 20.3, 15.7, 8.9, 12.1],
            'Delta': [0.84, 0.71, 0.55, 0.39, 0.25, 0.15],
            'Gamma': [0.050, 0.071, 0.082, 0.080, 0.066, 0.048],
            'Theta': [-0.0052, -0.0074, -0.0085, -0.0083, -0.0069, -0.0050],
            'Vega': [0.064, 0.091, 0.106, 0.103, 0.085, 0.062],
            'Implied Volatility': [20.12, 20.21, 20.42, 20.80, 21.14, 21.64]
        }

        self.put_options_exp_july_15_data = {
            'Exercise Price': [44, 46, 48, 50, 52, 54],
            'Price': [0.56, 0.92, 1.98, 3.14, 4.58, 6.21],
            # 'Theoretical value': [10.5, 20.3, 15.7, 8.9, 12.1],
            'Delta': [-0.16, -0.29, -0.45, -0.61, -0.75, -0.85],
            'Gamma': [0.050, 0.071, 0.082, 0.080, 0.066, 0.048],
            'Theta': [-0.0052, -0.0074, -0.0085, -0.0083, -0.0069, -0.0050],
            'Vega': [0.064, 0.091, 0.106, 0.103, 0.085, 0.062],
            'Implied Volatility': [20.12, 20.31, 20.42, 20.71, 21.25, 21.78]
        }

    def test_finding_theoretical_pricing(self):
        # Test theoretical price of an option given my volatility

        call_may_df = pd.DataFrame(self.call_options_exp_may_15_data)

        # Use the black-scholes model to get the theoretical price of an option
        call_option = call_may_df.iloc[0]

        current_stock_price = 48.40
        my_volatility = 18
        op_strike = call_option['Exercise Price']
        # 56 days to exp
        # 56 / 365 (total num trading days) = 0.21875 annualized num
        time_to_exp = 0.15
        interest_rate = 0.0
        op_type = 'call'

        theoretical_price_call_op = black_scholes_model_option_price(current_stock_price, op_strike, time_to_exp,
                                                                     interest_rate, my_volatility, op_type)
        self.assertEqual(theoretical_price_call_op, 4.53)
        # print(f'Theo price : {theoretical_price_call_op}')

        # Add test across the different prices

    def test_generating_straddles(self):
        # Put the options data into df
        call_may_df = pd.DataFrame(self.call_options_exp_may_15_data)
        put_may_df = pd.DataFrame(self.put_options_exp_may_15_data)

        may_options = option_data(call_may_df, put_may_df, 'May 15', 48.40,
                                  0.1534, 0.0, 18)

        straddleSpreads = getStraddleSpreads(may_options)

        # Test 3 spreads and the values

        straddleTestOne = straddleSpreads[1]
        self.assertEqual(straddleTestOne.cost, -4.79)
        self.assertEqual(straddleTestOne.greeks.get_greeks(), greeks(-0.84, -0.09, 0.01, -0.06, 0.01).get_greeks())
        # print('Print straddle one')
        # print(straddleTestOne.print_straddle())4

        straddleTestTwo = straddleSpreads[4]
        self.assertEqual(straddleTestTwo.cost, 3.1)
        self.assertEqual(straddleTestTwo.greeks.get_greeks(), greeks(0.12, 0.23, -0.02, 0.15, 0.01).get_greeks())

        straddleTestThree = straddleSpreads[7]
        self.assertEqual(straddleTestThree.cost, -3.46)
        self.assertEqual(straddleTestThree.greeks.get_greeks(), greeks(0.34, -0.21, 0.02, -0.14, 0.01).get_greeks())

    def test_generating_strangles(self):
        # Put the options data into df
        call_may_df = pd.DataFrame(self.call_options_exp_may_15_data)
        put_may_df = pd.DataFrame(self.put_options_exp_may_15_data)

        may_options = option_data(call_may_df, put_may_df, 'May 15', 48.40,
                                  0.1534, 0.0, 18)

        # Test for different ranges 2, 6, 10
        strangleSpreads_range2 = getStrangleSpreads(may_options, 2)
        strangleSpreads_range6 = getStrangleSpreads(may_options, 6)
        strangleSpreads_range10 = getStrangleSpreads(may_options, 10)

        # Test it got the correct number of strangles for the specific range
        # Includes both call and put strangles, and each long and short type
        self.assertEqual(len(strangleSpreads_range2), 10)
        self.assertEqual(len(strangleSpreads_range6), 6)
        self.assertEqual(len(strangleSpreads_range10), 2)

        # Test specific instances within each strangle

        # Test strangleSpreads_range2[7]
        self.assertEqual(strangleSpreads_range2[7].option_1.option_type, 'put')
        self.assertEqual(strangleSpreads_range2[7].option_2.option_type, 'call')
        self.assertEqual(strangleSpreads_range2[7].option_1.strike_price, 50)
        self.assertEqual(strangleSpreads_range2[7].option_2.strike_price, 52)
        self.assertEqual(strangleSpreads_range2[7].cost, -3)

        # Test strangleSpreads_range6[4]
        self.assertEqual(strangleSpreads_range6[4].option_1.option_type, 'put')
        self.assertEqual(strangleSpreads_range6[4].option_2.option_type, 'call')
        self.assertEqual(strangleSpreads_range6[4].option_1.strike_price, 48)
        self.assertEqual(strangleSpreads_range6[4].option_2.strike_price, 54)
        self.assertEqual(strangleSpreads_range6[4].cost, 1.58)

        # Test strangleSpreads_range10[1]
        self.assertEqual(strangleSpreads_range10[0].option_1.option_type, 'put')
        self.assertEqual(strangleSpreads_range10[0].option_2.option_type, 'call')
        self.assertEqual(strangleSpreads_range10[0].option_1.strike_price, 44)
        self.assertEqual(strangleSpreads_range10[0].option_2.strike_price, 54)
        self.assertEqual(strangleSpreads_range10[0].cost, 0.43)

    def test_generating_butterflies(self):
        # Put the options data into df
        call_may_df = pd.DataFrame(self.call_options_exp_may_15_data)
        put_may_df = pd.DataFrame(self.put_options_exp_may_15_data)

        may_options = option_data(call_may_df, put_may_df, 'May 15', 48.40,
                                  0.1534, 0.0, 18)

        butterflySpreads_range2 = getButterflySpreads(may_options, 2)
        butterflySpreads_range4 = getButterflySpreads(may_options, 4)

        self.assertEqual(len(butterflySpreads_range2), 16)
        self.assertEqual(len(butterflySpreads_range4), 8)

        # Test specific instances within each strangle

        # Test butterflySpreads_range2[3]
        self.assertEqual(butterflySpreads_range2[3].option_1.option_type, 'put')
        self.assertEqual(butterflySpreads_range2[3].option_2_1.option_type, 'put')
        self.assertEqual(butterflySpreads_range2[3].option_2_2.option_type, 'put')
        self.assertEqual(butterflySpreads_range2[3].option_3.option_type, 'put')
        self.assertEqual(butterflySpreads_range2[3].option_1.strike_price, 44)
        self.assertEqual(butterflySpreads_range2[3].option_2_1.strike_price, 46)
        self.assertEqual(butterflySpreads_range2[3].option_2_2.strike_price, 46)
        self.assertEqual(butterflySpreads_range2[3].option_3.strike_price, 48)
        self.assertEqual(butterflySpreads_range2[3].cost, -0.39)

        # Test butterflySpreads_range4[6]

        self.assertEqual(butterflySpreads_range4[6].option_1.option_type, 'call')
        self.assertEqual(butterflySpreads_range4[6].option_2_1.option_type, 'call')
        self.assertEqual(butterflySpreads_range4[6].option_2_2.option_type, 'call')
        self.assertEqual(butterflySpreads_range4[6].option_3.option_type, 'call')
        self.assertEqual(butterflySpreads_range4[6].option_1.strike_price, 46)
        self.assertEqual(butterflySpreads_range4[6].option_2_1.strike_price, 50)
        self.assertEqual(butterflySpreads_range4[6].option_2_2.strike_price, 50)
        self.assertEqual(butterflySpreads_range4[6].option_3.strike_price, 54)
        self.assertEqual(butterflySpreads_range4[6].cost, -1.36)

    def test_generating_condors(self):
        # Put the options data into df
        call_may_df = pd.DataFrame(self.call_options_exp_may_15_data)
        put_may_df = pd.DataFrame(self.put_options_exp_may_15_data)

        may_options = option_data(call_may_df, put_may_df, 'May 15', 48.40,
                                  0.1534, 0.0, 18)

        condorSpreads_range2_2 = getCondorSpreads(may_options, 2, 2)
        condorSpreads_range2_4 = getCondorSpreads(may_options, 2, 4)
        condorSpreads_range4_2 = getCondorSpreads(may_options, 4, 2)

        self.assertEqual(len(condorSpreads_range2_2), 12)
        self.assertEqual(len(condorSpreads_range2_4), 4)
        self.assertEqual(len(condorSpreads_range4_2), 8)

        # Test condorSpreads_range2_2[4]
        self.assertEqual(condorSpreads_range2_2[4].option_1.option_type, 'call')
        self.assertEqual(condorSpreads_range2_2[4].option_2.option_type, 'call')
        self.assertEqual(condorSpreads_range2_2[4].option_3.option_type, 'call')
        self.assertEqual(condorSpreads_range2_2[4].option_4.option_type, 'call')
        self.assertEqual(condorSpreads_range2_2[4].option_1.strike_price, 46)
        self.assertEqual(condorSpreads_range2_2[4].option_2.strike_price, 48)
        self.assertEqual(condorSpreads_range2_2[4].option_3.strike_price, 50)
        self.assertEqual(condorSpreads_range2_2[4].option_4.strike_price, 52)
        self.assertEqual(condorSpreads_range2_2[4].cost, 0.78)

        # Test condorSpreads_range2_4[1]
        self.assertEqual(condorSpreads_range2_4[1].option_1.option_type, 'put')
        self.assertEqual(condorSpreads_range2_4[1].option_2.option_type, 'put')
        self.assertEqual(condorSpreads_range2_4[1].option_3.option_type, 'put')
        self.assertEqual(condorSpreads_range2_4[1].option_4.option_type, 'put')
        self.assertEqual(condorSpreads_range2_4[1].option_1.strike_price, 44)
        self.assertEqual(condorSpreads_range2_4[1].option_2.strike_price, 48)
        self.assertEqual(condorSpreads_range2_4[1].option_3.strike_price, 50)
        self.assertEqual(condorSpreads_range2_4[1].option_4.strike_price, 54)
        self.assertEqual(condorSpreads_range2_4[1].cost, 2.16)

        # Test condorSpreads_range4_2[1]
        self.assertEqual(condorSpreads_range4_2[5].option_1.option_type, 'put')
        self.assertEqual(condorSpreads_range4_2[5].option_2.option_type, 'put')
        self.assertEqual(condorSpreads_range4_2[5].option_3.option_type, 'put')
        self.assertEqual(condorSpreads_range4_2[5].option_4.option_type, 'put')
        self.assertEqual(condorSpreads_range4_2[5].option_1.strike_price, 46)
        self.assertEqual(condorSpreads_range4_2[5].option_2.strike_price, 48)
        self.assertEqual(condorSpreads_range4_2[5].option_3.strike_price, 52)
        self.assertEqual(condorSpreads_range4_2[5].option_4.strike_price, 54)
        self.assertEqual(condorSpreads_range4_2[5].cost, 1.01)

    def test_generating_iron_condors(self):
        # Put the options data into df
        call_may_df = pd.DataFrame(self.call_options_exp_may_15_data)
        put_may_df = pd.DataFrame(self.put_options_exp_may_15_data)

        may_options = option_data(call_may_df, put_may_df, 'May 15', 48.40,
                                  0.1534, 0.0, 18)

        iron_CondorSpreads_range2_2 = getIronCondorSpreads(may_options, 2, 2)
        iron_CondorSpreads_range2_4 = getIronCondorSpreads(may_options, 2, 4)
        iron_CondorSpreads_range4_2 = getIronCondorSpreads(may_options, 4, 2)

        self.assertEqual(len(iron_CondorSpreads_range2_2), 6)
        self.assertEqual(len(iron_CondorSpreads_range2_4), 2)
        self.assertEqual(len(iron_CondorSpreads_range4_2), 4)

        # Test iron_CondorSpreads_range2_2[4]
        self.assertEqual(iron_CondorSpreads_range2_2[4].option_1.option_type, 'put')
        self.assertEqual(iron_CondorSpreads_range2_2[4].option_2.option_type, 'put')
        self.assertEqual(iron_CondorSpreads_range2_2[4].option_3.option_type, 'call')
        self.assertEqual(iron_CondorSpreads_range2_2[4].option_4.option_type, 'call')
        self.assertEqual(iron_CondorSpreads_range2_2[4].option_1.strike_price, 48)
        self.assertEqual(iron_CondorSpreads_range2_2[4].option_2.strike_price, 50)
        self.assertEqual(iron_CondorSpreads_range2_2[4].option_3.strike_price, 52)
        self.assertEqual(iron_CondorSpreads_range2_2[4].option_4.strike_price, 54)
        self.assertEqual(iron_CondorSpreads_range2_2[4].cost, 1.42)

        # Test iron_CondorSpreads_range2_4[1]
        self.assertEqual(iron_CondorSpreads_range2_4[1].option_1.option_type, 'put')
        self.assertEqual(iron_CondorSpreads_range2_4[1].option_2.option_type, 'put')
        self.assertEqual(iron_CondorSpreads_range2_4[1].option_3.option_type, 'call')
        self.assertEqual(iron_CondorSpreads_range2_4[1].option_4.option_type, 'call')
        self.assertEqual(iron_CondorSpreads_range2_4[1].option_1.strike_price, 44)
        self.assertEqual(iron_CondorSpreads_range2_4[1].option_2.strike_price, 48)
        self.assertEqual(iron_CondorSpreads_range2_4[1].option_3.strike_price, 50)
        self.assertEqual(iron_CondorSpreads_range2_4[1].option_4.strike_price, 54)
        self.assertEqual(iron_CondorSpreads_range2_4[1].cost, -1.85)

        # Test iron_CondorSpreads_range4_2[0]
        self.assertEqual(iron_CondorSpreads_range4_2[0].option_1.option_type, 'put')
        self.assertEqual(iron_CondorSpreads_range4_2[0].option_2.option_type, 'put')
        self.assertEqual(iron_CondorSpreads_range4_2[0].option_3.option_type, 'call')
        self.assertEqual(iron_CondorSpreads_range4_2[0].option_4.option_type, 'call')
        self.assertEqual(iron_CondorSpreads_range4_2[0].option_1.strike_price, 44)
        self.assertEqual(iron_CondorSpreads_range4_2[0].option_2.strike_price, 46)
        self.assertEqual(iron_CondorSpreads_range4_2[0].option_3.strike_price, 50)
        self.assertEqual(iron_CondorSpreads_range4_2[0].option_4.strike_price, 52)
        self.assertEqual(iron_CondorSpreads_range4_2[0].cost, 0.84)


class RiskProfileTest(unittest.TestCase):

    def setUp(self):
        self.call_options_exp_may_15_data = {
            'Exercise Price': [44, 46, 48, 50, 52, 54],
            'Price': [4.59, 2.99, 1.75, 0.93, 0.47, 0.23],
            # 'Theoretical value': [10.5, 20.3, 15.7, 8.9, 12.1],
            'Delta': [0.92, 0.78, 0.56, 0.33, 0.16, 0.06],
            'Gamma': [0.045, 0.088, 0.116, 0.107, 0.072, 0.037],
            'Theta': [-0.0046, -0.0091, -0.0121, -0.0111, -0.0075, -0.0038],
            'Vega': [0.029, 0.057, 0.075, 0.069, 0.047, 0.024],
            'Implied Volatility': [19.83, 20.25, 20.48, 20.88, 21.63, 22.46]
        }
        self.put_options_exp_may_15_data = {
            'Exercise Price': [44, 46, 48, 50, 52, 54],
            'Price': [0.20, 0.58, 1.35, 2.53, 4.06, 5.84],
            # 'Theoretical value': [10.5, 20.3, 15.7, 8.9, 12.1],
            'Delta': [-0.08, -0.22, -0.44, -0.67, -0.84, -0.94],
            'Gamma': [0.045, 0.088, 0.116, 0.107, 0.072, 0.037],
            'Theta': [-0.0046, -0.0091, -0.0121, -0.0111, -0.0075, -0.0038],
            'Vega': [0.029, 0.057, 0.075, 0.069, 0.047, 0.024],
            'Implied Volatility': [20.12, 20.09, 20.48, 20.88, 21.45, 22.73]
        }

        self.call_options_exp_july_15_data = {
            'Exercise Price': [44, 46, 48, 50, 52, 54],
            'Price': [4.96, 3.52, 2.38, 1.55, 0.97, 0.60],
            # 'Theoretical value': [10.5, 20.3, 15.7, 8.9, 12.1],
            'Delta': [0.84, 0.71, 0.55, 0.39, 0.25, 0.15],
            'Gamma': [0.050, 0.071, 0.082, 0.080, 0.066, 0.048],
            'Theta': [-0.0052, -0.0074, -0.0085, -0.0083, -0.0069, -0.0050],
            'Vega': [0.064, 0.091, 0.106, 0.103, 0.085, 0.062],
            'Implied Volatility': [20.12, 20.21, 20.42, 20.80, 21.14, 21.64]
        }

        self.put_options_exp_july_15_data = {
            'Exercise Price': [44, 46, 48, 50, 52, 54],
            'Price': [0.56, 0.92, 1.98, 3.14, 4.58, 6.21],
            # 'Theoretical value': [10.5, 20.3, 15.7, 8.9, 12.1],
            'Delta': [-0.16, -0.29, -0.45, -0.61, -0.75, -0.85],
            'Gamma': [0.050, 0.071, 0.082, 0.080, 0.066, 0.048],
            'Theta': [-0.0052, -0.0074, -0.0085, -0.0083, -0.0069, -0.0050],
            'Vega': [0.064, 0.091, 0.106, 0.103, 0.085, 0.062],
            'Implied Volatility': [20.12, 20.31, 20.42, 20.71, 21.25, 21.78]
        }
        self.test_option_Bought = option(option_type='call', strike_price=105, cost=4, implied_volatility=18,
                                         curr_greeks=greeks(0.1, 0.1, 0.1, 0.1, 0.1),
                                         curr_stock_price=100, annual_time_to_exp=0.1643, curr_int_rate=0.05,
                                         curr_volatility=19, trade='Bought')

        self.test_option_Sold = option(option_type='call', strike_price=105, cost=-4, implied_volatility=18,
                                       curr_greeks=greeks(0.1, 0.1, 0.1, 0.1, 0.1),
                                       curr_stock_price=100, annual_time_to_exp=0.1643, curr_int_rate=0.05,
                                       curr_volatility=19, trade='Sold')

        self.test_option_Bought_put = option(option_type='put', strike_price=105, cost=4, implied_volatility=18,
                                             curr_greeks=greeks(0.1, 0.1, 0.1, 0.1, 0.1),
                                             curr_stock_price=100, annual_time_to_exp=0.1643, curr_int_rate=0.05,
                                             curr_volatility=19, trade='Bought')

        self.test_option_Sold_put = option(option_type='put', strike_price=105, cost=-4, implied_volatility=18,
                                           curr_greeks=greeks(0.1, 0.1, 0.1, 0.1, 0.1),
                                           curr_stock_price=100, annual_time_to_exp=0.1643, curr_int_rate=0.05,
                                           curr_volatility=19, trade='Sold')

    def test_generating_risk_profile_option(self):

        self.assertEqual(self.test_option_Bought.max_profit, 14.1)
        self.assertEqual(self.test_option_Bought.max_loss, -4)

        self.assertEqual(self.test_option_Sold.max_profit, 4)
        self.assertEqual(self.test_option_Sold.max_loss, -14.1)

    def test_generating_risk_profile_spread_straddle(self):
        # Put the options data into df
        call_may_df = pd.DataFrame(self.call_options_exp_may_15_data)
        put_may_df = pd.DataFrame(self.put_options_exp_may_15_data)

        may_options = option_data(call_may_df, put_may_df, 'May 15', 48.40,
                                  0.1534, 0.0, 18)

        # Get Risk metrics for sold straddle
        straddleSpreads = getStraddleSpreads(may_options)
        straddleTestOne = straddleSpreads[1]

        self.assertEqual(straddleTestOne.max_profit, 4.79)
        self.assertEqual(straddleTestOne.max_loss, -9.85)

    def test_generating_risk_profile_spread_strangle(self):
        # Put the options data into df
        call_may_df = pd.DataFrame(self.call_options_exp_may_15_data)
        put_may_df = pd.DataFrame(self.put_options_exp_may_15_data)

        may_options = option_data(call_may_df, put_may_df, 'May 15', 48.40,
                                  0.1534, 0.0, 18)

        # Get Risk metrics for sold straddle
        strangleSpreads_range2 = getStrangleSpreads(may_options, 2)
        strangleTestOne = strangleSpreads_range2[1]

        self.assertEqual(strangleTestOne.max_profit, 3.19)
        self.assertEqual(strangleTestOne.max_loss, -9.45)

        # Get Risk metrics for sold straddle
        strangleSpreads_range4 = getStrangleSpreads(may_options, 4)
        strangleTestTwo = strangleSpreads_range4[3]

        self.assertEqual(strangleTestTwo.max_profit, 1.51)
        self.assertEqual(strangleTestTwo.max_loss, -7.13)

    def test_generating_risk_profile_spread_butterfly(self):
        # Put the options data into df
        call_may_df = pd.DataFrame(self.call_options_exp_may_15_data)
        put_may_df = pd.DataFrame(self.put_options_exp_may_15_data)

        may_options = option_data(call_may_df, put_may_df, 'May 15', 48.40,
                                  0.1534, 0.0, 18)

        # Test butterfly spread range 2
        butterflySpreads_range2 = getButterflySpreads(may_options, 2)
        butterflyTestOne = butterflySpreads_range2[2]

        self.assertEqual(butterflyTestOne.max_profit, 0.36)
        self.assertEqual(butterflyTestOne.max_loss, -1.64)

        # Test butterfly spread range 4
        butterflySpreads_range4 = getButterflySpreads(may_options, 4)
        butterflyTestTwo = butterflySpreads_range4[0]

        self.assertEqual(butterflyTestTwo.max_profit, 2.44)
        self.assertEqual(butterflyTestTwo.max_loss, -1.56)

    def test_generating_risk_profile_spread_condor(self):
        # Put the options data into df
        call_may_df = pd.DataFrame(self.call_options_exp_may_15_data)
        put_may_df = pd.DataFrame(self.put_options_exp_may_15_data)

        may_options = option_data(call_may_df, put_may_df, 'May 15', 48.40,
                                  0.1534, 0.0, 18)

        # Test condor spread 2_2
        condorSpreads_range2_2 = getCondorSpreads(may_options, 2, 2)
        condorTestOne = condorSpreads_range2_2[4]

        self.assertEqual(condorTestOne.max_profit, 1.22)
        self.assertEqual(condorTestOne.max_loss, -0.78)

        # Test condor spread 2_4
        condorSpreads_range2_4 = getCondorSpreads(may_options, 2, 4)
        condorTestTwo = condorSpreads_range2_4[1]

        self.assertEqual(condorTestTwo.max_profit, 1.84)
        self.assertEqual(condorTestTwo.max_loss, -2.16)

        # Test condor spread 4_2
        condorSpreads_range4_2 = getCondorSpreads(may_options, 4, 2)
        condorTestThree = condorSpreads_range4_2[3]

        self.assertEqual(condorTestThree.max_profit, 1.15)
        self.assertEqual(condorTestThree.max_loss, -0.85)

    def test_generating_risk_profile_spread_iron_condor(self):
        # Put the options data into df
        call_may_df = pd.DataFrame(self.call_options_exp_may_15_data)
        put_may_df = pd.DataFrame(self.put_options_exp_may_15_data)

        may_options = option_data(call_may_df, put_may_df, 'May 15', 48.40,
                                  0.1534, 0.0, 18)

        # Test iron condor spread 2_2
        iron_CondorSpreads_range2_2 = getIronCondorSpreads(may_options, 2, 2)
        iron_CondorTestOne = iron_CondorSpreads_range2_2[4]

        self.assertEqual(iron_CondorTestOne.max_profit, 0.58)
        self.assertEqual(iron_CondorTestOne.max_loss, -1.42)

        # Test iron Condor Spread 2_4
        iron_CondorSpreads_range2_4 = getIronCondorSpreads(may_options, 2, 4)
        iron_CondorTestTwo = iron_CondorSpreads_range2_4[1]

        self.assertEqual(iron_CondorTestTwo.max_profit, 1.85)
        self.assertEqual(iron_CondorTestTwo.max_loss, -2.15)

        # Test iron Condor Spread 4_2
        iron_CondorSpreads_range4_2 = getIronCondorSpreads(may_options, 4, 2)
        iron_CondorTestThree = iron_CondorSpreads_range4_2[2]

        self.assertEqual(iron_CondorTestTwo.max_profit, 0.99)
        self.assertEqual(iron_CondorTestTwo.max_loss, -1.01)

