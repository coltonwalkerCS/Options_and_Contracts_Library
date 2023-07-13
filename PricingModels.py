

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


# Test call expected value
print('Call & Put example 1: ')
underlying_prices_list = [80, 90, 100, 110, 120]
probs_associated_list = [0.2, 0.2, 0.2, 0.2, 0.2]

exp_val_call = call_option_expected_value(underlying_prices_list, probs_associated_list, 100)
assert(exp_val_call == 6)
print(f'Expected value of a call contract: {exp_val_call}')

exp_val_put = put_option_expected_value(underlying_prices_list, probs_associated_list, 100)
assert(exp_val_put == 6)
print(f'Expected value of a put contract: {exp_val_put}')


# Test theoretical value func
# Assuming 12% interest rate
int_rate, num_mo = 0.12, 2
theo_value = get_theoretical_value_of_contract(exp_val_call, int_rate, num_mo)
assert(theo_value == 5.88)
print(f'Theoretical value of a call contract: {theo_value}\n')


# Test using more realistic probability distributions
print('Call example | more realistic probs: ')
underlying_prices_list_2 = [80, 90, 100, 110, 120]
probs_associated_list_2 = [0.1, 0.2, 0.4, 0.2, 0.1]

exp_val_call_2 = call_option_expected_value(underlying_prices_list_2, probs_associated_list_2, 100)
assert(exp_val_call_2 == 4)
print(f'Expected value of a call contract: {exp_val_call_2}')

# & theo value
theo_value_2 = get_theoretical_value_of_contract(exp_val_call_2, int_rate, num_mo)
assert(theo_value_2 == 3.92)
print(f'Theoretical value of a call contract: {theo_value_2}\n')


# New example
print('Example assuming forward price is $102')
# Assume current stock is $100, the 2mo forward price = $100 * [1 * (0.12 * (2/12))] = $102
# If $102 is the expected value of the stock, instead of assigning the prob around $100 lets try $102
underlying_prices_example = [82, 92, 102, 112, 122]
probs_associated_example = [0.1, 0.2, 0.4, 0.2, 0.1]
exp_val_call_3 = call_option_expected_value(underlying_prices_example, probs_associated_example, 100)
assert(exp_val_call_3 == 5.40)
print(f'Expected value of a call contract: {exp_val_call_2}')

# & theo value | assume same int rate & number of months
theo_value_3 = get_theoretical_value_of_contract(exp_val_call_3, int_rate, num_mo)
assert(theo_value_3 == 5.29)
print(f'Theoretical value of a call contract: {theo_value_3}\n')
