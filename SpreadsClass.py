from OptionsClass import option, option_data, greeks


# Spread
class Spread:
    def __init__(self, options):
        # self.risk_profie = risk()
        self.greeks = self.generateSpreadGreeks(options)
        self.cost = round(sum(op.curr_cost for op in options), 2)

        return

    # Potentially will just place this function in __init__ if not used elsewhere
    def generateSpreadGreeks(self, options):
        # Delta, Gamma, Theta, Vega, Rho
        # TODO: Fix once rho is added to data
        delta, gamma, theta, vega, rho = 0, 0, 0, 0, 0.01

        for op in options:

            delta += op.greeks.delta
            gamma += op.greeks.gamma
            theta += op.greeks.theta
            vega += op.greeks.vega

        return greeks(round(delta, 2), round(gamma, 2), round(theta, 2), round(vega, 2), round(rho, 2))


class Straddle(Spread):
    def __init__(self, strike_price, call_option, put_option, expiration):
        super().__init__([call_option, put_option])
        self.strike_price = strike_price
        self.call_option = call_option
        self.put_option = put_option
        self.expiration = expiration

    def print_straddle(self):
        print(f'Strike price: {self.strike_price} at date {self.expiration}')
        print(f'Call option, Cost: {self.call_option.curr_cost}, Greeks {self.call_option.greeks.get_greeks()}')
        print(f'Put option, Cost: {self.put_option.curr_cost}, Greeks {self.put_option.greeks.get_greeks()}')
        print(f'Straddle, Cost: {self.cost}, Greeks {self.greeks.get_greeks()} \n')
