from PyOptionClasses.OptionsClass import option, option_data, greeks


# Spread
class Spread:
    def __init__(self, options):
        # self.risk_profile = risk()
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
        self.name = 'Straddle'
        self.strike_price = strike_price
        self.call_option = call_option
        self.put_option = put_option
        self.expiration = expiration

    def print_straddle(self):
        print(f'Strike price: {self.strike_price} at date {self.expiration}')
        print(f'Call option, Cost: {self.call_option.curr_cost}, Greeks {self.call_option.greeks.get_greeks()}')
        print(f'Put option, Cost: {self.put_option.curr_cost}, Greeks {self.put_option.greeks.get_greeks()}')
        print(f'Straddle, Cost: {self.cost}, Greeks {self.greeks.get_greeks()} \n')


class Strangle(Spread):
    def __init__(self, strangle_range, option_1, option_2, expiration):
        super().__init__([option_1, option_2])
        self.name = 'Strangle'
        self.strangle_range = strangle_range
        self.mid_price = abs(option_1.strike_price - option_2.strike_price)
        self.option_1 = option_1
        self.option_2 = option_2
        self.expiration = expiration

    def print_strangle(self):
        print(f'Mid price: {self.mid_price} and Range: {self.strangle_range} at date {self.expiration}')
        print(f'Option 1, Type: {self.option_1.option_type}, Strike: {self.option_1.strike_price}, '
              f'Cost: {self.option_1.curr_cost}, Greeks {self.option_1.greeks.get_greeks()}')
        print(f'Option 2, Type: {self.option_2.option_type}, Strike: {self.option_2.strike_price}, '
              f'Cost: {self.option_2.curr_cost}, Greeks {self.option_2.greeks.get_greeks()}')
        print(f'Strangle, Cost: {self.cost}, Greeks {self.greeks.get_greeks()} \n')


class Butterfly(Spread):

    def __init__(self, butterfly_range, option_1, option_2_1, option_2_2, option_3, expiration):
        super().__init__([option_1, option_2_1, option_2_2, option_3])
        self.name = 'Butterfly'
        self.butterfly_range = butterfly_range
        self.center_price = option_2_1.strike_price
        self.option_1 = option_1
        # Inherently has 2 middle options
        self.option_2_1 = option_2_1
        self.option_2_2 = option_2_2
        self.option_3 = option_3
        self.expiration = expiration

    def print_butterfly(self):
        print(f'Center price: {self.center_price} and Range: {self.butterfly_range} at date {self.expiration}')
        print(f'Option 1, Type: {self.option_1.option_type}, Strike: {self.option_1.strike_price}, '
              f'Cost: {self.option_1.curr_cost}, Greeks {self.option_1.greeks.get_greeks()}')
        print(f'Option 2_1, Type: {self.option_2_1.option_type}, Strike: {self.option_2_1.strike_price}, '
              f'Cost: {self.option_2_1.curr_cost}, Greeks {self.option_2_1.greeks.get_greeks()}')
        print(f'Option 2_2, Type: {self.option_2_2.option_type}, Strike: {self.option_2_2.strike_price}, '
              f'Cost: {self.option_2_2.curr_cost}, Greeks {self.option_2_2.greeks.get_greeks()}')
        print(f'Option 3, Type: {self.option_3.option_type}, Strike: {self.option_3.strike_price}, '
              f'Cost: {self.option_3.curr_cost}, Greeks {self.option_3.greeks.get_greeks()}')
        print(f'Butterfly, Cost: {self.cost}, Greeks {self.greeks.get_greeks()} \n')


class Condor(Spread):
    def __init__(self, condor_outer_range, condor_inner_range, option_1, option_2, option_3, option_4, expiration):
        super().__init__([option_1, option_2, option_3, option_4])
        self.name = 'Condor'
        self.condor_outer_range = condor_outer_range
        self.condor_inner_range = condor_inner_range
        self.center_price = abs(option_3.strike_price - option_2.strike_price)
        self.option_1 = option_1
        self.option_2 = option_2
        self.option_3 = option_3
        self.option_4 = option_4
        self.expiration = expiration

    def print_condor(self):
        print(f'Center price: {self.center_price}, Outer Range: {self.condor_outer_range}, Inner Range: '
              f'{self.condor_inner_range} at date {self.expiration}')
        print(f'Option 1, Type: {self.option_1.option_type}, Strike: {self.option_1.strike_price}, '
              f'Cost: {self.option_1.curr_cost}, Greeks {self.option_1.greeks.get_greeks()}')
        print(f'Option 2, Type: {self.option_2.option_type}, Strike: {self.option_2.strike_price}, '
              f'Cost: {self.option_2.curr_cost}, Greeks {self.option_2.greeks.get_greeks()}')
        print(f'Option 3, Type: {self.option_3.option_type}, Strike: {self.option_3.strike_price}, '
              f'Cost: {self.option_3.curr_cost}, Greeks {self.option_3.greeks.get_greeks()}')
        print(f'Option 4, Type: {self.option_4.option_type}, Strike: {self.option_4.strike_price}, '
              f'Cost: {self.option_4.curr_cost}, Greeks {self.option_4.greeks.get_greeks()}')
        print(f'Butterfly, Cost: {self.cost}, Greeks {self.greeks.get_greeks()} \n')
