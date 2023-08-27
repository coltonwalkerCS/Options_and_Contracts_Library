from PricingModels import black_scholes_model_option_price
import math
import numpy as np


class greeks:
    def __init__(self, delta, gamma, theta, vega, rho):
        self.delta = delta
        self.gamma = gamma
        self.theta = theta
        self.vega = vega
        self.rho = rho

    def update_greeks(self, delta, gamma, theta, vega, rho):
        self.delta = delta
        self.gamma = gamma
        self.theta = theta
        self.vega = vega
        self.rho = rho

    def get_greeks(self):
        return self.delta, self.gamma, self.theta, self.vega, self.rho

    def greeks_from_trade(self, trade):
        new_greek = greeks(self.delta, self.gamma, self.theta, self.vega, self.rho)
        if trade == 'Sold':
            new_greek.update_greeks(-1 * self.delta, -1 * self.gamma, -1 * self.theta, -1 * self.vega, -1 * self.rho)
        return new_greek


# Desc:
class option:

    def __init__(self, option_type, strike_price, cost, implied_volatility, curr_greeks, curr_stock_price,
                 annual_time_to_exp, curr_int_rate, curr_volatility, trade):
        # Call or put
        self.option_type = option_type
        self.strike_price = strike_price
        self.curr_cost = cost
        self.implied_volatility = implied_volatility
        self.greeks = curr_greeks
        self.curr_stock_price = curr_stock_price
        self.annual_time_to_expiration = annual_time_to_exp
        self.current_interest_rate = curr_int_rate
        self.current_volatility = curr_volatility

        self.theoretical_price = black_scholes_model_option_price(curr_stock_price, strike_price, annual_time_to_exp,
                                                                  curr_int_rate, curr_volatility, option_type)
        # Bought or Sold
        self.trade = trade

        self.price_range = self.get_standard_deviation_price_move_range()
        self.payoff_profile = self.calculate_payoff_profile(self.price_range, isCalendar=False)
        self.max_profit, self.max_loss, self.break_even_points = self.calculate_metrics(self.price_range)

    def update_time_to_expiration(self, time_to_exp, price_range):
        self.annual_time_to_expiration = time_to_exp
        self.price_range = price_range
        self.payoff_profile = self.calculate_payoff_profile(self.price_range, isCalendar=True)
        self.max_profit, self.max_loss, self.break_even_points = self.calculate_metrics(self.price_range)

    def create_option_trade(self, trade):
        trade_cost = self.curr_cost
        if trade == 'Sold':
            # Trade gives a credit
            trade_cost *= -1

        option_with_trade = option(self.option_type, self.strike_price, trade_cost, self.implied_volatility,
                                   self.greeks.greeks_from_trade(trade), self.curr_stock_price,
                                   self.annual_time_to_expiration, self.current_interest_rate,
                                   self.current_volatility, trade)
        return option_with_trade

    def get_standard_deviation_price_move_range(self):
        # STD dev based on Vol,time = volatility,annual * sqrt(time)
        standard_deviation = self.curr_stock_price * ((self.current_volatility/100) *
                                                      math.sqrt(1 / (256 * self.annual_time_to_expiration)))

        price_range_lower_bound = round(self.curr_stock_price - (3 * standard_deviation), 2)
        price_range_upper_bound = round(self.curr_stock_price + (3 * standard_deviation), 2)
        num_points = int(round((price_range_upper_bound - price_range_lower_bound), 2) * 100)

        price_range_list = np.linspace(price_range_lower_bound, price_range_upper_bound, num_points)
        rounded_price_range_list = np.round(price_range_list, 2)
        return rounded_price_range_list

    def calculate_payoff_profile(self, price_range, isCalendar):
        # Need to calc payoff for calenders

        # Find at expiration for non-calendar spreads
        if not isCalendar:
            payoff_profile = [0] * len(price_range)
            for i, price in enumerate(price_range):
                if self.option_type == 'call':
                    payoff = max(price - self.strike_price, 0)
                elif self.option_type == 'put':
                    payoff = max(self.strike_price - price, 0)
                else:
                    raise ValueError("Invalid option type")

                if self.trade == 'Sold':
                    payoff *= -1
                    payoff -= self.curr_cost
                    # Sold options have inverse payoff
                else:
                    payoff -= self.curr_cost

                payoff_profile[i] += round(payoff, 2)
        else:
            # Find theoretical value for it to add
            # Import theoretical price
            # Difference between cost and now new value
            payoff_profile = [0] * len(price_range)

            if self.annual_time_to_expiration != 0:
                for i, price in enumerate(price_range):
                    theoretical_value = black_scholes_model_option_price(price, self.strike_price,
                                                                         self.annual_time_to_expiration,
                                                                         self.current_interest_rate,
                                                                         self.current_volatility, self.option_type)
                    if self.trade == 'Sold':
                        # Need to buy back and difference is profit
                        # Curr cost will be neg bc credit
                        payoff = -1 * (self.curr_cost + theoretical_value)
                    else:
                        payoff = -1 * (self.curr_cost - theoretical_value)
                    payoff_profile[i] += round(payoff, 2)
            else:
                for i, price in enumerate(price_range):
                    if self.option_type == 'call':
                        payoff = max(price - self.strike_price, 0)
                    elif self.option_type == 'put':
                        payoff = max(self.strike_price - price, 0)
                    else:
                        raise ValueError("Invalid option type")

                    if self.trade == 'Sold':
                        payoff *= -1
                        payoff -= self.curr_cost
                        # Sold options have inverse payoff
                    else:
                        payoff -= self.curr_cost

                    payoff_profile[i] += round(payoff, 2)

        return payoff_profile

    def calculate_metrics(self, price_range):
        max_profit = round(max(self.payoff_profile), 2)
        max_loss = round(min(self.payoff_profile), 2)

        break_even_point = [price_range[i] for i, payoff in enumerate(self.payoff_profile) if payoff == 0]

        # risk_reward_ratio = -max_loss / max_profit if max_profit != 0 else None

        return max_profit, max_loss, break_even_point  # risk_reward_ratio


class option_data:
    def __init__(self, options_data_calls, options_data_puts, expiration_date, curr_stock_price, annual_time_to_exp,
                 curr_int_rate, curr_volatility):
        self.expiration_date = expiration_date
        self.current_stock_price = curr_stock_price
        self.annual_time_to_expiration = annual_time_to_exp
        self.current_interest_rate = curr_int_rate
        self.current_volatility = curr_volatility
        self.data_spread = abs(
            options_data_calls.loc[0, 'Exercise Price'] - options_data_calls.loc[1, 'Exercise Price'])

        # Only generate if there is data to parse
        if options_data_calls is not None:
            self.options_calls = self.generate_option_list(options_data_calls, 'call')

        if options_data_puts is not None:
            self.options_puts = self.generate_option_list(options_data_puts, 'put')

    def generate_option_list(self, options_data_calls, options_type):
        options = []
        for idx, op in options_data_calls.iterrows():
            # TODO: Fix in future once data contains Rho
            # TODO: Hopefully pulled data contains all greek values
            # if op['Rho'] is not None:
            #     rho = 0.01
            # else:
            #     rho = op['Rho']

            # Set Greeks and Option into Class
            option_greeks = greeks(delta=op['Delta'], gamma=op['Gamma'], theta=op['Theta'], vega=op['Vega'], rho=0.01)

            new_option = option(option_type=options_type, strike_price=op['Exercise Price'], cost=op['Price'],
                                implied_volatility=op['Implied Volatility'], curr_greeks=option_greeks,
                                curr_stock_price=self.current_stock_price,
                                annual_time_to_exp=self.annual_time_to_expiration,
                                curr_int_rate=self.current_interest_rate, curr_volatility=self.current_volatility,
                                trade=None)

            options.append(new_option)

        return options

    # Desc: Return
    # Input: N/A
    # Output: Returns the calls and put options data
    def get_options(self):
        return self.options_calls, self.options_puts

    def print_options(self):
        # TODO: ADJUST TO BE FORMATED WITH CALL AND PUT OPTIONS DATA
        print(f'Call options expiring {self.expiration_date} \n')
        print('| ExPr | Price| TheoP| Delta| Gamma |  Theta  | Vega  | ImpVo |')
        for op in self.options_calls:
            print(f'| {op.strike_price} | {op.curr_cost} | {op.theoretical_price} | {op.greeks.delta} |'
                  f' {op.greeks.gamma} | {op.greeks.theta} | {op.greeks.vega} | {op.implied_volatility} |')

        print(f'Put options expiring {self.expiration_date} \n')
        print('| ExPr | Price| TheoP| Delta| Gamma |  Theta  | Vega  | ImpVo |')
        for op in self.options_puts:
            print(f'| {op.strike_price} | {op.curr_cost} | {op.theoretical_price} | {op.greeks.delta} |'
                  f' {op.greeks.gamma} | {op.greeks.theta} | {op.greeks.vega} | {op.implied_volatility} |')
        return
