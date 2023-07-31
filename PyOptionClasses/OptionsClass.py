from PricingModels import black_scholes_model_option_price


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
            new_greek.update_greeks(-1*self.delta, -1*self.gamma, -1*self.theta, -1*self.vega, -1*self.rho)
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


class option_data:
    def __init__(self, options_data_calls, options_data_puts, expiration_date, curr_stock_price, annual_time_to_exp,
                 curr_int_rate, curr_volatility):
        self.expiration_date = expiration_date
        self.current_stock_price = curr_stock_price
        self.annual_time_to_expiration = annual_time_to_exp
        self.current_interest_rate = curr_int_rate
        self.current_volatility = curr_volatility

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
