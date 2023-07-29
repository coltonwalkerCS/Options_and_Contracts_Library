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


# Desc:
class option:

    def __init__(self, option_type, strike_price, cost, implied_volatility, curr_greeks, curr_stock_price, annual_time_to_exp,
                 curr_int_rate, curr_volatility):
        # 1 for call, -1 for put
        self.option_type = option_type
        self.strike_price = strike_price
        self.curr_cost = cost
        self.greeks = curr_greeks
        self.theoretical_price = black_scholes_model_option_price(curr_stock_price, strike_price, annual_time_to_exp,
                                                                  curr_int_rate, curr_volatility, option_type)
        self.implied_volatility = implied_volatility


class option_data:
    def __init__(self, options_data, expiration_date, options_type, curr_stock_price, annual_time_to_exp,
                 curr_int_rate, curr_volatility):

        self.options = []

        for idx, op in options_data.iterrows():
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
                                curr_stock_price=curr_stock_price, annual_time_to_exp=annual_time_to_exp,
                                curr_int_rate=curr_int_rate, curr_volatility=curr_volatility)

            self.options.append(new_option)

        self.expiration_date = expiration_date
        self.type = type

    def get_options(self):
        return self.options

    def print_options(self):
        print(f'{self.type} options expiring {self.expiration_date} \n')
        print('| ExPr | Price| TheoP| Delta| Gamma |  Theta  | Vega  | ImpVo |')
        for op in self.options:
            print(f'| {op.strike_price} | {op.curr_cost} | {op.theoretical_price} | {op.greeks.delta} |'
                  f' {op.greeks.gamma} | {op.greeks.theta} | {op.greeks.vega} | {op.implied_volatility} |')
