import math
import numpy as np
from scipy.stats import norm


# Expected value for a call (simple approach)

# Desc: Find the expected value of a call contract
# Input: Possible underlying prices @ expiration, probabilities of each price, strike price of option
# Output: Expected value of the call option
def call_option_expected_value(underlying_prices, prob_associated_w_price, strike_price):
    # Double check each underlying has an associated probability
    assert(len(underlying_prices) == len(prob_associated_w_price))

    expected_value = 0

    for i in range(0, len(underlying_prices)):
        # SUM i=1->n [ pi * max(Si - X, 0) ]
        # pi = probability associated w/ price, Si = possible underlying price at expiration
        expected_value += prob_associated_w_price[i] * max(underlying_prices[i]-strike_price, 0)

    return expected_value


# Desc: Find the expected value of a put contract
# Input: Possible underlying prices @ expiration, probabilities of each price, strike price of option
# Output: Expected value of the put option
def put_option_expected_value(underlying_prices, prob_associated_w_price, strike_price):
    # Double check each underlying has an associated probability
    assert(len(underlying_prices) == len(prob_associated_w_price))

    expected_value = 0

    for i in range(0, len(underlying_prices)):
        # SUM i=1->n [ pi * max(Si - X, 0) ]
        # pi = probability associated w/ price, Si = possible underlying price at expiration
        expected_value += prob_associated_w_price[i] * max(strike_price-underlying_prices[i], 0)

    return expected_value


# Desc: Find the theoretical value of an option contract
# Input: Expected value, interest rate, time to expiration (in months)
# Output: Theoretical value of the contract
def get_theoretical_value_of_contract(expected_value, interest_rate, num_months):
    theoretical_value = expected_value / (1 + (interest_rate * (num_months/12)))
    return round(theoretical_value, 2)


# Volatility functions

# Desc: Print the standard deviation for a stock
# Input: One year forward price, Annual volatility expresses as a % (20% = 20)
# Output: N/A
def get_standard_deviation_of_volatility(one_year_forward_price, annual_volatility):
    one_std_dev = one_year_forward_price * (annual_volatility / 100)
    one_std_upper_range = one_year_forward_price + one_std_dev
    one_std_lower_range = one_year_forward_price - one_std_dev

    two_std_dev = one_year_forward_price * (2 * (annual_volatility / 100))
    two_std_upper_range = one_year_forward_price + two_std_dev
    two_std_lower_range = one_year_forward_price - two_std_dev

    three_std_dev = one_year_forward_price * (2 * (annual_volatility / 100))
    three_std_upper_range = one_year_forward_price + three_std_dev
    three_std_lower_range = one_year_forward_price - three_std_dev

    print(f'The stock has a 68% prob of being inbetween {one_std_lower_range} - {one_std_upper_range}')
    print(f'The stock has a 95% prob of being inbetween {two_std_lower_range} - {two_std_upper_range}')
    print(f'The stock has a 99.7% prob of being inbetween {three_std_lower_range} - {three_std_upper_range}')

    return


# Desc: Return the scaled volatility for a stock | Assumes 256 trading days in a year
# Input: Annual volatility expresses as a % (20% = 20), Generic time frame [(month, week, day) '1m', '1w', '1d']
# Output: Scaled volatility of time frame rounded to 2 decimal places
def get_scaled_volatility(annual_volatility, generic_time_frame):
    generic_time_frame_denominator = {"1m": 12, "1w": 52, "1d": 256}

    scaled_vol = annual_volatility * (1 / math.sqrt(generic_time_frame_denominator[generic_time_frame]))

    return round(scaled_vol, 2)


# Desc: Get the black-scholes theoretical value for an option
# Input:
#         S (float): Current stock price
#         K (float): Option strike price
#         T (float): Time to expiration (in years)
#         r (float): Risk-free interest rate (annualized)
#         sigma (float): Volatility of the underlying asset (annualized)
#         option_type (str): 'call' for a call option, 'put' for a put option
# Output: The theoretical option price based on black-scholes model

def black_scholes_model_call_option_price(S, K, T, r, sigma, option_type):
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)

    if option_type == 'call':
        option_price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    elif option_type == 'put':
        option_price = K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
    else:
        raise ValueError("Invalid option type. Use 'call' or 'put'.")

    return round(option_price, 2)
